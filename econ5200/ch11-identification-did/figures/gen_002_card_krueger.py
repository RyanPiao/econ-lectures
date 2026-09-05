import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
# Card & Krueger (1994) FTE employment, the four cell means the lab reproduces.
nj = [20.44, 21.03]
pa = [23.33, 21.17]
fig, ax = plt.subplots(figsize=(6.4, 4.4))
x = [0, 1]
ax.plot(x, nj, "-o", color=ACCENT, lw=2.6, ms=8, label="New Jersey (raised wage)")
ax.plot(x, pa, "-o", color=SECONDARY, lw=2.6, ms=8, label="Pennsylvania (control)")
for xi, yi, lab in [(0, nj[0], "20.44"), (1, nj[1], "21.03")]:
    ax.annotate(lab, (xi, yi), textcoords="offset points", xytext=(0, 11),
                ha="center", color=ACCENT, fontsize=10, fontweight="bold")
for xi, yi, lab in [(0, pa[0], "23.33"), (1, pa[1], "21.17")]:
    ax.annotate(lab, (xi, yi), textcoords="offset points", xytext=(0, -18),
                ha="center", color=SECONDARY, fontsize=10, fontweight="bold")
ax.text(0.5, 24.4, r"$\Delta$NJ = +0.59       $\Delta$PA = $-$2.16",
        ha="center", color=TEXT, fontsize=10.5)
ax.text(0.5, 23.6, "DiD = (+0.59) $-$ ($-$2.16) = $+$2.75",
        ha="center", color=PRIMARY, fontsize=12.5, fontweight="bold")
ax.set_xlim(-0.28, 1.28); ax.set_ylim(19.2, 25.2)
ax.set_xticks(x); ax.set_xticklabels(["Feb 1992 (before)", "Nov 1992 (after)"])
ax.set_ylabel("mean FTE employment per restaurant")
ax.legend(loc="lower left", fontsize=9.5)
ax.grid(axis="y")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_002_card_krueger.png"), bbox_inches="tight")
