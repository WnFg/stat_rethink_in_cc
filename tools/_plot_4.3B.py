"""§4.3b 课堂图：双参数后验热力图 + MAP 点 + 后验采样点"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
heights = d[d['age'] >= 18]['height'].values

# ── 网格后验（绘图用）────────────────────────────────────────
mu_list    = np.linspace(150, 160, 200)
sigma_list = np.linspace(4, 12, 200)
MU, SIGMA  = np.meshgrid(mu_list, sigma_list)
log_lik    = np.sum(stats.norm.logpdf(heights[:, None, None], MU[None], SIGMA[None]), axis=0)
log_prior_mu    = stats.norm.logpdf(MU, 178, 20)
log_prior_sigma = np.where((SIGMA > 0) & (SIGMA <= 50), 0.0, -np.inf)
log_post = log_lik + log_prior_mu + log_prior_sigma
log_post -= log_post.max()
post = np.exp(log_post)
post /= post.sum()

# ── MAP 二次近似 ─────────────────────────────────────────────
def neg_log_post(params):
    mu, log_sigma = params
    sigma = np.exp(log_sigma)
    if sigma <= 0 or sigma > 50:
        return np.inf
    ll    = np.sum(stats.norm.logpdf(heights, mu, sigma))
    lp_mu = stats.norm.logpdf(mu, 178, 20)
    return -(ll + lp_mu)

res = minimize(neg_log_post, x0=[170.0, np.log(8.0)], method='BFGS')
mu_map    = res.x[0]
sigma_map = np.exp(res.x[1])

eps = 1e-4; x0 = res.x; H = np.zeros((2,2))
for i in range(2):
    for j in range(2):
        xpp=x0.copy(); xpp[i]+=eps; xpp[j]+=eps
        xpm=x0.copy(); xpm[i]+=eps; xpm[j]-=eps
        xmp=x0.copy(); xmp[i]-=eps; xmp[j]+=eps
        xmm=x0.copy(); xmm[i]-=eps; xmm[j]-=eps
        H[i,j]=(neg_log_post(xpp)-neg_log_post(xpm)-neg_log_post(xmp)+neg_log_post(xmm))/(4*eps**2)
cov_log = np.linalg.inv(H)

rng = np.random.default_rng(42)
samp_log = rng.multivariate_normal(res.x, cov_log, size=300)
samp_mu  = samp_log[:, 0]
samp_sig = np.exp(samp_log[:, 1])

# ── 绘图 ─────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle('§4.3b  Joint Posterior: MAP Quadratic Approximation + Samples', fontsize=12, fontweight='bold')

# Left: joint posterior heatmap + MAP + samples
ax = axes[0]
ax.contourf(mu_list, sigma_list, post, levels=30, cmap='Blues')
ax.contour (mu_list, sigma_list, post, levels=8,  colors='navy', alpha=0.4, linewidths=0.7)
ax.scatter(samp_mu, samp_sig, s=6, c='tomato', alpha=0.5, label='Posterior samples (n=300)\nfrom quadratic approx')
ax.plot(mu_map, sigma_map, 'k*', markersize=14, label=f'MAP  mu={mu_map:.2f}, sigma={sigma_map:.2f}')
ax.set_xlabel('mu  (mean height, cm)', fontsize=11)
ax.set_ylabel('sigma  (std height, cm)', fontsize=11)
ax.set_title('Joint Posterior Pr(mu, sigma | heights)\nBlue=grid approx  Red dots=quap samples', fontsize=10)
ax.legend(fontsize=8)

# Right: marginal of mu
se_mu    = np.sqrt(cov_log[0, 0])
se_sigma = np.sqrt(cov_log[1, 1]) * sigma_map  # delta method
ax2 = axes[1]
ax2.hist(samp_mu,  bins=30, color='steelblue', alpha=0.6, density=True, label='mu samples (quap)')
x_mu = np.linspace(mu_map - 4*se_mu, mu_map + 4*se_mu, 200)
ax2.plot(x_mu, stats.norm.pdf(x_mu, mu_map, se_mu), 'b-', lw=2.5,
         label=f'Theory N({mu_map:.2f}, {se_mu:.2f}^2)')
ax2.set_xlabel('mu (cm)', fontsize=11)
ax2.set_ylabel('Density', fontsize=11)
ax2.set_title(f'Marginal posterior of mu\nSE(mu) from Hessian = {se_mu:.2f} cm  SE(sigma) = {se_sigma:.2f} cm', fontsize=9)
ax2.legend(fontsize=9)

plt.tight_layout()
os.makedirs('materials/figures', exist_ok=True)
plt.savefig('materials/figures/4.3B_map_quap.png', dpi=130, bbox_inches='tight')
print("图已保存: materials/figures/4.3B_map_quap.png")
