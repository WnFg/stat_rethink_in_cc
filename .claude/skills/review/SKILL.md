---
name: review
description: 章末/阶段复习。当用户说"复习/review/章末测验"，或学完一章若干节后使用。清理误区状态、出混合练习、写复习报告。
---

# /review — 章末/阶段复习

读 `CLAUDE.md` 守规则。语言：中文为主 + 英文术语。

## 1. 收集
读 `progress/state.md`（当前章）、本章对应的 `progress/lessons/*.md`、`progress/error-log.md`、`progress/concept-log.md`、`progress/learner-profile.md`（按风格参数互动）、`materials/figures/`（本章可视化）。

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
更新 `progress/state.md`（记录"上次复习"）。

## 5. 更新学情画像（活）
把本章/本次复习的新观察整合进 `progress/learner-profile.md`：画像 Snapshot、教学风格参数（若学生暴露新偏好就改）、待强化、更新日志（写当天日期 + 增量）。误区状态变化也在这里反映"待强化"。

## 6. 生成复习卡（每次 /review 固定产出）
为本章撰写一份**个性化复习卡 HTML** 并打开。流程：
1. **复制统一模板**：`cp tools/card_template.html progress/reviews/chNN_card_body.html`，**逐段填充**（8 段顺序固定，详见 `curriculum/QUALITY.md`「E. 复习卡标准」）。重点：
   - **第 ② 段「数学思想与作者核心观点」必须充实**——用 `.principle` 块写出 McElreath 本章想传达的**核心观点/统计哲学**（小世界vs大世界、贝叶斯=数路径、模型非真理、概率是认知、先验是模型一部分、no free lunch…），**每条带 §节号+页码、忠实原文**（需要时回 `tools/pdftext.py` 核对，不凭记忆编）；再点明本章数学的**动机与直觉**。
   - **第 ⑥ 段「学习画像」** 取自 `learner-profile.md` + 本章真实表现（高光/易错红绿对照/待强化/已攻克）。
   - 其余段：主轴图、核心概念与公式、内嵌 `materials/figures/` 可视化、对比表、速查卡、下一步。
2. **渲染并打开**：
   ```
   python3 tools/render_card.py --title "第N章复习要点 · <章名>" --subtitle "<一句话>" \
     --meta "Ch.N (p..-..) · <日期>" --body progress/reviews/chNN_card_body.html \
     --out progress/reviews/chNN_review_notes.html --open
   ```
3. 告诉学生卡片路径，并提示"自包含、可随时浏览器打开/分享"。
卡片标准见 `curriculum/QUALITY.md`「复习卡标准」。

## 7. 收尾
若 git 仓库则 commit（报告 + 画像 + 复习卡）。

## headless 模式（无学生在场，如定时任务）
同样做误区状态更新，并生成**自测卷**：上面的练习 + 折叠的答案（`<details>` 块），写进 `progress/reviews/chNN.md`，在 state.md 标注已生成。
