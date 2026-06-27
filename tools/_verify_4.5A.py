"""验证 §4.5 二次多项式回归参考解 + 生成可视化"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib.pyplot as plt

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
heights = d['height'].values    # 全部 544 人（含儿童）
weights = d['weight'].values

# 标准化
w_mean, w_std = weights.mean(), weights.std()
ws  = (weights - w_mean) / w_std
ws2 = ws ** 2

def neg_log_post_poly(params):
    a, b1, b2, log_sigma = params
    sigma = np.exp(log_sigma)
    mu_i  = a + b1 * ws + b2 * ws2
    ll    = np.sum(stats.norm.logpdf(heights, mu_i, sigma))
    lp_a  = stats.norm.logpdf(a, 178, 100)
    lp_b1 = stats.norm.logpdf(b1, 0, 10)
    lp_b2 = stats.norm.logpdf(b2, 0, 10)
    return -(ll + lp_a + lp_b1 + lp_b2)

res = minimize(neg_log_post_poly, [120, 20, -8, np.log(6)], method='BFGS')
a_m, b1_m, b2_m, sigma_m = res.x[0], res.x[1], res.x[2], np.exp(res.x[3])

print(f"MAP: a={a_m:.2f}, b1={b1_m:.2f}, b2={b2_m:.2f}, sigma={sigma_m:.2f}")
print(f"书中: a=146.66, b1=21.40, b2=-8.42, sigma=5.75 (p125)")

assert 140 < a_m < 155
assert 18  < b1_m < 25
assert -12 < b2_m < -5
assert 4.5 < sigma_m < 7
print("✅ 参考解通过")

# ── 可视化：线性 vs 多项式曲线 ──────────────────────────────
rng = np.random.default_rng(42)
post_p = rng.multivariate_normal(res.x, res.hess_inv, 10000)
ws_seq   = np.linspace(-2.2, 2.1, 80)
w_seq_kg = ws_seq * w_std + w_mean  # 还原为 kg 显示

mu_pred = (post_p[:, 0:1]
           + post_p[:, 1:2] * ws_seq[None, :]
           + post_p[:, 2:3] * ws_seq[None, :] ** 2)
mu_mean = mu_pred.mean(axis=0)
mu_lo   = np.percentile(mu_pred, 5.5, axis=0)
mu_hi   = np.percentile(mu_pred, 94.5, axis=0)
h_sim   = rng.normal(mu_pred, np.exp(post_p[:, 3:4]))
pi_lo   = np.percentile(h_sim, 5.5, axis=0)
pi_hi   = np.percentile(h_sim, 94.5, axis=0)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('§4.5  Polynomial Regression  (all 544 people, including children)',
             fontsize=12, fontweight='bold')

# 左图：数据点 + 多项式曲线 + HPDI
ax = axes[0]
adults = d['age'] >= 18
ax.scatter(weights[~adults], heights[~adults], s=8, alpha=0.4, color='tomato',  label='Children')
ax.scatter(weights[adults],  heights[adults],  s=8, alpha=0.2, color='steelblue', label='Adults')
ax.plot(w_seq_kg, mu_mean, 'k-', lw=2.5, label='Posterior mean (parabola)')
ax.fill_between(w_seq_kg, mu_lo, mu_hi, alpha=0.35, color='navy', label='89% HPDI of mean')
ax.fill_between(w_seq_kg, pi_lo, pi_hi, alpha=0.12, color='gray', label='89% Prediction PI')
ax.set_xlabel('Weight (kg)', fontsize=11)
ax.set_ylabel('Height (cm)', fontsize=11)
ax.set_title('Quadratic fit: mu = a + b1*w_s + b2*w_s^2\n'
             f'MAP: a={a_m:.1f}, b1={b1_m:.1f}, b2={b2_m:.1f} (<0: opens downward)',
             fontsize=9)
ax.legend(fontsize=8)

# 右图：为什么要标准化——原始体重平方有多大
ax2 = axes[1]
w_raw  = np.linspace(5, 65, 100)
ax2.plot(w_raw, w_raw**2,  'tomato',    lw=2, label='w^2 (raw, up to 4225!)')
ax2.plot(w_raw, w_raw**3/1000, 'orange', lw=2, ls='--', label='w^3 / 1000 (raw, huge)')
ws_raw  = (w_raw - w_mean) / w_std
ax2.plot(w_raw, ws_raw**2, 'steelblue', lw=2.5, label='w_s^2 (standardized, max ~5)')
ax2.axhline(0, color='gray', lw=0.7)
ax2.set_xlabel('Weight (kg)', fontsize=11)
ax2.set_ylabel('Value of polynomial term', fontsize=11)
ax2.set_title('Why standardize before squaring?\n'
              'Raw w^2 blows up (4225);  standardized w_s^2 stays small (~5)',
              fontsize=9)
ax2.legend(fontsize=8)
ax2.set_ylim(-10, 300)

plt.tight_layout()
import os; os.makedirs('materials/figures', exist_ok=True)
plt.savefig('materials/figures/4.5A_poly_reg.png', dpi=130, bbox_inches='tight')
print("saved: materials/figures/4.5A_poly_reg.png")
