"""练习 3.2A · 实现 hpdi（OJ）
判题：python3 tools/judge.py materials/notebooks/ex_3.2A.py materials/notebooks/tests/_3.2A.py
"""
import numpy as np


def hpdi(samples, prob=0.5):
    """返回含 prob 质量的最窄后验区间 (lo, hi)。"""
    x = np.sort(samples)
    n = len(x)
    w = int(np.floor(prob * n))
    min_width = 999999999
    lo = hi = 0
    for i in range(n - w):
        width = x[i + w] - x[i]
        if width < min_width:
            min_width = width
            lo = x[i]
            hi = x[i + w]
    return lo, hi
