"""Homework §3.1 · prob_between 验证三区间"""
import numpy as np
from scipy.stats import binom

# ── 1. 计算后验 ──────────────────────────────────────
grid = np.linspace(0, 1, 1000)

prior = np.ones(1000)
prior = prior / prior.sum()

likelihood = binom.pmf(6, 9, grid)

unstd     = likelihood * prior
avg_like  = unstd.sum()
posterior = unstd / avg_like

print(f"avg_like = {avg_like:.6f}")

# ── 2. 生成样本 ──────────────────────────────────────
rng = np.random.default_rng(100)
samples = rng.choice(grid, size=10000, p=posterior)

# ── 3. 采样计算 ──────────────────────────────────────
def prob_between(samples, lo, hi):
    return np.mean((samples >= lo) & (samples < hi))

a = prob_between(samples, 0.0,  0.5)
b = prob_between(samples, 0.5,  0.75)
c = prob_between(samples, 0.75, 1.01)

print(f"P(p ∈ [0.00, 0.50)) = {a:.3f}")
print(f"P(p ∈ [0.50, 0.75)) = {b:.3f}")
print(f"P(p ∈ [0.75, 1.01)) = {c:.3f}")
print(f"三者之和             = {a+b+c:.3f}")
