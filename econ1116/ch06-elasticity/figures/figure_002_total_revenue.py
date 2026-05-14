"""Total revenue rectangles: elastic vs inelastic demand, before/after price change."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(6, 4))

# --- Panel 1: Elastic Demand (Campus Coffee) ---
ax = axes[0]
ax.set_title('Elastic Demand\n(Campus Coffee)', fontsize=9, weight='bold')

# Demand curve (steep = elastic for visual, but we show quantities changing a lot)
p_range = np.linspace(3, 7, 100)
q_range = 300 - 28 * p_range  # elastic: big Q change

ax.plot(q_range, p_range, color='#2196F3', linewidth=2)

# Before: P=4.50, Q=200
rect_before = mpatches.FancyBboxPatch((0, 0), 200, 4.50, boxstyle="square,pad=0",
                                       facecolor='#2196F3', alpha=0.15, edgecolor='#2196F3', linewidth=1)
ax.add_patch(rect_before)
ax.text(100, 2.25, 'TR = $900', ha='center', va='center', fontsize=8, color='#1565c0')

# After: P=5.50, Q=160
rect_after = mpatches.FancyBboxPatch((0, 0), 160, 5.50, boxstyle="square,pad=0",
                                      facecolor='#e74c3c', alpha=0.12, edgecolor='#e74c3c',
                                      linewidth=1, linestyle='--')
ax.add_patch(rect_after)
ax.text(80, 5.0, 'TR = $880', ha='center', va='center', fontsize=8, color='#c62828')

ax.annotate('TR falls!', xy=(180, 5.5), fontsize=9, color='#c62828', weight='bold')

ax.set_xlim(0, 250)
ax.set_ylim(0, 7)
ax.set_xlabel('Quantity', fontsize=8)
ax.set_ylabel('Price ($)', fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# --- Panel 2: Inelastic Demand (Eggs) ---
ax = axes[1]
ax.set_title('Inelastic Demand\n(Eggs)', fontsize=9, weight='bold')

# Nearly vertical demand curve
p_range2 = np.linspace(1, 6, 100)
q_range2 = 103 - 1.0 * p_range2  # inelastic: tiny Q change

ax.plot(q_range2, p_range2, color='#e74c3c', linewidth=2)

# Before: P=2.50, Q=100
rect_before2 = mpatches.FancyBboxPatch((0, 0), 100, 2.50, boxstyle="square,pad=0",
                                        facecolor='#2196F3', alpha=0.15, edgecolor='#2196F3', linewidth=1)
ax.add_patch(rect_before2)
ax.text(50, 1.25, 'TR = $250M', ha='center', va='center', fontsize=7, color='#1565c0')

# After: P=5.00, Q=98
rect_after2 = mpatches.FancyBboxPatch((0, 0), 98, 5.00, boxstyle="square,pad=0",
                                       facecolor='#4caf50', alpha=0.12, edgecolor='#4caf50',
                                       linewidth=1, linestyle='--')
ax.add_patch(rect_after2)
ax.text(49, 3.75, 'TR = $490M', ha='center', va='center', fontsize=7, color='#2e7d32')

ax.annotate('TR nearly doubles!', xy=(50, 5.3), fontsize=8, color='#2e7d32', weight='bold',
            ha='center')

ax.set_xlim(0, 120)
ax.set_ylim(0, 6.5)
ax.set_xlabel('Quantity (millions)', fontsize=8)
ax.set_ylabel('Price ($)', fontsize=8)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/figure_002_total_revenue.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_002_total_revenue.png")
