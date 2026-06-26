"""斜率 vs 曲率直觉图"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Slope vs Curvature — and why curvature determines uncertainty", fontsize=12)

x = np.linspace(-4, 4, 400)

# ── 左图：窄高斯 vs 宽高斯，看斜率切线 ────────────────────────
ax = axes[0]
y_narrow = stats.norm.pdf(x, 0, 0.7)   # 窄 → 大曲率
y_wide   = stats.norm.pdf(x, 0, 2.0)   # 宽 → 小曲率

ax.plot(x, y_narrow, 'steelblue', lw=2.5, label='Narrow peak  (large curvature)')
ax.plot(x, y_wide,   'tomato',    lw=2.5, label='Wide peak   (small curvature)')

# 在 x=0.7 处画切线，展示"当前斜率"
for y_func, sigma, col in [(y_narrow, 0.7, 'steelblue'), (y_wide, 2.0, 'tomato')]:
    x0 = 0.7
    # 数值导数（斜率）
    dx = 0.01
    slope = (stats.norm.pdf(x0+dx, 0, sigma) - stats.norm.pdf(x0-dx, 0, sigma)) / (2*dx)
    y0 = stats.norm.pdf(x0, 0, sigma)
    # 切线
    xl = np.linspace(x0-0.8, x0+0.8, 50)
    ax.plot(xl, y0 + slope*(xl - x0), color=col, ls='--', lw=1.5, alpha=0.8)
    ax.plot(x0, y0, 'o', color=col, markersize=7, zorder=5)

ax.axvline(0, color='gray', lw=0.8, ls=':')
ax.set_xlabel('parameter value', fontsize=11)
ax.set_ylabel('posterior density', fontsize=11)
ax.set_title('Same point x=0.7,  dashed = tangent (slope)\n'
             'Narrow peak: slope changes fast = large curvature\n'
             'Wide peak:   slope changes slow = small curvature', fontsize=9)
ax.legend(fontsize=9)
ax.set_ylim(-0.05, 0.65)

# ── 右图：二阶导（曲率）曲线，峰处=0，两侧负 ─────────────────
ax2 = axes[1]
# log posterior ∝ -x²/(2σ²)  →  f''=-1/σ²（常数，在 MAP 处）
# 画 log p 而不是 p，二阶导更清晰
lp_narrow = stats.norm.logpdf(x, 0, 0.7)
lp_wide   = stats.norm.logpdf(x, 0, 2.0)
d2_narrow = np.gradient(np.gradient(lp_narrow, x), x)
d2_wide   = np.gradient(np.gradient(lp_wide,   x), x)

ax2.plot(x, d2_narrow, 'steelblue', lw=2.5, label=f'Narrow  sigma=0.7   f\'\'(MAP)={-1/0.7**2:.2f}')
ax2.plot(x, d2_wide,   'tomato',    lw=2.5, label=f'Wide    sigma=2.0   f\'\'(MAP)={-1/2.0**2:.2f}')
ax2.axhline(0,  color='gray', lw=0.8, ls=':')
ax2.axvline(0,  color='gray', lw=0.8, ls=':', label='MAP (peak)')
ax2.set_xlabel('parameter value', fontsize=11)
ax2.set_ylabel("f''(x)  =  curvature of log-posterior", fontsize=11)
ax2.set_title('Curvature = d(slope)/dx = f\'\'(x)\n'
              'At MAP:  f\'\'= -1/sigma^2\n'
              'Large |f\'\'| = sharp peak = small uncertainty', fontsize=9)
ax2.legend(fontsize=9)
ax2.set_ylim(-5, 1)
ax2.set_xlim(-3.5, 3.5)

# 标注 MAP 处的曲率值
for sigma, col, yoff in [(0.7, 'steelblue', -0.6), (2.0, 'tomato', -0.3)]:
    ax2.annotate(f"f''(0) = -1/{sigma}^2 = {-1/sigma**2:.2f}",
                 xy=(0, -1/sigma**2), xytext=(1.0, -1/sigma**2 + yoff),
                 fontsize=8, color=col,
                 arrowprops=dict(arrowstyle='->', color=col, lw=1.2))

plt.tight_layout()
plt.savefig('materials/figures/4.3B_slope_curvature.png', dpi=130, bbox_inches='tight')
print("saved: materials/figures/4.3B_slope_curvature.png")
