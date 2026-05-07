"""
Figure 006: AI Productivity Perception Gap
Dual bar chart comparing measured vs perceived AI productivity impact
from the Peng et al. (2023) and METR (2025) studies.
"""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)

studies = ['Peng et al.\n(2023)\nModular tasks', 'METR\n(2025)\nComplex codebases']
measured = [55.8, -19]
perceived = [None, 20]  # Peng didn't measure perception

x = np.array([0, 1.2])
width = 0.35

# Measured bars
bars1 = ax.bar(x - width/2, measured, width, label='Measured Impact',
               color=['#16a34a', '#dc2626'], edgecolor='white', linewidth=0.5, zorder=3)

# Perceived bars (only METR)
bars2 = ax.bar(x[1] + width/2, [perceived[1]], width, label='Perceived Impact',
               color='#f59e0b', edgecolor='white', linewidth=0.5, zorder=3)

# Add value labels
for bar, val in zip(bars1, measured):
    ypos = bar.get_height() if val >= 0 else bar.get_height()
    va = 'bottom' if val >= 0 else 'top'
    offset = 2 if val >= 0 else -2
    ax.text(bar.get_x() + bar.get_width()/2, ypos + offset,
            f'{val:+.1f}%', ha='center', va=va, fontsize=10, fontweight='bold')

ax.text(bars2[0].get_x() + bars2[0].get_width()/2,
        bars2[0].get_height() + 2,
        f'+{perceived[1]}%', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Perception gap annotation
ax.annotate('', xy=(x[1] + width/2, 20), xytext=(x[1] - width/2, -19),
            arrowprops=dict(arrowstyle='<->', color='#6b7280', lw=1.5))
ax.text(x[1] + 0.55, 0.5, '~40pp\ngap', ha='left', va='center',
        fontsize=8, color='#6b7280', fontstyle='italic')

ax.axhline(y=0, color='black', linewidth=0.8, zorder=2)
ax.set_ylabel('Productivity Impact (%)', fontsize=10)
ax.set_xticks(x)
ax.set_xticklabels(studies, fontsize=9)
ax.set_ylim(-30, 70)
ax.legend(loc='upper left', fontsize=8, framealpha=0.9)
ax.grid(axis='y', alpha=0.15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("figures/figure_006_perception_gap.png",
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figure_006_perception_gap.png")
