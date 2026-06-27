"""
练习 4.4-1（OJ）：实现线性回归 MAP 估计

函数签名：
    fit_linear_map(heights, weights) -> (alpha, beta, sigma)

模型：
    hi  ~ Normal(μi, σ)
    μi   = α + β·wi
    α   ~ Normal(178, 100)
    β   ~ Normal(0, 10)
    σ   ~ Uniform(0, 50)（等价于对 log_sigma 无约束优化）

返回：MAP 估计的 (alpha, beta, sigma)，类型均为 float

判题：python3 tools/judge.py materials/notebooks/ex_4.4A.py materials/notebooks/tests/_4.4A.py
"""
import numpy as np
from scipy import stats
from scipy.optimize import minimize


def fit_linear_map(heights, weights):
    heights = np.asarray(heights, dtype=float)
    weights = np.asarray(weights, dtype=float)

    # 步骤 1：负对数后验
    # 参数向量 = (α, β, log_σ)，log_σ 保证 σ>0
    def neg_log_post(params):
        a, b, log_sigma = params
        sigma = np.exp(log_sigma)
        mu_i  = a + b * weights                             # 线性模型：确定值
        ll    = np.sum(stats.norm.logpdf(heights, mu_i, sigma))  # log 似然
        lp_a  = stats.norm.logpdf(a, 178, 100)             # log α 先验
        lp_b  = stats.norm.logpdf(b, 0, 10)                # log β 先验
        return -(ll + lp_a + lp_b)                         # σ 先验为常数，忽略

    # 步骤 2：BFGS 求 MAP
    res = minimize(neg_log_post, x0=[114.0, 0.9, np.log(5.0)], method='BFGS')

    alpha = res.x[0]
    beta  = res.x[1]
    sigma = np.exp(res.x[2])                               # log_σ → σ

    return alpha, beta, sigma
