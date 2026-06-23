"""Original surge-pricing tradeoff diagram for ECON 2316 Ch 1.
A demand surge shifts demand D0 -> D1. Letting the price rise to the new
equilibrium E1 clears the market (short wait) at a higher fare; capping the
fare at the old normal level (E0's price) leaves quantity demanded far above
quantity supplied -> a shortage (long waits, no cars).
Convention: point markers drawn ON TOP of the curves."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"d1": "#3b6f99", "d0": "#9DB9CC", "supply": "#6A8E6B", "surge": "#C47B5A",
     "cap": "#A85C5C", "muted": "#8C8580", "text": "#2D2D2D"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

def S(Q):  return 4 + Q          # drivers' supply
def D0(Q): return 16 - Q         # normal demand
def D1(Q): return 24 - Q         # surge demand (shifted right)
E0 = (6, 10)                     # normal equilibrium  -> normal fare = 10
E1 = (10, 14)                    # surge equilibrium
Pcap = 10                        # capped at the normal fare
Qd_cap = 14                      # demand on D1 at the cap

fig, ax = plt.subplots(figsize=(7.0, 4.7))

Q = np.array([0, 20])
ax.plot(Q, S(Q), color=C["supply"], lw=2.7, zorder=3)
ax.plot(np.array([0, 16]), D0(np.array([0, 16])), color=C["d0"], lw=2.3, ls="--", zorder=2)
ax.plot(Q, D1(Q), color=C["d1"], lw=2.7, zorder=3)
ax.text(19.6, S(19.6), "S", color=C["supply"], fontsize=14, fontweight="bold", va="center")
ax.text(15.2, 1.1, "$D_0$", color=C["d0"], fontsize=13, fontweight="bold")
ax.text(19.4, D1(19.4) - 0.6, "$D_1$ (surge)", color=C["d1"], fontsize=12.5, fontweight="bold", va="top")

# normal equilibrium + surge equilibrium (markers on top)
ax.scatter([E0[0]], [E0[1]], s=55, color=C["muted"], zorder=6)
ax.plot([0, E1[0]], [E1[1], E1[1]], ls=":", color=C["surge"], lw=1.2, zorder=1)
ax.scatter([E1[0]], [E1[1]], s=95, color=C["surge"], zorder=6)
ax.annotate("surge price clears the\nmarket (short wait)", xy=E1, xytext=(5.6, 20.5),
            fontsize=10.5, color=C["surge"], fontweight="bold", ha="left",
            arrowprops=dict(arrowstyle="->", color=C["surge"], lw=1.3))

# capped fare -> shortage
ax.axhline(Pcap, color=C["cap"], lw=2, ls="--", zorder=2)
ax.text(0.3, Pcap + 0.6, "normal fare", color=C["cap"], fontsize=10, fontweight="bold")
ax.scatter([Qd_cap], [Pcap], s=46, color=C["cap"], zorder=6)
ax.annotate("", xy=(Qd_cap, Pcap), xytext=(E0[0], Pcap),
            arrowprops=dict(arrowstyle="<->", color=C["cap"], lw=1.6))
ax.text(13.0, Pcap - 2.5, "SHORTAGE\nlong waits, no cars",
        color=C["cap"], fontsize=10.5, fontweight="bold", ha="center", linespacing=1.15)

ax.set_xlim(0, 21)
ax.set_ylim(0, 26)
ax.set_xlabel("Rides per hour")
ax.set_ylabel("Price per ride ($)")
ax.set_xticks([]); ax.set_yticks([])

fig.savefig(os.path.join(OUT, "surge-tradeoff.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "surge-tradeoff.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote surge-tradeoff.png + .svg")
