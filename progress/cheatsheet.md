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

## 2.3 — Components of the Model（四零件 + Bayes 定理）
- **四零件**（§2.3）：parameter p / likelihood Pr(W|p)=binom.pmf(W,N,p) / prior Pr(p) / posterior Pr(p|W)。
- **Bayes 定理**（p49–50）：`后验 = (似然 × 先验) / 平均似然`。
- **平均似然 Pr(W)**（分母）= `Σ(似然×先验)`（离散）=`∫like·prior dp`（连续）= 归一化常数，作用=让后验和为1。
  - 即昨天的 `post/post.sum()` 里那个 `.sum()`。
- ⚠️ 坑：分母乘 `prior(p)`（先验权重）不是 `p`（参数值）；似然 Pr(W|p) ≠ 后验 Pr(p|W)。
- Python：
  ```python
  unstd = binom.pmf(W,N,grid) * prior      # 似然×先验
  avg_like = unstd.sum()                    # 平均似然 = 分母
  posterior = unstd / avg_like
  ```

## 2.4 — Making the Model Go（三种引擎 + 二次近似）
- **三引擎**（p52）：① grid（切网格逐点算，教学用、随参数爆炸 p54）② quadratic（高斯近似）③ MCMC（抽样，ch8）。
- **quadratic approximation（=Laplace 近似）**：后验峰附近≈高斯，两数描述：MAP（峰）+ SD（宽）。
  - 两步（p55）：minimize 找峰 MAP；峰处算曲率 |f''| → `SD = 1/√|f''|`。
  - 理论链：对数后验 --二阶泰勒(近似)→ 抛物线 --exp(精确)→ 高斯；μ=MAP、σ²=1/|f''|。
  - 多维：|f''|→Hessian 矩阵，σ²=负 Hessian 的逆。
  - 何时准：大样本→后验趋高斯(Bernstein–von Mises)；小样本/偏态失真(Fig 2.8)。
  - MAP（均匀先验）= MLE = 观测频率 W/N；贝叶斯多给了 SD 与整条分布。
- ⚠️ 坑：① `(neg(m+eps)-neg(m))/eps` 括号别漏（/ 优先级高）；② 近似的是【对数后验】，不是高斯本身。
- Python（数值二阶导）：
  ```python
  neg = lambda p: -binom.logpmf(W, N, np.clip(p,1e-9,1-1e-9))
  m = minimize(neg, 0.5, bounds=[(1e-6,1-1e-6)]).x[0]
  second = (neg(m+eps) - 2*neg(m) + neg(m-eps))/eps**2   # 曲率
  sd = 1/np.sqrt(second)
  ```

## 3.1 — Sampling from a Grid-Approximate Posterior（从网格后验采样）
- **本章主旨**：后验算出来只是开始；本章用采样把"积分问题"变成"数数问题"（p62）。
- **采样一行**：`samples = rng.choice(p_grid, size=10000, p=posterior)` — 每个 p 按后验权重出现（p65）。
- **数数代积分**：`P(lo ≤ p < hi) = np.mean((samples >= lo) & (samples < hi))`。
- **直觉**：样本里各 p 的频率 ≈ 后验密度；大样本时误差 < 0.01（p66）。
- **为什么早学**：MCMC（ch8）只给样本不给公式，提前掌握样本处理以后水到渠成（p64）。
- **常见坑**：采样结果与网格解不需要精确相等，有随机波动是正常的。

## 3.2 — Sampling to Summarize（区间与点估计）
- **PI**：`np.percentile(s, [lo_pct, hi_pct])`，等尾，偏态时漏峰（p69）。
- **HPDI**：滑动窗口——排序→窗口大小 w=floor(prob×n)→枚举 x[i+w]-x[i]→取最小（p69–70）。
- **偏态 3/3 对比**：PI50≈[0.71,0.93] 宽0.22；HPDI50≈[0.84,1.00] 宽0.16，含峰更窄。
- **点估计选择**：绝对损失|d-p|→中位数；平方损失(d-p)²→均值；MAP=后验峰（p71–73）。
- **核心直觉**：整条后验才是估计，区间只是摘要；换区间结论就变 → 画整条后验（p70）。
- **坑**：多个区间之和=1 是集合覆盖，不是采样精度巧合。
