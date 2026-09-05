import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _palette import *
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle

setup()
fig, ax = plt.subplots(figsize=(6.6, 4.7))
ax.set_xlim(0, 11.6); ax.set_ylim(0, 7.6); ax.axis("off")

nodes = {"Z": (1.5, 4.3, BLUE), "D": (5.1, 4.3, CHARCOAL),
         "Y": (8.7, 4.3, CHARCOAL), "U": (6.9, 6.8, ROSE)}
labels = {"Z": "$Z$", "D": "$D$", "Y": "$Y$", "U": "$U$"}

for k, (x, y, c) in nodes.items():
    dashed = (k == "U")
    ax.add_patch(Circle((x, y), 0.60, facecolor="white", edgecolor=c,
                        linewidth=2.0, linestyle="--" if dashed else "-", zorder=3))
    ax.text(x, y, labels[k], ha="center", va="center", fontsize=17, color=c, zorder=4)

ax.text(1.5, 5.30, "instrument", ha="center", va="bottom", fontsize=9.5, color=MUTED)
ax.text(4.45, 5.30, "treatment", ha="center", va="bottom", fontsize=9.5, color=MUTED)
ax.text(9.45, 4.30, "outcome", ha="left", va="center", fontsize=9.5, color=MUTED)
ax.text(6.15, 6.95, "unobserved confounder", ha="right", va="center", fontsize=9.5, color=ROSE)
ax.text(6.15, 6.45, "no arrow into $Z$", ha="right", va="center", fontsize=9, color=MUTED,
        style="italic")

def arrow(a, b, color, style="-", lw=2.0):
    x1, y1, _ = nodes[a]; x2, y2, _ = nodes[b]
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
        mutation_scale=17, linewidth=lw, color=color, linestyle=style,
        shrinkA=23, shrinkB=23, zorder=2))

arrow("Z", "D", BLUE)
arrow("D", "Y", CHARCOAL)
arrow("U", "D", ROSE, style="--", lw=1.7)
arrow("U", "Y", ROSE, style="--", lw=1.7)

ax.text(3.30, 4.62, "relevance:  $\\pi \\neq 0$", ha="center", va="bottom",
        fontsize=9.5, color=BLUE)

# The forbidden arrow, routed well below the node row
ax.add_patch(FancyArrowPatch((1.5, 4.3), (8.7, 4.3), connectionstyle="arc3,rad=0.55",
    arrowstyle="-|>", mutation_scale=15, linewidth=1.8, color=TERRA,
    linestyle=(0, (5, 4)), shrinkA=22, shrinkB=22, zorder=2))
cx, cy = 5.1, 2.32
ax.plot([cx - 0.42, cx + 0.42], [cy - 0.42, cy + 0.42], color=TERRA, lw=3.4, zorder=5)
ax.plot([cx - 0.42, cx + 0.42], [cy + 0.42, cy - 0.42], color=TERRA, lw=3.4, zorder=5)
ax.add_patch(Circle((cx, cy), 0.70, facecolor="white", edgecolor="none", zorder=4))
ax.plot([cx - 0.42, cx + 0.42], [cy - 0.42, cy + 0.42], color=TERRA, lw=3.4, zorder=5)
ax.plot([cx - 0.42, cx + 0.42], [cy + 0.42, cy - 0.42], color=TERRA, lw=3.4, zorder=5)

ax.text(5.1, 0.75, "the arrow that is not there  =  the exclusion restriction",
        ha="center", va="center", fontsize=11, color=TERRA, style="italic")

fig.tight_layout()
fig.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "figure_001_iv_dag.png"), bbox_inches="tight")
print("ok")
