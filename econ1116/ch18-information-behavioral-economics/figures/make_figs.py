#!/usr/bin/env python3
"""Ch 18 — Information, Uncertainty & Behavioral Economics: lecture figures (White Academia palette)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np

# Avoid mathtext parsing of '$' in labels (Ch11 lesson)
rcParams["text.parse_math"] = False
rcParams["font.family"] = "DejaVu Sans"
rcParams["font.size"] = 13
rcParams["axes.titlesize"] = 16
rcParams["axes.titleweight"] = "bold"
rcParams["savefig.dpi"] = 150
rcParams["figure.dpi"] = 150

# Palette
PRIMARY = "#2D2D2D"
SECONDARY = "#6B8BA4"   # dusty blue
ACCENT = "#C47B5A"      # terracotta
SUCCESS = "#6A8E6B"     # sage
DANGER = "#A85C5C"      # rosewood
MUTED = "#8C8580"
LINE = "#D5CEC7"
PAPER = "#f8f6f3"
FIGDIR = "."


def style_ax(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=11)
    for lbl in ax.get_xticklabels() + ax.get_yticklabels():
        lbl.set_color(PRIMARY)


def save(fig, name):
    fig.savefig(f"{FIGDIR}/{name}", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", name)


# ============================================================
# 1. THE LEMONS UNRAVELING — adverse-selection spiral
#    Each round: buyers pay average -> plums exit -> avg quality falls
# ============================================================
def fig_lemons():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    rounds = ["Round 1\nall cars", "Round 2\nplums leave", "Round 3\nbest exit", "Round 4\nonly lemons"]
    avg_price = [10000, 7500, 6000, 5000]
    share_plums = [50, 33, 17, 0]
    x = np.arange(len(rounds))
    bars = ax.bar(x, avg_price, width=0.55, color=[SECONDARY, ACCENT, "#B5806A", DANGER])
    for b, p, s in zip(bars, avg_price, share_plums):
        ax.text(b.get_x() + b.get_width()/2, p + 220, f"${p:,}", ha="center",
                fontweight="bold", color=PRIMARY, fontsize=12.5)
        ax.text(b.get_x() + b.get_width()/2, 600, f"{s}% plums", ha="center",
                color="white", fontsize=10.5, fontweight="bold")
    ax.annotate("", xy=(3, 5600), xytext=(0, 10600),
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=2.2,
                                connectionstyle="arc3,rad=-0.18"))
    ax.text(1.4, 9400, "the market unravels", color=DANGER, fontsize=12,
            fontweight="bold", rotation=-14)
    ax.set_ylim(0, 11800)
    ax.set_xticks(x); ax.set_xticklabels(rounds, fontsize=10.5)
    ax.set_ylabel("Average price buyers will pay", color=PRIMARY)
    ax.set_title("Adverse selection: good cars driven out by bad", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-lemons.png")


# ============================================================
# 2. PROSPECT THEORY — the value function (reference-dependent, loss-averse)
#    v(x)=x^0.88 for gains ; v(x)=-2.25*(-x)^0.88 for losses
# ============================================================
def fig_prospect():
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    g = np.linspace(0, 100, 200)
    l = np.linspace(-100, 0, 200)
    vg = np.power(g, 0.88)
    vl = -2.25 * np.power(-l, 0.88)
    ax.plot(g, vg, color=SUCCESS, lw=3.0)
    ax.plot(l, vl, color=DANGER, lw=3.0)
    ax.axhline(0, color=MUTED, lw=1.0)
    ax.axvline(0, color=MUTED, lw=1.0)

    # symmetric $100 reference arrows
    ax.plot([100, 100], [0, np.power(100, 0.88)], color=SUCCESS, ls=":", lw=1.5)
    ax.plot([-100, -100], [0, -2.25*np.power(100, 0.88)], color=DANGER, ls=":", lw=1.5)
    ax.annotate("a $100 gain\nfeels like +57", (100, np.power(100, 0.88)),
                xytext=(40, 30), color=SUCCESS, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.4))
    ax.annotate("a $100 loss\nhurts like -128", (-100, -2.25*np.power(100, 0.88)),
                xytext=(-95, -80), color=DANGER, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.4))
    ax.text(0, 145, "REFERENCE\nPOINT", ha="center", color=PRIMARY,
            fontsize=10.5, fontweight="bold")
    ax.scatter([0], [0], color=PRIMARY, zorder=6, s=45)

    ax.set_xlim(-115, 115); ax.set_ylim(-150, 160)
    ax.set_xlabel("Outcome relative to reference point ($)", color=PRIMARY)
    ax.set_ylabel("Psychological value", color=PRIMARY)
    ax.set_title("Prospect theory: losses loom larger than gains", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-prospect.png")


# ============================================================
# 3. RISK AVERSION — concave utility, certainty equivalent, risk premium
#    U(x)=sqrt(x). Gamble: 0.5*$36 + 0.5*$4. EV=$20, EU=4, CE=$16, RP=$4
# ============================================================
def fig_risk_utility():
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    x = np.linspace(0, 40, 200)
    ax.plot(x, np.sqrt(x), color=SECONDARY, lw=3.0, label="U(x) = √x  (risk-averse)")

    # endpoints of the gamble
    for xv in (4, 36):
        ax.scatter([xv], [np.sqrt(xv)], color=PRIMARY, zorder=6, s=45)
    # chord between outcomes -> expected utility at EV=20
    ax.plot([4, 36], [2, 6], color=MUTED, ls="--", lw=1.6)
    ax.scatter([20], [4], color=DANGER, zorder=6, s=60)          # EU = 4
    ax.scatter([20], [np.sqrt(20)], color=SUCCESS, zorder=6, s=60)  # U(EV)=4.47
    ax.plot([20, 20], [0, np.sqrt(20)], color=MUTED, ls=":", lw=1.2)

    # certainty equivalent at U=4 -> x=16
    ax.plot([0, 16], [4, 4], color=DANGER, ls=":", lw=1.3)
    ax.plot([16, 16], [0, 4], color=DANGER, ls=":", lw=1.3)
    ax.scatter([16], [4], color=DANGER, zorder=6, s=45)

    # risk premium bracket
    ax.annotate("", xy=(20, 1.2), xytext=(16, 1.2),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=2.0))
    ax.text(18, 0.7, "risk premium\n= $4", ha="center", color=ACCENT,
            fontsize=10.5, fontweight="bold")

    ax.text(20.5, np.sqrt(20)+0.1, "U(EV) = 4.47", color=SUCCESS, fontsize=10.5, fontweight="bold")
    ax.text(20.5, 3.55, "EU = 4.0", color=DANGER, fontsize=10.5, fontweight="bold")
    ax.text(16, 4.25, "CE = $16", ha="center", color=DANGER, fontsize=10, fontweight="bold")
    ax.text(21.4, 0.35, "EV = $20", ha="left", color=PRIMARY, fontsize=10, fontweight="bold")

    ax.set_xlim(0, 40); ax.set_ylim(0, 7)
    ax.set_xlabel("Wealth ($)", color=PRIMARY)
    ax.set_ylabel("Utility (utils)", color=PRIMARY)
    ax.set_title("Why risk-averse people pay for certainty", color=PRIMARY)
    ax.legend(loc="lower right", fontsize=10.5, frameon=False)
    style_ax(ax)
    save(fig, "fig-risk-utility.png")


# ============================================================
# 4. ANCHORING — the SSN-digit bid experiment ($16 vs $56)
# ============================================================
def fig_anchoring():
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    cats = ["Low digits\n(01–20)", "High digits\n(80–99)"]
    vals = [16, 56]
    bars = ax.bar(cats, vals, width=0.5, color=[SECONDARY, DANGER])
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 1.4, f"${v}", ha="center",
                fontweight="bold", color=PRIMARY, fontsize=15)
    ax.annotate("3.5× higher bid\nfor the same keyboard", xy=(1, 56),
                xytext=(0.30, 44), ha="center", color=DANGER, fontsize=11.5,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.6))
    ax.set_ylim(0, 66)
    ax.set_ylabel("Average bid ($)", color=PRIMARY)
    ax.set_title("Anchoring: a random number reshapes willingness to pay", color=PRIMARY)
    ax.text(0.5, -11, "Last 2 digits of Social Security number written before bidding",
            ha="center", color=MUTED, fontsize=10, transform=ax.transData)
    style_ax(ax)
    save(fig, "fig-anchoring.png")


# ============================================================
# 5. THE DEFAULT NUDGE — auto-enrollment vs opt-in
#    Participation 94 vs 64 ; contribution 12.3 vs 7.4
# ============================================================
def fig_nudge():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    groups = ["Participation\nrate (%)", "Avg contribution\n(% of pay)"]
    optin = [64, 7.4]
    auto = [94, 12.3]
    x = np.arange(len(groups)); w = 0.36
    b1 = ax.bar(x - w/2, optin, w, color=MUTED, label="Opt-in (voluntary)")
    b2 = ax.bar(x + w/2, auto, w, color=SUCCESS, label="Auto-enroll (opt-out default)")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.2,
                    f"{b.get_height():g}", ha="center", fontweight="bold",
                    color=PRIMARY, fontsize=12)
    ax.set_xticks(x); ax.set_xticklabels(groups, fontsize=11.5)
    ax.set_ylim(0, 116)
    ax.set_ylabel("Value", color=PRIMARY)
    ax.set_title("The most powerful nudge: change the default", color=PRIMARY)
    ax.legend(loc="upper center", fontsize=10.5, frameon=False, ncol=2,
              bbox_to_anchor=(0.5, 1.0))
    style_ax(ax)
    save(fig, "fig-nudge.png")


# ============================================================
# 6. LOSS AVERSION — the rejected coin flip (+$12 / -$10)
#    Money is +$1 EV, but felt value is negative
# ============================================================
def fig_loss_aversion():
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    cats = ["Money value\n(EV)", "Felt value\n(loss-averse)"]
    # EV = .5*12 + .5*(-10) = +1 ; felt = .5*12 + .5*(-2 * 10) = +6 -10 = -4
    money = 1.0
    felt = 0.5*12 + 0.5*(-2.0*10)
    bars = ax.bar(cats, [money, felt], width=0.5,
                  color=[SUCCESS, DANGER])
    ax.axhline(0, color=MUTED, lw=1.2)
    ax.text(0, money + 0.4, "+$1.00", ha="center", fontweight="bold", color=SUCCESS, fontsize=14)
    ax.text(1, felt - 0.9, "−$4.00", ha="center", fontweight="bold", color=DANGER, fontsize=14)
    ax.annotate("a positive bet\nfeels like a loss → most refuse", xy=(1, felt),
                xytext=(0.45, -2.6), ha="center", color=DANGER, fontsize=11,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.5))
    ax.set_ylim(-5.5, 3)
    ax.set_ylabel("Net value of a +$12 / −$10 coin flip", color=PRIMARY)
    ax.set_title("Loss aversion: losses weighted ~2× gains", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-loss-aversion.png")


if __name__ == "__main__":
    fig_lemons()
    fig_prospect()
    fig_risk_utility()
    fig_anchoring()
    fig_nudge()
    fig_loss_aversion()
    print("done")
