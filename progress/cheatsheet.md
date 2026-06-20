# 速查 Cheatsheet（累积）

每节课后追加：公式、关键直觉、Python 片段、常见坑。按 `## 章.节 — 标题` 分段。

## 2.1 — The Garden of Forking Data（数路径花园）
- **核心**：贝叶斯推断 = 数"有多少种方式产生观测数据"，再比大小（p33）。全是数数，无玄学。
- **数路径**：每次观测是一层分叉；各层可能数**相乘**得总路径数；观测把不符路径**剪枝**（p34–36）。
- **标准化**：`posterior = ways / ways.sum()` → 一条**概率分布**（不是一个点）（p39–40）。
- **四词汇**（p40）：parameter `p`（要估的未知量）/ likelihood（某 p 的相对路径数）/ prior（初始权重）/ posterior（标准化后）。
- **乘先验**（p38）：有先验信息时 `新计数 = 先验计数 × 新路径数`，等价于增量更新。
- Python 速记：
  ```python
  import numpy as np
  blue = np.array([0,1,2,3,4]); white = 4 - blue
  ways = blue * white * blue          # 观测 🔵⚪🔵 的三层相乘
  std  = ways / ways.sum()            # 标准化为概率
  ```
- ⚠️ 坑：似然(路径数)未必归一；归一后才是概率。别忘了 ÷总和。

## 2.2 — Building a Model（globe tossing）
- **场景**：抛地球仪估水比例 p；观测 `W L W W W L W L W`=6W3L（p41）。离散弹珠→连续 p，逻辑不变。
- **data story**（p42）：独立+二值+同一 p ⟹ Binomial(N,p)。故事可丢、多对一——拟合好≠因果故事对。
- **Bayesian updating**（p43–44）：均匀先验起，逐数据更新；见 W 峰右移、见 L 左移；越多越窄；**顺序无关**。
- **逐步≡一次性**：逐次伯努利 `p^W(1-p)^L` 与二项 `C(N,W)p^W(1-p)^L` 只差常数 C(N,W)，归一化约掉 ⇒ 同后验。
- Python：
  ```python
  post = prior * binom.pmf(W, N, grid)   # 一次性二项
  post = post / post.sum()
  ```
- OJ 练习用 `tools/judge.py 学生实现 隐藏测试`。
