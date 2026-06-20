"""练习 2.3A · 用 Bayes 定理显式算后验（OJ 形式）

判题：python3 tools/judge.py materials/notebooks/ex_2.3A.py materials/notebooks/tests/_2.3A.py
"""
import numpy as np
from scipy.stats import binom


def posterior_bayes(grid, W, N, prior=None):
    """按 Bayes 定理显式计算 globe tossing 的后验，并返回归一化分母。

    输入：
        grid  : np.ndarray，p 的网格
        W, N  : int，水的个数 / 总抛掷数
        prior : np.ndarray | None，与 grid 同长的先验；None = 均匀先验
    输出：
        (avg_like, posterior)
        avg_like  : 标量，平均似然 Pr(w) = Σ 似然×先验（离散版 ∫likelihood·prior dp）
        posterior : np.ndarray，归一化后验（和为 1）

    步骤（对应 Bayes 定理 Posterior = Likelihood×Prior / AvgLikelihood）：
        1. 先验归一化
        2. likelihood = binom.pmf(W, N, grid)
        3. unstd = likelihood × prior
        4. avg_like = unstd 的总和   ← 这就是归一化分母 Pr(w)
        5. posterior = unstd / avg_like
    """
    # 1. 先验归一化（None = 均匀）
    prior = np.ones_like(grid, float) if prior is None else np.array(prior, float)
    prior = prior / prior.sum()
    # 2. 似然
    likelihood = binom.pmf(W, N, grid)
    # 3. 未归一化后验 = 似然 × 先验（注意：乘的是 prior 权重，不是 grid）
    unstd = likelihood * prior
    # 4. avg_like = Σ(似然 × 先验)  ← Bayes 定理的分母 Pr(W)
    avg_like = unstd.sum()
    # 5. 归一化
    posterior = unstd / avg_like
    return avg_like, posterior
