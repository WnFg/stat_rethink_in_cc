"""练习 2.2A · 贝叶斯更新 bayes_update（按学生算法描述实现）

判题：python3 tools/judge.py materials/notebooks/ex_2.2A.py materials/notebooks/tests/_2.2A.py
"""
import numpy as np
from scipy.stats import binom


def bayes_update(grid, data, prior=None):
    # 1. 对 grid 生成均匀先验（None 时）
    prior = np.ones_like(grid, dtype=float) if prior is None else np.array(prior, dtype=float)
    prior = prior / prior.sum()

    # 2. 计算似然：data 视为二项分布生成，W 的个数 ~ Binomial(N, p)
    W = data.count("W")
    N = len(data)
    likelihood = binom.pmf(W, N, grid)

    # 3. 后验：对每个猜想 p，先验 × 似然，再归一化
    post = prior * likelihood
    post = post / post.sum()
    return post
