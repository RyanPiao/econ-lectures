"""Figure 3: Supply and demand equilibrium for avocados with surplus/shortage zones."""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

# Data
prices = np.array([0.50, 1.00, 1.50, 2.00, 2.50, 3.00])
qd = np.array([120, 100, 80, 60, 40, 20])
qs = np.array([10, 30, 50, 70, 90, 110])

# Interpolate for smooth curves
p_fine = np.linspace(0.3, 3.2, 100)
qd_fine = np.interp(p_fine, prices, qd[::-1])[::-1]  # demand is decreasing
qs_fine = np.interp(p_fine, prices, qs)

# Equilibrium approximately at P=1.75, Q=70
eq_p = 1.75
eq_q = 70

fig, ax = plt.subplots(figsize=(6, 4.5))

# Plot curves
ax.plot(qd, prices, 'o-', color='#2196F3', linewidth=2.5, markersize=7,
        markerfacecolor='white', markeredgewidth=2, markeredgecolor='#2196F3',
        label='Demand (D)', zorder=5)
ax.plot(qs, prices, 's-', color='#F44336', linewidth=2.5, markersize=7,
        markerfacecolor='white', markeredgewidth=2, markeredgecolor='#F44336',
        label='Supply (S)', zorder=5)

# Equilibrium point
ax.plot(eq_q, eq_p, 'D', color='#4CAF50', markersize=12, zorder=6)
ax.annotate(f'Equilibrium\nP* = ${eq_p:.2f}, Q* = {eq_q}K',
            xy=(eq_q, eq_p), xytext=(95, 1.30),
            fontsize=9, fontweight='bold', color='#4CAF50',
            arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#4CAF50', alpha=0.9))

# Dashed lines to axes
ax.plot([eq_q, eq_q], [0, eq_p], '--', color='#4CAF50', alpha=0.5, linewidth=1)
ax.plot([0, eq_q], [eq_p, eq_p], '--', color='#4CAF50', alpha=0.5, linewidth=1)

# Surplus zone (above equilibrium)
ax.fill_betweenx([2.00, 2.50], [60, 40], [70, 90], alpha=0.15, color='#FF9800')
ax.annotate('Surplus', xy=(75, 2.25), fontsize=10, fontweight='bold',
            color='#FF9800', ha='center')

# Shortage zone (below equilibrium)
ax.fill_betweenx([1.00, 1.50], [30, 50], [100, 80], alpha=0.15, color='#9C27B0')
ax.annotate('Shortage', xy=(65, 1.10), fontsize=10, fontweight='bold',
            color='#9C27B0', ha='center')

# Labels
ax.set_xlabel('Quantity (thousands per week)', fontsize=11, fontweight='bold')
ax.set_ylabel('Price per avocado ($)', fontsize=11, fontweight='bold')
ax.set_xlim(0, 140)
ax.set_ylim(0, 3.50)
ax.set_xticks([0, 20, 40, 60, 80, 100, 120])
ax.set_yticks([0.50, 1.00, 1.50, 2.00, 2.50, 3.00])
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:.2f}'))

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.2, linestyle='--')
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

plt.tight_layout()
plt.savefig('figures/fig_003_equilibrium.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: fig_003_equilibrium.png")
