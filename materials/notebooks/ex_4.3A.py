"""
练习 4.3-1（OJ）：实现双参数网格近似后验

函数签名：
    height_posterior(heights, mu_lo=150, mu_hi=160,
                     sigma_lo=4, sigma_hi=10, n=100) -> (MU, SIGMA, post)

参数：
    heights  : 身高数组（1D numpy array，单位 cm）
    mu_lo/hi : μ 的网格范围
    sigma_lo/hi: σ 的网格范围
    n        : 每个维度的格点数

返回：
    MU    : 形状 (n, n) 的 μ 网格矩阵
    SIGMA : 形状 (n, n) 的 σ 网格矩阵
    post  : 形状 (n, n) 的**归一化后验**概率矩阵

先验：μ ~ Normal(178, 20)，σ ~ Uniform(0, 50)

判题：python3 tools/judge.py materials/notebooks/ex_4.3A.py materials/notebooks/tests/_4.3A.py
"""
import numpy as np
from scipy import stats


def height_posterior(heights, mu_lo=150, mu_hi=160,
                     sigma_lo=4, sigma_hi=10, n=100):
    # 步骤 1：网格
    mu_list    = np.linspace(mu_lo, mu_hi, n)
    sigma_list = np.linspace(sigma_lo, sigma_hi, n)
    MU, SIGMA  = np.meshgrid(mu_list, sigma_list)      # (n, n)

    # 步骤 2：log 似然，广播 (352,1,1) × (1,n,n) → (352,n,n)，sum axis=0 → (n,n)
    log_lik = np.sum(
        stats.norm.logpdf(heights[:, None, None], MU[None], SIGMA[None]),
        axis=0
    )

    # 步骤 3：log 先验
    log_prior_mu    = stats.norm.logpdf(MU, 178, 20)
    log_prior_sigma = np.where((SIGMA > 0) & (SIGMA <= 50), 0.0, -np.inf)

    # 步骤 4：合并 → 数值稳定 → exp → 归一化（= 除以平均似然）
    log_post  = log_lik + log_prior_mu + log_prior_sigma
    log_post -= log_post.max()
    post      = np.exp(log_post)
    post     /= post.sum()

    return MU, SIGMA, post
