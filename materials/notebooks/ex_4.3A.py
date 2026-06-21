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


def height_posterior(heights, mu_lo=150, mu_hi=160,
                     sigma_lo=4, sigma_hi=10, n=100):
    # TODO: 请在这里实现
    raise NotImplementedError
