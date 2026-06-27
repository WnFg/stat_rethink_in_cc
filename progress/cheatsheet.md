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

## 3.3 — Sampling to Simulate Prediction（后验预测检查）
- **生成数据**：`rng.binomial(n, p)` — p 是数组时广播，输出等形整数数组（p74）。
- **后验预测**：`ppc = rng.binomial(n, samples)` — 一行传播参数不确定性（p78–79）。
- **为何不用点估计**：`rng.binomial(n, map_p)` 过度自信，std 更窄（p79）。
- **PPC 检验**：不只看水数，换角度（最长游程、切换次数）；观测落尾部=模型失败（p81）。
- **坑**：模型检查不是判对错——所有模型都错，看"怎么错、要不要紧"（p78）。

## 4.1 — Why Normal Distributions are Normal（正态分布为何正态）
- **地心模型**：线性回归=托勒密地心模型，描述有用、结构可能全错；用之有益、信之危险（p84）。
- **三条路径** → 高斯：① 加法（CLT）② 小效应乘法≈加法 ③ 大效应对数乘法=对数之和（p85–88）。
- **CLT 直觉**：大量叠加→波动互相抵消→落在均值的路径最多→钟形（p86–87）。
- **关键公式**：`Var(Uniform(-1,1)) = 1/3`；`Var(n步和) = n/3`；`std = sqrt(n/3)`（步数×4 → std×2）。
- **独立方差相加**：`Var(X₁+…+Xₙ) = n × Var(X₁)`（独立时，p85–86）。
- **两类辩护**：本体论（物理加法机制产生高斯）; 认识论（仅知均值/方差→高斯=最大熵=最保守，p88–89）。
- **Python**：`rng.uniform(-1,1,(n_people,n_steps)).sum(axis=1)` → shape (n_people,) 的位置数组。
- **坑**：不要"因为数据看起来正态就用高斯"——辩护来自机制，不来自外貌（p93）。

## 4.2 — A Language for Describing Models（模型规范语言）
- **~**：随机关系，变量服从分布（不确定）；**=**：确定关系，由其他量完全决定。
- **结构**：第一行 likelihood（~）；其余行 prior（~）；linear model 用 `=`（无随机性）。
- **Globe Tossing 规范**：`w ~ Binomial(n, p)` / `p ~ Uniform(0, 1)`（两行搞定所有假设）。
- **先验预测**：`μ_s ~ prior; σ_s ~ prior; yi = rng.normal(μ_s, σ_s)` → 检验先验合理性（p95–96）。
- **下标 i**：`μi = α + β·xi`——明确每行有自己的均值；σ 无下标=同方差假设。
- **坑**：`μi =` 用等号不用波浪号——μ 由参数完全决定，没有自己的分布。

## 4.3 — A Gaussian Model of Height（双参数网格近似 + MAP 二次近似）
- **模型**：`hi ~ Normal(μ,σ)` / `μ ~ Normal(178,20)` / `σ ~ Uniform(0,50)`（§4.3, p92–103）。
- **联合后验**：`Pr(μ,σ|h) ∝ ∏ Normal(hi|μ,σ) × Normal(μ|178,20) × Uniform(σ|0,50)`。
- **网格近似 5 步**：linspace+meshgrid → 广播 log_lik → +log_prior → 数值稳定 → exp+归一化。
- **广播关键**：`heights[:,None,None]` (352,1,1) × `MU[None]` (1,n,n) → (352,n,n)，`sum(axis=0)` → (n,n)。
- **数值稳定**：`log_post -= log_post.max()`，防止 exp(-4000)=0 下溢。
- **归一化 = 除以平均似然**：`post /= post.sum()` 等价于 Bayes 分母 Σ[likelihood×prior]。
- **MAP 结果**（p100）：μ≈154.61 cm，σ≈7.73 cm（352 名成人）。
- **MAP 二次近似**：`minimize(neg_log_post, x0, method='BFGS')` 找峰；Hessian 的逆 = 后验协方差。
- **log_sigma 参数化**：用 `log_sigma` 而非 `sigma` 作优化变量，确保 σ>0（`sigma=exp(log_sigma)`）。
- **坑 1**：`heights[n,n]` 不对，应是 `heights[:,None,None]`——None 插维度，整数是索引。
- **坑 2**：`np.where(SIGMA,...)` 不对，需布尔条件 `(SIGMA>0)&(SIGMA<=50)`。

## 4.3b — MAP 完整版：Hessian 协方差 + 多维后验采样（§4.3.5–4.3.6, p99–103）
- **MAP 为什么不用积分**：Bayes 分母 P(data) 对所有 θ 是常数，argmax 时直接扔；只 maximize 分子。
- **Hessian 直觉**：2D 参数空间里各方向二阶导的压缩；对角线=轴向曲率，非对角线=混合偏导（参数相关性）。
- **混合偏导 ∂²f/∂μ∂σ**："μ 方向斜率随 σ 变化有多快"；=0 ↔ 等高线轴对齐 ↔ 后验不相关。
- **v^T H v 是二阶方向导数**，不是几何曲率；在 MAP 处（一阶=0）决定 f 沿方向 v 的下降速率。
- **协方差 = H 的逆**：H 是 neg_log_post 的 Hessian（最小值处正定），cov = inv(H)。
- **四点差分 Hessian**：`H[i,j] = (f(++)-f(+-)-f(-+)+f(--)) / (4·eps²)`，eps=1e-4。
- **delta method**：SE(σ) = SE(log_σ) × σ（因为 ∂σ/∂log_σ = σ）。
- **采样流程**：`samp_log = rng.multivariate_normal(res.x, cov_log, n)` → `exp` 还原 σ → `column_stack`。
- **结果（p100）**：mu=154.61±0.41 cm，sigma=7.73±0.29 cm（352 名成人，均匀先验下 MAP≈MLE）。
- **坑**：测试文件放 `materials/notebooks/tests/`，judge.py 拼接后直接调函数，不要用 importlib。
- **BFGS（quasi-Newton）**：每步用 (s=位移, y=梯度变化) 更新 Hessian 近似 B；方向=-B×∇f；停止条件=||∇f||<gtol(默认1e-5)；内层 Wolfe 线搜索定步长。
- **为什么不用网格**：n 参数需 k^n 格点，维度诅咒；10 参数=10^20 格点不可行；BFGS 爬山步数线性增长。
- **三引擎定位**：Grid(1-3参数,教学) → quap/MAP(几十参数,后验≈高斯) → MCMC(任意维度任意形状,第8章)。

## 4.4 — Adding a Predictor（线性回归，§4.4.1–4.4.3, p105–122）
- **模型规范**：`h_i ~ N(μ_i, σ)` / `μ_i = α + β·w_i`（= 不是 ~）/ `α~N(178,100)` / `β~N(0,10)` / `σ~U(0,50)`。
- **关键**：μ_i 是确定值，先验只加 α、β、σ，**μ_i 没有先验**（= 号表达确定关系）。
- **neg_log_post**：`-(ll + lp_a + lp_b)`，σ 先验为常数忽略；ll = `sum(norm.logpdf(heights, mu_i, sigma))`。
- **MAP 结果**（p111）：α≈113.90，β≈0.90，σ≈5.07（352 名成人）。
- **中心化**：`w_c = w - w.mean()`；中心化后 α ≈ heights.mean()≈154.6 cm（有意义）；β 不变。
- **后验 = 直线分布**：从后验采 20 对 (α,β) 各画一条线，边缘发散、中心集中（图左）。
- **两类不确定性**（p115–122）：均值HPDI（只含参数 α,β 的后验）vs 预测PI（还加 σ 的随机性）；PI 远宽于 HPDI。
- **采样计算均值HPDI**：`mu_mat = a_samp[:,None] + b_samp[:,None]*w_seq[None,:]`，`percentile(mu_mat,[5.5,94.5],axis=0)`。
- **采样计算预测PI**：`h_sim = rng.normal(mu_mat, sigma_samp[:,None])`，`percentile(h_sim,[5.5,94.5],axis=0)`。
- **坑**：`μ_i` 用等号不用波浪号；先验别误写到 μ_i 上；预测PI务必包含 σ 才完整。

## 4.5 — Polynomial Regression（多项式回归，§4.5, p123–127）
- **模型**：`ws=(w-mean)/std`；`mu_i=a+b1*ws+b2*ws²`；参数 (a,b1,b2,log_sigma)。
- **标准化两个理由**：① 避免 w² 数值爆炸（catastrophic cancellation + 条件数）；② β 可解释为"每增 1SD 对应的变化"，多变量时可横向比较。
- **条件数**：原始 w² 时 kappa~10⁷（细长山谷，zigzag）；标准化后 kappa~1（圆形，快速收敛）。
- **MAP 结果（全544人，p125）**：a≈146.66，b1≈21.40，b2≈-8.42（负=开口向下），sigma≈5.75。
- **b2<0 的直觉**：轻时每 kg 长高多（线性段陡）；重时增速放缓（抛物线变平）。
- **警告（p123）**：多项式是 geocentric 描述工具，拟合好≠解释正确；勿沉迷。
- **坑**：标准化用传入数据自身的 mean/std，不要硬编码；x0 初始值要在合理范围内。
