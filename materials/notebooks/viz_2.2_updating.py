"""可视化：globe tossing 的逐次贝叶斯更新（复现书 Figure 2.5, p43）。
每喂入一个观测画一格：虚线=上一步后验，实线=更新后后验。"""
import numpy as np
from scipy.stats import binom
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = "WLWWWLWLW"
grid = np.linspace(0, 1, 200)


def density(post):
    """归一化为密度（面积=1），方便看曲线变高变窄。"""
    return post / np.trapezoid(post, grid)


fig, axes = plt.subplots(3, 3, figsize=(11, 9), sharex=True)
post = np.ones_like(grid)                      # 均匀先验
post = post / post.sum()

for i, (obs, ax) in enumerate(zip(data, axes.ravel()), 1):
    prev = post.copy()
    like = grid if obs == "W" else 1 - grid    # 单次似然：W→p，L→1-p
    post = post * like
    post = post / post.sum()

    if i > 1:
        ax.plot(grid, density(prev), "--", color="gray", lw=1.2, label="prior (prev)")
    ax.plot(grid, density(post), "-", color="C0", lw=2, label="posterior")
    peak = grid[np.argmax(post)]
    ax.axvline(peak, color="C3", ls=":", lw=1)
    seen = data[:i]
    ax.set_title(f"n={i}  obs='{obs}'  ({seen.count('W')}W {seen.count('L')}L)  peak≈{peak:.2f}",
                 fontsize=10)
    ax.set_ylim(bottom=0)
    if i == 1:
        ax.legend(fontsize=8, loc="upper left")

for ax in axes[-1]:
    ax.set_xlabel("proportion water  p")
for ax in axes[:, 0]:
    ax.set_ylabel("plausibility (density)")

fig.suptitle("Bayesian updating, one observation at a time — globe tossing 'WLWWWLWLW'  (cf. Fig 2.5, p43)",
             fontsize=12)
fig.tight_layout(rect=[0, 0, 1, 0.97])
out = "materials/figures/2.2_updating.png"
fig.savefig(out, dpi=110)
print("saved:", out)
