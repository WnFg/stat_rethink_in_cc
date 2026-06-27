"""隐藏测试：ch4 ex 4.5A — fit_poly_map（二次多项式回归）"""
import numpy as np
import pandas as pd
# fit_poly_map 来自学生实现（judge.py 拼接）

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
heights = d['height'].values    # 544 人（含儿童）
weights = d['weight'].values

a, b1, b2, s = fit_poly_map(heights, weights)
a, b1, b2, s = float(a), float(b1), float(b2), float(s)

# T1：MAP 值（书 p125）
assert 140 < a < 155,   f"alpha 应≈146.66，实际={a:.2f}"
assert 18  < b1 < 25,   f"beta1 应≈21.40，实际={b1:.2f}"
assert -12 < b2 < -5,   f"beta2 应≈-8.42（负=开口向下），实际={b2:.2f}"
assert 4.5 < s  < 7.0,  f"sigma 应≈5.75，实际={s:.2f}"
print(f"T1 PASS: a={a:.2f}, b1={b1:.2f}, b2={b2:.2f}, sigma={s:.2f}")

# T2：beta2 < 0（抛物线开口向下，符合生长曲线形状）
assert b2 < 0, f"beta2 应<0（开口向下），实际={b2:.2f}"
print("T2 PASS: beta2 < 0 (parabola opens downward)")

# T3：比线性模型 sigma 更小（多项式拟合更好）
linear_sigma = 5.07   # §4.4 成人线性模型（参考值，此处用全数据对比意义有限，但 poly 应该更好）
assert s < linear_sigma + 2.0, f"多项式 sigma 应合理，实际={s:.2f}"
print(f"T3 PASS: sigma={s:.2f} < linear_sigma+2={linear_sigma+2:.2f}")

# T4：预测在合理范围（50–200 cm）
ws_test = np.array([-2, -1, 0, 1, 2], dtype=float)
mu_test = a + b1 * ws_test + b2 * ws_test**2
assert mu_test.min() > 50 and mu_test.max() < 210, \
    f"预测均值超出合理范围：{mu_test}"
print(f"T4 PASS: 预测范围 [{mu_test.min():.1f}, {mu_test.max():.1f}] cm")

# T5：标准化用自身数据（不是硬编码均值）
# 用子集测试：结果应该不同
heights_sub = heights[:100]; weights_sub = weights[:100]
a2, b1_2, b2_2, s2 = fit_poly_map(heights_sub, weights_sub)
assert abs(float(a2) - a) > 0.1, "应用传入数据自己算标准化，不要硬编码均值/标准差"
print("T5 PASS: 标准化使用传入数据（非硬编码）")

print(f"\n书中结果 (p125): a=146.66, b1=21.40, b2=-8.42, sigma=5.75")
print(f"你的结果:        a={a:.2f}, b1={b1:.2f}, b2={b2:.2f}, sigma={s:.2f}")
print("4.5A ALL PASS")
