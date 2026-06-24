"""Marginal benefit vs marginal cost 'snooze button' figure for ECON 2316 Ch 1.
MB of one more hour of sleep falls; MC of skipping one more class rises; the
optimal stopping point is where they cross. Curve descriptions live in the slide
text, so the figure carries only clean one-line labels."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"mb": "#5B86A8", "mc": "#B5704A", "text": "#2D2D2D", "muted": "#8C8580"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 12,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

x = np.linspace(0, 9.5, 300)
MB = 9.5 * np.exp(-0.30 * x)
MC = 0.9 * np.exp(0.27 * x)

xc = np.log(9.5 / 0.9) / (0.30 + 0.27)
yc = 9.5 * np.exp(-0.30 * xc)

fig, ax = plt.subplots(figsize=(6.6, 4.2))
ax.plot(x, MB, color=C["mb"], lw=3.0, zorder=3)
ax.plot(x, MC, color=C["mc"], lw=3.0, zorder=3)

# optimal-decision dropline
ax.plot([xc, xc], [0, yc], ls=":", color=C["mc"], lw=1.4, zorder=1)
ax.text(xc + 0.15, 0.5, "Optimal Decision", color=C["mc"], fontsize=11, fontweight="bold")

# clean one-line curve labels (clear of the curves)
ax.text(1.2, 9.1, "Marginal Benefit", color=C["mb"], fontsize=13, fontweight="bold", ha="left")
ax.text(8.5, 9.1, "Marginal Cost", color=C["mc"], fontsize=13, fontweight="bold", ha="right")

ax.set_xlim(0, 9.5)
ax.set_ylim(0, 10)
ax.set_xlabel("Mornings slept in")
ax.set_ylabel("Benefit / Cost")
ax.set_xticks([]); ax.set_yticks([])

fig.savefig(os.path.join(OUT, "snooze-mb-mc.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "snooze-mb-mc.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote snooze-mb-mc.png + .svg")
