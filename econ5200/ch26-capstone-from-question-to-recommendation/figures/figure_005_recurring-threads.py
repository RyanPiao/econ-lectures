"""Figure 5: Recurring Threads timeline — 4 datasets across 25 chapters."""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5))

threads = {
    'California\nHousing': {'chapters': [4, 12, 13, 15, 16, 19, 22], 'color': '#e74c3c', 'y': 3.5},
    'FRED &\nMacro':       {'chapters': [2, 5, 12, 16, 20, 21], 'color': '#3498db', 'y': 2.5},
    'Lalonde\nNSW':        {'chapters': [8, 9, 10, 24], 'color': '#27ae60', 'y': 1.5},
    'FedSpeak':            {'chapters': [23, 24, 25], 'color': '#9b59b6', 'y': 0.5},
}

ax.set_xlim(0, 27)
ax.set_ylim(-0.2, 4.5)

for name, info in threads.items():
    y = info['y']
    chs = info['chapters']
    color = info['color']

    # Draw connecting line
    ax.plot([min(chs), max(chs)], [y, y], color=color, linewidth=2, alpha=0.4)

    # Draw chapter markers
    ax.scatter(chs, [y]*len(chs), color=color, s=60, zorder=5, edgecolors='white', linewidth=0.5)

    # Label
    ax.text(-0.5, y, name, fontsize=8, fontweight='bold', color=color,
            ha='right', va='center')

# Ch 26 marker
ax.axvline(x=26, color='#2c3e50', linestyle='--', alpha=0.5, linewidth=1)
ax.text(26, 4.2, 'Ch 26\nCapstone', fontsize=8, ha='center', color='#2c3e50', fontweight='bold')

# Axis formatting
ax.set_xlabel('Chapter', fontsize=10)
ax.set_xticks([1, 5, 10, 15, 20, 25])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('figure_005_recurring-threads.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('OK: figure_005_recurring-threads.png')
