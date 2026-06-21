"""练习 3.1A · 用后验样本求区间概率（OJ）
判题：python3 tools/judge.py materials/notebooks/ex_3.1A.py materials/notebooks/tests/_3.1A.py
"""
import numpy as np


def prob_between(samples, lo, hi):
    """用后验样本估计 p 落在 [lo, hi) 的后验概率（频率法）。
    samples: 后验样本数组；lo, hi: 区间下界/上界
    返回: 落在 [lo, hi) 的样本比例（0~1）
    提示：布尔条件 (samples>=lo) & (samples<hi) 取平均就是频率。
    """
    return np.mean((samples >= lo) & (samples < hi))
