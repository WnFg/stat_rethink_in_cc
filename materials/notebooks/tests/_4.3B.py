"""隐藏测试：ch4 ex 4.3B — map_quap（MAP 二次近似 + 多维后验采样）"""
import numpy as np
import pandas as pd
# map_quap 来自学生实现（judge.py 拼接）

DATA_PATH = 'materials/data/Howell1.csv'
d = pd.read_csv(DATA_PATH, sep=';')
heights = d[d['age'] >= 18]['height'].values   # 352 人

# ── T1：返回值类型与形状 ──────────────────────────────────────
result = map_quap(heights)
assert isinstance(result, tuple) and len(result) == 3, \
    f"应返回 3 元素 tuple，实际={type(result)}"
mu_map, sigma_map, post_samples = result
assert isinstance(post_samples, np.ndarray), "post_samples 应为 np.ndarray"
assert post_samples.shape == (10000, 2), \
    f"post_samples 形状应为 (10000, 2)，实际={post_samples.shape}"
print("T1 PASS: 返回值类型与形状")

# ── T2：MAP 值（书 p100：μ≈154.61, σ≈7.73）──────────────────
assert 154.0 < float(mu_map) < 156.0, \
    f"mu_map 应≈154.6，实际={mu_map:.3f}"
assert 7.0 < float(sigma_map) < 8.5, \
    f"sigma_map 应≈7.7，实际={sigma_map:.3f}"
print(f"T2 PASS: MAP mu={mu_map:.3f}, sigma={sigma_map:.3f}")

# ── T3：后验样本均值与 MAP 接近 ──────────────────────────────
mu_samp_mean  = float(post_samples[:, 0].mean())
sig_samp_mean = float(post_samples[:, 1].mean())
assert abs(mu_samp_mean - mu_map) < 0.5, \
    f"样本 mu 均值={mu_samp_mean:.3f} 与 MAP {mu_map:.3f} 偏差过大"
assert abs(sig_samp_mean - sigma_map) < 0.5, \
    f"样本 sigma 均值={sig_samp_mean:.3f} 与 MAP {sigma_map:.3f} 偏差过大"
print(f"T3 PASS: 样本均值 mu={mu_samp_mean:.3f}, sigma={sig_samp_mean:.3f}")

# ── T4：后验样本标准差（书 p100：SE(μ)≈0.41, SE(σ)≈0.29）───
mu_std  = float(post_samples[:, 0].std())
sig_std = float(post_samples[:, 1].std())
assert 0.2 < mu_std < 0.8, \
    f"mu 样本 std 应≈0.41，实际={mu_std:.3f}（Hessian 逆正确？）"
assert 0.1 < sig_std < 0.6, \
    f"sigma 样本 std 应≈0.29，实际={sig_std:.3f}（exp 还原？）"
print(f"T4 PASS: 样本 std  mu={mu_std:.3f}, sigma={sig_std:.3f}")

# ── T5：n_samples 参数生效 ───────────────────────────────────
_, _, s2 = map_quap(heights, n_samples=500, seed=0)
assert s2.shape == (500, 2), f"n_samples=500 时形状应 (500,2)，实际={s2.shape}"
print("T5 PASS: n_samples 参数正确")

# ── T6：σ 样本全部为正（exp 还原正确）───────────────────────
assert (post_samples[:, 1] > 0).all(), "sigma 样本应全部为正（exp(log_sigma)？）"
print("T6 PASS: sigma 样本全部为正")

print(f"\n书中结果 (p100): mu=154.61±0.41, sigma=7.73±0.29")
print(f"你的结果:        mu={mu_map:.2f}±{mu_std:.2f}, sigma={sigma_map:.2f}±{sig_std:.2f}")
print("4.3B ALL PASS")
