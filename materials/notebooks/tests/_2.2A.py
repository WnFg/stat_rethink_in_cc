# 隐藏测试集 · 练习 2.2A · bayes_update（学生勿看）
import numpy as np

g = np.linspace(0, 1, 1000)
post = bayes_update(g, "WLWWWLWLW")

# 形状与归一化
assert len(post) == len(g), "返回长度应与 grid 相同"
assert np.isclose(post.sum(), 1), "后验应归一化（和为 1）"

# 峰值 ≈ 6/9（连续 MLE）
assert abs(g[np.argmax(post)] - 2/3) < 0.01, "WLWWWLWLW 的后验峰值应≈0.667"

# 顺序无关（p44）
assert np.allclose(post, bayes_update(g, "WWWWWWLLL")), "更新应与数据顺序无关"

# 见到一个 W：p=0 不可能；后验偏向大 p
single = bayes_update(g, "W")
assert np.isclose(single[0], 0), "只见 W 时，p=0 的后验应为 0"
assert np.sum(g * single) > 0.5, "只见 W 时，后验均值应 > 0.5"

# 均匀先验（None）应等价于显式全 1 先验
assert np.allclose(bayes_update(g, "WLWWWLWLW", prior=np.ones_like(g)), post), "均匀先验应与 None 等价"

# 数据越多后验越窄
def _sd(d):
    m = np.sum(g * d); return np.sqrt(np.sum(d * (g - m) ** 2))
assert _sd(bayes_update(g, "WLWWWLWLW" * 2)) < _sd(post), "数据翻倍（同比例）后验应更窄"

print("（隐藏测试：8 项断言）")
