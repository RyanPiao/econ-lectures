import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
HERE = os.path.abspath(".")
PRIMARY="#2D2D2D"; SECONDARY="#6B8BA4"; TEXT="#3A3632"
MUTED="#8C8580"; LINE="#D5CEC7"; DANGER="#A85C5C"; SUCCESS="#6A8E6B"
plt.rcParams.update({
    "font.size": 11, "axes.facecolor": "white", "figure.facecolor": "white",
    "axes.edgecolor": PRIMARY, "axes.labelcolor": TEXT, "axes.linewidth": 1.0,
    "xtick.color": TEXT, "ytick.color": TEXT, "legend.frameon": False,
    "savefig.facecolor": "white", "savefig.bbox": "tight", "savefig.dpi": 150,
})

labels = ["IPO price\n(Jun 11)", "Opened\n(Jun 12)", "Day-1 close\n(Jun 12)", "Latest\n(Jul 21)"]
vals   = [135.00, 150.00, 160.95, 123.54]
cols   = [SECONDARY, SUCCESS, SUCCESS, DANGER]

fig, ax = plt.subplots(figsize=(7.4, 4.6))
ax.bar(range(4), vals, color=cols, width=0.56, zorder=3)
for i, v in enumerate(vals):
    ax.text(i, v + 3.5, r"\$%.2f" % v, ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=PRIMARY, zorder=5)

ax.axhline(135, color=SECONDARY, ls="--", lw=1.4, zorder=2)
# (no dashed-line label: bar 1 is already labelled "IPO price", and the
# dashed reference line visibly extends from its top)

ax.text(3.0, 186, "below its\nIPO price", ha="center", va="top",
        fontsize=10, color=DANGER, fontweight="bold", linespacing=1.3, zorder=6)
ax.annotate("", xy=(3.0, 132), xytext=(3.0, 168),
            arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.8), zorder=6)

ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=10)
ax.set_xlim(-0.62, 3.62)
ax.set_ylim(0, 200)
ax.set_yticks([0, 50, 100, 150])
ax.set_yticklabels([r"\$0", r"\$50", r"\$100", r"\$150"], fontsize=10)
ax.set_ylabel("Share price (USD)", fontsize=10.5, fontstyle="italic")
ax.set_title("SPCX  ·  SpaceX on the Nasdaq, 2026", fontsize=13.5,
             fontweight="bold", color=PRIMARY, pad=27)
ax.text(0.5, 1.05, r"Raised \$75B  ·  ~\$2.1T market cap at the open  ·  the largest IPO ever",
        transform=ax.transAxes, ha="center", va="bottom", fontsize=10, color=MUTED)
ax.text(0.0, -0.245, "Verified marks only, not daily closes.   Sources: Forbes (Jun 12, 2026); quoted close Jul 21, 2026.",
        transform=ax.transAxes, ha="left", va="top", fontsize=8.5, color=MUTED, fontstyle="italic")
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", color=LINE, lw=0.6, zorder=0)
ax.set_axisbelow(True)
plt.savefig(os.path.join(HERE, "fig-spacex-ipo-price.png"))
plt.close(fig)
print("ok")
