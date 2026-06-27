"""验证 4.4A 参考解"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize

def fit_linear_map(heights, weights):
    heights = np.asarray(heights, dtype=float)
    weights = np.asarray(weights, dtype=float)
    def neg_log_post(params):
        a, b, log_sigma = params
        sigma = np.exp(log_sigma)
        mu_i  = a + b * weights
        ll    = np.sum(stats.norm.logpdf(heights, mu_i, sigma))
        lp_a  = stats.norm.logpdf(a, 178, 100)
        lp_b  = stats.norm.logpdf(b, 0, 10)
        return -(ll + lp_a + lp_b)
    res = minimize(neg_log_post, [114, 0.9, np.log(5)], method='BFGS')
    return res.x[0], res.x[1], np.exp(res.x[2])

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
d2 = d[d['age'] >= 18]
a, b, s = fit_linear_map(d2['height'].values, d2['weight'].values)
print(f"α={a:.2f}, β={b:.2f}, σ={s:.2f}")
assert 111 < a < 117 and 0.84 < b < 0.96 and 4.7 < s < 5.4
print("✅ 参考解通过")
