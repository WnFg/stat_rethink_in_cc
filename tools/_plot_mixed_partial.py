"""混合二阶偏导直觉图：轴对齐 vs 倾斜等高线"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Mixed partial  d2f/dmu/dsigma:  zero (A) vs nonzero (B)", fontsize=13)

mu_g  = np.linspace(-3, 3, 300)
sig_g = np.linspace(-3, 3, 300)
MU, SG = np.meshgrid(mu_g, sig_g)

# ── Case A: axis-aligned ellipse (H[0,1]=0, uncorrelated) ──────────────
ax = axes[0]
# Hessian: diag [4, 1]  (steep in mu, shallow in sigma)
f_A = 2*MU**2 + 0.5*SG**2
cs = ax.contourf(MU, SG, f_A, levels=15, cmap='Blues_r')
ax.contour (MU, SG, f_A, levels=8, colors='navy', linewidths=0.8, alpha=0.6)
ax.axhline(0, color='gray', lw=0.7, ls='--')
ax.axvline(0, color='gray', lw=0.7, ls='--')

# 在两个不同 sigma 位置标出"往东的坡度"
for sg_val, col in [(-1.5, 'tomato'), (1.5, 'darkorange')]:
    ax.annotate('', xy=(0.8, sg_val), xytext=(-0.8, sg_val),
                arrowprops=dict(arrowstyle='->', color=col, lw=2.2))
    ax.text(0.0, sg_val+0.3, f'slope same\nat sigma={sg_val}', ha='center',
            fontsize=8, color=col)

ax.plot(0, 0, 'k*', markersize=14, zorder=5, label='MAP (peak)')
ax.set_xlabel('mu', fontsize=11); ax.set_ylabel('sigma', fontsize=11)
ax.set_title('Case A: axis-aligned contours\n'
             'd2f/dmu/dsigma = 0  →  mu, sigma uncorrelated\n'
             '(eastward slope does NOT change as sigma changes)',
             fontsize=9)
ax.legend(fontsize=9)
ax.set_xlim(-3,3); ax.set_ylim(-3,3)

# ── Case B: tilted ellipse (H[0,1]≠0, correlated) ──────────────────────
ax2 = axes[1]
# Hessian with off-diagonal: rotate the ellipse 45 degrees-ish
# f = [mu, sigma] @ H @ [mu, sigma]^T,  H = [[2,1.5],[1.5,2]]
f_B = 2*MU**2 + 3*MU*SG + 2*SG**2
cs2 = ax2.contourf(MU, SG, f_B, levels=15, cmap='Oranges_r')
ax2.contour (MU, SG, f_B, levels=8, colors='saddlebrown', linewidths=0.8, alpha=0.6)
ax2.axhline(0, color='gray', lw=0.7, ls='--')
ax2.axvline(0, color='gray', lw=0.7, ls='--')

# 在两个 sigma 位置，"往东"的坡度不同 → 箭头长度不同
for sg_val, length, col in [(-1.5, 1.8, 'tomato'), (1.5, 0.5, 'darkorange')]:
    ax2.annotate('', xy=(length/2, sg_val), xytext=(-length/2, sg_val),
                 arrowprops=dict(arrowstyle='->', color=col, lw=2.2))
    ax2.text(0.0, sg_val+0.3, f'slope DIFFERENT\nat sigma={sg_val}', ha='center',
             fontsize=8, color=col)

ax2.plot(0, 0, 'k*', markersize=14, zorder=5, label='MAP (peak)')
ax2.set_xlabel('mu', fontsize=11); ax2.set_ylabel('sigma', fontsize=11)
ax2.set_title('Case B: tilted contours\n'
              'd2f/dmu/dsigma != 0  →  mu, sigma correlated\n'
              '(eastward slope CHANGES as sigma changes)',
              fontsize=9)
ax2.legend(fontsize=9)
ax2.set_xlim(-3,3); ax2.set_ylim(-3,3)

plt.tight_layout()
plt.savefig('materials/figures/4.3B_mixed_partial.png', dpi=130, bbox_inches='tight')
print("saved: materials/figures/4.3B_mixed_partial.png")
