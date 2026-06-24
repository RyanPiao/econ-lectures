"""Average vs marginal revenue figure for Walkthrough 1.3.
R(q)=20q-0.1q^2  ->  AR(q)=20-0.1q,  MR(q)=20-0.2q.
MR hits 0 at q*=100 (total revenue peaks) where AR is still 10. Markers on top."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"ar": "#5B86A8", "mr": "#C47B5A", "text": "#2D2D2D", "muted": "#8C8580"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 12,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#374151", "ytick.color": "#374151",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(6.6, 4.4))
qa = np.array([0, 160]); ax.plot(qa, 20 - 0.1 * qa, color=C["ar"], lw=2.8, zorder=3)
qm = np.array([0, 120]); ax.plot(qm, 20 - 0.2 * qm, color=C["mr"], lw=2.8, zorder=3)
ax.text(150, 20 - 0.1 * 150 + 0.7, "AR", color=C["ar"], fontsize=13, fontweight="bold", ha="center")
ax.text(38, 9.0, "MR", color=C["mr"], fontsize=13, fontweight="bold", ha="center")

# marked points
for q, ar, mr in [(50, 15, 10), (100, 10, 0)]:
    ax.scatter([q], [ar], s=52, color=C["ar"], zorder=6)
    ax.scatter([q], [mr], s=52, color=C["mr"], zorder=6)
    ax.plot([q, q], [0, ar], ls=":", color=C["muted"], lw=1.0, zorder=1)

# revenue-max callout at q*=100 (below AR, clear of the lines)
ax.annotate("MR = 0 here $\\Rightarrow$ revenue peaks", xy=(100, 0), xytext=(104, 3.2),
            fontsize=10.5, color=C["mr"], fontweight="bold", ha="left",
            arrowprops=dict(arrowstyle="->", color=C["mr"], lw=1.2))
ax.annotate("AR still $=10$", xy=(100, 10), xytext=(54, 16.5),
            fontsize=10.5, color=C["ar"], fontweight="bold", ha="left",
            arrowprops=dict(arrowstyle="->", color=C["ar"], lw=1.2))

ax.set_xlim(0, 165)
ax.set_ylim(0, 21)
ax.set_xlabel("Output  q")
ax.set_ylabel("$ per unit")
ax.set_xticks([50, 100]); ax.set_yticks([0])

fig.savefig(os.path.join(OUT, "w13-ar-mr.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "w13-ar-mr.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote w13-ar-mr.png + .svg")
