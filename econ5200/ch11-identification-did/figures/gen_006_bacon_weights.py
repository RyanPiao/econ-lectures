import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
names = ["Treated vs\nnever-treated", "Earlier vs\nlater treated",
         "Later vs earlier\n(FORBIDDEN)"]
weight = [0.6119, 0.1455, 0.2425]
effect = [7.6844, 5.0854, -3.0460]
contrib = [4.7024, 0.7400, -0.7388]
cols = [SECONDARY, SECONDARY, DANGER]
fig, axes = plt.subplots(2, 1, figsize=(5.6, 7.4), sharey=True)
y = np.arange(3)[::-1]
axes[0].barh(y, weight, color=cols, height=0.52)
for yi, w in zip(y, weight):
    axes[0].text(w + 0.015, yi, f"{w:.1%}", va="center", color=PRIMARY,
                 fontsize=11, fontweight="bold")
axes[0].set_xlim(0, 0.78); axes[0].set_xlabel("Bacon weight")
axes[0].set_yticks(y); axes[0].set_yticklabels(names, fontsize=10)

axes[1].barh(y, contrib, color=cols, height=0.52)
for yi, c, e in zip(y, contrib, effect):
    axes[1].text(max(c, 0.0) + 0.18, yi, f"{c:+.2f}   (avg effect {e:+.2f})",
                 va="center", ha="left", color=PRIMARY, fontsize=9.5,
                 fontweight="bold")
axes[1].axvline(0, color=PRIMARY, lw=1.2)
axes[1].set_xlim(-1.6, 8.4); axes[1].set_xlabel("contribution to the TWFE estimate")
axes[1].text(8.2, 2.55, "sum = 4.70", color=PRIMARY, fontsize=11,
             fontweight="bold", ha="right")
for a in axes:
    a.grid(axis="x")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_006_bacon_weights.png"), bbox_inches="tight")
