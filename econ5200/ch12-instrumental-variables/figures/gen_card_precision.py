import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _palette import *
import matplotlib.pyplot as plt

setup()
fig, ax = plt.subplots(figsize=(6.4, 4.4))

est = [("OLS", 0.0932, 0.0037, BLUE), ("2SLS (IV)", 0.2587, 0.0337, TERRA)]
ys = [1.0, 0.4]
for (name, b, se, c), y in zip(est, ys):
    lo, hi = b - 1.96 * se, b + 1.96 * se
    ax.plot([lo, hi], [y, y], color=c, linewidth=3.0, solid_capstyle="round", zorder=2)
    for e in (lo, hi):
        ax.plot([e, e], [y - 0.055, y + 0.055], color=c, linewidth=2.0, zorder=2)
    ax.plot([b], [y], "o", color=c, markersize=11, markeredgecolor="white",
            markeredgewidth=1.6, zorder=3)
    ax.text(b, y + 0.115, f"{b:.4f}", ha="center", fontsize=11.5, color=c, weight="bold")
    ax.text(-0.012, y, name, ha="right", va="center", fontsize=11.5, color=CHARCOAL)
    ax.text(hi + 0.008, y, f"SE {se:.4f}", ha="left", va="center", fontsize=9.5, color=MUTED)

ax.annotate("", xy=(0.2587, 0.20), xytext=(0.0932, 0.20),
            arrowprops=dict(arrowstyle="<|-|>", color=MUTED, linewidth=1.3))
ax.text(0.176, 0.135, "2.78$\\times$ larger — and in the wrong direction\nif ability biased OLS upward",
        ha="center", va="top", fontsize=9.5, color=MUTED, style="italic")

ax.set_xlim(-0.012, 0.40); ax.set_ylim(0.0, 1.28)
ax.set_yticks([])
ax.set_xlabel("return to one year of schooling (log points), 95% CI")
ax.spines["left"].set_visible(False)
ax.grid(axis="x", color=LINE, linewidth=0.7, alpha=0.7)
ax.set_axisbelow(True)
fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "figure_002_card_precision.png"), bbox_inches="tight")
print("ok")
