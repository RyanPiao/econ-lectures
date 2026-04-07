"""Figure 6: Comparative statics — Austin housing double shift (D↓, S↑)."""
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5))

q = np.linspace(5, 200, 100)

# Original demand: P = 800 - 2Q (thousands of homes, price in $K)
p_d1 = 800 - 2 * q

# Shifted demand (left — rates up, tech layoffs): P = 700 - 2Q
p_d2 = 700 - 2 * q

# Original supply: P = 200 + 1.5Q
p_s1 = 200 + 1.5 * q

# Shifted supply (right — new construction): P = 150 + 1.5Q
p_s2 = 150 + 1.5 * q

# Eq1: 800 - 2Q = 200 + 1.5Q → 600 = 3.5Q → Q ≈ 171.4, P ≈ 457.1
eq1_q = 600 / 3.5
eq1_p = 200 + 1.5 * eq1_q

# Eq2: 700 - 2Q = 150 + 1.5Q → 550 = 3.5Q → Q ≈ 157.1, P ≈ 385.7
eq2_q = 550 / 3.5
eq2_p = 150 + 1.5 * eq2_q

# Plot original curves (dashed)
mask = lambda p: (p > 100) & (p < 850)
ax.plot(q[mask(p_d1)], p_d1[mask(p_d1)], '--', color='#2196F3', linewidth=1.8, alpha=0.5, label='D₁ (before)')
ax.plot(q[mask(p_s1)], p_s1[mask(p_s1)], '--', color='#F44336', linewidth=1.8, alpha=0.5, label='S₁ (before)')

# Plot shifted curves (solid)
ax.plot(q[mask(p_d2)], p_d2[mask(p_d2)], '-', color='#2196F3', linewidth=2.5, label='D₂ (after)')
ax.plot(q[mask(p_s2)], p_s2[mask(p_s2)], '-', color='#F44336', linewidth=2.5, label='S₂ (after)')

# Shift arrows
ax.annotate('', xy=(100, 500), xytext=(130, 540),
            arrowprops=dict(arrowstyle='->', color='#2196F3', lw=2))
ax.text(105, 555, 'D shifts\nleft', fontsize=8, color='#2196F3', fontweight='bold')

ax.annotate('', xy=(170, 405), xytext=(140, 410),
            arrowprops=dict(arrowstyle='->', color='#F44336', lw=2))
ax.text(148, 425, 'S shifts\nright', fontsize=8, color='#F44336', fontweight='bold')

# Equilibria
ax.plot(eq1_q, eq1_p, 'o', color='#9E9E9E', markersize=10, zorder=5)
ax.annotate(f'E₁: ~$457K', xy=(eq1_q, eq1_p), xytext=(eq1_q + 15, eq1_p + 50),
            fontsize=9, color='#9E9E9E',
            arrowprops=dict(arrowstyle='->', color='#9E9E9E', lw=1.2))

ax.plot(eq2_q, eq2_p, 'D', color='#4CAF50', markersize=12, zorder=6)
ax.annotate(f'E₂: ~$386K\nP ↓ for sure', xy=(eq2_q, eq2_p), xytext=(eq2_q - 60, eq2_p - 80),
            fontsize=9, fontweight='bold', color='#4CAF50',
            arrowprops=dict(arrowstyle='->', color='#4CAF50', lw=1.5),
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#4CAF50', alpha=0.9))

# Labels
ax.set_xlabel('Quantity of homes (thousands)', fontsize=11, fontweight='bold')
ax.set_ylabel('Price ($K)', fontsize=11, fontweight='bold')
ax.set_xlim(50, 210)
ax.set_ylim(200, 700)

# Style
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.2, linestyle='--')
ax.legend(loc='upper right', fontsize=8, framealpha=0.9, ncol=2)

plt.tight_layout()
plt.savefig('figures/fig_006_austin_double_shift.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: fig_006_austin_double_shift.png")
