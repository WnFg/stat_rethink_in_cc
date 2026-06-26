"""
练习 4.3-2（OJ）：MAP 二次近似 + 多维后验采样
§4.3.5–4.3.6, p99–103

函数签名：
    map_quap(heights, n_samples=10000, seed=42) -> (mu_map, sigma_map, post_samples)

参数：
    heights      : 身高数组（1D numpy array，单位 cm）
    n_samples    : 从近似后验中采样的数量
    seed         : 随机数种子（传给 np.random.default_rng）

返回：
    mu_map       : float，MAP 下的 μ 估计值（应≈154.6 cm）
    sigma_map    : float，MAP 下的 σ 估计值（应≈7.7 cm）
    post_samples : np.ndarray，形状 (n_samples, 2)
                   每行为 (μ, σ) 的一个后验样本

模型：
    h_i   ~ Normal(μ, σ)
    μ     ~ Normal(178, 20)
    σ     ~ Uniform(0, 50)

实现提示：
    1. 写 neg_log_post(params)，params = (μ, log_σ)（log_σ 参数化确保 σ>0）
    2. scipy.optimize.minimize(neg_log_post, x0, method='BFGS') 找 MAP
    3. 数值四点差分 Hessian → np.linalg.inv(H) 得协方差矩阵 cov_log
    4. rng.multivariate_normal(res.x, cov_log, size=n_samples) 采样 (μ, log_σ)
    5. exp 还原 σ，拼成 (n_samples, 2)

判题：
    conda run -n base python tools/judge.py materials/notebooks/ex_4.3B.py tests/_4.3B.py
"""
import numpy as np
from scipy import stats
from scipy.optimize import minimize


def map_quap(heights, n_samples=10000, seed=42):
    # ── 步骤 1：定义负对数后验 ──────────────────────────────
    # params = (μ, log_σ)；内部用 log_σ 保证 σ > 0
    def neg_log_post(params):
        mu, log_sigma = params
        sigma = np.exp(log_sigma)
        ll    = np.sum(stats.norm.logpdf(heights, mu, sigma))  # log 似然
        lp_mu = stats.norm.logpdf(mu, 178, 20)                 # log μ 先验
        return -(ll + lp_mu)                                    # 取负，供 minimize

    # ── 步骤 2：最优化找 MAP ────────────────────────────────
    res = minimize(neg_log_post, x0=[170.0, np.log(8.0)], method='BFGS')
    mu_map    = res.x[0]
    sigma_map = np.exp(res.x[1])          # log_σ → σ

    # ── 步骤 3：数值 Hessian（四点差分）────────────────────
    # H[i,j] = (f(++)-f(+-)-f(-+)+f(--)) / (4·eps²)
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

    cov_log = np.linalg.inv(H)           # 协方差 = Hessian 的逆（(μ, log_σ) 空间）

    # ── 步骤 4：从多维高斯中采样 ────────────────────────────
    rng      = np.random.default_rng(seed)
    samp_log = rng.multivariate_normal(res.x, cov_log, size=n_samples)  # (n, 2)

    # ── 步骤 5：exp 还原 σ，拼成 (n_samples, 2) ─────────────
    post_samples = np.column_stack([samp_log[:, 0],        # μ 列
                                    np.exp(samp_log[:, 1])]) # σ 列（exp 还原）

    return mu_map, sigma_map, post_samples
