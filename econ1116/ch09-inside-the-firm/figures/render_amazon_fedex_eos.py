"""Economies-of-scale LRATC curve marking Amazon (mid-scale) and FedEx
(further along the curve, near MES). Mirrors the user's reference
screenshot but in the deck's warm-paper palette.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

PRIMARY = '#0a2e5c'
ACCENT = '#C47B5A'
GREEN = '#0A5538'
SECONDARY = '#6B8BA4'

q = np.linspace(1, 12, 500)
# Smooth declining curve: high at low Q, asymptotes near 1.0
y = 1.0 + 9.5 / (q ** 0.95)

fig, ax = plt.subplots(figsize=(8.0, 4.8))
ax.plot(q, y, color=PRIMARY, linewidth=3.4, zorder=3)

# Amazon point (mid-scale)
Q_AMAZON = 3.5
Y_AMAZON = 1.0 + 9.5 / (Q_AMAZON ** 0.95)
ax.plot([Q_AMAZON], [Y_AMAZON], 'o', color=ACCENT, markersize=15,
        markeredgecolor='white', markeredgewidth=2.5, zorder=6)
ax.annotate('Amazon\n3.6M sq ft warehouses\n→ hyper-specialization',
            xy=(Q_AMAZON, Y_AMAZON), xytext=(Q_AMAZON + 2.7, Y_AMAZON + 1.4),
            fontsize=11, color=ACCENT, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=ACCENT, linewidth=1.5),
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

# FedEx point (further along)
Q_FEDEX = 7.5
Y_FEDEX = 1.0 + 9.5 / (Q_FEDEX ** 0.95)
ax.plot([Q_FEDEX], [Y_FEDEX], 'o', color=GREEN, markersize=15,
        markeredgecolor='white', markeredgewidth=2.5, zorder=6)
ax.annotate('FedEx\n225 flights/night\n→ network effects',
            xy=(Q_FEDEX, Y_FEDEX), xytext=(Q_FEDEX + 1.6, Y_FEDEX + 1.7),
            fontsize=11, color=GREEN, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                      edgecolor=GREEN, linewidth=1.5),
            arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))

# "Economies of Scale" shaded arrow region
ax.fill_between([1.2, 9.0], [10.5, 10.5], [0, 0], color='#d8d8d4', alpha=0.18,
                zorder=1)
ax.text(4.5, 9.0, 'Economies of Scale\n(LRATC falling)',
        fontsize=12.5, color=PRIMARY, fontweight='bold', ha='center',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                  edgecolor=PRIMARY, linewidth=1.4),
        zorder=4)

ax.set_xlabel('Output  (Q)', fontsize=12, fontweight='bold')
ax.set_ylabel('Cost per unit', fontsize=12, fontweight='bold')
ax.set_xlim(0, 13)
ax.set_ylim(0, 11)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('fig-amazon-fedex-eos.png', dpi=160, bbox_inches='tight',
            facecolor='white')
print('saved fig-amazon-fedex-eos.png')
