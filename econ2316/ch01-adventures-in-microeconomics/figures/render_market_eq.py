"""Basic supply-demand market-equilibrium diagram for ECON 2316 Ch 1.
Equilibrium E at (Q*, P*) = (70,000 lbs/day, $1.75/lb). Shaded SURPLUS region
above P* (Q^s > Q^d -> price falls) and SHORTAGE region below P* (Q^d > Q^s ->
price rises). Convention: the E marker is drawn ON TOP of the curves."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"demand": "#6B8BA4", "supply": "#6A8E6B", "surplus": "#C47B5A",
     "shortage": "#A85C5C", "text": "#2D2D2D", "muted": "#8C8580"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 12,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

# linear curves crossing at (Q*, P*) = (70000, 1.75)
def Qd(P): return 40000 * (3.5 - P)        # P=0 -> 140k ; P=3.5 -> 0
def Qs(P): return 20000 + 28571.4 * P      # P=0 -> 20k  ; P=1.75 -> 70k
Pstar, Qstar = 1.75, 70000

fig, ax = plt.subplots(figsize=(6.6, 4.6))

# shaded regions ------------------------------------------------------------
Pup = np.linspace(Pstar, 3.05, 60)
ax.fill_betweenx(Pup, Qd(Pup), Qs(Pup), color=C["surplus"], alpha=0.16, zorder=0)
Plo = np.linspace(0.55, Pstar, 60)
ax.fill_betweenx(Plo, Qs(Plo), Qd(Plo), color=C["shortage"], alpha=0.15, zorder=0)

# curves --------------------------------------------------------------------
Pline = np.array([0.55, 3.3])
ax.plot(Qd(Pline), Pline, color=C["demand"], lw=2.8, zorder=3)
ax.plot(Qs(Pline), Pline, color=C["supply"], lw=2.8, zorder=3)
ax.text(Qd(0.55) + 2500, 0.55, "D", color=C["demand"], fontsize=15, fontweight="bold", va="center")
ax.text(Qs(3.3) + 2000, 3.3, "S", color=C["supply"], fontsize=15, fontweight="bold", va="center")

# equilibrium dashed guides + point (marker on top) -------------------------
ax.plot([0, Qstar], [Pstar, Pstar], ls="--", color=C["muted"], lw=1.2, zorder=1)
ax.plot([Qstar, Qstar], [0, Pstar], ls="--", color=C["muted"], lw=1.2, zorder=1)
ax.scatter([Qstar], [Pstar], s=95, color=C["text"], zorder=6)
ax.text(Qstar + 3500, Pstar + 0.12, "E", color=C["text"], fontsize=14, fontweight="bold")
ax.text(-3000, Pstar, "$P^{*}$", color=C["text"], fontsize=14, fontweight="bold", ha="right", va="center")
ax.text(Qstar, -0.22, "$Q^{*}$", color=C["text"], fontsize=14, fontweight="bold", ha="center")

# region captions — centered inside each wedge -------------------------------
ax.text(67000, 2.52, "SURPLUS", color=C["surplus"], fontsize=14, fontweight="bold", ha="center")
ax.text(67000, 2.28, "$Q^{s}>Q^{d}\\ \\Rightarrow$ price falls", color=C["surplus"], fontsize=10.5, ha="center", fontstyle="italic")
ax.text(74000, 1.00, "SHORTAGE", color=C["shortage"], fontsize=14, fontweight="bold", ha="center")
ax.text(74000, 0.76, "$Q^{d}>Q^{s}\\ \\Rightarrow$ price rises", color=C["shortage"], fontsize=10.5, ha="center", fontstyle="italic")

# axis labels at top / far-right so they clear the P*/Q* labels
ax.text(2500, 3.42, "Price ($/lb)", fontsize=12, fontweight="bold", color="#374151", ha="left", va="center")
ax.text(150000, 0.13, "Quantity (lbs/day)", fontsize=12, fontweight="bold", color="#374151", ha="right", va="center")

ax.set_xlim(0, 152000)
ax.set_ylim(0, 3.5)
ax.set_xticks([]); ax.set_yticks([])

fig.savefig(os.path.join(OUT, "market-equilibrium.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "market-equilibrium.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote market-equilibrium.png + .svg")
