import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _palette import *
import matplotlib.pyplot as plt

setup()
fig, ax = plt.subplots(figsize=(6.5, 4.6))

pis   = ["1.00", "0.50", "0.05", "0.01"]
tsls  = [1.029, 1.058, 1.583, 3.949]
x = list(range(len(pis)))

ax.axhline(1.0, color=SAGE, linewidth=1.8, linestyle="--", zorder=1)
ax.axhline(2.018, color=TERRA, linewidth=1.8, linestyle="--", zorder=1)
ax.text(3.42, 1.0, "truth\n$\\beta = 1.0$", ha="left", va="center", fontsize=9.5, color=SAGE)
ax.text(3.42, 2.018, "OLS\n2.018", ha="left", va="center", fontsize=9.5, color=TERRA)

ax.plot(x, tsls, color=BLUE, linewidth=2.2, zorder=2)
lbl = [(0.0, 0.22, "center"), (0.0, 0.22, "center"),
       (-0.14, 0.20, "right"), (-0.16, 0.16, "right")]
for xi, v, (dx, dy, ha) in zip(x, tsls, lbl):
    c = ROSE if v > 2.018 else BLUE
    ax.plot([xi], [v], "o", color=c, markersize=11, markeredgecolor="white",
            markeredgewidth=1.6, zorder=3)
    ax.text(xi + dx, v + dy, f"{v:.3f}", ha=ha, fontsize=11, color=c, weight="bold")

ax.annotate("worse than the OLS\nit was hired to fix",
            xy=(2.93, 3.90), xytext=(1.35, 3.30), fontsize=10.5, color=ROSE,
            ha="center", va="center",
            arrowprops=dict(arrowstyle="-|>", color=ROSE, linewidth=1.4,
                            shrinkA=6, shrinkB=8, connectionstyle="arc3,rad=-0.2"))

ax.set_xticks(x); ax.set_xticklabels(pis)
ax.set_xlim(-0.45, 4.35); ax.set_ylim(0.35, 4.55)
ax.set_xlabel("first-stage strength  $\\pi$   (strong $\\rightarrow$ weak)")
ax.set_ylabel("2SLS estimate of $\\beta$")
ax.grid(axis="y", color=LINE, linewidth=0.7, alpha=0.7)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "figure_003_weak_instrument.png"), bbox_inches="tight")
print("ok")
