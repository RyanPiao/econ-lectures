import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
e = np.array([-4, -3, -2, -1, 0, 1, 2, 3])
att = np.array([-0.35, 0.28, -0.18, 0.0, 0.95, 1.42, 1.71, 1.88])
se = np.array([0.62, 0.58, 0.55, 0.0, 0.42, 0.44, 0.47, 0.52])
fig, ax = plt.subplots(figsize=(6.4, 4.4))
pre = e < 0
ax.errorbar(e[pre], att[pre], yerr=1.96 * se[pre], fmt="o", color=MUTED,
            ecolor=MUTED, elinewidth=1.6, capsize=4, ms=6, label="pre-treatment")
post = e >= 0
ax.errorbar(e[post], att[post], yerr=1.96 * se[post], fmt="o", color=ACCENT,
            ecolor=ACCENT, elinewidth=1.8, capsize=4, ms=7, label="post-treatment")
ax.axhline(0, color=LINE, lw=1.2)
ax.axvline(-0.5, color=PRIMARY, lw=1.2, ls="--")
# The pre-trend line the intervals still admit
ax.plot([-4, 3], [-4 * 0.30, 3 * 0.30], color=DANGER, lw=1.8, ls=":",
        label="a pre-trend the CIs still admit")
ax.set_xlabel("event time $e = t - g$")
ax.set_ylabel("estimated effect")
ax.set_xticks(e)
ax.legend(loc="upper left", fontsize=9)
ax.grid(axis="y")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_003_event_study_wide.png"), bbox_inches="tight")
