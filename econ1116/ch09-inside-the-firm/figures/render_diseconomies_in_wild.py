"""Vertical-farming diseconomies chart: Operational Complexity (red,
exponential) crosses Crop Value (black, linear). Once they cross,
each extra acre of vertical farm loses money — complexity thresholds
invert the unit economics.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PRIMARY = '#2D2D2D'
DANGER = '#C72A2A'
MUTED = '#6b6b6b'

q = np.linspace(0, 10, 500)
# Linear crop value: y = 0.5 + 0.55*q
value = 0.5 + 0.55 * q
# Exponential operational complexity: y = 0.4 + 0.04 * exp(0.55*q)
complexity = 0.4 + 0.04 * np.exp(0.55 * q)

fig, ax = plt.subplots(figsize=(7.6, 4.6))
ax.plot(q, value, color=PRIMARY, linewidth=3.4, label='Crop Value', zorder=3)
ax.plot(q, complexity, color=DANGER, linewidth=3.4, label='Operational Complexity', zorder=3)

# Find crossing point
diff = complexity - value
sign_changes = np.where(np.diff(np.sign(diff)))[0]
if len(sign_changes) > 0:
    idx = sign_changes[0]
    q_cross = q[idx]
    y_cross = value[idx]
    ax.plot([q_cross], [y_cross], 'o', color=DANGER, markersize=14,
            markeredgecolor='white', markeredgewidth=2.5, zorder=6)
    ax.annotate('Crossover —\nunit economics flip',
                xy=(q_cross, y_cross), xytext=(q_cross + 1.4, y_cross + 1.4),
                fontsize=10.5, color=DANGER, fontweight='bold', ha='center',
                bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                          edgecolor=DANGER, linewidth=1.4),
                arrowprops=dict(arrowstyle='->', color=DANGER, lw=1.4))

# Cost-source annotations on the right side of complexity curve
ax.annotate('Energy',
            xy=(7.5, 0.4 + 0.04 * np.exp(0.55 * 7.5) - 0.4),
            xytext=(6.0, 4.6),
            fontsize=11, color=MUTED, ha='center',
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.0,
                            connectionstyle='arc3,rad=0.2'))
ax.annotate('Lighting',
            xy=(8.0, 0.4 + 0.04 * np.exp(0.55 * 8.0) - 0.5),
            xytext=(6.7, 5.4),
            fontsize=11, color=MUTED, ha='center',
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.0,
                            connectionstyle='arc3,rad=0.2'))
ax.annotate('Robotics\nMaintenance',
            xy=(8.5, 0.4 + 0.04 * np.exp(0.55 * 8.5) - 0.6),
            xytext=(7.6, 6.4),
            fontsize=10.5, color=MUTED, ha='center',
            arrowprops=dict(arrowstyle='->', color=MUTED, lw=1.0,
                            connectionstyle='arc3,rad=0.2'))

# Curve labels at right edge
ax.text(10.2, value[-1], 'Crop Value',
        fontsize=12, color=PRIMARY, fontweight='bold', va='center', ha='left')
ax.text(10.2, complexity[-1], 'Operational\nComplexity',
        fontsize=12, color=DANGER, fontweight='bold', va='center', ha='left')

ax.set_xlim(0, 13)
ax.set_ylim(0, 11)
ax.set_xlabel('Scale of Operations', fontsize=12, fontweight='bold')
ax.set_ylabel('Value  /  Complexity', fontsize=12, fontweight='bold')
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.15)

plt.tight_layout()
plt.savefig('fig-vertical-farming.png', dpi=160, bbox_inches='tight',
            facecolor='white')
print('saved fig-vertical-farming.png')
