"""Derivative-intro figure for ECON 2316 Ch 1: weight lost vs hours worked out
is nonlinear, so the slope (the derivative) changes along the curve -- steep
early (losing fast), flat later (plateau). Two tangents make the point."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"curve": "#5B86A8", "tan": "#C47B5A", "text": "#2D2D2D", "muted": "#8C8580"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 12,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

def f(x):  return 4 * (1 - np.exp(-0.35 * x))
def fp(x): return 1.4 * np.exp(-0.35 * x)

x = np.linspace(0, 8, 300)
fig, ax = plt.subplots(figsize=(6.6, 4.3))
ax.plot(x, f(x), color=C["curve"], lw=3.0, zorder=3)

def tangent(x0, half, label, lx, ly):
    m, y0 = fp(x0), f(x0)
    xs = np.array([x0 - half, x0 + half])
    ax.plot(xs, y0 + m * (xs - x0), color=C["tan"], lw=2.2, zorder=4)
    ax.scatter([x0], [y0], s=55, color=C["tan"], zorder=6)
    ax.text(lx, ly, label, color=C["tan"], fontsize=11, fontweight="bold", ha="center", linespacing=1.1)

tangent(1.0, 1.5, "slope ≈ 1\n(losing fast)", 1.0, 3.0)
tangent(7.0, 1.5, "slope ≈ 0\n(plateau)", 6.2, 2.2)

ax.set_xlim(0, 8.2)
ax.set_ylim(0, 4.4)
ax.set_xlabel("Hours spent working out (x)")
ax.set_ylabel("Weight lost, lbs (y)")
ax.set_xticks([]); ax.set_yticks([])

fig.savefig(os.path.join(OUT, "derivative-intro.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "derivative-intro.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote derivative-intro.png + .svg")
