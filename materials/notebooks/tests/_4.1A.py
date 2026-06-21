"""隐藏测试：ch4 ex 4.1A — gaussian_by_addition"""
import numpy as np
from scipy import stats as sp_stats
from ex_4_1A import gaussian_by_addition  # 学生实现

pos_4  = gaussian_by_addition(4)
pos_16 = gaussian_by_addition(16)
pos_64 = gaussian_by_addition(64)

# 返回值类型和长度
assert isinstance(pos_16, np.ndarray), "应返回 np.ndarray"
assert len(pos_16) == 10000, f"默认 n_people=10000，实际={len(pos_16)}"

# 均值应≈0
assert abs(pos_16.mean()) < 0.15, f"mean 应≈0，实际={pos_16.mean():.3f}"

# 方差应≈n_steps/3
for n, p in [(4, pos_4), (16, pos_16), (64, pos_64)]:
    expected_std = np.sqrt(n / 3)
    assert abs(p.std() - expected_std) < 0.5, \
        f"n={n}: std={p.std():.2f}，expected≈{expected_std:.2f}"

# 步数越多越正态（Shapiro-Wilk: n=16 步应被接受为正态）
rng = np.random.default_rng(0)
_, shap_n4  = sp_stats.shapiro(rng.choice(pos_4,  800, replace=False))
_, shap_n16 = sp_stats.shapiro(rng.choice(pos_16, 800, replace=False))
assert shap_n16 > 0.01, f"n=16 步应接近正态，Shapiro pval={shap_n16:.4f}"

# seed 固定 → 可复现
p1 = gaussian_by_addition(16, seed=7)
p2 = gaussian_by_addition(16, seed=7)
assert np.allclose(p1, p2), "相同 seed 应得相同结果"

print("4.1A ALL PASS")
