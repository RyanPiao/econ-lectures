"""Walkthrough 3.4 -- Logan rideshare per-ride fee, a unit tax.
Massport raised the per-trip fee $3.25 -> $5.50 on 1 July 2025, so t = $2.25.
Elasticities are anchored, not invented:
  eD = -0.57 for UberX (Cohen, Hahn, Hall, Levitt & Metcalfe 2016, NBER w22627;
       RD design on surge pricing, four US markets). Rounded to -0.6.
  eS large: Hall, Horton & Knoepfle find driver supply highly elastic -- no hours
       restriction, minimal entry barriers. Using +2.0.
Emits ONE PANEL PER CASE so the deck can reveal them in step with the algebra:
  a: dpc/dt = 2.0/2.6 = 0.769 -> rider $1.73 / driver $0.52   (the estimated case)
  b: swapped = 0.6/2.6 = 0.231 -> rider $0.52 / driver $1.73   (counterfactual)
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, RED, INK, MUTE = "#2E6DB4", "#C0392B", "#2D2D2D", "#6B6B6B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": INK,
                     "axes.linewidth": 1.1, "figure.dpi": 170})
T = 2.25
split = lambda eD, eS: (eS / (eS - eD) * T, (1 - eS / (eS - eD)) * T)

def panel(fn, eD, eS, title):
    rider, driver = split(eD, eS)
    fig, ax = plt.subplots(figsize=(3.5, 4.0))
    ax.bar([0], [rider], 0.62, color=BLUE, zorder=3)
    ax.bar([0], [driver], 0.62, bottom=[rider], color=RED, zorder=3)
    ax.text(0, rider / 2, f"rider\n\\${rider:.2f}", ha="center", va="center",
            color="white", fontweight="bold", fontsize=13, linespacing=1.3, zorder=4)
    ax.text(0, rider + driver / 2, f"driver\n\\${driver:.2f}", ha="center", va="center",
            color="white", fontweight="bold", fontsize=13, linespacing=1.3, zorder=4)
    ax.plot([-0.55, 0.55], [T, T], ls=":", color=MUTE, lw=1.4, zorder=2)
    ax.text(0.58, T, f"$t=\\${T:.2f}$", va="center", ha="left", color=INK,
            fontweight="bold", fontsize=11)
    ax.set_title(title, fontsize=12.5, pad=10)
    ax.set_xticks([]); ax.set_xlim(-0.75, 1.25); ax.set_ylim(0, 2.6)
    ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.yaxis.set_major_formatter(lambda v, _: f"\\${v:,.2f}")
    ax.spines[["top", "right", "bottom"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(fn, bbox_inches="tight")
    print(f"  {fn}: eD={eD} eS={eS} dpc/dt={eS/(eS-eD):.4f} rider=${rider:.4f} driver=${driver:.4f} sum=${rider+driver:.4f}")

panel("logan-incidence-a.png", -0.6, 2.0, "(a)  $\\varepsilon_D=-0.6$, $\\varepsilon_S=+2.0$")
panel("logan-incidence-b.png", -2.0, 0.6, "(c)  swapped")
