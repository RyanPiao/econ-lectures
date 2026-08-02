"""Regenerates three ECON 2316 Ch 10 deck figures.

  fig-sr-profit.png       slide 23 — demand shock lifts P above ATC (burger example)
  fig-entry-exit.png      slide 28 — entry competes profit to zero (burger example)
  fig-austin-entry-sd.png slide 26 — Austin rideshare re-entry

Run:  python3 gen_ch10_market_figs.py

Locked calibration, shared by the first two figures so the panels tell one story:
  market   S0: P = 0.004Q - 2       D0: P = 18 - 0.004Q      D1: P = 22 - 0.004Q
           S1 (after entry): P = 0.004Q - 6
           equilibria  (2500, $8) -> shock -> (3000, $10) -> entry -> (3500, $8)
  firm     TC(q) = 16.384 + 11.072q - 0.24q^2 + 0.004q^3
           chosen so ATC is minimised at q = 32 with min ATC = $8 exactly,
           which forces MC to cut ATC at that same point.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# deck palette (styles.css)
NAVY = "#1F3B57"
BLUE = "#6B8BA4"
TERRA = "#C47B5A"
SAGE = "#6A8E6B"
ROSE = "#A85C5C"
MUTED = "#8C8580"
INK = "#2D2D2D"
ORANGE = "#D98324"
CYAN = "#2E93B8"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#7A736D",
    "axes.linewidth": 1.1,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": INK,
    "ytick.color": INK,
})

# ---------------------------------------------------------------- firm costs
# F is deliberately large enough that ATC sits visibly clear of AVC at the
# right-hand end of the plotted range; with a small F the two curves converge
# and read as if they cross, which they never do (ATC - AVC = F/q > 0).
F, A, B, C = 118.8, 4.6715, -0.14, 0.004
ATC = lambda q: F / q + A + B * q + C * q ** 2
AVC = lambda q: A + B * q + C * q ** 2
MC = lambda q: A + 2 * B * q + 3 * C * q ** 2

Q_MIN_ATC = 32.0          # ATC minimised here, ATC = MC = $8
Q_AT_P10 = 35.75          # upper root of MC(q) = 10


def _clean(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=10)


def _below_legend(ax, ncol):
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=ncol,
              frameon=False, fontsize=10.5, handlelength=1.9,
              columnspacing=1.5, borderaxespad=0)


# ============================================================ fig-sr-profit
def sr_profit():
    fig, (axm, axf) = plt.subplots(1, 2, figsize=(13.6, 6.0))
    fig.suptitle("A demand shock lifts price above ATC  →  the burger shop earns "
                 "short-run economic profit",
                 fontsize=15, fontweight="bold", y=0.97)

    # ---- market panel
    q = np.linspace(0, 5600, 400)
    axm.plot(q, 0.004 * q - 2, color=SAGE, lw=2.6, label="$S_0$", zorder=3)
    axm.plot(q, 18 - 0.004 * q, color=BLUE, lw=2.4, ls="--", label="$D_0$", zorder=3)
    axm.plot(q, 22 - 0.004 * q, color=NAVY, lw=2.8,
             label="$D_1$ (after the dorm)", zorder=3)

    for qq, pp, col in ((2500, 8, MUTED), (3000, 10, TERRA)):
        axm.plot([0, qq], [pp, pp], color=MUTED, lw=1.0, ls=":", zorder=1)
        axm.plot([qq, qq], [0, pp], color=MUTED, lw=1.0, ls=":", zorder=1)
        axm.scatter([qq], [pp], s=95, color=col, zorder=5,
                    edgecolor="white", linewidth=1.4)

    # shift annotation, drawn exactly across the D0 -> D1 gap so it touches neither
    y_arrow = 13.5
    axm.annotate("", xy=((22 - y_arrow) / 0.004 - 55, y_arrow),
                 xytext=((18 - y_arrow) / 0.004 + 55, y_arrow),
                 arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2.2,
                                 mutation_scale=17))
    # horizontal text is wider than the 4-unit vertical gap between D0 and D1
    # can accommodate, so it is masked with an opaque box rather than squeezed
    axm.text(1625, 12.35, "demand shifts right", ha="center", va="center",
             fontsize=11.5, fontweight="bold", color=NAVY, zorder=6,
             bbox=dict(boxstyle="round,pad=0.28", fc="white", ec="none"))

    axm.set_xlim(0, 5600)
    axm.set_ylim(0, 17)
    axm.set_yticks([8, 10])
    axm.set_yticklabels(["\\$8", "\\$10"], fontsize=11)
    axm.set_xticks([2500, 3000])
    axm.set_xticklabels(["2500", "3000"], fontsize=11)
    axm.set_xlabel("Quantity — whole market (burgers/day)", fontsize=11.5)
    axm.set_title("The Market", fontsize=13.5, fontweight="bold", pad=10)
    _clean(axm)
    _below_legend(axm, 3)

    # ---- firm panel
    qq = np.linspace(6, 55, 400)
    axf.fill_between([0, Q_AT_P10], ATC(Q_AT_P10), 10,
                     color=SAGE, alpha=0.20, zorder=1)
    axf.plot(qq, MC(qq), color=ORANGE, lw=2.6, label="MC", zorder=4)
    axf.plot(qq, ATC(qq), color=NAVY, lw=2.6, label="ATC", zorder=4)
    axf.plot(qq, AVC(qq), color=CYAN, lw=2.2, label="AVC", zorder=4)
    axf.axhline(10, color=TERRA, lw=2.4, label="P = MR = \\$10", zorder=3)
    axf.axhline(8, color=MUTED, lw=1.0, ls=":", zorder=1)

    axf.scatter([Q_AT_P10], [10], s=95, color=TERRA, zorder=6,
                edgecolor="white", linewidth=1.4)
    axf.scatter([Q_AT_P10], [ATC(Q_AT_P10)], s=85, color=SAGE, zorder=6,
                edgecolor="white", linewidth=1.4)
    axf.plot([Q_AT_P10, Q_AT_P10], [0, 10], color=MUTED, lw=1.0, ls=":", zorder=1)
    axf.plot([Q_MIN_ATC, Q_MIN_ATC], [0, 8], color=MUTED, lw=1.0, ls=":", zorder=1)
    axf.text(19, 9.05, "Profit", fontsize=14, fontweight="bold",
             color="#2F6B3A", ha="center", va="center", zorder=7)

    axf.set_xlim(4, 56)
    axf.set_ylim(2, 17)
    axf.set_yticks([8, 10])
    axf.set_yticklabels(["\\$8", "\\$10"], fontsize=11)
    axf.set_xticks([Q_MIN_ATC, Q_AT_P10])
    axf.set_xticklabels(["$q_0$", "$q_1$"], fontsize=12)
    axf.set_xlabel("Quantity — one burger shop", fontsize=11.5)
    axf.set_title("The Representative Burger Shop", fontsize=13.5,
                  fontweight="bold", pad=10)
    _clean(axf)
    _below_legend(axf, 4)

    fig.tight_layout(rect=[0, 0.02, 1, 0.94])
    fig.savefig("fig-sr-profit.png", dpi=155, facecolor="white")
    plt.close(fig)


# =========================================================== fig-entry-exit
def entry_exit():
    fig, (axm, axf) = plt.subplots(1, 2, figsize=(13.8, 6.0))
    fig.suptitle("Free entry competes economic profit to zero  (P → min ATC)",
                 fontsize=15, fontweight="bold", y=0.97)

    # ---- market panel
    q = np.linspace(0, 5600, 400)
    axm.plot(q, 22 - 0.004 * q, color=NAVY, lw=2.8, label="$D_1$ (after the dorm)")
    axm.plot(q, 0.004 * q - 2, color=SAGE, lw=2.4, ls="--", label="$S_0$ (few shops)")
    axm.plot(q, 0.004 * q - 6, color="#2FA34E", lw=2.8, label="$S_1$ (after entry)")

    for qq, pp, col in ((3000, 10, TERRA), (3500, 8, "#2FA34E")):
        axm.plot([0, qq], [pp, pp], color=MUTED, lw=1.0, ls=":", zorder=1)
        axm.plot([qq, qq], [0, pp], color=MUTED, lw=1.0, ls=":", zorder=1)
        axm.scatter([qq], [pp], s=95, color=col, zorder=5,
                    edgecolor="white", linewidth=1.4)

    # "entry" arrow slides down the demand curve, label offset clear of the line
    axm.annotate("", xy=(3440, 8.32), xytext=(3060, 9.68),
                 arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.8,
                                 mutation_scale=15))
    axm.text(3560, 9.9, "entry", fontsize=12, fontweight="bold",
             style="italic", color=INK, ha="left", va="center", zorder=6,
             bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none"))

    axm.set_xlim(0, 5600)
    axm.set_ylim(0, 17)
    axm.set_yticks([8, 10])
    axm.set_yticklabels(["\\$8", "\\$10"], fontsize=11)
    axm.set_xticks([3000, 3500])
    axm.set_xticklabels(["3000", "3500"], fontsize=11)
    axm.set_xlabel("Quantity — whole market (burgers/day)", fontsize=11.5)
    axm.set_title("Panel A · The Market", fontsize=13.5, fontweight="bold", pad=10)
    _clean(axm)
    _below_legend(axm, 3)

    # ---- firm panel
    qq = np.linspace(6, 55, 400)
    axf.plot(qq, ATC(qq), color=NAVY, lw=2.6, label="ATC")
    axf.plot(qq, MC(qq), color=ORANGE, lw=2.6, label="MC")
    axf.axhline(10, color=MUTED, lw=1.4, ls=":")
    axf.axhline(8, color="#2FA34E", lw=2.4)
    axf.text(7.0, 10.35, "\\$10", fontsize=11.5, fontweight="bold", color=MUTED)
    axf.text(7.0, 8.32, "\\$8", fontsize=11.5, fontweight="bold", color="#2FA34E")

    # price-fall arrow parked left of the ATC branch; label sits in the
    # empty wedge between MC and ATC so it crosses neither curve
    axf.annotate("", xy=(11.4, 8.25), xytext=(11.4, 9.85),
                 arrowprops=dict(arrowstyle="-|>", color=ROSE, lw=2.4,
                                 mutation_scale=16))
    axf.text(13.2, 7.05, "entry pushes P ↓", fontsize=11.5,
             fontweight="bold", color=ROSE, ha="left", va="center")

    axf.scatter([Q_MIN_ATC], [8], marker="*", s=430, color="#E8A33D",
                edgecolor=INK, linewidth=0.9, zorder=6)
    axf.annotate("P = min ATC\nprofit = 0",
                 xy=(Q_MIN_ATC + 1.1, 7.75), xytext=(41, 5.1),
                 fontsize=11.5, fontweight="bold", color=NAVY,
                 ha="left", va="center",
                 bbox=dict(boxstyle="round,pad=0.42", fc="white",
                           ec="#E8A33D", lw=1.5),
                 arrowprops=dict(arrowstyle="-", color=NAVY, lw=1.1))

    axf.set_xlim(4, 56)
    axf.set_ylim(2, 17)
    axf.set_yticks([8, 10])
    axf.set_yticklabels(["\\$8", "\\$10"], fontsize=11)
    axf.set_xticks([Q_MIN_ATC])
    axf.set_xticklabels(["$q^{*}$"], fontsize=12)
    axf.set_xlabel("Quantity — one burger shop", fontsize=11.5)
    axf.set_title("Panel B · A representative burger shop",
                  fontsize=13.5, fontweight="bold", pad=10)
    _clean(axf)
    _below_legend(axf, 2)

    fig.tight_layout(rect=[0, 0.02, 1, 0.94])
    fig.savefig("fig-entry-exit.png", dpi=155, facecolor="white")
    plt.close(fig)


# ====================================================== fig-austin-entry-sd
def austin():
    fig, ax = plt.subplots(figsize=(9.6, 6.4))

    q = np.linspace(0, 10, 300)
    D = 9.4 - 0.72 * q
    S0 = 0.9 + 0.78 * q
    S1 = 0.9 + 0.78 * (q - 2.55)

    ax.plot(q, D, color=BLUE, lw=2.7, zorder=3)
    ax.plot(q, S0, color=TERRA, lw=2.7, zorder=3)
    ax.plot(q, S1, color=TERRA, lw=2.7, ls="--", zorder=3)

    q0, p0 = 5.667, 5.32
    q1, p1 = 7.10, 4.29

    for qq, pp in ((q0, p0), (q1, p1)):
        ax.plot([0, qq], [pp, pp], color=MUTED, lw=0.9, ls=":", zorder=1)
        ax.plot([qq, qq], [0, pp], color=MUTED, lw=0.9, ls=":", zorder=1)
    ax.scatter([q0], [p0], s=90, color=INK, zorder=6, edgecolor="white", lw=1.3)
    ax.scatter([q1], [p1], s=90, color=ROSE, zorder=6, edgecolor="white", lw=1.3)
    ax.text(q0 + 0.16, p0 + 0.30, "A", fontsize=14, fontweight="bold", color=INK)
    ax.text(q1 + 0.16, p1 + 0.30, "B", fontsize=14, fontweight="bold", color=ROSE)

    # curve labels: anchored past the end of each line, offset off its slope
    ax.annotate("$S_0$", xy=(9.55, 0.9 + 0.78 * 9.55), xytext=(-4, 12),
                textcoords="offset points", fontsize=14, color=TERRA,
                fontweight="bold", ha="center")
    ax.annotate("$S_1$ (after entry)", xy=(8.55, 0.9 + 0.78 * (8.55 - 2.55)),
                xytext=(-14, 26), textcoords="offset points", fontsize=13,
                color=TERRA, fontweight="bold", ha="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.24", fc="white", ec="none"))
    ax.annotate("$D$", xy=(9.55, 9.4 - 0.72 * 9.55), xytext=(16, -4),
                textcoords="offset points", fontsize=14, color=BLUE,
                fontweight="bold", va="center")

    # fare fall, drawn on the axis gutter well clear of every curve
    ax.annotate("", xy=(1.05, p1), xytext=(1.05, p0),
                arrowprops=dict(arrowstyle="-|>", color=ROSE, lw=2.3,
                                mutation_scale=16))
    ax.text(1.32, (p0 + p1) / 2, "fare ↓", fontsize=12.5,
            fontweight="bold", color=ROSE, ha="left", va="center")

    # market quantity rise, along the bottom in open space
    ax.annotate("", xy=(q1, 1.30), xytext=(q0, 1.30),
                arrowprops=dict(arrowstyle="-|>", color=SAGE, lw=2.3,
                                mutation_scale=16))
    ax.text((q0 + q1) / 2, 0.86, "total rides ↑", fontsize=12.5,
            fontweight="bold", color=SAGE, ha="center", va="center")

    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 10.2)
    ax.set_xticks([q0, q1])
    ax.set_xticklabels(["$Q_0$", "$Q_1$"], fontsize=13)
    ax.set_yticks([p1, p0])
    ax.set_yticklabels(["$P_1$", "$P_0$"], fontsize=13)
    ax.set_xlabel("Quantity — rides across the whole Austin market", fontsize=12)
    ax.set_ylabel("Price (fare per ride)", fontsize=12)
    ax.set_title("Entry expands market supply: fares fall, total rides rise",
                 fontsize=13.5, fontweight="bold", pad=12)
    _clean(ax)

    fig.tight_layout()
    fig.savefig("fig-austin-entry-sd.png", dpi=155, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    sr_profit()
    entry_exit()
    austin()
    print("wrote fig-sr-profit.png, fig-entry-exit.png, fig-austin-entry-sd.png")
