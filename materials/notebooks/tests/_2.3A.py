# 隐藏测试 · 练习 2.3A · posterior_bayes（学生勿看）
import numpy as np
from scipy.stats import binom

g = np.linspace(0, 1, 1000)
avg, post = posterior_bayes(g, 6, 9)

assert np.ndim(avg) == 0 and avg > 0, "avg_like 应是一个正的标量"
assert len(post) == len(g) and np.isclose(post.sum(), 1), "后验应归一化"
assert abs(g[np.argmax(post)] - 6/9) < 0.01, "峰值应≈6/9"

# 核心：avg_like 正是归一化分母 —— post * avg_like 应还原出 似然×先验
like = binom.pmf(6, 9, g)
pri = np.ones_like(g) / len(g)
assert np.allclose(post * avg, like * pri), "post×avg_like 应等于 似然×先验（avg=分母）"

# 均匀先验 None == 显式全 1
avg2, post2 = posterior_bayes(g, 6, 9, prior=np.ones_like(g))
assert np.allclose(post, post2), "均匀先验应与 None 等价"

# 不同先验会改变 avg_like
avg3, _ = posterior_bayes(g, 6, 9, prior=(g >= 0.5).astype(float))
assert not np.isclose(avg, avg3), "换先验应改变 avg_like"

print("（隐藏测试：6 项断言）")
