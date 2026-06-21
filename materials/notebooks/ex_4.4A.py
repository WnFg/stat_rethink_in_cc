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


def fit_linear_map(heights, weights):
    # TODO: 请在这里实现
    raise NotImplementedError
