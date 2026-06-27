"""
练习 4.5-1（OJ）：二次多项式回归 MAP 估计
§4.5, p123–127

函数签名：
    fit_poly_map(heights, weights) -> (alpha, beta1, beta2, sigma)

模型（使用标准化体重 ws）：
    ws   = (weights - weights.mean()) / weights.std()
    mu_i = alpha + beta1 * ws_i + beta2 * ws_i**2
    h_i  ~ Normal(mu_i, sigma)
    alpha ~ Normal(178, 100)
    beta1 ~ Normal(0, 10)
    beta2 ~ Normal(0, 10)
    sigma ~ Uniform(0, 50)

注意：标准化要用传入的 weights 自身计算均值和标准差（不要硬编码）

返回：MAP 估计的 (alpha, beta1, beta2, sigma)，均为 float

书中预期结果 (p125)：
    alpha ≈ 146.66,  beta1 ≈ 21.40,  beta2 ≈ -8.42,  sigma ≈ 5.75

判题：
    conda run -n base python tools/judge.py materials/notebooks/ex_4.5A.py materials/notebooks/tests/_4.5A.py
"""
import numpy as np
from scipy import stats
from scipy.optimize import minimize


def fit_poly_map(heights, weights):
    heights = np.asarray(heights, dtype=float)
    weights = np.asarray(weights, dtype=float)

    # 步骤 1：标准化体重
    w_mean, w_std = weights.mean(), weights.std()
    ws  = (weights - w_mean) / w_std      # 标准化：均值=0, std=1
    ws2 = ws ** 2                          # 二次项

    # 步骤 2：负对数后验，params = (alpha, beta1, beta2, log_sigma)
    def neg_log_post(params):
        a, b1, b2, log_sigma = params
        sigma = np.exp(log_sigma)
        mu_i  = a + b1 * ws + b2 * ws2
        ll    = np.sum(stats.norm.logpdf(heights, mu_i, sigma))
        lp_a  = stats.norm.logpdf(a,  178, 100)
        lp_b1 = stats.norm.logpdf(b1, 0, 10)
        lp_b2 = stats.norm.logpdf(b2, 0, 10)
        return -(ll + lp_a + lp_b1 + lp_b2)   # σ 先验常数，忽略

    # 步骤 3：BFGS 找 MAP
    res = minimize(neg_log_post, x0=[120.0, 20.0, -8.0, np.log(6.0)], method='BFGS')

    # 步骤 4：解包，log_sigma → sigma
    alpha, beta1, beta2 = res.x[0], res.x[1], res.x[2]
    sigma = np.exp(res.x[3])

    return alpha, beta1, beta2, sigma
