---
name: chapter
description: 渐进式生成某一章的详细教案与练习。当用户说"生成第 N 章/准备第 N 章/chapter N"，或上课时发现当前章的 curriculum/chapters/chNN.md 不存在时使用。读教材原文，产出按小节组织的教案+设计练习。
---

# /chapter N — 渐进式生成第 N 章教案

目标：把第 N 章变成一份**按小节组织、可直接上课**的教案 `curriculum/chapters/chNN.md`（NN 两位补零）。
这是"渐进式"的核心：**只在学生临到该章时生成**，每次只读这一章进上下文。
读 `CLAUDE.md` 守规则——尤其"课程设计纪律"：**先读懂教材再设计，严禁凭记忆编写，讲授出题都标注页码**。语言：中文为主 + 英文术语。

## 流程

### 1. 定位 + 通读原文（强制，不可跳过）
从 `curriculum/syllabus.md`（或 `CLAUDE.md` 的页码表）取第 N 章页区间。
`python3 tools/pdftext.py <起页> <止页>` 抽取原文。**章长时分小节区间多次抽取并逐段真正读完**（输出过大被截断时，写到临时文件再用 Read 完整读，不能只看预览就动笔）。
**必须读懂并能追溯到页码**：每节的核心概念、用到的数据集、worked example 的设定与数值、**章末 Practice 题的真实编号与题面**（Easy/Medium/Hard，回原文核对，不得凭记忆）。
只有在确认已读懂该章后，才进入第 3 步写教案。

### 2. 翻译为 Python
书里是 R/rethinking，**把每个模型翻成等价 Python**：
- 网格近似 → NumPy（构造 grid、prior、likelihood、归一化）
- 二次近似 quap → `scipy.optimize.minimize` 求 MAP + Hessian 取协方差，或 PyMC `find_MAP` + `Laplace`
- MCMC → PyMC（`pm.sample`）+ ArviZ 诊断
- 数据集：书中常用 Howell1、WaffleDivorce、milk、tulips 等。能构造就构造，需外部数据则在教案里注明来源/如何放到 `materials/data/`。

### 3. 写 `curriculum/chapters/chNN.md`
结构：开头一句"本章定位 + 里程碑"，然后**每个小节一段**，每段含：

**结构与质量标准必须遵循 `curriculum/QUALITY.md`**（教案 rubric A1–A6、练习 rubric B1–B5、练习的标准格式 C）。每个小节一段，每段含：

```
## N.M 小节标题（PDF p..–..）

> ⚠️ 以下两块必填，不可省略：

- **问题引入（承上启下）**：
  先写"上一节/章解决了什么 → 本节还回答不了什么问题（旧工具的局限）→ 本节新工具作为答案"。
  **不得直接从机制名开场**；要给足背景让学生知道"为什么现在要学这个"。

- **作者核心观点（精华，带页码）**：
  McElreath 本节想传达的统计哲学/核心主张，**忠实原文、每条带 §节号+页码**。
  不能只留算法步骤；书中 Rethinking/Overthinking 框的核心洞见必须在此体现。

- **学习目标**：1 句话
- **核心概念**：中文讲解 + 英文术语对照（posterior / likelihood…），关键论点标注页码（如 p46）
- **关键直觉**：这一节"到底在说什么、为什么这么做"，用书里的类比（注明出处页）
- **Worked example**：对应教材中的例子（注明页码）；自包含可运行的 Python（自带 import）；数值声明让代码 print 或 assert 自证
- **设计练习**（2–3 道）：贴近真实问题；**计算题必须按 QUALITY.md 格式 C 配折叠 `<details>` 解法块，并用 `assert` 钉死预期答案**；纯讨论题在题面写"预期回答要点"；注明延伸/呼应教材哪节
- **关联书题**：章末 Practice 里精选 1–3 道，**用真实编号与页码**（如 2M1, p58），标 E/M/H
- **常见误区**：1–3 条，供 /lesson 热身 drill（尽量对应教材 Rethinking/Overthinking 框中的提醒）
```

引用纪律：每个概念/例子/练习尽量带 **§小节号 + PDF 页码**。书题编号必须回原文核对。
练习设计原则：理论结合实践；可延伸但忠实反映该节教学目标；复用前面学过的概念；难度从模仿到迁移。

### 4. 质量闸门（三层，必须全过才算完成）
写完 chNN.md 后，**依次过三关**（标准见 `curriculum/QUALITY.md` §D）：
- **L1+L2**：跑 `python3 tools/check_chapter.py curriculum/chapters/chNN.md --pages <起页> <止页>`。必须 `PASS ✅`。失败就按报告修（结构缺字段、页码越界、代码报错、assert 不成立——assert 不过往往意味着**预期答案写错了**，回去核对）。
- **L3 独立审阅（每章强制）**：起一个 subagent（general-purpose），让它**重读该章原文**（用 `tools/pdftext.py`）后按 QUALITY.md 的 A1/A6/B3/B5 审忠实性、教学性、目标对齐、表述，返回"原文页码 vs 教案写法"的问题清单。把清单里的问题逐条修掉或写明豁免理由，必要时重跑 L1+L2。
- 三关全过后，向学生**汇报检查结论**（L1/L2 PASS、L3 处理了哪些问题）。

### 5. 收尾
更新 `progress/state.md` 的"已生成章教案"。
告诉学生：第 N 章已就绪、已过质检，本章规划 X 节课，第一节是 N.1，用 `/lesson` 开始。
若本章起需要 PyMC 而未装，提醒 `pip install pymc arviz`。
（不写 progress/lessons，不算一节课。）
