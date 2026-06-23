"""Marginal-value step chart for Walkthrough 1.1 (Maya's time budget).
Study's marginal value falls in blocks ($30/$20/$15/$0) against a flat $18 wage;
she studies while MV > wage and works after. Crossover (the optimum) at S* = 20.
Convention: markers/points drawn ON TOP of lines (high zorder)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"mv": "#3b82f6", "wage": "#f97316", "study": "#6A8E6B", "work": "#6B8BA4",
     "muted": "#9ca3af", "text": "#374151"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(6.2, 4.1))

# region shading: study (MV>wage) vs work (wage>MV)
ax.axvspan(0, 20, color=C["study"], alpha=0.09, zorder=0)
ax.axvspan(20, 40, color=C["work"], alpha=0.09, zorder=0)

# marginal value of study — descending step function
xs = [0, 10, 20, 30, 40]
ys = [30, 20, 15, 0, 0]
ax.step(xs, ys, where="post", color=C["mv"], lw=2.8, zorder=3,
        label="Marginal value of study")

# flat wage line
ax.axhline(18, color=C["wage"], lw=2.2, ls="--", zorder=2)
ax.text(39.5, 18, "wage = $18/hr", color=C["wage"], fontsize=10.5,
        fontweight="bold", va="center", ha="right",
        bbox=dict(facecolor="white", edgecolor="none", pad=1.5))

# block value labels above each step
for x0, v in [(5, 30), (15, 20), (25, 15)]:
    ax.text(x0, v + 1.4, f"${v}", ha="center", color=C["mv"], fontsize=11, fontweight="bold")

# crossover / optimum marker ON TOP
ax.axvline(20, color=C["muted"], lw=1.3, ls=":", zorder=1)
ax.scatter([20], [18], s=80, color=C["text"], zorder=6)
ax.annotate("switch here\n$S^{*}=20$", xy=(20, 18), xytext=(24.5, 25),
            fontsize=10.5, color=C["text"], ha="left",
            arrowprops=dict(arrowstyle="->", color=C["text"], lw=1.2))

# region captions
ax.text(10, 4.5, "STUDY\nMV > wage", ha="center", color=C["study"],
        fontsize=10.5, fontweight="bold", linespacing=1.2)
ax.text(30, 9.0, "WORK\nwage > MV", ha="center", color=C["work"],
        fontsize=10.5, fontweight="bold", linespacing=1.2)

ax.set_xlim(0, 40)
ax.set_ylim(0, 34)
ax.set_xlabel("Hours of study  (then work fills the rest of 97)")
ax.set_ylabel("$ per hour")
ax.set_xticks([0, 10, 20, 30, 40])
ax.set_yticks([0, 15, 18, 30])

fig.savefig(os.path.join(OUT, "maya-marginal-value.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "maya-marginal-value.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote maya-marginal-value.png + .svg")
