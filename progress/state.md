# 课程状态 Course State

- **状态 Status**: active
- **当前章 Chapter**: 4 — Linear Models
- **当前小节 Section**: §4.3b PASS ✅ MAP+Hessian+采样完整版；待进入 §4.4 线性回归
- **下一节课焦点 Next lesson focus**: §4.4 线性回归——引入预测变量 x，μ_i = α + β·x_i，后验预测可视化
- **已生成章教案 Chapters prepared**: ch02, ch03, ch04（均过 L1+L2+L3 质检）
- **上次复习 Last review**: 第 3 章 2026-06-21（reviews/ch03.md）
- **待检查 homework**: §4.3b homework — 强先验 N(178,0.1) 下 MAP 和 SE 变化（2026-06-27 布置，写到 homework/hw_4.3B.py）

## 本节延伸追问（待下节按需回顾）
- BFGS：拟牛顿法，每步从 (s,y) 学 Hessian 近似；停止条件 = ||∇f|| < gtol=1e-5
- 维度诅咒：n 参数网格 100^n 格点，10 参数即 10^20；MAP+MCMC 是出路
- 三引擎定位：Grid(教学/1-3参数) → quap/MAP(几十参数,后验近高斯) → MCMC(任意,第8章)
- **上次复习 Last review**: 第 2 章 2026-06-20（reviews/ch02.md）—— 3 条错题复习全对、暂仍 active
- **学情画像 Learner profile**: 见 → `progress/learner-profile.md`（活文档：画像 + 教学风格参数，每节读并更新）
