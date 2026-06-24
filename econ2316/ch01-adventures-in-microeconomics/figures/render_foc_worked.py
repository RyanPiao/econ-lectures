"""FOC figure using Calculus Corner 1.1's worked example: profit pi(q)=10q-0.5q^2.
Peak at q*=10, pi=$50 with a flat tangent (FOC); tangents left (slope>0) and
right (slope<0). Markers drawn ON TOP of the curve."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"curve": "#5B86A8", "tan": "#C47B5A", "peak": "#2D2D2D", "muted": "#8C8580"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 12,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#374151", "ytick.color": "#374151",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

def pi(q):  return 10 * q - 0.5 * q**2
def dpi(q): return 10 - q

q = np.linspace(0, 20, 300)
fig, ax = plt.subplots(figsize=(6.6, 4.5))
ax.plot(q, pi(q), color=C["curve"], lw=3.0, zorder=3)

def tan(q0, half, color, label, lx, ly):
    m, y0 = dpi(q0), pi(q0)
    xs = np.array([q0 - half, q0 + half])
    ax.plot(xs, y0 + m * (xs - q0), color=color, lw=2.2, zorder=4)
    ax.text(lx, ly, label, color=color, fontsize=10.5, fontweight="bold", ha="center")

# flat tangent at the peak (FOC)
tan(10, 4.0, C["tan"], "", 0, 0)
ax.scatter([10], [50], s=95, color=C["peak"], zorder=6)
ax.text(10, 54.5, r"$\pi'(q^{*})=0$  (max)", color=C["tan"], fontsize=12, fontweight="bold", ha="center")
# left / right tangents
tan(5, 2.0, C["muted"], "slope $>0$", 3.0, 47)
tan(15, 2.0, C["muted"], "slope $<0$", 17.0, 47)

# droplines + axis values
ax.plot([10, 10], [0, 50], ls=":", color=C["muted"], lw=1.2, zorder=1)
ax.plot([0, 10], [50, 50], ls=":", color=C["muted"], lw=1.2, zorder=1)
ax.text(10.7, 3.0, r"$q^{*}=10$", color=C["peak"], fontsize=12, fontweight="bold", ha="left")
ax.text(-0.4, 50, r"$\pi=\$50$", color=C["peak"], fontsize=11.5, fontweight="bold", ha="right", va="center")

ax.set_xlim(0, 20.5)
ax.set_ylim(0, 58)
ax.set_xlabel(r"Output  $q$")
ax.set_ylabel(r"Profit  $\pi(q)$,  \$")
ax.set_xticks([]); ax.set_yticks([])

fig.savefig(os.path.join(OUT, "foc-worked-example.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "foc-worked-example.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote foc-worked-example.png + .svg")
