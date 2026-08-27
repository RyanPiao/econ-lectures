"""Egg market: two point elasticities at the SAME equilibrium.
Qd = 200 - 5p, Qs = 50 + 10p  =>  p* = 10, Q* = 150.
eps_D = (-5)(10/150) = -1/3 ;  eps_S = (+10)(10/150) = +2/3.
The p/Q rescaling is identical for both -- only dQ/dp differs. This is the
mirror image of Heads Up 3.2 (same dQ/dp, different p/Q).
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, numpy as np

BLUE, RED, GREEN, INK, MUTE = "#2E6DB4", "#C0392B", "#2E7D4F", "#2D2D2D", "#6B6B6B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": INK,
                     "axes.linewidth": 1.1, "figure.dpi": 170})

fig, ax = plt.subplots(figsize=(7.4, 5.0))
p = np.linspace(0, 21, 200)
ax.plot(200 - 5*p, p, color=BLUE, lw=2.8, label=r"$Q^d = 200 - 5p$", zorder=3)
ax.plot(50 + 10*p, p, color=RED,  lw=2.8, label=r"$Q^s = 50 + 10p$", zorder=3)

ax.plot(150, 10, "o", color=GREEN, ms=12, zorder=6)
ax.plot([0, 150], [10, 10], ":", color=MUTE, lw=1.4, zorder=2)
ax.plot([150, 150], [0, 10], ":", color=MUTE, lw=1.4, zorder=2)
ax.text(4, 10.7, r"$p^{*}=\$10$", color=GREEN, fontsize=11.5, fontweight="bold")
ax.text(154, 0.55, r"$Q^{*}=150$", color=GREEN, fontsize=11.5, fontweight="bold")
ax.text(157, 10.9, r"$E_0$", color=GREEN, fontsize=13, fontweight="bold")

box = dict(boxstyle="round,pad=0.42", fc="white", lw=1.5, alpha=0.96)
ax.annotate(r"$\varepsilon_D = -5 \cdot \dfrac{10}{150} = -\dfrac{1}{3}$",
            xy=(150, 10), xytext=(20, 16.6), color=BLUE, fontsize=12.5,
            bbox=dict(ec=BLUE, **box),
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5,
                            connectionstyle="arc3,rad=-0.18"), zorder=7)
ax.annotate(r"$\varepsilon_S = +10 \cdot \dfrac{10}{150} = +\dfrac{2}{3}$",
            xy=(150, 10), xytext=(104, 2.4), color=RED, fontsize=12.5,
            bbox=dict(ec=RED, **box),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.5,
                            connectionstyle="arc3,rad=0.20"), zorder=7)
# the "same p/Q, different dQ/dp" line lives on the slide, not in the figure
ax.set_xlim(0, 215); ax.set_ylim(0, 21)
ax.set_xlabel("Quantity $Q$ (millions of dozens / week)")
ax.set_ylabel("Price $p$ (\\$/dozen)")
ax.yaxis.set_major_formatter(lambda v, _: f"\\${v:,.0f}")
ax.spines[["top", "right"]].set_visible(False)
ax.spines["bottom"].set_position(("data", 0))
ax.legend(loc="upper right", frameon=False, fontsize=11.5, handlelength=1.6,
          borderaxespad=0.6, bbox_to_anchor=(1.0, 0.94))
fig.tight_layout()
fig.savefig("egg-point-elasticity.png", bbox_inches="tight")
Qd,Qs=200-5*10, 50+10*10
print(f"check: Qd(10)={Qd}  Qs(10)={Qs}  equal={Qd==Qs}")
print(f"       eps_D={-5*10/150:+.4f} (= -1/3 {abs(-5*10/150+1/3)<1e-12})   eps_S={10*10/150:+.4f} (= +2/3 {abs(10*10/150-2/3)<1e-12})")
