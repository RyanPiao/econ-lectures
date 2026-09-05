import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
style()
fig, ax = plt.subplots(figsize=(6.4, 4.8))
rows = [("Never-treated", 2.30, None), ("Late cohort  (g = 8)", 1.30, 8),
        ("Early cohort  (g = 4)", 0.30, 4)]
for name, y, g in rows:
    ax.add_patch(Rectangle((1, y), 11, 0.55, facecolor="#F4F1ED",
                           edgecolor=LINE, lw=0.8))
    if g is not None:
        ax.add_patch(Rectangle((g, y), 12 - g, 0.55, facecolor=ACCENT,
                               alpha=0.32, edgecolor="none"))
        ax.plot([g, g], [y, y + 0.55], color=ACCENT, lw=2.6)
        ax.text((g + 12) / 2, y + 0.275, "treated", ha="center", va="center",
                color=ACCENT, fontsize=9.5, fontweight="bold")
    ax.text(0.8, y + 0.275, name, ha="right", va="center",
            color=TEXT, fontsize=10)

def bracket(x0, x1, y, label, colour):
    ax.annotate("", xy=(x0, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="<->", color=colour, lw=1.8))
    ax.text((x0 + x1) / 2, y + 0.10, label, ha="center",
            color=colour, fontsize=9.5, fontweight="bold")

bracket(4, 8, 3.30, "3  early vs late, late still untreated  — valid", SECONDARY)
bracket(8, 12, 3.80, "4  late vs already-treated early  — FORBIDDEN", DANGER)
ax.text(1.0, 3.02, "1  early vs never-treated — valid          "
                   "2  late vs never-treated — valid",
        color=SECONDARY, fontsize=9.5, fontweight="bold")

ax.set_xlim(-0.1, 12.8); ax.set_ylim(0.05, 4.25)
ax.set_xticks([1, 4, 8, 12]); ax.set_yticks([])
ax.set_xlabel("period")
ax.spines["left"].set_visible(False)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_004_bacon_timeline.png"), bbox_inches="tight")
