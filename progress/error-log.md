# 误区 / 错误库 Error Log

category：`misconception`(概念误区) / `math-derivation`(推导错误) / `code-bug`(代码错误) / `interpretation`(结果解读错误)
status：`active` → `reviewing`（2 周无复发）→ `mastered`（再 2 周无复发）；复发回 `active` 且 count+1。

| date | 学生的理解/写法 | 正确版本 | category | count | status |
|------|----------------|---------|----------|-------|--------|
| 2026-06-20 | 平均似然分母 = Σ(似然 × 猜想p) | Σ(似然 × 先验权重 prior(p))，乘的是先验不是参数值 p | misconception | 1 | active |
| 2026-06-20 | 二阶导写成 (neg(m+eps) - neg(m) / eps) | 先减后除要加括号：(neg(m+eps)-neg(m))/eps（/ 优先级高于 -） | code-bug | 1 | active |
| 2026-06-20 | 二次近似：高斯≈二次多项式 / 泰勒展开二次多项式 | 被泰勒近似的是【对数后验】→抛物线；高斯↔抛物线是精确(对数关系) | misconception | 1 | active |
