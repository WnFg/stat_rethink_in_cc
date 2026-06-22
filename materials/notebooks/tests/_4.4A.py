"""隐藏测试：ch4 ex 4.4A — fit_linear_map（线性回归 MAP）"""
import numpy as np
import pandas as pd
import os
# fit_linear_map 来自学生实现（judge.py 拼接）

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
d2 = d[d['age'] >= 18]
heights = d2['height'].values
weights = d2['weight'].values

a, b, s = fit_linear_map(heights, weights)

# 返回值均为标量
assert np.isscalar(a) or (hasattr(a, '__len__') and len(np.asarray(a)) == 1), \
    f"alpha 应为标量"

a, b, s = float(a), float(b), float(s)

# 书中值（p111）: α≈113.90, β≈0.90, σ≈5.07
assert 111.0 < a < 117.0, f"α 应≈113.9，实际={a:.2f}"
assert 0.84  < b < 0.96,  f"β 应≈0.90，实际={b:.2f}"
assert 4.7   < s < 5.4,   f"σ 应≈5.07，实际={s:.2f}"

# σ > 0
assert s > 0, "σ 应为正数"

# 预测合理性：每增加 10 kg 体重，身高增加约 8-10 cm
assert 8.4 < b * 10 < 9.6, f"10kg → Δheight 应约 9cm，实际={b*10:.2f}"

# 在均值体重处，预测身高≈均值身高
w_mean = weights.mean()
h_pred_at_wmean = a + b * w_mean
assert abs(h_pred_at_wmean - heights.mean()) < 2.0, \
    f"均值体重处预测身高应≈均值身高={heights.mean():.1f}，实际={h_pred_at_wmean:.1f}"

print("4.4A ALL PASS")
