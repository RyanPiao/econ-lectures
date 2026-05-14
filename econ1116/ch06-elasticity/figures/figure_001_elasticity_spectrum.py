"""Elasticity spectrum: goods arranged by PED from inelastic to elastic."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

goods = [
    ("Insulin", 0.01),
    ("Eggs", 0.03),
    ("Salt", 0.1),
    ("Gasoline (SR)", 0.25),
    ("Cigarettes (adults)", 0.35),
    ("Coffee", 0.3),
    ("Cigarettes (youth)", 0.7),
    ("Shoes", 0.9),
    ("Netflix", 1.2),
    ("Automobiles", 1.2),
    ("Restaurant meals", 2.3),
    ("Foreign travel", 4.0),
    ("Mountain Dew", 4.4),
]

labels = [g[0] for g in goods]
values = [g[1] for g in goods]

colors = []
for v in values:
    if v < 1:
        colors.append('#e74c3c')   # red for inelastic
    elif v == 1.0:
        colors.append('#f39c12')   # orange for unit elastic
    else:
        colors.append('#2196F3')   # blue for elastic

fig, ax = plt.subplots(figsize=(6, 4.5))

y_pos = np.arange(len(labels))
bars = ax.barh(y_pos, values, color=colors, edgecolor='white', height=0.6)

# Add value labels
for i, (bar, val) in enumerate(zip(bars, values)):
    ax.text(bar.get_width() + 0.08, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}' if val < 0.1 else f'{val:.1f}',
            va='center', fontsize=8, color='#333')

ax.set_yticks(y_pos)
ax.set_yticklabels(labels, fontsize=8)
ax.invert_yaxis()
ax.set_xlabel('Price Elasticity of Demand', fontsize=10)

# Add unit elastic line
ax.axvline(x=1.0, color='#f39c12', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(1.05, -0.5, 'Unit\nElastic', fontsize=7, color='#f39c12', va='center')

# Zone labels
ax.text(0.4, len(labels) + 0.3, 'INELASTIC', fontsize=8, color='#e74c3c',
        ha='center', weight='bold', alpha=0.7)
ax.text(2.5, len(labels) + 0.3, 'ELASTIC', fontsize=8, color='#2196F3',
        ha='center', weight='bold', alpha=0.7)

ax.set_xlim(0, 5.0)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('figures/figure_001_elasticity_spectrum.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_001_elasticity_spectrum.png")
