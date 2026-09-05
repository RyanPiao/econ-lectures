import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _wa import *
import numpy as np, matplotlib.pyplot as plt
style()
fig, ax = plt.subplots(figsize=(6.4, 4.4))
x = np.arange(2)
w = 0.34
truth = [8.65, 9.56]
twfe = [4.70, -0.97]
ax.bar(x - w / 2, truth, w, color=MUTED, label="true ATT")
ax.bar(x + w / 2, twfe, w, color=[DANGER, DANGER], label="TWFE estimate")
for xi, v in zip(x - w / 2, truth):
    ax.text(xi, v + 0.3, f"{v:+.2f}", ha="center", color=PRIMARY,
            fontsize=11.5, fontweight="bold")
for xi, v in zip(x + w / 2, twfe):
    off = 0.3 if v >= 0 else -0.95
    ax.text(xi, v + off, f"{v:+.2f}", ha="center", color=DANGER,
            fontsize=11.5, fontweight="bold")
ax.axhline(0, color=PRIMARY, lw=1.2)
ax.set_xticks(x)
ax.set_xticklabels(["30% never-treated\n(forbidden weight 24%)",
                    "everyone eventually treated\n(forbidden weight 75%)"],
                   fontsize=10)
ax.set_ylabel("effect")
ax.set_ylim(-3.2, 12.2)
ax.legend(loc="upper left", fontsize=9.5)
ax.grid(axis="y")
ax.text(1.0, -2.7, "wrong sign, precisely estimated", ha="center",
        color=DANGER, fontsize=10, fontstyle="italic")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)),
            "figure_009_sign_flip.png"), bbox_inches="tight")
