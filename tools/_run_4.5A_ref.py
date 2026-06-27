"""参考解 + 隐藏测试验证"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize

def fit_poly_map(heights, weights):
    heights = np.asarray(heights, dtype=float)
    weights = np.asarray(weights, dtype=float)
    w_mean, w_std = weights.mean(), weights.std()
    ws  = (weights - w_mean) / w_std
    ws2 = ws ** 2
    def neg_log_post(params):
        a, b1, b2, log_sigma = params
        sigma = np.exp(log_sigma)
        mu_i  = a + b1 * ws + b2 * ws2
        ll    = np.sum(stats.norm.logpdf(heights, mu_i, sigma))
        lp_a  = stats.norm.logpdf(a, 178, 100)
        lp_b1 = stats.norm.logpdf(b1, 0, 10)
        lp_b2 = stats.norm.logpdf(b2, 0, 10)
        return -(ll + lp_a + lp_b1 + lp_b2)
    res = minimize(neg_log_post, [120, 20, -8, np.log(6)], method='BFGS')
    return res.x[0], res.x[1], res.x[2], np.exp(res.x[3])

# 隐藏测试
DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
heights = d['height'].values
weights = d['weight'].values

a, b1, b2, s = fit_poly_map(heights, weights)
a, b1, b2, s = float(a), float(b1), float(b2), float(s)

assert 140 < a < 155
assert 18  < b1 < 25
assert -12 < b2 < -5
assert 4.5 < s  < 7.0
print(f"T1 PASS: a={a:.2f}, b1={b1:.2f}, b2={b2:.2f}, sigma={s:.2f}")
assert b2 < 0
print("T2 PASS: beta2 < 0")
assert s < 5.07 + 2.0
print(f"T3 PASS: sigma={s:.2f}")
ws_test = np.array([-2, -1, 0, 1, 2], dtype=float)
mu_test = a + b1 * ws_test + b2 * ws_test**2
assert mu_test.min() > 50 and mu_test.max() < 210
print(f"T4 PASS: 预测范围 [{mu_test.min():.1f}, {mu_test.max():.1f}]")
heights_sub = heights[:100]; weights_sub = weights[:100]
a2, b1_2, b2_2, s2 = fit_poly_map(heights_sub, weights_sub)
assert abs(float(a2) - a) > 0.1
print("T5 PASS: 标准化使用传入数据")
print("\n✅ 参考解通过全部 5 项测试")
