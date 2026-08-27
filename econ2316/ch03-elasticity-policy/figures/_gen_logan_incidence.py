"""Walkthrough 3.4 -- Logan rideshare per-ride fee, a unit tax.
Massport raised the per-trip rideshare fee $3.25 -> $5.50 on 1 July 2025, so t = $2.25.
(The original proposal was $7.50; that second step was frozen.)
Teaching elasticities are ASSUMED, chosen to be plausible and to flip cleanly:
  A: eD = -0.8, eS = +2.0  -> dpc/dt = 2.0/2.8 = 0.714  -> rider $1.61 / driver $0.64
  B: swapped               -> dpc/dt = 0.8/2.8 = 0.286  -> rider $0.64 / driver $1.61
"""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, RED, INK, MUTE = "#2E6DB4", "#C0392B", "#2D2D2D", "#6B6B6B"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11, "axes.edgecolor": INK,
                     "axes.linewidth": 1.1, "figure.dpi": 170})
T = 2.25

def split(eD, eS):
    share_c = eS / (eS - eD)
    return share_c * T, (1 - share_c) * T

A = split(-0.8, 2.0)
B = split(-2.0, 0.8)

fig, ax = plt.subplots(figsize=(7.2, 4.3))
labels = ["A.  riders stuck\n$\\varepsilon_D=-0.8$, $\\varepsilon_S=+2.0$",
          "B.  riders can switch\n$\\varepsilon_D=-2.0$, $\\varepsilon_S=+0.8$"]
x = [0, 1]
rider = [A[0], B[0]]
driver = [A[1], B[1]]
ax.bar(x, rider, 0.5, color=BLUE, label="borne by the rider", zorder=3)
ax.bar(x, driver, 0.5, bottom=rider, color=RED, label="borne by the driver", zorder=3)

for i in range(2):
    ax.text(i, rider[i] / 2, f"\\${rider[i]:.2f}", ha="center", va="center",
            color="white", fontweight="bold", fontsize=14, zorder=4)
    ax.text(i, rider[i] + driver[i] / 2, f"\\${driver[i]:.2f}", ha="center", va="center",
            color="white", fontweight="bold", fontsize=14, zorder=4)

ax.plot([-0.45, 1.32], [T, T], ls=":", color=MUTE, lw=1.4, zorder=2)
ax.text(1.38, T, f"$t=\\${T:.2f}$", va="center", ha="left", color=INK,
        fontweight="bold", fontsize=12.5,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=MUTE, lw=1.0))
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11.5)
ax.set_ylim(0, 2.75); ax.set_xlim(-0.55, 1.75)
ax.set_ylabel("Per-ride fee increase (\\$)")
ax.yaxis.set_major_formatter(lambda v, _: f"\\${v:,.2f}")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.42, 1.14), ncol=2, frameon=False, fontsize=11)
fig.tight_layout()
fig.savefig("logan-incidence.png", bbox_inches="tight")
print(f"t = ${T}")
for n, (rc, dv), (eD, eS) in [("A", A, (-0.8, 2.0)), ("B", B, (-2.0, 0.8))]:
    print(f"  {n}: eD={eD} eS={eS}  dpc/dt={eS/(eS-eD):.4f}  rider=${rc:.4f} driver=${dv:.4f}  sum=${rc+dv:.4f}")
