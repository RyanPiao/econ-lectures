"""Regenerate the 3 amc-panel figures (slide 58).

Earlier version had two sets of region labels — top "Increasing returns / Diminishing
returns" arrows dividing the chart at the MC minimum (~Q=90), AND bottom "When
MC < AVC, AVC is falling / When MC > AVC, AVC is rising" annotations dividing
at the AVC minimum (Q=120). Same chart, two different divisions → confusing.

This version drops both label sets. The chart shows only the curves + crossing
point. The slide's caption + bullet card handles the explanation.

Cost function: VC(Q) = a*Q + b*Q^2 + c*Q^3, with coefficients chosen so AVC
minimum sits at Q=120 (MC=AVC there) and ATC minimum at Q=140 (MC=ATC there).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Cost-function coefficients chosen so AVC_min is at Q=120 and ATC_min is at Q=140
a = 1.20
b = -0.0108
c = 0.000045
FC = 35.0

q = np.linspace(20, 155, 600)
vc  = a*q + b*q**2 + c*q**3
tc  = FC + vc
afc = FC / q
avc = vc / q
atc = tc / q
mc  = a + 2*b*q + 3*c*q**2

# Identify crossing points
avc_min_idx = int(np.argmin(avc))
atc_min_idx = int(np.argmin(atc))
q_avc_min, avc_min = q[avc_min_idx], avc[avc_min_idx]
q_atc_min, atc_min = q[atc_min_idx], atc[atc_min_idx]

# Color palette (matches slide markup)
COLOR_AVC = '#9C6FCC'
COLOR_ATC = '#F08C26'
COLOR_AFC = '#0A5538'
COLOR_MC  = '#C72A2A'
GRID      = '#d8d8d4'

# Nearly-square aspect (5.6 wide × 5.4 tall ≈ 1.04) so 3-up at column width
# ~410px each, figures render ~395px tall — fills the slide's vertical budget
# without spilling past the 1280px horizontal canvas.
FIG_W, FIG_H = 5.6, 5.4
DPI = 160

def common_axis(ax, ymax):
    ax.set_xlim(0, 160)
    ax.set_ylim(0, ymax)
    ax.set_xticks([0, 20, 50, 90, 120, 140, 155])
    ax.set_xlabel('Q', fontsize=12)
    ax.set_ylabel('$ per unit', fontsize=12)
    ax.grid(True, color=GRID, linewidth=0.7, alpha=0.7)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ============ Panel 1: AVC + MC ============
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.plot(q, avc, color=COLOR_AVC, linewidth=3.2, label='AVC')
ax.plot(q, mc,  color=COLOR_MC,  linewidth=3.2, label='MC')
ax.plot(q_avc_min, avc_min, 'o', color='#15803d', markersize=14,
        markeredgecolor='white', markeredgewidth=2.5, zorder=5)
ax.annotate(f'MC = AVC\n(AVC min,  Q = {int(q_avc_min)})',
            xy=(q_avc_min, avc_min), xytext=(q_avc_min - 38, avc_min + 0.75),
            fontsize=11, color='#15803d', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor='#15803d', linewidth=1.4),
            arrowprops=dict(arrowstyle='->', color='#15803d', lw=1.6))
common_axis(ax, ymax=3.6)
ax.legend(loc='upper left', fontsize=12, frameon=True, framealpha=0.95)
plt.tight_layout()
plt.savefig('fig-amc-panel-avc-mc.png', dpi=DPI,
            bbox_inches='tight', facecolor='white')
plt.close()
print(f'saved fig-amc-panel-avc-mc.png  (AVC min @ Q={q_avc_min:.0f}, '
      f'AVC = ${avc_min:.2f})')


# ============ Panel 2: ATC + MC ============
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.plot(q, atc, color=COLOR_ATC, linewidth=3.2, label='ATC')
ax.plot(q, mc,  color=COLOR_MC,  linewidth=3.2, label='MC')
ax.plot(q_atc_min, atc_min, 'o', color='#15803d', markersize=14,
        markeredgecolor='white', markeredgewidth=2.5, zorder=5)
ax.annotate(f'MC = ATC\n(ATC min,  Q = {int(q_atc_min)})',
            xy=(q_atc_min, atc_min), xytext=(q_atc_min - 32, atc_min + 0.80),
            fontsize=11, color='#15803d', fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor='#15803d', linewidth=1.4),
            arrowprops=dict(arrowstyle='->', color='#15803d', lw=1.6))
common_axis(ax, ymax=3.6)
ax.legend(loc='upper left', fontsize=12, frameon=True, framealpha=0.95)
plt.tight_layout()
plt.savefig('fig-amc-panel-atc-mc.png', dpi=DPI,
            bbox_inches='tight', facecolor='white')
plt.close()
print(f'saved fig-amc-panel-atc-mc.png  (ATC min @ Q={q_atc_min:.0f}, '
      f'ATC = ${atc_min:.2f})')


# ============ Panel 3: AFC ============
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
ax.plot(q, afc, color=COLOR_AFC, linewidth=3.2, label='AFC')
ax.annotate('AFC = FC / Q\nFC spread over more units',
            xy=(85, afc[np.argmin(np.abs(q - 85))]),
            xytext=(95, 1.10),
            fontsize=11, color=COLOR_AFC, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                      edgecolor=COLOR_AFC, linewidth=1.4),
            arrowprops=dict(arrowstyle='->', color=COLOR_AFC, lw=1.4))
common_axis(ax, ymax=2.2)
ax.legend(loc='upper right', fontsize=12, frameon=True, framealpha=0.95)
plt.tight_layout()
plt.savefig('fig-amc-panel-afc.png', dpi=DPI,
            bbox_inches='tight', facecolor='white')
plt.close()
print('saved fig-amc-panel-afc.png')
