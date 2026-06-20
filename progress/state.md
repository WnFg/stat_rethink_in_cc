# 课程状态 Course State

- **状态 Status**: active
- **当前章 Chapter**: 2 — Small Worlds and Large Worlds
- **当前小节 Section**: 2.4 已完成 —— **第 2 章全部小节学完**（next = /review 章末复习 → /chapter 3）
- **下一节课焦点 Next lesson focus**: 第 2 章 /review（误区清理 + 混合练习），然后 /chapter 3 Sampling the Imaginary
- **已生成章教案 Chapters prepared**: ch02
- **待检查 homework**: 有（① avg_like 均匀 vs step 先验；② bayes_update_seq 验证逐步≡一次性；③ quap_globe(6,9) 95% 区间 vs beta(7,4) 真实区间）
- **上次复习 Last review**: 无
- **学情画像 Learner profile**（2026-06-20 摸底）:
  - **数学**：微积分/线代生疏 → 教学重直觉+图+代码，少手推；必要推导才给，且讲清动机。
  - **编程**：底子可以，但 NumPy/PyMC 等库用得少 → 代码逻辑不用多讲，重点在库 API（np.linspace/trapezoid、scipy.stats、pm.sample 等）给足提示与模板。
  - **统计**：频率派+贝叶斯都接触过，有基础 → 概念可走快；**重点防频率派直觉的误读**（可信区间≠置信区间、p 值、把 MLE 当唯一答案）。
  - **目标**：工作/数据分析提升 → 多用业务化例子（转化率、A/B 测试、计数/分类），少用纯学术题。
  - **直觉起点（亮点）**：抛硬币 2/3 题答"样本太少、靠先验、约 1/2"——已具备"先验 vs 数据权衡 / 收缩"的直觉，且不盲信 MLE。是很好的贝叶斯起点。
  - **隐含先验意识**：会用先验但未显式化——第 2–3 章正好把"显式先验 + 完整后验分布（而非点估计）"补上。
