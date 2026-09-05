import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
fig, ax = plt.subplots(figsize=(6.4, 4.4))
t = np.array([0.0, 1.0])
ctrl = np.array([4.0, 5.2])          # control path
trt_obs = np.array([7.0, 10.4])      # treated, observed
trt_cf = np.array([7.0, 8.2])        # treated counterfactual (parallel to control)

ax.plot(t, ctrl, "-o", color=SECONDARY, lw=2.4, ms=7, label="Control — observed")
ax.plot(t, trt_obs, "-o", color=ACCENT, lw=2.4, ms=7, label="Treated — observed")
ax.plot(t, trt_cf, "--o", color=MUTED, lw=2.0, ms=6, mfc="white",
        label="Treated — counterfactual (never observed)")

ax.annotate("", xy=(1.0, trt_obs[1]), xytext=(1.0, trt_cf[1]),
            arrowprops=dict(arrowstyle="<->", color=PRIMARY, lw=1.8))
ax.text(1.045, (trt_obs[1] + trt_cf[1]) / 2, "ATT", color=PRIMARY,
        fontsize=12, fontweight="bold", va="center")

ax.axvline(0.5, color=LINE, lw=1.4, ls=":")
ax.text(0.5, 3.15, "treatment", color=MUTED, fontsize=9, ha="center")

ax.annotate("level gap —\nabsorbed by the\ngroup fixed effect",
            xy=(0.0, 5.5), xytext=(0.06, 5.4), color=MUTED, fontsize=9)
ax.annotate("", xy=(0.0, 7.0), xytext=(0.0, 4.0),
            arrowprops=dict(arrowstyle="<->", color=LINE, lw=1.6))

ax.set_xlim(-0.08, 1.32); ax.set_ylim(3.0, 11.2)
ax.set_xticks([0, 1]); ax.set_xticklabels(["before", "after"])
ax.set_ylabel("outcome")
ax.set_yticks([])
ax.legend(loc="upper left", fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_001_parallel_trends.png"), bbox_inches="tight")
