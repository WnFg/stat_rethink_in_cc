"""Chapter 1 Figure 1.2 重现：H → P → M 多对多关系图"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis('off')
fig.patch.set_facecolor('#f8f9fa')

# ── 列标题 ─────────────────────────────────────────────────────
for x, label, sub in [
    (1.8, 'Hypotheses', '(H)\n模糊的语言声明'),
    (6.5, 'Process Models', '(P)\n精确的机制规范'),
    (11.2, 'Statistical Models', '(M)\n数学分布特征'),
]:
    ax.text(x, 6.6, label, ha='center', va='center',
            fontsize=13, fontweight='bold', color='#1a1a2e')
    ax.text(x, 6.1, sub, ha='center', va='center',
            fontsize=9, color='#555', style='italic')

ax.axhline(5.75, color='#ccc', lw=0.8, xmin=0.02, xmax=0.98)

# ── 假设框 H ──────────────────────────────────────────────────
def box(ax, x, y, w, h, text, color, textcolor='white', fontsize=10):
    rect = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.1", fc=color, ec='white', lw=1.5, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, color=textcolor, fontweight='bold', zorder=4)

box(ax, 1.8, 4.3, 2.8, 1.2, 'H0\n"进化是中性的"\n(neutral)', '#2196F3')
box(ax, 1.8, 2.0, 2.8, 1.2, 'H1\n"自然选择起作用"\n(selection)', '#9C27B0')

# ── 过程模型框 P ───────────────────────────────────────────────
box(ax, 6.5, 5.2, 2.6, 0.9, 'P0A\n中性 · 稳态种群', '#1565C0', fontsize=9)
box(ax, 6.5, 4.0, 2.6, 0.9, 'P0B\n中性 · 波动种群', '#1976D2', fontsize=9)
box(ax, 6.5, 2.8, 2.6, 0.9, 'P1A\n恒定选择方向', '#6A1B9A', fontsize=9)
box(ax, 6.5, 1.6, 2.6, 0.9, 'P1B\n波动选择方向', '#7B1FA2', fontsize=9)

# ── 统计模型框 M ───────────────────────────────────────────────
box(ax, 11.2, 4.6, 2.3, 0.85, 'MI', '#546E7A', fontsize=10)
box(ax, 11.2, 3.3, 2.3, 0.85, 'MII\n（幂律分布）', '#37474F', fontsize=9)
box(ax, 11.2, 2.0, 2.3, 0.85, 'MIII', '#546E7A', fontsize=10)

# ── 箭头：H → P ────────────────────────────────────────────────
arrow_kw = dict(arrowstyle='->', color='#888', lw=1.4,
                connectionstyle='arc3,rad=0.0')

def arr(ax, x1, y1, x2, y2, rad=0.0, color='#888', lw=1.4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'))

# H0 → P0A, P0B
arr(ax, 3.15, 4.5, 5.22, 5.2,  rad=-0.1, color='#2196F3')
arr(ax, 3.15, 4.1, 5.22, 4.0,  rad= 0.0, color='#2196F3')
# H1 → P1A, P1B
arr(ax, 3.15, 2.2, 5.22, 2.8,  rad= 0.0, color='#9C27B0')
arr(ax, 3.15, 1.8, 5.22, 1.6,  rad= 0.1, color='#9C27B0')

# ── 箭头：P → M ────────────────────────────────────────────────
# P0A → MII  (中性稳态产生幂律)
arr(ax, 7.78, 5.2, 10.08, 3.5, rad=-0.2, color='#1565C0')
# P0B → MI
arr(ax, 7.78, 4.0, 10.08, 4.6, rad= 0.1, color='#1976D2')
# P1A → MIII
arr(ax, 7.78, 2.8, 10.08, 2.2, rad= 0.0, color='#6A1B9A')
# P1B → MII  (关键！选择模型也产生幂律)
arr(ax, 7.78, 1.6, 10.08, 3.1, rad= 0.2, color='#FF5722', lw=2.0)

# ── 关键注释 ───────────────────────────────────────────────────
ax.annotate('⚠️ P0A 和 P1B\n都产生 MII（幂律）\n→ 统计上无法区分',
            xy=(10.5, 3.2), xytext=(8.8, 1.0),
            fontsize=8.5, color='#FF5722',
            arrowprops=dict(arrowstyle='->', color='#FF5722', lw=1.2))

# ── 底部总结 ───────────────────────────────────────────────────
ax.text(6.5, 0.4,
        'H 多对多 P  ←  假设是模糊语言声明，需要填充机制细节才能精确化\n'
        'P 多对一 M  ←  最大熵：不同机制在数学上收敛到相同分布形式',
        ha='center', va='center', fontsize=9.5, color='#333',
        bbox=dict(boxstyle='round,pad=0.4', fc='#FFF9C4', ec='#F9A825', lw=1))

ax.set_title('Figure 1.2 重现：假设 H → 过程模型 P → 统计模型 M\n'
             '（§1.2.1, p18-20，McElreath Statistical Rethinking）',
             fontsize=11, pad=12, color='#1a1a2e')

import os; os.makedirs('materials/figures', exist_ok=True)
plt.tight_layout()
plt.savefig('materials/figures/ch1_hpm_diagram.png', dpi=140,
            bbox_inches='tight', facecolor=fig.get_facecolor())
print("saved: materials/figures/ch1_hpm_diagram.png")
