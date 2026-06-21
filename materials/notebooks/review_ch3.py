"""第3章复习 · AB测试完整流程"""
import numpy as np
from scipy.stats import binom
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = ["Arial Unicode MS", "DejaVu Sans"]

# ── 1. 建模 ──────────────────────────────────────────
# 参数：点击概率 p；似然：Binomial(200, p)；先验：均匀
grid  = np.linspace(0, 1, 1000)
prior = np.ones(1000) / 1000

# ── 2. 后验（Bayes 定理）─────────────────────────────
likelihood = binom.pmf(35, 200, grid)
unstd      = likelihood * prior
avg_like   = unstd.sum()
posterior  = unstd / avg_like

# ── 3. 采样 ──────────────────────────────────────────
rng     = np.random.default_rng(42)
samples = rng.choice(grid, size=10000, p=posterior)

# a) P(点击率 > 0.2)
p_gt_02 = np.mean(samples > 0.2)

# b) 90% HPDI
def hpdi(samples, prob=0.9):
    x = np.sort(samples); n = len(x); w = int(np.floor(prob * n))
    widths = x[w:] - x[:n-w]; i = np.argmin(widths)
    return x[i], x[i+w]

lo, hi = hpdi(samples, 0.9)

print(f"P(点击率 > 0.2)  = {p_gt_02:.3f}")
print(f"90% HPDI         = [{lo:.3f}, {hi:.3f}]")

# ── 4. PPC ───────────────────────────────────────────
ppc = rng.binomial(200, samples)

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(ppc, bins=30, color="#7c3aed", alpha=0.6, density=True, label="后验预测分布")
ax.axvline(35, color="#dc2626", lw=2, label=f"观测值 = 35")
ax.set_xlabel("200封邮件中的点击数")
ax.set_ylabel("密度")
ax.set_title("AB测试 PPC · 再发200封的预测点击数分布")
ax.legend()
plt.tight_layout()
plt.savefig("materials/figures/review_ch3_ppc.png", dpi=130)
print("图已保存 → materials/figures/review_ch3_ppc.png")
print(f"PPC 均值={ppc.mean():.1f}  std={ppc.std():.1f}")
print(f"P(预测点击数=35) ≈ {np.mean(ppc==35):.3f}")
