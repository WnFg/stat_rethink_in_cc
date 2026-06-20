# 隐藏测试 · 3.1A · prob_between（学生勿看）
import numpy as np
from scipy.stats import binom
p = np.linspace(0, 1, 1000); post = binom.pmf(6, 9, p); post /= post.sum()
s = np.random.default_rng(100).choice(p, size=20000, p=post)
assert abs(prob_between(s, 0.0, 0.5) - post[p < 0.5].sum()) < 0.02, "应与网格求和一致(≈0.172)"
assert abs(prob_between(s, 0.5, 0.75) - 0.606) < 0.03, "0.5~0.75 应≈0.61"
assert np.isclose(prob_between(s, 0.0, 1.01), 1.0), "全区间应=1"
print("（隐藏测试：3 项断言）")
