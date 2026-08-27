"""FOC worked example — calibrated to Ch 3 Walkthrough 3.2 (revenue-maximising NYC toll).
Q^d(P) = 300,000 - 5,000P  =>  R(P) = 300,000P - 5,000P^2
R'(P) = 300,000 - 10,000P = 0  =>  P* = $30, R* = $4.5M/day.  R'' = -10,000 < 0 (max).
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np

BLUE, RED, GREEN, INK, MUTE = "#2E6DB4", "#C0392B", "#2E7D4F", "#2D2D2D", "#6B6B6B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": INK,
                     "axes.linewidth": 1.1, "figure.dpi": 170})

R  = lambda p: (300_000*p - 5_000*p**2) / 1e6      # $ millions
Rp = lambda p: (300_000 - 10_000*p) / 1e6          # $ millions per $1 of toll

fig, ax = plt.subplots(figsize=(7.0, 4.5))
P = np.linspace(0, 60, 400)
ax.plot(P, R(P), color=BLUE, lw=2.8, zorder=3)

def tangent(p0, half, color, lw=2.2):
    x = np.array([p0 - half, p0 + half])
    ax.plot(x, R(p0) + Rp(p0)*(x - p0), color=color, lw=lw, zorder=4)

tangent(15, 7, RED); tangent(45, 7, RED); tangent(30, 11, GREEN, 2.8)

ax.plot(30, R(30), "o", color=GREEN, ms=11, zorder=6, clip_on=False)
ax.plot([30, 30], [0, R(30)], ":", color=MUTE, lw=1.4, zorder=2)
ax.plot([0, 30], [R(30), R(30)], ":", color=MUTE, lw=1.4, zorder=2)

ax.text(30, 6.02, "$R'(P^{*}) = 0$", color=GREEN, ha="center", va="bottom",
        fontsize=13, fontweight="bold")
ax.text(12, 5.28, "$R'(P) > 0$\nraise the toll", color=RED, ha="center", va="bottom",
        fontsize=11, fontweight="bold", linespacing=1.35)
ax.text(48, 5.28, "$R'(P) < 0$\nlower the toll", color=RED, ha="center", va="bottom",
        fontsize=11, fontweight="bold", linespacing=1.35)
ax.text(1.2, R(30) + 0.10, "$R^{*}=\\$4.5\\,\\mathrm{M/day}$", color=GREEN, ha="left", va="bottom",
        fontsize=11, fontweight="bold")
ax.text(30.9, 0.16, "$P^{*}=\\$30$", color=GREEN, ha="left", fontsize=11.5, fontweight="bold")

ax.set_xlim(0, 60); ax.set_ylim(0, 6.7)
ax.set_xlabel("Toll $P$ (\\$)"); ax.set_ylabel("Daily revenue $R(P)$")
ax.set_yticks([0, 1, 2, 3, 4, 5])
ax.xaxis.set_major_formatter(lambda v, _: f"\\${v:,.0f}")
ax.yaxis.set_major_formatter(lambda v, _: f"\\${v:,.0f}M")
ax.spines[["top", "right"]].set_visible(False)
ax.spines["bottom"].set_position(("data", 0))
ax.spines["left"].set_bounds(0, 5.2)
fig.tight_layout()
fig.savefig("foc-worked-example.png", bbox_inches="tight")
print("wrote foc-worked-example.png")
print(f"  check: R(30)={R(30):.3f}M  R'(30)={Rp(30):.3f}  R(15)={R(15):.3f}M  R'(15)={Rp(15):+.3f}")
