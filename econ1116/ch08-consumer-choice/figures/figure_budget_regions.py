"""Budget Constraint regions — affordable (green) vs not affordable (pink)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(9, 5.6))

# Budget line: 4*Q_beef + 1*Q_avo = 16
# Endpoints (avo, beef): (0, 4) and (16, 0)
x_line = np.array([0, 16])
y_line = np.array([4, 0])

# Plot region: affordable (green triangle below line) + unaffordable (pink above)
x_max, y_max = 18, 5

# Affordable region — below the line + axes
affordable_x = [0, 16, 0]
affordable_y = [0, 0, 4]
ax.fill(affordable_x, affordable_y, color='#dcfce7', alpha=0.85, zorder=1)

# Not affordable region — everything above the line within the plot area
# Vertices: (0,4) → (16,0) → (x_max,0) → (x_max,y_max) → (0,y_max) → (0,4)
not_affordable_x = [0, 16, x_max, x_max, 0, 0]
not_affordable_y = [4, 0, 0, y_max, y_max, 4]
ax.fill(not_affordable_x, not_affordable_y, color='#fee2e2', alpha=0.85, zorder=1)

# Budget line on top — solid_capstyle round + zorder>marker so the line meets
# the marker center instead of stopping short of it
ax.plot(x_line, y_line, color='#6d28d9', linewidth=4, zorder=7,
        solid_capstyle='round')

# Endpoint markers
ax.plot(0, 4, 'o', color='#dc2626', markersize=18, zorder=6,
        markeredgecolor='#7f1d1d', markeredgewidth=1.5)
ax.annotate('4 lbs Beef', xy=(0, 4), xytext=(0.6, 4.25),
            fontsize=13, weight='bold', color='#dc2626', ha='left')

ax.plot(16, 0, 'o', color='#15803d', markersize=18, zorder=6,
        markeredgecolor='#14532d', markeredgewidth=1.5)
ax.annotate('16 Avocados', xy=(16, 0), xytext=(14.4, 0.45),
            fontsize=13, weight='bold', color='#15803d')

# Region labels
ax.text(4, 1.0, 'AFFORDABLE\n(Attainable)', fontsize=18, weight='bold',
        color='#15803d', ha='center', va='center')
ax.text(11, 3.3, 'NOT AFFORDABLE\n(Unattainable)', fontsize=18, weight='bold',
        color='#b91c1c', ha='center', va='center')

# Axis labels
ax.set_xlabel('$Q_{Avocado}$', fontsize=14, weight='bold')
ax.set_ylabel('$Q_{Beef}$', fontsize=14, weight='bold')

# Axes anchored at (0, 0)
ax.set_xlim(0, x_max)
ax.set_ylim(0, y_max)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#1f2937')
ax.spines['bottom'].set_color('#1f2937')
ax.spines['left'].set_linewidth(2.2)
ax.spines['bottom'].set_linewidth(2.2)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))

plt.tight_layout()
plt.savefig('figures/figure_budget_regions.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_budget_regions.png")
