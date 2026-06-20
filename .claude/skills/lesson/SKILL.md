---
name: lesson
description: 上一节 20–30 分钟的小节课。当用户说"开始上课/上课/下一节/lesson"时使用。按 准备→热身→讲解→实践→反馈→小结+持久化 六段流程，重实践，每节只纠 3–4 个错误。
---

# /lesson — 一节小节课（20–30 分钟）

读 `CLAUDE.md` 守教学规则。语言：中文为主 + 英文术语。**实践是核心**，讲解精简。

## 阶段 0 · 准备（静默，不输出给学生）
读：`progress/state.md`（当前章/节）、`progress/error-log.md`（取 2–3 个 active 误区）、`progress/concept-log.md`（挑 1–2 个旧概念待复用）、当前 `curriculum/chapters/chNN.md` 的本节段落。
检查 `homework/` 是否有新提交。
**若当前章教案 `chNN.md` 不存在** → 不硬上，提示学生先 `/chapter N`，停止。
选定本节目标（来自 chNN.md 的"学习目标"）。

## 阶段 1 · 热身（3–5 分钟）
打招呼，宣布本节目标（一句话）。
若有 homework：检查，肯定一个亮点，纠 1–2 个错。
快问快答 drill 2–3 个 active 误区（用新例子，别照搬原题）。

## 阶段 2 · 讲解（8–10 分钟）
讲本节核心：**先直觉，后数学，再代码**。
- 用书里的类比把"在说什么"讲清楚
- **标注教材出处**：讲到的概念/例子/公式尽量带上 §小节号 + 页码（如「§2.4, p50」），方便学生回查；出题时也注明对应教材哪节
- 给 1 个 worked example，连同可跑的 Python 骨架；必要时真的跑一下展示输出/图（图存 `materials/figures/`）

## 阶段 3 · 实践（10–12 分钟，核心）
优先用 chNN.md 里已过质检的练习；若临场新出题，**必须遵守 `curriculum/QUALITY.md` 练习 rubric B1–B5**：先自己写出可跑解法并实跑（计算题用 `assert` 钉死答案，亲自 Bash 跑通）确认"有解且答案正确"，再给学生——**不得凭记忆报预期答案**。
**计算题首选 OJ 形式**（QUALITY.md C2）：给出函数签名+规范（可写 `materials/notebooks/ex_<id>.py` stub）+ 隐藏测试 `tests/_<id>.py`，学生写实现，老师用 `python3 tools/judge.py <学生实现> <隐藏测试>` 判定。隐藏测试须先用参考解跑通再交学生。
让学生**自己写/跑 Python、解读结果**：
- 鼓励先说思路再写代码；卡住给提示而非直接给答案
- 至少 1 道要求复用前面学过的概念（如回到 posterior ∝ prior × likelihood）
- 代码可让学生写在 `materials/notebooks/`
- 新出的好题，课后回填进 chNN.md（按格式 C 配 `<details>`+assert 解法），并重跑 `check_chapter.py` 保持全绿

## 阶段 4 · 反馈（3–5 分钟）
**只纠 3–4 个高价值错误**（概念误区 > 解读 > 代码 > 笔误）。格式：❌ → ✅ → 为什么。
肯定 1 个具体进步。

## 阶段 5 · 小结（固定 4 项）
```
🧠 核心总结：本节概念/公式/直觉/Python 要点
❗ 关键错误：本节纠的 3–4 个
📝 Homework：1 道小任务（≤15 分钟，针对本节目标）
🎯 下节焦点：来自 syllabus/chNN 的下一小节
```

## 阶段 6 · 持久化
1. 写 `progress/lessons/YYYY-MM-DD-chX-sY.md`（目标、用的例子、4 项小结）。`date +%F` 取日期。
2. 追加 `progress/error-log.md`（新误区；复发的 count+1）。
3. 追加 `progress/concept-log.md`（本节新概念）。
4. 追加 `progress/cheatsheet.md`（`## X.Y — 标题` 段：公式+直觉+代码片段+坑）。
5. 更新 `progress/state.md`（当前节前移、清待办标志）。
6. 若是 git 仓库：`git add . && git commit -m "lesson: 第X章 Y节 ..."`（结尾 `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`）。
