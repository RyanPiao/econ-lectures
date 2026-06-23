"""Original 'requests vs completed rides' figure for the surge case-study slide.
Illustrative (schematic) bars, NOT a reproduction of the Economist chart:
with surge off the fare is stuck and most requests go unfilled (a shortage);
with surge on the market clears and nearly all requests are completed."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.dirname(os.path.abspath(__file__))
C = {"req": "#CBC5BC", "off": "#A85C5C", "on": "#6A8E6B", "muted": "#8C8580", "text": "#2D2D2D"}

plt.rcParams.update({
    "font.family": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 11,
    "axes.edgecolor": "#6b7280", "axes.labelcolor": "#374151",
    "xtick.color": "#374151", "ytick.color": "#6b7280",
    "axes.grid": False, "axes.spines.top": False, "axes.spines.right": False,
})

fig, ax = plt.subplots(figsize=(6.4, 4.4))
w = 0.34
# group 1: surge OFF ; group 2: surge ON
ax.bar(0 - w/2, 100, w, color=C["req"], zorder=2)
ax.bar(0 + w/2, 25, w, color=C["off"], zorder=2)
ax.bar(1 - w/2, 100, w, color=C["req"], zorder=2)
ax.bar(1 + w/2, 96, w, color=C["on"], zorder=2)

# "unfilled" gap bracket on the surge-OFF scenario (offset right of the bar)
bx = 0 + w/2 + 0.30
ax.annotate("", xy=(bx, 100), xytext=(bx, 25),
            arrowprops=dict(arrowstyle="<->", color=C["off"], lw=1.5))
ax.text(bx + 0.06, 62, "unfilled\n(shortage)", color=C["off"], fontsize=10,
        fontweight="bold", va="center", linespacing=1.1)

# bar value labels
ax.text(0 - w/2, 102, "requested", ha="center", fontsize=9.5, color=C["muted"])
ax.text(1 - w/2, 102, "requested", ha="center", fontsize=9.5, color=C["muted"])
ax.text(0 + w/2, 22, "few\ncompleted", ha="center", va="top", fontsize=9.5, color="white", fontweight="bold", linespacing=1.05)
ax.text(1 + w/2, 92, "nearly all\ncompleted", ha="center", va="top", fontsize=9.5, color="white", fontweight="bold", linespacing=1.05)

ax.set_xticks([0, 1])
ax.set_xticklabels(["Surge OFF\n(NYE 2014)", "Surge ON\n(concert)"], fontsize=11.5, fontweight="bold")
ax.set_ylim(0, 115)
ax.set_yticks([])
ax.set_ylabel("Ride requests vs. completed")
ax.set_title("Does the market clear?  (illustrative)", fontsize=12, color=C["text"], pad=8)

fig.savefig(os.path.join(OUT, "surge-completion.png"), dpi=200, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "surge-completion.svg"), bbox_inches="tight")
plt.close(fig)
print("wrote surge-completion.png + .svg")
