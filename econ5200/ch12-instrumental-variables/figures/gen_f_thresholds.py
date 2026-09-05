import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _palette import *
import matplotlib.pyplot as plt

setup()
fig, ax = plt.subplots(figsize=(6.5, 4.3))

rows = [("Lee et al. (2022)\nvalid 5% test", 104.7, SAGE),
        ("Card (1995)\n$nearc4$ first stage", 59.07, TERRA),
        ("Staiger & Stock (1997)\nthe rule everyone teaches", 10.0, ROSE)]
ys = [2, 1, 0]
for (label, v, c), y in zip(rows, ys):
    ax.barh(y, v, height=0.52, color=c, alpha=0.85, zorder=2)
    ax.text(v + 2.5, y, f"F = {v:g}", va="center", fontsize=12,
            color=c, weight="bold")
    ax.text(-3, y, label, ha="right", va="center", fontsize=10, color=CHARCOAL)

ax.axvline(104.7, color=SAGE, linewidth=1.4, linestyle="--", zorder=1)
ax.text(59.07 / 2, 1, "clears the rule,\nmisses the requirement", ha="center", va="center",
        fontsize=9, color="white", style="italic", zorder=3)

ax.set_yticks([]); ax.set_ylim(-0.6, 2.75); ax.set_xlim(-3, 128)
ax.set_xlabel("first-stage $F$-statistic")
ax.spines["left"].set_visible(False)
ax.grid(axis="x", color=LINE, linewidth=0.7, alpha=0.7)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "figure_004_f_thresholds.png"), bbox_inches="tight")
print("ok")
