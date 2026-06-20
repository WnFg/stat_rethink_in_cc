"""可视化：二次近似 vs 真实后验（复现书 Figure 2.8, p56）。
蓝实线=解析后验 Beta(W+1,N-W+1)；黑虚线=高斯近似 N(MAP, SD)。
随数据增多（n=9/18/36，同比例），高斯近似越来越准。"""
import numpy as np
from scipy.stats import beta, binom
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def quap(W, N):
    neg = lambda p: -binom.logpmf(W, N, np.clip(p, 1e-9, 1 - 1e-9))
    m = minimize(neg, 0.5, method="L-BFGS-B", bounds=[(1e-6, 1 - 1e-6)]).x[0]
    eps = 1e-4
    second = (neg(m + eps) - 2 * neg(m) + neg(m - eps)) / eps ** 2
    return m, 1 / np.sqrt(second)


from scipy.stats import norm
grid = np.linspace(0, 1, 400)
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
for (W, N), ax in zip([(6, 9), (12, 18), (24, 36)], axes):
    exact = beta.pdf(grid, W + 1, N - W + 1)       # 解析后验
    m, sd = quap(W, N)
    approx = norm.pdf(grid, m, sd)                  # 高斯近似
    ax.plot(grid, exact, "-", color="C0", lw=2, label="exact posterior  Beta")
    ax.plot(grid, approx, "--", color="k", lw=1.8, label=f"quap  N({m:.2f},{sd:.2f})")
    ax.set_title(f"n={N}  (W={W})")
    ax.set_xlabel("proportion water  p")
    ax.legend(fontsize=8)
axes[0].set_ylabel("density")
fig.suptitle("Quadratic approximation vs exact posterior (cf. Fig 2.8, p56) — improves with more data")
fig.tight_layout(rect=[0, 0, 1, 0.95])
out = "materials/figures/2.4_quap.png"
fig.savefig(out, dpi=110)
print("saved:", out)
print("n=9 :", [round(x, 3) for x in quap(6, 9)])
print("n=36:", [round(x, 3) for x in quap(24, 36)])
