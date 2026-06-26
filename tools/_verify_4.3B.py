"""验证参考解：§4.3b MAP + Hessian + 多维后验采样"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
heights = d[d['age'] >= 18]['height'].values  # (352,)

def map_quap(heights, n_samples=10000, seed=42):
    """
    MAP 二次近似 (quadratic approximation)：
    1. minimize neg_log_posterior 找 MAP
    2. 数值 Hessian → 协方差矩阵
    3. 从多维高斯中采样
    返回: (mu_map, sigma_map, post_samples)
      post_samples: (n_samples, 2) 列 = [μ, σ]
    """
    def neg_log_post(params):
        mu, log_sigma = params
        sigma = np.exp(log_sigma)
        if sigma <= 0 or sigma > 50:
            return np.inf
        ll    = np.sum(stats.norm.logpdf(heights, mu, sigma))
        lp_mu = stats.norm.logpdf(mu, 178, 20)
        return -(ll + lp_mu)

    res = minimize(neg_log_post, x0=[170.0, np.log(8.0)], method='BFGS')
    mu_map    = res.x[0]
    sigma_map = np.exp(res.x[1])

    # 四点差分数值 Hessian（在 (μ, log_σ) 空间）
    eps = 1e-4
    x0  = res.x
    H   = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            xpp = x0.copy(); xpp[i] += eps; xpp[j] += eps
            xpm = x0.copy(); xpm[i] += eps; xpm[j] -= eps
            xmp = x0.copy(); xmp[i] -= eps; xmp[j] += eps
            xmm = x0.copy(); xmm[i] -= eps; xmm[j] -= eps
            H[i, j] = (neg_log_post(xpp) - neg_log_post(xpm)
                       - neg_log_post(xmp) + neg_log_post(xmm)) / (4 * eps**2)
    cov_log = np.linalg.inv(H)   # 协方差 = 负 Hessian 的逆

    # 在 (μ, log_σ) 空间采样，再 exp 还原 σ
    rng = np.random.default_rng(seed)
    samp_log = rng.multivariate_normal(res.x, cov_log, size=n_samples)
    post_samples = np.column_stack([samp_log[:, 0], np.exp(samp_log[:, 1])])

    return mu_map, sigma_map, post_samples

mu_map, sigma_map, post_samples = map_quap(heights)
print(f"MAP: μ={mu_map:.3f}, σ={sigma_map:.3f}")
print(f"后验样本 μ: mean={post_samples[:,0].mean():.3f}, std={post_samples[:,0].std():.3f}")
print(f"后验样本 σ: mean={post_samples[:,1].mean():.3f}, std={post_samples[:,1].std():.3f}")
print(f"样本形状: {post_samples.shape}")

# 断言（书中 p100：μ≈154.61±0.41, σ≈7.73±0.29）
assert 154.0 < mu_map < 156.0,   f"μ MAP 超界: {mu_map:.3f}"
assert 7.0   < sigma_map < 8.5,  f"σ MAP 超界: {sigma_map:.3f}"
assert post_samples.shape == (10000, 2), f"形状错误: {post_samples.shape}"
assert abs(post_samples[:,0].mean() - mu_map) < 0.5, "μ 样本均值偏差过大"
assert abs(post_samples[:,1].mean() - sigma_map) < 0.5, "σ 样本均值偏差过大"
assert 0.2 < post_samples[:,0].std() < 0.8, f"μ 样本 std 应≈0.41，实际={post_samples[:,0].std():.3f}"
assert 0.1 < post_samples[:,1].std() < 0.6, f"σ 样本 std 应≈0.29，实际={post_samples[:,1].std():.3f}"
print("✅ 参考解全部断言通过")
