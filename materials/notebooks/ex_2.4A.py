"""练习 2.4A · 二次近似 quadratic approximation（OJ 形式）

判题：python3 tools/judge.py materials/notebooks/ex_2.4A.py materials/notebooks/tests/_2.4A.py
"""
import numpy as np
from scipy.stats import binom
from scipy.optimize import minimize


def quap_globe(W, N):
    """对 globe tossing 后验做二次近似（均匀先验），返回高斯近似的两个参数。

    输入： W, N —— 水的个数 / 总抛掷数
    输出： (map_p, sd)
        map_p : 后验峰值 MAP（均匀先验下 = MLE）
        sd    : 峰附近的标准差（由二阶导/曲率估计）

    二次近似两步（§2.4.2, p55）：
      1. 找峰：最小化 "负对数后验"。均匀先验下后验 ∝ 似然，故最小化 -logpmf。
      2. 估曲率：在峰处算负对数后验的二阶导 second，则 sd = 1/sqrt(second)。

    脚手架已给好，补全两个 TODO 即可。
    """
    # 负对数后验（均匀先验 ∝ -log 似然）；clip 防 log(0)
    neg = lambda p: -binom.logpmf(W, N, np.clip(p, 1e-9, 1 - 1e-9))

    # 1) 找峰 MAP：用 minimize 从 0.5 出发，bounds=[(1e-6, 1-1e-6)]
    res = minimize(neg, 0.5, method="L-BFGS-B", bounds=[(1e-6, 1 - 1e-6)])
    map_p = res.x[0]

    # 2) 估曲率：二阶导 = (前向一阶导 − 后向一阶导) / eps  —— 学生自己的推法
    eps = 1e-4
    forward  = (neg(map_p + eps) - neg(map_p)) / eps          # 前向一阶导
    backward = (neg(map_p) - neg(map_p - eps)) / eps          # 后向一阶导
    second = (forward - backward) / eps                       # 二阶导（= 曲率 |f''|）
    sd = 1 / np.sqrt(second)

    return map_p, sd
