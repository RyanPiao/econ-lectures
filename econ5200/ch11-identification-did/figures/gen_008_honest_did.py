import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
M = np.linspace(0, 3.0, 300)
point = 6.0
half = 1.1 + 2.75 * M          # identified set half-width grows with M-bar
lo, hi = point - half, point + half
fig, ax = plt.subplots(figsize=(6.4, 4.4))
ax.fill_between(M, lo, hi, color=SECONDARY, alpha=0.22,
                label="identified set")
ax.plot(M, lo, color=SECONDARY, lw=1.6)
ax.plot(M, hi, color=SECONDARY, lw=1.6)
ax.axhline(point, color=ACCENT, lw=2.0, label="point estimate (+6%)")
ax.axhline(0, color=PRIMARY, lw=1.3, ls="--")
bp = (point - 1.1) / 2.75
ax.plot([bp], [0], "o", color=DANGER, ms=9, zorder=5)
ax.annotate(f"breakdown point\n" + r"$\bar{M}$" + f" = {bp:.2f}",
            xy=(bp, 0), xytext=(bp + 0.16, -3.2), color=DANGER,
            fontsize=10, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.3))
ax.text(0.04, point + 1.4, r"$\bar{M}=0$ recovers standard DiD",
        color=MUTED, fontsize=9)
ax.set_xlabel(r"$\bar{M}$  — allowed post-trend violation, in units of the largest pre-trend")
ax.set_ylabel("treatment effect (%)")
ax.set_xlim(0, 3.0); ax.set_ylim(-6.5, 16)
ax.legend(loc="upper left", fontsize=9)
ax.grid(axis="y")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_008_honest_did.png"), bbox_inches="tight")
