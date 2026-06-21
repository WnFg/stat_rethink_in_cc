"""练习 3.3A · 后验预测分布（OJ）
判题：python3 tools/judge.py materials/notebooks/ex_3.3A.py materials/notebooks/tests/_3.3A.py
"""
import numpy as np


def posterior_predictive(samples, n, rng):
    """对每个后验样本 p 模拟 n 次伯努利的成功计数。
    返回与 samples 等长的整数数组（每个元素 0..n）。
    """
    return rng.binomial(n, samples)
