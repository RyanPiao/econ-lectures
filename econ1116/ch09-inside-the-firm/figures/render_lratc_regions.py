"""Render a clean LRATC U-curve with the three labelled regions:
Economies of Scale → Constant Returns to Scale → Diseconomies of Scale.
Marks ATC_min and the Q0 / Q1 boundaries where the flat-bottom region
begins and ends.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Build a piecewise LRATC: declining curve → flat plateau → rising curve.
GREEN = '#5C8C3F'
PRIMARY = '#0a2e5c'
MUTED = '#666'

q1 = np.linspace(1.0, 4, 300)   # economies-of-scale region (falling)
q2 = np.linspace(4, 8, 100)     # constant-returns plateau (flat)
q3 = np.linspace(8, 12, 300)    # diseconomies region (rising)

# ATC_min is the plateau value
ATC_MIN = 1.0
# Falling: smooth cosine-blend from ATC_MIN + h0 at q1[0] down to ATC_MIN at q1[-1]
h0 = 2.6
t1 = (q1 - q1[0]) / (q1[-1] - q1[0])
y1 = ATC_MIN + h0 * (1 + np.cos(np.pi * t1)) / 2
# Flat plateau
y2 = np.full_like(q2, ATC_MIN)
# Rising: smooth cosine-blend from ATC_MIN at q3[0] up to ATC_MIN + h1 at q3[-1]
h1 = 2.6
t3 = (q3 - q3[0]) / (q3[-1] - q3[0])
y3 = ATC_MIN + h1 * (1 - np.cos(np.pi * t3)) / 2

q_all = np.concatenate([q1, q2, q3])
y_all = np.concatenate([y1, y2, y3])

fig, ax = plt.subplots(figsize=(7.2, 4.6))
ax.plot(q_all, y_all, color=GREEN, linewidth=3.4, zorder=3)

# Plateau endpoints
ax.plot([4], [ATC_MIN], 'o', color='white', markersize=10, zorder=5,
        markeredgecolor=GREEN, markeredgewidth=2.5)
ax.plot([8], [ATC_MIN], 'o', color='white', markersize=10, zorder=5,
        markeredgecolor=GREEN, markeredgewidth=2.5)

# Horizontal ATC_min dashed line
ax.plot([0, 4], [ATC_MIN, ATC_MIN], '--', color=MUTED, linewidth=1.0, alpha=0.7)
# Vertical dashed at Q0 and Q1
ax.plot([4, 4], [0, ATC_MIN], '--', color=MUTED, linewidth=1.0, alpha=0.7)
ax.plot([8, 8], [0, ATC_MIN], '--', color=MUTED, linewidth=1.0, alpha=0.7)

# Region annotation: Economies of Scale (top-left arrow into falling part)
ax.annotate('Economies\nof Scale',
            xy=(1.6, y1[40] - 0.1), xytext=(1.5, 4.2),
            fontsize=11, color='#1f6f3f', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor='#1f6f3f', linewidth=1.3),
            arrowprops=dict(arrowstyle='->', color='#1f6f3f', lw=1.3))

# Region annotation: Diseconomies of Scale (top-right arrow into rising part)
ax.annotate('Diseconomies\nof Scale',
            xy=(10.2, y3[100]), xytext=(10.5, 4.2),
            fontsize=11, color='#a14a1f', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor='#a14a1f', linewidth=1.3),
            arrowprops=dict(arrowstyle='->', color='#a14a1f', lw=1.3))

# Region annotation: Constant Returns to Scale (bottom-middle pointing to plateau)
ax.annotate('Constant Returns\nto Scale',
            xy=(6, ATC_MIN), xytext=(6, 0.25),
            fontsize=10.5, color=PRIMARY, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                      edgecolor=PRIMARY, linewidth=1.2),
            arrowprops=dict(arrowstyle='->', color=PRIMARY, lw=1.2))

# LRATC label on the right
ax.text(11.9, y3[-1] + 0.1, 'LRATC',
        fontsize=14, color=GREEN, fontweight='bold', fontstyle='italic',
        ha='right', va='bottom')

# Axes labels
ax.set_xlabel('Output  (Q)', fontsize=12, fontweight='bold')
ax.set_ylabel('Cost per unit', fontsize=12, fontweight='bold')

# Tick labels for ATC_min, Q0, Q1
ax.set_yticks([ATC_MIN])
ax.set_yticklabels(['$ATC_{min}$'], fontsize=11, fontstyle='italic')
ax.set_xticks([4, 8])
ax.set_xticklabels(['$Q_0$', '$Q_1$'], fontsize=12, fontstyle='italic')

ax.set_xlim(0, 12.5)
ax.set_ylim(0, 4.8)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(True, alpha=0.15)

plt.tight_layout()
plt.savefig('fig-lratc-regions.png', dpi=160, bbox_inches='tight',
            facecolor='white')
print('saved fig-lratc-regions.png')
