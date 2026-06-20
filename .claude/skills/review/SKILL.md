---
name: review
description: 章末/阶段复习。当用户说"复习/review/章末测验"，或学完一章若干节后使用。清理误区状态、出混合练习、写复习报告。
---

# /review — 章末/阶段复习

读 `CLAUDE.md` 守规则。语言：中文为主 + 英文术语。

## 1. 收集
读 `progress/state.md`（当前章）、本章对应的 `progress/lessons/*.md`、`progress/error-log.md`、`progress/concept-log.md`。

## 2. 误区状态更新
按 status 规则流转：
- `active` 连续 2 周无复发 → `reviewing`
- `reviewing` 再 2 周无复发 → `mastered`
- 复习中任何复发 → 回 `active`，count+1
把更新写回 `progress/error-log.md`。

## 3. 混合练习（互动）
先口头回顾本章：学了哪些节、核心概念、里程碑是否达成、top 复发误区。
然后出一组练习，学生逐题作答：
- **3–4 道 fix-this**：给一段有概念误区或 code-bug 的推理/代码，让学生找错并改对（取材本章 active 误区，换新例子）
- **2 道结果解读**：给一个 posterior / 区间 / 模型对比输出，让学生解读（防"区间=频率派置信区间"等误读）
- **1 道综合建模**：一个本章主题的小问题，要求从模型设定到 Python 实现到解读走完整流程，复用 ≥2 个本章概念

按 `/lesson` 阶段 4 的规则反馈（只纠 3–4 个、肯定亮点）。

## 4. 报告
写 `progress/reviews/chNN.md`：
```
# 第 N 章复习（YYYY-MM-DD）
## 小结：完成的节、核心概念、里程碑达成情况
## 误区统计：按 category；复发 top；新晋 mastered
## 亮点：具体进步
## 下一步：进入第 N+1 章前要补的弱点 → 提示 /chapter N+1
```
更新 `progress/state.md`（记录"上次复习"）。若 git 仓库则 commit。

## headless 模式（无学生在场，如定时任务）
同样做误区状态更新，并生成**自测卷**：上面的练习 + 折叠的答案（`<details>` 块），写进 `progress/reviews/chNN.md`，在 state.md 标注已生成。
