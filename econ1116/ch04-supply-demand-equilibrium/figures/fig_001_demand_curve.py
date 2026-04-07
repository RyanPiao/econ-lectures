"""Figure 1: Demand curve for avocados in Boston market."""
import matplotlib.pyplot as plt
import numpy as np

# Data from chapter demand schedule
prices = [0.50, 1.00, 1.50, 2.00, 2.50, 3.00]
qd = [120, 100, 80, 60, 40, 20]

fig, ax = plt.subplots(figsize=(6, 4.5))

# Plot demand curve
ax.plot(qd, prices, 'o-', color='#2196F3', linewidth=2.5, markersize=8,
        markerfacecolor='white', markeredgewidth=2, markeredgecolor='#2196F3',
        label='Demand (D)', zorder=5)

# Shade under curve lightly
ax.fill_between(qd, prices, alpha=0.08, color='#2196F3')

# Annotate a reading example
ax.annotate('', xy=(60, 0), xytext=(60, 2.00),
            arrowprops=dict(arrowstyle='->', color='#666', lw=1.2, ls='--'))
ax.annotate('', xy=(0, 2.00), xytext=(60, 2.00),
            arrowprops=dict(arrowstyle='->', color='#666', lw=1.2, ls='--'))
ax.plot(60, 2.00, 'o', color='#FF5722', markersize=10, zorder=6)
ax.annotate('At P = $2.00,\nQd = 60K', xy=(60, 2.00), xytext=(80, 2.60),
            fontsize=9, color='#FF5722', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#FF5722', lw=1.5))

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
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='upper right', fontsize=10, framealpha=0.9)

plt.tight_layout()
plt.savefig('figures/fig_001_demand_curve.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: fig_001_demand_curve.png")
