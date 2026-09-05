import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
labels = ["True ATT", "TWFE", "Callaway–Sant'Anna"]
vals = [8.65, 4.70, 8.49]
ses = [None, 0.27, 0.18]
cols = [MUTED, DANGER, SUCCESS]
fig, ax = plt.subplots(figsize=(6.4, 4.4))
bars = ax.bar(labels, vals, color=cols, width=0.5)
ax.errorbar([1, 2], [4.70, 8.49], yerr=[1.96 * 0.27, 1.96 * 0.18], fmt="none",
            ecolor=PRIMARY, elinewidth=1.6, capsize=7)
ax.axhline(8.65, color=MUTED, lw=1.3, ls="--")
ax.text(2.42, 8.9, "truth", color=MUTED, fontsize=9, ha="right")
tops = [8.65, 4.70 + 1.96 * 0.27, 8.49 + 1.96 * 0.18]
for i, (v, top) in enumerate(zip(vals, tops)):
    ax.text(i, top + 0.42, f"{v:.2f}", ha="center", color=PRIMARY,
            fontsize=14, fontweight="bold")
ax.text(1, 2.55, "SE 0.27\ntruth is 14 SEs\nfrom the estimate", ha="center",
        va="center", color="white", fontsize=9.5)
ax.text(2, 2.55, "SE 0.18\ntruth sits inside\nthe interval", ha="center",
        va="center", color="white", fontsize=9.5)
ax.set_ylabel("estimated average effect")
ax.set_ylim(0, 11.4)
ax.grid(axis="y")
ax.set_axisbelow(True)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_005_twfe_vs_truth.png"), bbox_inches="tight")
