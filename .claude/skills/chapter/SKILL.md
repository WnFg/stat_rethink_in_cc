---
name: chapter
description: 渐进式生成某一章的详细教案与练习。当用户说"生成第 N 章/准备第 N 章/chapter N"，或上课时发现当前章的 curriculum/chapters/chNN.md 不存在时使用。读教材原文，产出按小节组织的教案+设计练习。
---

# /chapter N — 渐进式生成第 N 章教案

目标：把第 N 章变成一份**按小节组织、可直接上课**的教案 `curriculum/chapters/chNN.md`（NN 两位补零）。
这是"渐进式"的核心：**只在学生临到该章时生成**，每次只读这一章进上下文。
读 `CLAUDE.md` 守规则。语言：中文为主 + 英文术语。

## 流程

### 1. 定位 + 读原文
从 `curriculum/syllabus.md`（或 `CLAUDE.md` 的页码表）取第 N 章页区间。
`python3 tools/pdftext.py <起页> <止页>` 抽取原文。章很长就分几次按小节区间抽，避免一次塞太多。
**重点读懂**：每节的核心概念、用到的数据集、worked example、章末 Practice 题（Easy/Medium/Hard）。

### 2. 翻译为 Python
书里是 R/rethinking，**把每个模型翻成等价 Python**：
- 网格近似 → NumPy（构造 grid、prior、likelihood、归一化）
- 二次近似 quap → `scipy.optimize.minimize` 求 MAP + Hessian 取协方差，或 PyMC `find_MAP` + `Laplace`
- MCMC → PyMC（`pm.sample`）+ ArviZ 诊断
- 数据集：书中常用 Howell1、WaffleDivorce、milk、tulips 等。能构造就构造，需外部数据则在教案里注明来源/如何放到 `materials/data/`。

### 3. 写 `curriculum/chapters/chNN.md`
结构：开头一句"本章定位 + 里程碑"，然后**每个小节一段**，每段含：

```
## N.M 小节标题（PDF p..–..）
- **学习目标**：1 句话
- **核心概念**：中文讲解 + 英文术语对照（posterior / likelihood…）
- **关键直觉**：这一节"到底在说什么、为什么这么做"，用书里的类比
- **Worked example**：模型设定 + Python 代码骨架（可跑），预期输出/图
- **设计练习**（2–3 道）：贴近真实问题、可跑 Python、每题附"预期结论"供老师对照
- **关联书题**：章末 Practice 里精选 1–3 道（标 E/M/H）
- **常见误区**：1–3 条，供 /lesson 热身 drill
```

练习设计原则：理论结合实践，让学生在解决问题中理解；优先复用前面学过的概念；难度从模仿 worked example 到稍作迁移。

### 4. 收尾
更新 `progress/state.md` 的"已生成章教案"。
告诉学生：第 N 章已就绪，本章规划 X 节课，第一节是 N.1，用 `/lesson` 开始。
若本章起需要 PyMC 而未装，提醒 `pip install pymc arviz`。
（不写 progress/lessons，不算一节课。）
