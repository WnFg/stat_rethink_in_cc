"""BFGS 原理图：梯度下降 vs Newton vs BFGS 路径对比"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# ── 目标函数：细长椭圆（梯度下降会剧烈zigzag，BFGS很快）──
def f(xy):
    x, y = xy
    return 5*x**2 + 0.5*y**2          # 椭圆，x方向很陡

def grad_f(xy):
    x, y = xy
    return np.array([10*x, y])

# ── 梯度下降（固定步长，展示 zigzag）────────────────────────
def gradient_descent(x0, lr=0.15, n_steps=25):
    path = [np.array(x0, dtype=float)]
    x = np.array(x0, dtype=float)
    for _ in range(n_steps):
        x = x - lr * grad_f(x)
        path.append(x.copy())
    return np.array(path)

# ── Newton（用精确 Hessian：[[10,0],[0,1]]）─────────────────
def newton(x0, n_steps=4):
    H_inv = np.array([[0.1, 0], [0, 1.0]])   # H^{-1} 精确值
    path = [np.array(x0, dtype=float)]
    x = np.array(x0, dtype=float)
    for _ in range(n_steps):
        x = x - H_inv @ grad_f(x)
        path.append(x.copy())
    return np.array(path)

# ── BFGS（scipy 记录路径）────────────────────────────────────
x0 = [3.0, 4.0]
bfgs_path = [np.array(x0)]
def callback(xk):
    bfgs_path.append(xk.copy())
minimize(f, x0, method='BFGS', jac=grad_f, callback=callback,
         options={'gtol': 1e-8})

gd_path  = gradient_descent(x0)
nt_path  = newton(x0)
bp       = np.array(bfgs_path)

# ── 绘图 ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 7))

xg = np.linspace(-3.5, 3.5, 300)
yg = np.linspace(-5, 5, 300)
XG, YG = np.meshgrid(xg, yg)
ZG = 5*XG**2 + 0.5*YG**2

ax.contourf(XG, YG, ZG, levels=25, cmap='Blues_r', alpha=0.7)
ax.contour (XG, YG, ZG, levels=12, colors='navy', linewidths=0.6, alpha=0.5)

# 梯度下降
ax.plot(gd_path[:,0], gd_path[:,1], 'tomato',
        lw=1.8, marker='o', ms=4, label=f'Gradient Descent ({len(gd_path)-1} steps, slow zigzag)')

# BFGS
ax.plot(bp[:,0], bp[:,1], 'seagreen',
        lw=2.2, marker='s', ms=6, label=f'BFGS ({len(bp)-1} steps, learns curvature)')

# Newton（只需 1-2 步就到了）
ax.plot(nt_path[:,0], nt_path[:,1], 'darkorange',
        lw=2.2, marker='^', ms=8, label=f'Newton ({len(nt_path)-1} steps, exact Hessian)')

# 起点与终点
ax.plot(*x0, 'ko', ms=10, zorder=10, label='Start')
ax.plot(0, 0, 'k*', ms=16, zorder=10, label='Minimum (0,0)')

ax.set_xlabel('x  (steep direction)', fontsize=11)
ax.set_ylabel('y  (shallow direction)', fontsize=11)
ax.set_title('Optimization paths on f(x,y)=5x²+0.5y²\n'
             'GD: only gradient  |  Newton: exact Hessian  |  BFGS: learned Hessian',
             fontsize=10)
ax.legend(fontsize=9, loc='upper right')
ax.set_xlim(-3.8, 3.8); ax.set_ylim(-5, 5)

# 标注 BFGS 关键步骤
for i, (xi, yi) in enumerate(bp[:5]):
    ax.annotate(f'B{i}', (xi, yi), fontsize=7, color='seagreen',
                xytext=(xi+0.15, yi+0.3))

plt.tight_layout()
plt.savefig('materials/figures/4.3B_bfgs_paths.png', dpi=130, bbox_inches='tight')
print("saved: materials/figures/4.3B_bfgs_paths.png")
