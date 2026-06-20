# 总大纲 Syllabus · Statistical Rethinking (1st ed)

实践驱动的贝叶斯统计课。粒度按小节，每节 20–30 分钟。动手用 Python（NumPy/SciPy → PyMC）。
页码为 `tools/pdftext.py` 用的 0 基页码。详细教案见 `curriculum/chapters/chNN.md`（由 `/chapter N` 渐进生成）。

---

## 阶段一 · 基础与推断引擎（ch1–3）

### 第 1 章 The Golem of Prague（p14–31）· 纯概念导论
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 1.1–1.4 | 统计模型像 golem；三种工具（贝叶斯/多层/因果） | 14–31 | 建立"模型是会犯错的小机器人"的世界观 | 无（口头/讨论） |
> 里程碑：能说清"小世界 vs 大世界"，以及为什么作者偏好贝叶斯+多层模型。

### 第 2 章 Small Worlds and Large Worlds（p32–61）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 2.1 | The garden of forking data | 33 | 用"数路径"理解概率与贝叶斯更新 | numpy |
| 2.2 | Building a model | 41 | globe tossing：把问题写成 likelihood+prior | numpy |
| 2.3 | Components of the model | 45 | likelihood / parameter / prior / posterior 各是什么 | numpy |
| 2.4 | Making the model go | 50 | 三种引擎：grid / quadratic / MCMC（先 grid） | numpy, scipy |
> 里程碑：能用网格近似手写出 globe tossing 的 posterior 并解读。

### 第 3 章 Sampling the Imaginary（p62–83）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 3.1 | Sampling from a grid-approximate posterior | 65 | 从 posterior 抽样代替积分 | numpy |
| 3.2 | Sampling to summarize | 66 | 区间、点估计、PI vs HPDI | numpy |
| 3.3 | Sampling to simulate prediction | 74 | 后验预测分布、模型检查 | numpy |
> 里程碑：能从 posterior 采样并算出可信区间、做后验预测检查。

---

## 阶段二 · 线性回归家族（ch4–7）

### 第 4 章 Linear Models（p84–131）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 4.1 | Why normal distributions are normal | 85 | 正态分布从何而来 | numpy |
| 4.2 | A language for describing models | 90 | 模型的数学记法 | — |
| 4.3 | A Gaussian model of height | 91 | 身高的高斯模型 + 二次近似 | scipy/pymc |
| 4.4 | Adding a predictor | 105 | 一元线性回归 | pymc |
| 4.5 | Polynomial regression | 123 | 多项式回归与样条 | pymc |
> 里程碑：能为身高数据建一元线性回归并解读后验。

### 第 5 章 Multivariate Linear Models（p132–177）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 5.1 | Spurious association | 134 | 多元回归与伪相关 | pymc |
| 5.2 | Masked relationship | 148 | 被掩盖的关系 | pymc |
| 5.3 | When adding variables hurts | 154 | 多重共线性等坑 | pymc |
| 5.4 | Categorical variables | 165 | 分类变量编码 | pymc |
> 里程碑：能用多元回归区分伪相关与真实关联，并画 counterfactual 图。

### 第 6 章 Overfitting, Regularization & Information Criteria（p178–221）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 6.1 | The problem with parameters | 180 | 过拟合 vs 欠拟合 | pymc |
| 6.2 | Information theory and model performance | 187 | 熵、KL 散度、deviance | numpy |
| 6.3 | Regularization | 199 | 正则化先验 | pymc |
| 6.4–6.5 | Information criteria | 201 | AIC/WAIC/比较模型 | pymc/arviz |
> 里程碑：能用 WAIC 比较模型并解释偏差-方差权衡。

### 第 7 章 Interactions（p222–253）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 7.1 | Building an interaction | 224 | 交互项的含义 | pymc |
| 7.2 | Symmetry of the linear interaction | 236 | 交互的对称性 | pymc |
| 7.3 | Continuous interactions | 238 | 连续变量交互、三联图 | pymc |
> 里程碑：能建含交互项的模型并用 triptych 图解读。

---

## 阶段三 · 计算与 GLM（ch8–11）  ⚠️ 本阶段起需 `pip install pymc arviz`

### 第 8 章 Markov Chain Monte Carlo（p254–279）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 8.1 | Good King Markov and his island kingdom | 255 | Metropolis 直觉 | numpy |
| 8.2 | Markov chain Monte Carlo | 257 | 为什么需要 MCMC | numpy |
| 8.3 | Easy HMC | 260 | 用 PyMC 采样 | pymc |
| 8.4 | Care and feeding of your Markov chain | 268 | 收敛诊断（trace/R̂/n_eff） | pymc/arviz |
> 里程碑：能跑 HMC 并判断链是否收敛。

### 第 9 章 Big Entropy and the GLM（p280–303）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 9.1 | Maximum entropy | 281 | 最大熵选分布 | numpy |
| 9.2 | Generalized linear models | 293 | 连接函数、GLM 框架 | pymc |
| 9.3 | Maximum entropy priors | 301 | 最大熵先验 | — |
> 里程碑：能解释为何用某分布作 likelihood、链接函数的作用。

### 第 10 章 Counting and Classification（p304–343）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 10.1 | Binomial regression | 304 | 逻辑回归 | pymc |
| 10.2 | Poisson regression | 324 | 泊松回归 | pymc |
| 10.3 | Other count regressions | 335 | 其他计数模型 | pymc |
> 里程碑：能建逻辑/泊松回归并在结果尺度上解读系数。

### 第 11 章 Monsters and Mixtures（p344–367）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 11.1 | Ordered categorical outcomes | 344 | 有序分类 | pymc |
| 11.2 | Zero-inflated outcomes | 355 | 零膨胀 | pymc |
| 11.3 | Over-dispersed outcomes | 359 | 过度离散 | pymc |
> 里程碑：能为有序/零膨胀/过散数据选对模型。

---

## 阶段四 · 多层与进阶（ch12–15）

### 第 12 章 Multilevel Models（p368–399）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 12.1 | Multilevel tadpoles | 370 | 变化截距入门 | pymc |
| 12.2 | Varying effects & the trade-off | 377 | 部分汇集、收缩 | pymc |
| 12.3 | More than one type of cluster | 383 | 多组聚类 | pymc |
| 12.4 | Multilevel posterior predictions | 389 | 多层后验预测 | pymc |
> 里程碑：能建变化截距模型并解释收缩（shrinkage）。

### 第 13 章 Adventures in Covariance（p400–435）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 13.1 | Varying slopes by construction | 402 | 变化斜率 | pymc |
| 13.2 | Admission decisions and gender | 411 | 实例分析 | pymc |
| 13.3 | Cross-classified chimpanzees | 416 | 交叉分类变化斜率 | pymc |
| 13.4 | Continuous categories and the Gaussian process | 423 | 高斯过程 | pymc |
> 里程碑：能建变化斜率模型，理解相关先验与高斯过程概念。

### 第 14 章 Missing Data and Other Opportunities（p436–453）
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 14.1 | Measurement error | 437 | 测量误差建模 | pymc |
| 14.2 | Missing data | 444 | 缺失数据的贝叶斯处理 | pymc |
> 里程碑：能把测量误差/缺失当作参数纳入模型。

### 第 15 章 Horoscopes（p454–457）· 收尾反思
| 节 | 标题 | 页 | 目标 | 工具 |
|----|------|----|------|------|
| 15 | Horoscopes | 454 | 科研实践中的统计伦理与反思 | 讨论 |
> 里程碑：能批判性看待统计流程，避免"星座式"过度解读。
