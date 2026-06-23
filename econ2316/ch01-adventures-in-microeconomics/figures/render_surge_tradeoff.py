"""Original surge-pricing tradeoff diagram for ECON 2316 Ch 1.
During a demand surge: letting the price rise to the equilibrium clears the
market (short wait) but at a higher fare; capping the fare at the normal level
leaves quantity demanded above quantity supplied -> a shortage (long waits, no
cars). Efficiency vs fairness; the market clears either way only at the surge price.
Convention: point markers drawn ON TOP of the curves."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"demand": "#6B8BA4", "supply": "#6A8E6B", "surge": "#C47B5A",
     "cap": "#A85C5C", "muted": "#8C8580", "text": "#2D2D2D"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#6b7280", "ytick.color": "#6b7280",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

def D(Q): return 30 - Q          # surge-level demand
def S(Q): return 6 + 0.5 * Q     # drivers' supply
Qstar, Pstar = 16, 14            # surge equilibrium
Pcap = 8                         # normal fare (no surge)
Qs_cap, Qd_cap = 4, 22           # supply & demand at the capped fare

fig, ax = plt.subplots(figsize=(6.8, 4.5))

Q = np.array([0, 24])
ax.plot(Q, D(Q), color=C["demand"], lw=2.7, zorder=3)
ax.plot(Q, S(Q), color=C["supply"], lw=2.7, zorder=3)
ax.text(24.4, D(24), "D", color=C["demand"], fontsize=14, fontweight="bold", va="center")
ax.text(24.4, S(24), "S", color=C["supply"], fontsize=14, fontweight="bold", va="center")

# surge equilibrium (clears)
ax.plot([0, Qstar], [Pstar, Pstar], ls=":", color=C["surge"], lw=1.2, zorder=1)
ax.scatter([Qstar], [Pstar], s=90, color=C["surge"], zorder=6)
ax.annotate("surge price clears\nthe market (short wait)", xy=(Qstar, Pstar),
            xytext=(17.5, 22), fontsize=10.5, color=C["surge"], fontweight="bold",
            ha="left", arrowprops=dict(arrowstyle="->", color=C["surge"], lw=1.3))

# capped fare -> shortage
ax.axhline(Pcap, color=C["cap"], lw=2, ls="--", zorder=2)
ax.text(0.3, Pcap + 0.7, "normal fare (no surge)", color=C["cap"], fontsize=10, fontweight="bold")
ax.scatter([Qs_cap, Qd_cap], [Pcap, Pcap], s=46, color=C["cap"], zorder=6)
ax.annotate("", xy=(Qd_cap, Pcap), xytext=(Qs_cap, Pcap),
            arrowprops=dict(arrowstyle="<->", color=C["cap"], lw=1.6))
ax.text((Qs_cap + Qd_cap) / 2, Pcap - 2.6, "SHORTAGE\nlong waits, no cars",
        color=C["cap"], fontsize=10.5, fontweight="bold", ha="center", linespacing=1.15)

ax.set_xlim(0, 27)
ax.set_ylim(0, 31)
ax.set_xlabel("Rides per hour")
ax.set_ylabel("Price per ride ($)")
ax.set_xticks([]); ax.set_yticks([])

fig.savefig(os.path.join(OUT, "surge-tradeoff.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "surge-tradeoff.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote surge-tradeoff.png + .svg")
