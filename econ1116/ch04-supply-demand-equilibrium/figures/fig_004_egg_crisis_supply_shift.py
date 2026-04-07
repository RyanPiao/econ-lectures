"""Figure 4: Comparative statics — Egg crisis supply shift (leftward)."""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5))

# Generic S&D for eggs (stylized)
q = np.linspace(5, 100, 100)

# Demand curve: P = 8 - 0.06Q
p_demand = 8 - 0.06 * q

# Original supply: P = 1 + 0.05Q
p_supply1 = 1 + 0.05 * q

# Shifted supply (left): P = 3 + 0.05Q (shifted up by $2 = left shift)
p_supply2 = 3 + 0.05 * q

# Find equilibria
# D = S1: 8 - 0.06Q = 1 + 0.05Q → 7 = 0.11Q → Q = 63.6, P = 4.18
eq1_q = 7 / 0.11
eq1_p = 8 - 0.06 * eq1_q

# D = S2: 8 - 0.06Q = 3 + 0.05Q → 5 = 0.11Q → Q = 45.5, P = 5.27
eq2_q = 5 / 0.11
eq2_p = 8 - 0.06 * eq2_q

# Plot demand
ax.plot(q, p_demand, '-', color='#2196F3', linewidth=2.5, label='Demand (D)')

# Plot original supply (dashed)
mask1 = (p_supply1 > 0) & (p_supply1 < 8)
ax.plot(q[mask1], p_supply1[mask1], '--', color='#F44336', linewidth=2, alpha=0.5,
        label='Supply before (S₁)')

# Plot shifted supply (solid)
mask2 = (p_supply2 > 0) & (p_supply2 < 8)
ax.plot(q[mask2], p_supply2[mask2], '-', color='#F44336', linewidth=2.5,
        label='Supply after (S₂)')

# Shift arrow
ax.annotate('', xy=(35, 4.75), xytext=(55, 3.75),
            arrowprops=dict(arrowstyle='->', color='#F44336', lw=2.5))
ax.text(38, 3.95, 'Supply\nshifts left', fontsize=9, color='#F44336',
        fontweight='bold', ha='center')

# Original equilibrium
ax.plot(eq1_q, eq1_p, 'o', color='#9E9E9E', markersize=10, zorder=5)
ax.annotate(f'E₁: P=${eq1_p:.2f}', xy=(eq1_q, eq1_p), xytext=(78, 3.80),
            fontsize=9, color='#9E9E9E',
            arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.2))

# New equilibrium
ax.plot(eq2_q, eq2_p, 'D', color='#4CAF50', markersize=12, zorder=6)
ax.annotate(f'E₂: P=${eq2_p:.2f}', xy=(eq2_q, eq2_p), xytext=(20, 6.20),
            fontsize=9, fontweight='bold', color='#4CAF50',
            arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#4CAF50', alpha=0.9))

# Price increase arrow
ax.annotate('', xy=(8, eq2_p), xytext=(8, eq1_p),
            arrowprops=dict(arrowstyle='<->', color='#FF9800', lw=2))
ax.text(12, (eq1_p + eq2_p)/2, 'P ↑', fontsize=11, fontweight='bold',
        color='#FF9800', ha='center', va='center')

# Quantity decrease arrow
ax.annotate('', xy=(eq2_q, 1.2), xytext=(eq1_q, 1.2),
            arrowprops=dict(arrowstyle='<->', color='#FF9800', lw=2))
ax.text((eq1_q + eq2_q)/2, 0.8, 'Q ↓', fontsize=11, fontweight='bold',
        color='#FF9800', ha='center')

# Labels
ax.set_xlabel('Quantity of eggs', fontsize=11, fontweight='bold')
ax.set_ylabel('Price per dozen ($)', fontsize=11, fontweight='bold')
ax.set_xlim(0, 105)
ax.set_ylim(0, 8)

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.2, linestyle='--')
ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig('figures/fig_004_egg_crisis_supply_shift.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: fig_004_egg_crisis_supply_shift.png")
