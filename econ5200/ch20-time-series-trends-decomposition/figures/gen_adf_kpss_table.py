"""Generate ADF/KPSS 2x2 diagnostic table as a clean slide figure."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Colors
green = '#2ecc71'
red = '#e74c3c'
orange = '#f39c12'
gray = '#95a5a6'

# Header
ax.text(5, 7.5, 'ADF / KPSS Diagnostic Table', ha='center', va='center',
        fontsize=14, fontweight='bold', color='#2c3e50')

# Column headers
ax.text(6.5, 6.5, 'KPSS: Don\'t Reject H₀\n(stationary)', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#34495e')
ax.text(8.75, 6.5, 'KPSS: Reject H₀\n(non-stationary)', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#34495e')

# Row headers
ax.text(2.5, 5.0, 'ADF: Reject H₀\n(no unit root)', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#34495e')
ax.text(2.5, 2.5, 'ADF: Don\'t Reject H₀\n(unit root)', ha='center', va='center',
        fontsize=8, fontweight='bold', color='#34495e')

# Cells
cells = [
    (6.5, 5.0, 'STATIONARY ✓', 'Model directly', green),
    (8.75, 5.0, 'TREND-\nSTATIONARY', 'Detrend, don\'t\ndifference', orange),
    (6.5, 2.5, 'NON-\nSTATIONARY', 'Difference\nthe series', red),
    (8.75, 2.5, 'INCONCLUSIVE', 'Increase sample\nor try alt. tests', gray),
]

for x, y, label, action, color in cells:
    rect = mpatches.FancyBboxPatch((x-1.0, y-1.0), 2.0, 2.0,
                                    boxstyle='round,pad=0.1',
                                    facecolor=color, alpha=0.15,
                                    edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y+0.3, label, ha='center', va='center',
            fontsize=9, fontweight='bold', color=color)
    ax.text(x, y-0.5, action, ha='center', va='center',
            fontsize=7, color='#555555')

# Grid lines
ax.plot([4.25, 4.25], [1.0, 7.0], color='#bdc3c7', linewidth=1)
ax.plot([7.625, 7.625], [1.0, 7.0], color='#bdc3c7', linewidth=1)
ax.plot([4.25, 10], [3.75, 3.75], color='#bdc3c7', linewidth=1)
ax.plot([4.25, 10], [6.0, 6.0], color='#bdc3c7', linewidth=1)

plt.tight_layout()
plt.savefig('figures/ch20-adf-kpss-diagnostic-table.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print('OK: ch20-adf-kpss-diagnostic-table.png')
