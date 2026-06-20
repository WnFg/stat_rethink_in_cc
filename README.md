# 统计反思 · 贝叶斯课程（Statistical Rethinking in Claude Code）

基于 McElreath《Statistical Rethinking》(1st ed) 的渐进式、实践驱动的贝叶斯统计课程。
理论结合实践：每节课讲透一个小节的概念与直觉，并用 **Python（NumPy / SciPy / PyMC）** 设计的练习题动手解决真实问题。

## 怎么上课

在本目录用 Claude Code 触发以下 skill（中文/英文均可，括号是触发词）：

| 命令 | 作用 |
|------|------|
| `/setup` | 课程初始化：摸底 + 生成总大纲 `curriculum/syllabus.md` |
| `/chapter N` | 渐进式生成第 N 章的详细教案与练习 `curriculum/chapters/chNN.md` |
| `/lesson` | 上一节 20–30 分钟的小节课（讲解 → 实践 → 反馈 → 小结） |
| `/review` | 章末/阶段复习：误区清理 + 混合练习 |
| `/progress` | 只读进度面板 |

第一次：先 `/setup`，再 `/chapter 2`，然后 `/lesson`。

## 环境

- Python 3.12，已装 numpy / scipy / matplotlib / pandas
- MCMC 章节（第 8 章起）需 `pip install pymc arviz`（前几章网格近似纯 numpy 即可）
- 读教材用 `python3 tools/pdftext.py <起页> <止页>`（0 基页码），`--toc` 看目录

## 目录

- `curriculum/` 课程设计（总大纲 + 渐进式章教案）
- `progress/` 学生记忆（进度指针、概念库、错误库、速查、逐课记录）
- `materials/` 数据集 / 学生代码 / 图
- `homework/` 学生提交
- `tools/pdftext.py` 教材文本抽取工具
