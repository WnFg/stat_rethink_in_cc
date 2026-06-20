# 内容质量标准 QUALITY.md

本文件定义 `/chapter` 教案与 `/lesson` 练习的**质量标准（rubric）**与**检验流程**。
它既是生成内容时的规格，也是 `tools/check_chapter.py` 与 L3 审阅的依据。
与 `CLAUDE.md`「课程设计纪律」配套：纪律管"忠实来源"，本文件管"正确、可解、对齐、可验证"。

---

## A. 教案 rubric（每个 `## N.M` 小节都要满足）

| # | 标准 | 含义 | 谁来查 |
|---|------|------|--------|
| A1 | **忠实** | 反映教材该节内容与教学目标，不脱离原文另起炉灶 | L3 |
| A2 | **可追溯** | 核心概念/例子/练习带 §节号 + PDF 页码；书题用真实编号 | L1 + L3 |
| A3 | **正确** | 公式、数值、结论正确；**代码能跑且输出与文中声明一致** | L2 |
| A4 | **完整** | 含全部必填字段：学习目标 / 核心概念 / 关键直觉 / Worked example / 设计练习 / 常见误区 | L1 |
| A5 | **可跑示例** | 非纯讨论的小节，Worked example 含**自包含、可运行**的 Python（自带 import） | L1 + L2 |
| A6 | **教学性** | 直觉优先；建立在已学概念上；贴合学情画像（轻数学、Python、业务化例子） | L3 |

> 纯概念/讨论小节（syllabus 标"无/讨论"）豁免 A5 的代码要求，但仍需 A1/A2/A4。

## B. 练习 rubric（每道"设计练习"都要满足）

| # | 标准 | 含义 | 谁来查 |
|---|------|------|--------|
| B1 | **有解且答案正确** | 题目有明确解；给出的预期结论真实正确 | L2（assert） |
| B2 | **可机器验证** | 计算题必须配**隐藏可跑解法**，预期答案由代码产出、用 `assert` 钉死 | L1 + L2 |
| B3 | **对齐目标** | 考的是本节学习目标；尽量复用前面学过的概念 | L3 |
| B4 | **有出处** | 注明延伸/呼应教材哪一节或哪道书题 | L1 + L3 |
| B5 | **表述清晰** | 问法无歧义；难度从模仿 worked example 到稍作迁移 | L3 |

---

## C. 练习的标准格式（强约束）

每道**计算类**设计练习 = 一段题面 + 一个折叠的可跑解法。解法块**必须用 `assert` 钉住预期答案**，
这样 `check_chapter.py` 跑一遍就同时验证了"代码能跑"和"答案正确"。

````markdown
- **练习 N.M-k**：<题面>……（呼应 §N.M / 书题 2Mx, pXX）
  <details><summary>解法与预期答案</summary>

  ```python
  # solution: ch2 ex 2.1-1
  import numpy as np
  blue = np.array([0, 1, 2, 3]); white = 3 - blue
  ways = blue * blue * white
  std = ways / ways.sum()
  assert list(ways) == [0, 2, 4, 0]                 # 钉死路径数
  assert np.isclose(std[2], 2/3)                    # 钉死最可信猜想的概率
  print("ways =", ways, " std =", std)
  ```
  </details>
````

- 纯概念/讨论题（无需计算）可不配代码，但要在题面写清"预期回答要点"，由 L3 审"答得对不对"。
- Worked example 的代码若有数值声明（如"≈0.636"），也应让代码 `print` 出来或用 `assert` 自证。

### C2. OJ（在线判题）形式 —— 计算练习的**首选**格式

让学生真正动手"实现"而非"对答案"：老师定义**函数签名 + 输入/输出规范**，学生只写实现，老师用**隐藏测试集**判定。

- **题面**给出函数签名与规范（可放学生 stub 文件 `materials/notebooks/ex_<id>.py`）。
- **隐藏测试集** `materials/notebooks/tests/_<id>.py`：若干 assert，引用该函数名，覆盖正确性/边界/性质（如归一化、顺序无关、收敛）。
- **参考解 + 自测**：chNN.md 内折叠块放参考实现 + 同一批断言（供 `check_chapter.py` L2 自证答案正确）。
- **判题**：`python3 tools/judge.py <学生实现.py> <隐藏测试.py>`，全过 PASS / 否则 FAIL 并指出失败断言。

格式（chNN.md 内）：
````markdown
- **练习 N.M-k（OJ）**：实现 `def f(...) -> ...`（输入/输出规范……）。判题：`tools/judge.py`。
  <details><summary>参考解与隐藏测试</summary>

  ```python
  # solution+tests: ch2 ex 2.2A
  import numpy as np
  def f(...):            # 参考实现
      ...
  # --- 同一批断言（与 tests/_2.2A.py 一致）---
  assert ...
  ```
  </details>
````
隐藏测试要先用参考解跑通（`judge.py 参考解 隐藏测试` = PASS）才能交给学生。

---

## D. 三层检验流程

- **L1 结构 / 引用 lint**（`check_chapter.py`）：每节字段齐全（A4）；非讨论节有代码块（A5）；引用页码落在本章页区间内（A2）；每道练习有折叠解法或被标记为讨论题（B2/B4）。
- **L2 代码执行闸门**（`check_chapter.py`）：抽出教案**全部** Python 代码块（含 `<details>` 内解法），逐块在独立子进程运行；任何报错或 `AssertionError` → **fail**（覆盖 A3/A5/B1/B2）。
- **L3 独立审阅**（subagent，每章强制）：另起一个 agent 重读该章原文，按 A1/A6/B3/B5 审忠实性、教学性、目标对齐、表述；返回问题清单，修完才算过。

**通过线**：L1、L2 必须全绿；L3 的问题全部已处理或有明确豁免理由。`/chapter` 与 `/lesson` 未过检不得标记完成，并须把检查结论汇报给学生。
