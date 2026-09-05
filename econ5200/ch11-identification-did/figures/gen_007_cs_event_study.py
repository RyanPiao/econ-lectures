import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
e = np.arange(-6, 9)
att = np.array([0.10, 0.28, -0.23, -0.19, -0.00, 0.16,
                1.94, 3.77, 5.86, 7.68, 9.75, 11.94, 13.97, 15.90, 17.91])
se = np.array([0.20, 0.21, 0.19, 0.18, 0.13, 0.15,
               0.16, 0.15, 0.15, 0.13, 0.16, 0.20, 0.21, 0.19, 0.21])
truth = np.where(e >= 0, 2.0 * (e + 1), 0.0)
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.plot(e, truth, color=MUTED, lw=2.0, ls="--", label="true effect path")
pre = e < 0
ax.errorbar(e[pre], att[pre], yerr=1.96 * se[pre], fmt="o", color=SECONDARY,
            ecolor=SECONDARY, elinewidth=1.6, capsize=3.5, ms=6,
            label="Callaway–Sant'Anna, pre")
ax.errorbar(e[~pre], att[~pre], yerr=1.96 * se[~pre], fmt="o", color=SUCCESS,
            ecolor=SUCCESS, elinewidth=1.6, capsize=3.5, ms=6,
            label="Callaway–Sant'Anna, post")
ax.axhline(0, color=LINE, lw=1.2)
ax.axvline(-0.5, color=PRIMARY, lw=1.2, ls="--")
ax.annotate("e = 0:  1.94", xy=(0, 1.94), xytext=(0.5, -2.6),
            color=PRIMARY, fontsize=9.5,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.annotate("e = 8:  17.91", xy=(8, 17.91), xytext=(4.4, 18.6),
            color=PRIMARY, fontsize=9.5,
            arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.1))
ax.set_xlabel("event time $e = t - g$")
ax.set_ylabel("ATT at event time $e$")
ax.set_xticks(e[::2])
ax.set_ylim(-4.2, 21.5)
ax.legend(loc="upper left", fontsize=9)
ax.grid(axis="y")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_007_cs_event_study.png"), bbox_inches="tight")
