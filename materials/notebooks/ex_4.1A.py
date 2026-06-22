"""
练习 4.1-1（OJ）：实现随机游走的高斯涌现

函数签名：gaussian_by_addition(n_steps, n_people=10000, seed=42) -> np.ndarray
- 让 n_people 个人各走 n_steps 步，每步从 Uniform(-1, 1) 采样距离
- 返回 n_people 个人的最终位置数组（形状 (n_people,)）

判题：python3 tools/judge.py materials/notebooks/ex_4.1A.py materials/notebooks/tests/_4.1A.py
"""
import numpy as np


def gaussian_by_addition(n_steps, n_people=10000, seed=42):
    rng = np.random.default_rng(seed)
    steps = rng.uniform(-1, 1, (n_people, n_steps))  # shape: (n_people, n_steps)
    return steps.sum(axis=1)                          # 每人的步长求和 → shape: (n_people,)
