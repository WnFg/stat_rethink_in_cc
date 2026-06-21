"""隐藏测试：3.3A posterior_predictive"""
import numpy as np
from scipy.stats import binom

def posterior_predictive(samples, n, rng):
    return rng.binomial(n, samples)

p = np.linspace(0, 1, 1000); post = binom.pmf(6, 9, p); post /= post.sum()
rng = np.random.default_rng(7)
s = rng.choice(p, size=20000, p=post)
ppc = posterior_predictive(s, 9, rng)

assert ppc.shape == s.shape,               "输出长度应与 samples 相同"
assert ppc.min() >= 0 and ppc.max() <= 9,  "计数应在 0..9 范围内"
assert np.argmax(np.bincount(ppc, minlength=10)) in (6, 7), "众数应在观测值 6 附近"

point = rng.binomial(9, 0.667, size=20000)
assert ppc.std() > point.std(), "后验预测应比点估计预测更宽（更诚实）"

print("3.3A ok")
