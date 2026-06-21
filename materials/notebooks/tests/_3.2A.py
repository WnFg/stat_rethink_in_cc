"""隐藏测试：3.2A hpdi"""
import numpy as np
from scipy.stats import binom

# 参考解（老师用，判题时注入）
def hpdi(samples, prob=0.5):
    x = np.sort(samples); n = len(x); w = int(np.floor(prob * n))
    widths = x[w:] - x[:n - w]; i = int(np.argmin(widths))
    return x[i], x[i + w]

# ── 测试 1：偏态后验 3/3，HPDI 必含峰(≈1)且比 PI 窄 ──
p = np.linspace(0, 1, 1000); post = binom.pmf(3, 3, p); post /= post.sum()
s = np.random.default_rng(1).choice(p, size=30000, p=post)
lo, hi = hpdi(s, 0.5)
assert hi > 0.97, f"HPDI 上界应接近 1，实际={hi:.3f}"
assert (hi - lo) <= (np.percentile(s, 75) - np.percentile(s, 25)) + 1e-9, "HPDI 不应比 PI 宽"

# ── 测试 2：对称后验 6/9，HPDI ≈ PI（容差 0.05）──
post2 = binom.pmf(6, 9, p); post2 /= post2.sum()
s2 = np.random.default_rng(2).choice(p, size=30000, p=post2)
lo2, hi2 = hpdi(s2, 0.8); pi2 = np.percentile(s2, [10, 90])
assert abs(lo2 - pi2[0]) < 0.05, f"对称后验 HPDI lo 应≈PI lo，差={abs(lo2-pi2[0]):.3f}"
assert abs(hi2 - pi2[1]) < 0.05, f"对称后验 HPDI hi 应≈PI hi，差={abs(hi2-pi2[1]):.3f}"

# ── 测试 3：prob=0.9，区间宽度合理（< 0.6）──
lo3, hi3 = hpdi(s, 0.9)
assert hi3 - lo3 < 0.6, "90% HPDI 宽度应 < 0.6"
assert lo3 >= 0 and hi3 <= 1.001, "区间应在 [0,1] 内"

print("3.2A ok")
