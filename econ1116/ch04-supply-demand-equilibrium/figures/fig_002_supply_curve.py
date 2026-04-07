"""Figure 2: Supply curve for avocados in Boston market."""
import matplotlib.pyplot as plt
import numpy as np

# Data from chapter supply schedule
prices = [0.50, 1.00, 1.50, 2.00, 2.50, 3.00]
qs = [10, 30, 50, 70, 90, 110]

fig, ax = plt.subplots(figsize=(6, 4.5))

# Plot supply curve
ax.plot(qs, prices, 's-', color='#F44336', linewidth=2.5, markersize=8,
        markerfacecolor='white', markeredgewidth=2, markeredgecolor='#F44336',
        label='Supply (S)', zorder=5)

# Shade under curve lightly
ax.fill_between(qs, prices, alpha=0.08, color='#F44336')

# Annotate a reading example
ax.plot(70, 2.00, 's', color='#FF9800', markersize=10, zorder=6)
ax.annotate('At P = $2.00,\nQs = 70K', xy=(70, 2.00), xytext=(30, 2.60),
            fontsize=9, color='#FF9800', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#FF9800', lw=1.5))

# Labels
ax.set_xlabel('Quantity (thousands per week)', fontsize=11, fontweight='bold')
ax.set_ylabel('Price per avocado ($)', fontsize=11, fontweight='bold')
ax.set_xlim(0, 130)
ax.set_ylim(0, 3.50)
ax.set_xticks([0, 20, 40, 60, 80, 100, 120])
ax.set_yticks([0.50, 1.00, 1.50, 2.00, 2.50, 3.00])
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:.2f}'))

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(loc='lower right', fontsize=10, framealpha=0.9)

plt.tight_layout()
plt.savefig('figures/fig_002_supply_curve.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: fig_002_supply_curve.png")
