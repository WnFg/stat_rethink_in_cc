"""优化地形：原始 vs 标准化 — 条件数对比"""
import numpy as np
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('Optimization landscape: raw weights vs standardized weights',
             fontsize=12, fontweight='bold')

# 模拟两个参数: alpha (scale ~150) and beta2 interacting with w^2
# Raw: beta2 * w^2, w~45kg -> w^2~2025, so landscape stretched by ~2025
# Std: beta2 * ws^2, ws~0-1 -> ws^2~0-1, balanced

a_vals  = np.linspace(-3, 3, 300)
b2_vals = np.linspace(-3, 3, 300)
A, B2   = np.meshgrid(a_vals, b2_vals)

# Raw weights landscape: beta2 has 2000x larger scale than alpha
scale_raw = 2000
f_raw = A**2 + (scale_raw * B2)**2     # 极度扁平山谷

# Standardized landscape: balanced
f_std = A**2 + B2**2                   # 接近圆形

ax = axes[0]
cs = ax.contourf(A, B2, f_raw, levels=30, cmap='Blues_r')
ax.contour(A, B2, f_raw, levels=10, colors='navy', linewidths=0.6, alpha=0.5)
ax.set_xlabel('alpha (direction)', fontsize=11)
ax.set_ylabel('beta2 (direction)', fontsize=11)
ax.set_title('Raw weights (w^2 up to 3600)\n'
             'Condition number kappa >> 1\n'
             'Contours: extremely narrow valley — gradient points wrong way!',
             fontsize=9)
# 画一个梯度下降轨迹（zigzag in narrow valley）
path_x, path_y = [2.8], [0.002]
for _ in range(20):
    gx = 2 * path_x[-1]
    gy = 2 * scale_raw**2 * path_y[-1]
    lr = 0.05 / max(abs(gx), abs(gy))
    path_x.append(path_x[-1] - lr * gx)
    path_y.append(path_y[-1] - lr * gy)
ax.plot(path_x, path_y, 'tomato', lw=2, marker='o', ms=3,
        label='GD path: slow zigzag')
ax.plot(0, 0, 'k*', ms=14, zorder=5, label='Minimum')
ax.legend(fontsize=8)

ax2 = axes[1]
cs2 = ax2.contourf(A, B2, f_std, levels=30, cmap='Greens_r')
ax2.contour(A, B2, f_std, levels=10, colors='darkgreen', linewidths=0.6, alpha=0.5)
ax2.set_xlabel('alpha_s (direction)', fontsize=11)
ax2.set_ylabel('beta2_s (direction)', fontsize=11)
ax2.set_title('Standardized weights (ws^2 up to ~4)\n'
              'Condition number kappa ~ 1\n'
              'Contours: near-circular — gradient points toward minimum!',
              fontsize=9)
# 画梯度下降轨迹（直接收敛）
path2_x, path2_y = [2.8], [2.5]
for _ in range(8):
    gx = 2 * path2_x[-1]
    gy = 2 * path2_y[-1]
    lr = 0.18 / max(abs(gx), abs(gy))
    path2_x.append(path2_x[-1] - lr * gx)
    path2_y.append(path2_y[-1] - lr * gy)
ax2.plot(path2_x, path2_y, 'seagreen', lw=2, marker='o', ms=4,
         label='GD path: fast convergence')
ax2.plot(0, 0, 'k*', ms=14, zorder=5, label='Minimum')
ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig('materials/figures/4.5_conditioning.png', dpi=130, bbox_inches='tight')
print("saved: materials/figures/4.5_conditioning.png")
