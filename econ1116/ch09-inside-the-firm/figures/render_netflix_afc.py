"""Netflix AFC chart: $17B fixed content cost spread over N subscribers.
AFC(N) = $17B / N. Mark Netflix's actual scale at 312.5M subscribers.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

GREEN = '#0A5538'
ACCENT = '#C47B5A'
PRIMARY = '#0a2e5c'

FC_BILLION = 17.0  # $17B fixed content cost
N_RANGE = np.linspace(20, 400, 500)  # subscribers in millions
afc = FC_BILLION * 1000 / N_RANGE   # $ per subscriber (FC in millions / N)

# Netflix actual scale
N_NETFLIX = 312.5
AFC_NETFLIX = FC_BILLION * 1000 / N_NETFLIX  # = $54.40

fig, ax = plt.subplots(figsize=(7.5, 4.6))
ax.plot(N_RANGE, afc, color=GREEN, linewidth=3.4, zorder=3)

# Mark Netflix's current scale
ax.plot([N_NETFLIX], [AFC_NETFLIX], 'o', color=GREEN, markersize=14,
        markeredgecolor='white', markeredgewidth=2.5, zorder=5)
ax.annotate(f'Netflix today: {N_NETFLIX:.1f}M subs\nAFC = ${AFC_NETFLIX:.2f}/sub',
            xy=(N_NETFLIX, AFC_NETFLIX), xytext=(N_NETFLIX - 130, AFC_NETFLIX + 110),
            fontsize=11, color=GREEN, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=GREEN, linewidth=1.4),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.6))

# Annotation at low scale (illustrates the steep early decline)
N_SMALL = 30
ax.annotate('At 30M subs:\nAFC = $567/sub',
            xy=(N_SMALL, FC_BILLION * 1000 / N_SMALL),
            xytext=(N_SMALL + 80, FC_BILLION * 1000 / N_SMALL + 30),
            fontsize=10.5, color=ACCENT, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor=ACCENT, linewidth=1.3),
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.3))

ax.set_xlabel('Subscribers  (millions)', fontsize=12, fontweight='bold')
ax.set_ylabel('AFC = $17B / N  ($ per subscriber)', fontsize=12, fontweight='bold')
ax.set_xlim(0, 410)
ax.set_ylim(0, 700)
ax.set_xticks([0, 100, 200, 300, 400])
ax.set_yticks([0, 100, 200, 300, 400, 500, 600])
ax.grid(True, alpha=0.18)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_title('Survival by Spreading: AFC Collapses with Scale',
             fontsize=12.5, fontweight='bold', loc='left', pad=10)

plt.tight_layout()
plt.savefig('fig-netflix-afc.png', dpi=160, bbox_inches='tight',
            facecolor='white')
print(f'saved fig-netflix-afc.png  (Netflix AFC @ 312.5M = ${AFC_NETFLIX:.2f})')
