"""隐藏测试：ch4 ex 4.3A — height_posterior（双参数网格近似）"""
import numpy as np
import pandas as pd
import os
# height_posterior 来自学生实现（judge.py 拼接）

# 加载数据
DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
heights = d[d['age'] >= 18]['height'].values

MU, SIGMA, post = height_posterior(heights)

# 形状
assert MU.shape == (100, 100),   f"MU 形状应 (100,100)，实际={MU.shape}"
assert SIGMA.shape == (100, 100), f"SIGMA 形状应 (100,100)，实际={SIGMA.shape}"
assert post.shape == (100, 100),  f"post 形状应 (100,100)，实际={post.shape}"

# 归一化
assert np.isclose(post.sum(), 1.0, atol=1e-5), f"后验应归一化，sum={post.sum():.6f}"

# 所有值非负
assert (post >= 0).all(), "后验值不应有负数"

# MAP 在合理范围
idx = np.unravel_index(post.argmax(), post.shape)
mu_map    = MU[idx]
sigma_map = SIGMA[idx]
assert 154.0 < mu_map < 156.0,    f"μ MAP 应≈154.6，实际={mu_map:.2f}"
assert 7.0   < sigma_map < 9.0,   f"σ MAP 应≈7.7，实际={sigma_map:.2f}"

# 后验集中度（中心区域应含大部分质量）
mid_post = post[25:75, 25:75]
assert mid_post.sum() > 0.5, "后验应集中在格点中心区域"

# 小样本测试（不应崩溃）
small_h = heights[:30]
MU2, SIGMA2, post2 = height_posterior(small_h)
assert np.isclose(post2.sum(), 1.0, atol=1e-5), "小样本归一化失败"

print("4.3A ALL PASS")
