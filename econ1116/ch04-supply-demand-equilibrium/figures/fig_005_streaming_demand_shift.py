"""Figure 5: Comparative statics — Streaming Wars demand shift (rightward)."""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5))

q = np.linspace(5, 200, 100)

# Supply: P = 5 + 0.04Q (streaming capacity is fairly elastic)
p_supply = 5 + 0.04 * q

# Original demand: P = 25 - 0.08Q
p_demand1 = 25 - 0.08 * q

# Shifted demand (right): P = 32 - 0.08Q
p_demand2 = 32 - 0.08 * q

# Eq1: 25 - 0.08Q = 5 + 0.04Q → 20 = 0.12Q → Q ≈ 167, P ≈ 11.67
eq1_q = 20 / 0.12
eq1_p = 5 + 0.04 * eq1_q

# Eq2: 32 - 0.08Q = 5 + 0.04Q → 27 = 0.12Q → Q = 225... too high
# Adjust: P = 30 - 0.1Q for D2
p_demand2 = 30 - 0.1 * q
# Eq2: 30 - 0.1Q = 5 + 0.04Q → 25 = 0.14Q → Q ≈ 178.6, P ≈ 12.14
eq2_q = 25 / 0.14
eq2_p = 5 + 0.04 * eq2_q

# Plot supply
mask_s = (p_supply > 0) & (p_supply < 30)
ax.plot(q[mask_s], p_supply[mask_s], '-', color='#F44336', linewidth=2.5, label='Supply (S)')

# Plot original demand (dashed)
mask1 = (p_demand1 > 0) & (p_demand1 < 30)
ax.plot(q[mask1], p_demand1[mask1], '--', color='#2196F3', linewidth=2, alpha=0.5,
        label='Demand before (D₁)')

# Plot shifted demand (solid)
mask2 = (p_demand2 > 0) & (p_demand2 < 30)
ax.plot(q[mask2], p_demand2[mask2], '-', color='#2196F3', linewidth=2.5,
        label='Demand after (D₂)')

# Shift arrow
ax.annotate('', xy=(160, 16), xytext=(130, 16),
            arrowprops=dict(arrowstyle='->', color='#2196F3', lw=2.5))
ax.text(145, 17.5, 'Demand\nshifts right', fontsize=9, color='#2196F3',
        fontweight='bold', ha='center')

# Original equilibrium
ax.plot(eq1_q, eq1_p, 'o', color='#9E9E9E', markersize=10, zorder=5)
ax.annotate(f'E₁', xy=(eq1_q, eq1_p), xytext=(eq1_q - 25, eq1_p - 2),
            fontsize=10, color='#9E9E9E', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.2))

# New equilibrium
ax.plot(eq2_q, eq2_p, 'D', color='#4CAF50', markersize=12, zorder=6)
ax.annotate(f'E₂: P↑, Q↑', xy=(eq2_q, eq2_p), xytext=(eq2_q + 10, eq2_p + 3),
            fontsize=9, fontweight='bold', color='#4CAF50',
            arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#4CAF50', alpha=0.9))

# Labels
ax.set_xlabel('Quantity of subscriptions (millions)', fontsize=11, fontweight='bold')
ax.set_ylabel('Price per month ($)', fontsize=11, fontweight='bold')
ax.set_xlim(0, 220)
ax.set_ylim(0, 28)

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.2, linestyle='--')
ax.legend(loc='upper right', fontsize=9, framealpha=0.9)

plt.tight_layout()
plt.savefig('figures/fig_005_streaming_demand_shift.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: fig_005_streaming_demand_shift.png")
