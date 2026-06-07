"""Ch 11 — Economies of Scale / Natural Monopoly deep-dive figures (our style).
Recreates the user's reference screenshots 2, 4, 5 in the White-Academia palette.
  fig-natural-monopoly : declining LRATC, one firm (b, $100, Q=279,495) vs two firms (a, $200, 139,747 each)
  fig-zero-mc          : the L-shaped cost curve ($10B fixed up front, $0 marginal)
  fig-digital-pillars  : 3-pillar Venn -> Absolute Market Power
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

NAVY='#0a2e5c'; CYAN='#0891b2'; AMBER='#d97706'; GREEN='#16a34a'
SAGE='#6A8E6B'; GOLD='#f59e0b'; GREY='#9ca3af'; ORANGE='#e07a4f'
INK='#1a1a1a'; RED='#b91c1c'; PINK='#ec9bb0'; PLUM='#7C3A5F'; TERRA='#C47B5A'
OLIVE='#6f8f3f'
plt.rcParams.update({'font.size': 12, 'figure.facecolor': 'white'})
plt.rcParams['text.parse_math'] = False   # render literal $ correctly


# ============ FIG 1 — natural monopoly: declining LRATC ============
def fig_natural_monopoly():
    fig, ax = plt.subplots(figsize=(9.2, 6.0))
    X0, X1 = 90000, 350000
    Q = np.linspace(95000, 348000, 400)
    LRATC = 2.795e7 / Q                       # = $200 at 139,747; $100 at 279,495 (declining cost per subscriber)
    ax.plot(Q, LRATC, color=OLIVE, lw=3.2, label='LRATC (cost per subscriber)', zorder=5)

    a = (139747, 200); b = (279495, 100)
    # demand lines pass THROUGH the points: D1 (half market) → a ; D0 (whole market) → b
    ax.plot([95000, 200000], [307, 56], color=PINK, lw=2.4, label='D₁ (half market)', zorder=4)   # through a
    ax.plot([110000, 345000], [320, 15], color=RED, lw=2.4, label='D₀ (whole market)', zorder=4)   # through b

    for (qx, px, lab) in [(a[0], a[1], 'a'), (b[0], b[1], 'b')]:
        ax.plot([qx], [px], 'o', color='white', mec=INK, mew=1.7, ms=12, zorder=9)
        ax.text(qx+5500, px+12, lab, fontsize=15, style='italic', ha='left', color=INK, zorder=9)
        ax.plot([X0, qx], [px, px], color=PLUM, ls=':', lw=1.2, zorder=2)   # horiz guide to y-axis
        ax.plot([qx, qx], [0, px], color=PLUM, ls=':', lw=1.2, zorder=2)    # vert guide to x-axis

    ax.set_xlim(X0, X1); ax.set_ylim(0, 330)
    ax.set_xticks([139747, 279495]); ax.set_xticklabels(['Q÷2', 'Q'])
    ax.set_yticks([100, 200]); ax.set_yticklabels(['$100/mo', '$200/mo'])
    ax.set_xlabel('Quantity (housing units served)', fontsize=12)
    ax.set_ylabel('Price / cost', fontsize=12)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.14)
    ax.set_title('Natural Monopoly — one firm serves the whole market more cheaply',
                 fontsize=13.5, weight='bold', pad=10)
    ax.annotate('Two firms compete:\neach serves 139,747\n→ ATC = $200', xy=(139747, 200),
                xytext=(150000, 250), fontsize=10.5, color=PLUM, weight='bold', ha='left',
                arrowprops=dict(arrowstyle='->', color=PLUM, lw=1.4))
    ax.annotate('One firm (natural monopoly):\nserves all 279,495\n→ ATC = $100', xy=(279495, 100),
                xytext=(232000, 165), fontsize=10.5, color=NAVY, weight='bold', ha='left',
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.4))
    ax.legend(loc='upper right', fontsize=10.5, frameon=True)
    plt.tight_layout()
    plt.savefig('fig-natural-monopoly.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(); print('saved fig-natural-monopoly.png')


# ============ FIG 2 — the math of zero marginal cost (L-curve) ============
def fig_zero_mc():
    fig, ax = plt.subplots(figsize=(9.6, 5.4))
    ax.plot([0.35, 0.35, 10], [9.2, 0.35, 0.35], color=ORANGE, lw=6, solid_capstyle='round', zorder=5)
    ax.annotate('Fixed upfront cost  ($10B)\nbuilding the initial constellation',
                xy=(0.35, 8.4), xytext=(1.3, 8.6), fontsize=12.5, weight='bold', color=INK, va='center',
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2))
    ax.annotate('Marginal cost  ($0)\nmail a dish, flip a software switch',
                xy=(5.2, 0.35), xytext=(3.4, 1.9), fontsize=12.5, weight='bold', color=INK,
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlabel('Subscribers  →', fontsize=12); ax.set_ylabel('Cost per unit  →', fontsize=12)
    for s in ['top', 'right']: ax.spines[s].set_visible(False)
    ax.set_title('The Math of Zero Marginal Cost', fontsize=15, weight='bold', pad=12, loc='left')
    plt.tight_layout()
    plt.savefig('fig-zero-mc.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(); print('saved fig-zero-mc.png')


# ============ FIG 3 — the 3-pillar digital monopoly Venn ============
def fig_digital_pillars():
    fig, ax = plt.subplots(figsize=(8.8, 7.0))
    r = 1.55
    centers = {'tl': (-0.86, 0.5), 'tr': (0.86, 0.5), 'b': (0.0, -1.0)}
    for c in centers.values():
        ax.add_patch(Circle(c, r, fill=False, ec=INK, lw=2.2, zorder=3))
    # pillar labels (outer area of each circle)
    ax.text(-1.75, 1.35, 'Pillar 1\nAlgorithmic\nMarket-Making', fontsize=12.5, weight='bold', ha='center', color=NAVY)
    ax.text(-1.92, 0.62, 'Dictate dynamic pricing\n& shape demand', fontsize=9.5, ha='center', color='#444')
    ax.text(1.75, 1.35, 'Pillar 2\nEcosystem\nLock-In', fontsize=12.5, weight='bold', ha='center', color=TERRA)
    ax.text(1.92, 0.62, 'Capture intent +\nsoftware switching costs', fontsize=9.5, ha='center', color='#444')
    ax.text(0.0, -2.05, 'Pillar 3 — Economies of Scale', fontsize=12.5, weight='bold', ha='center', color=SAGE)
    ax.text(0.0, -2.42, 'Massive fixed capital → zero-marginal-cost expansion', fontsize=9.5, ha='center', color='#444')
    # center = absolute market power (orange Reuleaux-ish marker)
    ax.add_patch(Circle((0.0, -0.02), 0.62, facecolor=ORANGE, ec='white', lw=1.5, zorder=4, alpha=0.95))
    ax.text(0.0, -0.02, 'Absolute\nMarket\nPower', fontsize=12.5, weight='bold', ha='center', va='center', color='white', zorder=5)
    ax.set_xlim(-3.0, 3.0); ax.set_ylim(-2.7, 2.4); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('The Anatomy of a Digital Monopoly', fontsize=15, weight='bold', pad=4)
    fig.text(0.5, 0.015, 'Hailing a ride, running an AI model, or beaming internet from space — modern digital power\n'
             'relies on eliminating viable substitutes and orchestrating scale. The invisible hand is now coded.',
             ha='center', fontsize=10, color='#555', style='italic')
    plt.tight_layout()
    plt.savefig('fig-digital-pillars.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(); print('saved fig-digital-pillars.png')


if __name__ == '__main__':
    fig_natural_monopoly(); fig_zero_mc(); fig_digital_pillars()
    print('--- ch11 scale figures done ---')
