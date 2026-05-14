"""Supply elasticity over time: three supply curves getting flatter (market period, short run, long run)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5))

q = np.linspace(80, 120, 100)

# Market period: nearly vertical
q_mp = np.full(100, 100)
p_mp = np.linspace(2, 6, 100)
ax.plot(q_mp, p_mp, color='#e74c3c', linewidth=2.5, label='Market Period (vertical)')

# Short run: steep positive slope
p_sr = 1.5 + 0.04 * (q - 80)
ax.plot(q, p_sr, color='#f39c12', linewidth=2.5, label='Short Run (steep)')

# Long run: gentle positive slope
p_lr = 2.5 + 0.015 * (q - 80)
ax.plot(q, p_lr, color='#2196F3', linewidth=2.5, label='Long Run (gentle)')

# Equilibrium points
ax.plot(100, 3.3, 'ko', markersize=6, zorder=5)

# Demand curve
q_d = np.linspace(80, 120, 100)
p_d = 7 - 0.04 * q_d
ax.plot(q_d, p_d, color='#9e9e9e', linewidth=1.5, linestyle='--', alpha=0.6, label='Demand')

# Annotation arrows
ax.annotate('Supply becomes\nmore elastic\nover time', xy=(113, 3.0), fontsize=8,
            ha='center', color='#333', style='italic',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#e3f2fd', alpha=0.8))

ax.set_xlabel('Quantity', fontsize=10)
ax.set_ylabel('Price ($)', fontsize=10)
ax.set_xlim(78, 122)
ax.set_ylim(1.5, 6.5)
ax.legend(fontsize=8, loc='upper left', framealpha=0.9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(alpha=0.2)

plt.tight_layout()
plt.savefig('figures/figure_003_supply_elasticity_time.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_003_supply_elasticity_time.png")
