"""§4.4 课堂图：后验直线云 + 均值HPDI + 预测PI"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib.pyplot as plt

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
d2 = d[d['age'] >= 18].reset_index(drop=True)
heights = d2['height'].values
weights = d2['weight'].values

def neg_log_post_lm(params):
    a, b, log_sigma = params
    sigma = np.exp(log_sigma)
    mu_i  = a + b * weights
    ll    = np.sum(stats.norm.logpdf(heights, mu_i, sigma))
    lp_a  = stats.norm.logpdf(a, 178, 100)
    lp_b  = stats.norm.logpdf(b, 0, 10)
    return -(ll + lp_a + lp_b)

res = minimize(neg_log_post_lm, [114, 0.9, np.log(5)], method='BFGS')
a_map, b_map, sigma_map = res.x[0], res.x[1], np.exp(res.x[2])

rng = np.random.default_rng(42)
post_samples = rng.multivariate_normal(res.x, res.hess_inv, size=10000)
a_samp     = post_samples[:, 0]
b_samp     = post_samples[:, 1]
sigma_samp = np.exp(post_samples[:, 2])

w_seq = np.linspace(25, 70, 100)
mu_mat = a_samp[:, None] + b_samp[:, None] * w_seq[None, :]  # (10000, 100)
mu_mean     = mu_mat.mean(axis=0)
mu_lo       = np.percentile(mu_mat,  5.5, axis=0)
mu_hi       = np.percentile(mu_mat, 94.5, axis=0)
h_sim       = rng.normal(mu_mat, sigma_samp[:, None])
pi_lo       = np.percentile(h_sim,  5.5, axis=0)
pi_hi       = np.percentile(h_sim, 94.5, axis=0)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('§4.4  Linear Regression Posterior  (height ~ alpha + beta*weight)',
             fontsize=12, fontweight='bold')

# ── 左图：20条后验采样直线（"后验 = 无数条直线的分布"）
ax = axes[0]
ax.scatter(weights, heights, s=8, alpha=0.3, color='steelblue', label='Data (n=352)')
idx20 = rng.choice(10000, 20, replace=False)
for i in idx20:
    ax.plot(w_seq, a_samp[i] + b_samp[i]*w_seq, 'tomato', alpha=0.25, lw=0.9)
ax.plot(w_seq, mu_mean, 'k-', lw=2, label=f'MAP line: h={a_map:.1f}+{b_map:.2f}w')
ax.set_xlabel('Weight (kg)', fontsize=11)
ax.set_ylabel('Height (cm)', fontsize=11)
ax.set_title('Posterior = distribution over lines\n20 sampled lines (red) from quap posterior',
             fontsize=9)
ax.legend(fontsize=8)

# ── 右图：均值HPDI + 预测PI
ax2 = axes[1]
ax2.scatter(weights, heights, s=8, alpha=0.25, color='steelblue')
ax2.plot(w_seq, mu_mean, 'k-', lw=2, label='Posterior mean line')
ax2.fill_between(w_seq, mu_lo, mu_hi, alpha=0.4, color='navy',
                 label='89% HPDI of mean (parameter uncertainty)')
ax2.fill_between(w_seq, pi_lo, pi_hi, alpha=0.15, color='tomato',
                 label='89% PI (prediction = mean + sigma)')
ax2.set_xlabel('Weight (kg)', fontsize=11)
ax2.set_ylabel('Height (cm)', fontsize=11)
ax2.set_title('Two kinds of uncertainty (§4.4.3.4-5, p115-122)\n'
              'Blue=parameter  Red=prediction (much wider)',
              fontsize=9)
ax2.legend(fontsize=8)

plt.tight_layout()
plt.savefig('materials/figures/4.4A_linear_reg.png', dpi=130, bbox_inches='tight')
print("saved: materials/figures/4.4A_linear_reg.png")
print(f"MAP: alpha={a_map:.2f}, beta={b_map:.2f}, sigma={sigma_map:.2f}")
