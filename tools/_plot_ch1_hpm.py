"""Chapter 1 Figure 1.2: H -> P -> M many-to-many diagram (English labels)"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(13, 7))
ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis('off')
fig.patch.set_facecolor('#f8f9fa')

# ── Column headers ─────────────────────────────────────────────
for x, label, sub in [
    (1.8,  'Hypotheses',       '(H)\nvague verbal conjectures'),
    (6.5,  'Process Models',   '(P)\nexplicit mechanistic specs'),
    (11.2, 'Statistical Models','(M)\nmathematical predictions'),
]:
    ax.text(x, 6.6, label, ha='center', va='center',
            fontsize=13, fontweight='bold', color='#1a1a2e')
    ax.text(x, 6.1, sub, ha='center', va='center',
            fontsize=9, color='#555', style='italic')

ax.axhline(5.75, color='#ccc', lw=0.8, xmin=0.02, xmax=0.98)

# ── Box helper ────────────────────────────────────────────────
def box(ax, x, y, w, h, text, color, textcolor='white', fontsize=10):
    rect = mpatches.FancyBboxPatch((x-w/2, y-h/2), w, h,
        boxstyle="round,pad=0.1", fc=color, ec='white', lw=1.5, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y, text, ha='center', va='center',
            fontsize=fontsize, color=textcolor, fontweight='bold', zorder=4)

# ── Hypothesis boxes H ────────────────────────────────────────
box(ax, 1.8, 4.3, 2.8, 1.2,
    'H0\n"Evolution is neutral"\n(neutral model)', '#2196F3')
box(ax, 1.8, 2.0, 2.8, 1.2,
    'H1\n"Selection matters"\n(selection model)', '#9C27B0')

# ── Process model boxes P ─────────────────────────────────────
box(ax, 6.5, 5.2, 2.6, 0.9, 'P0A\nNeutral, equilibrium\n(constant pop size)', '#1565C0', fontsize=8.5)
box(ax, 6.5, 4.0, 2.6, 0.9, 'P0B\nNeutral, non-equilibrium\n(fluctuating pop size)', '#1976D2', fontsize=8.5)
box(ax, 6.5, 2.8, 2.6, 0.9, 'P1A\nConstant selection\n(one direction)', '#6A1B9A', fontsize=8.5)
box(ax, 6.5, 1.6, 2.6, 0.9, 'P1B\nFluctuating selection\n(varying direction)', '#7B1FA2', fontsize=8.5)

# ── Statistical model boxes M ─────────────────────────────────
box(ax, 11.2, 4.6, 2.3, 0.85, 'MI', '#546E7A', fontsize=10)
box(ax, 11.2, 3.3, 2.3, 0.85, 'MII\n(power law)', '#37474F', fontsize=9)
box(ax, 11.2, 2.0, 2.3, 0.85, 'MIII', '#546E7A', fontsize=10)

# ── Arrow helper ──────────────────────────────────────────────
def arr(ax, x1, y1, x2, y2, rad=0.0, color='#888', lw=1.4):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=lw,
                                connectionstyle=f'arc3,rad={rad}'))

# H0 -> P0A, P0B
arr(ax, 3.15, 4.5, 5.22, 5.2, rad=-0.1, color='#2196F3')
arr(ax, 3.15, 4.1, 5.22, 4.0, rad= 0.0, color='#2196F3')
# H1 -> P1A, P1B
arr(ax, 3.15, 2.2, 5.22, 2.8, rad= 0.0, color='#9C27B0')
arr(ax, 3.15, 1.8, 5.22, 1.6, rad= 0.1, color='#9C27B0')

# P0A -> MII  (neutral equilibrium produces power law)
arr(ax, 7.78, 5.2, 10.08, 3.5, rad=-0.2, color='#1565C0')
# P0B -> MI
arr(ax, 7.78, 4.0, 10.08, 4.6, rad= 0.1, color='#1976D2')
# P1A -> MIII
arr(ax, 7.78, 2.8, 10.08, 2.2, rad= 0.0, color='#6A1B9A')
# P1B -> MII  (KEY: selection model ALSO produces power law!)
arr(ax, 7.78, 1.6, 10.08, 3.1, rad= 0.2, color='#FF5722', lw=2.2)

# ── Key annotation ─────────────────────────────────────────────
ax.annotate('WARNING: P0A and P1B\nboth produce MII (power law)\n-> statistically indistinguishable!',
            xy=(10.5, 3.2), xytext=(8.5, 0.9),
            fontsize=8.5, color='#FF5722',
            arrowprops=dict(arrowstyle='->', color='#FF5722', lw=1.2))

# ── Bottom summary box ─────────────────────────────────────────
ax.text(6.5, 0.35,
        'H -> multiple P:  hypotheses are vague; explicit mechanistic choices yield different P\n'
        'P -> same M:      max-entropy distributions; different mechanisms converge to same form',
        ha='center', va='center', fontsize=9.5, color='#333',
        bbox=dict(boxstyle='round,pad=0.4', fc='#FFF9C4', ec='#F9A825', lw=1))

ax.set_title('Figure 1.2  Hypotheses (H) -> Process Models (P) -> Statistical Models (M)\n'
             'Reproduced from McElreath, Statistical Rethinking, §1.2.1, p18-20',
             fontsize=11, pad=12, color='#1a1a2e')

import os; os.makedirs('materials/figures', exist_ok=True)
plt.tight_layout()
plt.savefig('materials/figures/ch1_hpm_diagram.png', dpi=140,
            bbox_inches='tight', facecolor=fig.get_facecolor())
print("saved: materials/figures/ch1_hpm_diagram.png")
