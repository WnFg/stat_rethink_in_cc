---
name: progress
description: 只读进度面板。当用户说"进度/我学到哪了/progress/怎么样了"时使用。只读不改任何文件，展示当前进度、错误库统计、概念库、节奏检查。
---

# /progress — 进度面板（只读）

**只读**：读文件、展示，绝不修改任何文件。
读：`progress/state.md`、`progress/error-log.md`、`progress/concept-log.md`、`curriculum/syllabus.md`、`progress/lessons/`（计数）。

输出格式（中文）：
```
📍 进度：第 X 章 / 共 15 章 — <章标题>，当前小节 X.Y | 已上 N 节课
🎯 当前焦点：<state.md 的下一节焦点>
📦 已生成章教案：<列出 chNN>

❗ 错误库：A active / B reviewing / C mastered
   按类别：misconception X · interpretation X · code-bug X · math-derivation X
   top 复发（count≥2）：最多列 5 条带计数

📚 概念库：已掌握 N 个（最近 3 个举例）

⏱ 节奏检查：已上 N 节 vs 计划，里程碑达成情况；落后则给一句建议
```
结尾给一句具体、鼓励的观察（如"interpretation 类错误从 4 降到 1，对 posterior 的解读明显稳了"）。
