"""Linear-case figure for the derivative intro: weight lost = constant rate x
hours, a straight line with a constant slope (rise/run = 0.5 lb per hour)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"line": "#5B86A8", "stair": "#A85C5C", "text": "#2D2D2D", "muted": "#8C8580"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 12,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(6.4, 4.2))
ax.plot([0, 8], [0, 4], color=C["line"], lw=3.0, zorder=3)

# two points + rise/run stair
ax.scatter([2, 6], [1, 3], s=55, color=C["text"], zorder=6)
ax.plot([2, 6], [1, 1], color=C["stair"], lw=2.0, zorder=4)   # run
ax.plot([6, 6], [1, 3], color=C["stair"], lw=2.0, zorder=4)   # rise
ax.text(4, 0.62, r"run $=\Delta x = 4$", color=C["stair"], fontsize=10.5, ha="center", fontweight="bold")
ax.text(6.2, 2.0, r"rise $=\Delta y = 2$", color=C["stair"], fontsize=10.5, ha="left", va="center", fontweight="bold")

ax.text(0.4, 3.7, r"slope $= \dfrac{\mathrm{rise}}{\mathrm{run}} = \dfrac{2}{4} = 0.5$ lb/hr",
        color=C["line"], fontsize=12, fontweight="bold")

ax.set_xlim(0, 8)
ax.set_ylim(0, 4.4)
ax.set_xlabel("Hours spent working out (x)")
ax.set_ylabel("Weight lost, lbs (y)")
ax.set_xticks([]); ax.set_yticks([])

fig.savefig(os.path.join(OUT, "linear-intro.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "linear-intro.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote linear-intro.png + .svg")
