#!/usr/bin/env python3
"""Ch 16 — Externalities & the Environment: lecture figures (White Academia palette)."""
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
# 1. NEGATIVE EXTERNALITY — Clearwater Chemical
#    MPC = 60 + 2Q ; Demand P = 200 - 2Q ; MSC = 100 + 2Q
#    Qmkt = 35, P = 130 ; Q* = 25, P = 150 ; DWL = $200k
# ============================================================
def fig_negative():
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    Q = np.linspace(0, 60, 200)
    D = 200 - 2 * Q
    MPC = 60 + 2 * Q
    MSC = 100 + 2 * Q
    ax.plot(Q, D, color=PRIMARY, lw=2.6, label="Demand (MPB)")
    ax.plot(Q, MPC, color=SECONDARY, lw=2.6, label="MPC = Supply")
    ax.plot(Q, MSC, color=DANGER, lw=2.6, label="MSC = MPC + external cost")

    Qm, Pm = 35, 130
    Qs, Ps = 25, 150
    # DWL triangle between MSC and Demand from Q*=25 to Qm=35
    qfill = np.linspace(Qs, Qm, 40)
    ax.fill_between(qfill, 200 - 2 * qfill, 100 + 2 * qfill,
                    color=DANGER, alpha=0.22, label="Deadweight loss")

    for (Qx, Px, c) in [(Qm, Pm, SECONDARY), (Qs, Ps, SUCCESS)]:
        ax.plot([Qx, Qx], [0, Px], color=c, ls=":", lw=1.5)
        ax.plot([0, Qx], [Px, Px], color=c, ls=":", lw=1.5)
    ax.scatter([Qm, Qs], [Pm, Ps], color=[SECONDARY, SUCCESS], zorder=5, s=55)

    ax.annotate("Market\n Q = 35", (Qm, Pm), xytext=(Qm + 2, Pm - 34),
                color=SECONDARY, fontweight="bold", fontsize=11)
    ax.annotate("Social optimum\n Q* = 25", (Qs, Ps), xytext=(Qs - 22, Ps + 14),
                color=SUCCESS, fontweight="bold", fontsize=11)
    ax.annotate("DWL\n$200k/wk", (30.5, 152), color=DANGER, fontweight="bold",
                fontsize=10.5, ha="center")
    # external cost arrow
    ax.annotate("", xy=(12, 100 + 2 * 12), xytext=(12, 60 + 2 * 12),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.3))
    ax.text(13, 96, "external\ncost $40", color=MUTED, fontsize=9.5)

    ax.set_xlim(0, 60); ax.set_ylim(0, 210)
    ax.set_xlabel("Quantity (thousand gallons / week)", color=PRIMARY)
    ax.set_ylabel("Price ($)", color=PRIMARY)
    ax.set_title("Negative externality: the market overproduces", color=PRIMARY)
    ax.legend(loc="upper right", fontsize=9.5, frameon=False)
    style_ax(ax)
    save(fig, "fig-negative-externality.png")


# ============================================================
# 2. POSITIVE EXTERNALITY — Flu vaccine
#    Supply (MC) = 20 flat; MPB (Demand) = 80 - 1.2Q ; MSB = MPB + 30
#    Market Q where MPB=20 -> 50 ; Social Q where MSB=20 -> 75
# ============================================================
def fig_positive():
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    Q = np.linspace(0, 70, 200)
    MPB = 80 - 1.0 * Q
    MSB = 110 - 1.0 * Q
    S = np.full_like(Q, 20)
    ax.plot(Q, MPB, color=PRIMARY, lw=2.6, label="MPB = Demand")
    ax.plot(Q, MSB, color=SUCCESS, lw=2.6, label="MSB = MPB + external benefit")
    ax.plot(Q, S, color=SECONDARY, lw=2.6, label="Supply (MC = $20)")

    Qm = 60   # 80 - Q = 20
    Qs = 90   # capped by axis; recompute properly below
    Qm = 80 - 20            # =60
    Qs = 110 - 20           # =90 -> off axis, clamp display
    Qm, Qs = 60, 90
    # keep within 0-70 view: rescale by using slope 1, market Q=60, social Q would be 90 -> extend x
    ax.set_xlim(0, 100)
    Q = np.linspace(0, 100, 200)
    MPB = 80 - 1.0 * Q; MSB = 110 - 1.0 * Q; S = np.full_like(Q, 20)
    ax.cla()
    ax.plot(Q, MPB, color=PRIMARY, lw=2.6, label="MPB = Demand")
    ax.plot(Q, MSB, color=SUCCESS, lw=2.6, label="MSB = MPB + external benefit")
    ax.plot(Q, S, color=SECONDARY, lw=2.6, label="Supply (MC = $20)")

    qfill = np.linspace(Qm, Qs, 40)
    ax.fill_between(qfill, 20, 110 - qfill, color=SUCCESS, alpha=0.18,
                    label="Welfare gain forgone (DWL)")
    for (Qx, c, lab, dy) in [(Qm, SECONDARY, "Market\nQ = 60", -1),
                              (Qs, SUCCESS, "Social optimum\nQ* = 90", 1)]:
        ax.plot([Qx, Qx], [0, 20], color=c, ls=":", lw=1.5)
    ax.scatter([Qm, Qs], [20, 20], color=[SECONDARY, SUCCESS], zorder=5, s=55)
    ax.annotate("Market\nQ = 60", (Qm, 20), xytext=(Qm - 4, 30),
                color=SECONDARY, fontweight="bold", fontsize=11, ha="right")
    ax.annotate("Social optimum\nQ* = 90", (Qs, 20), xytext=(Qs - 2, 30),
                color=SUCCESS, fontweight="bold", fontsize=11)
    ax.annotate("", xy=(30, 110 - 30), xytext=(30, 80 - 30),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.3))
    ax.text(32, 64, "external\nbenefit $30", color=MUTED, fontsize=9.5)

    ax.set_ylim(0, 120)
    ax.set_xlabel("Quantity (vaccinations)", color=PRIMARY)
    ax.set_ylabel("Benefit / Price ($)", color=PRIMARY)
    ax.set_title("Positive externality: the market underproduces", color=PRIMARY)
    ax.legend(loc="upper right", fontsize=9.3, frameon=False)
    style_ax(ax)
    save(fig, "fig-positive-externality.png")


# ============================================================
# 3. COASE — Dog barking MB vs MC bars (efficient Q = 2)
# ============================================================
def fig_coase():
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    hours = [1, 2, 3, 4]
    MB = [400, 300, 200, 100]
    MC = [100, 200, 400, 500]
    x = np.arange(len(hours))
    w = 0.38
    ax.bar(x - w/2, MB, w, color=SECONDARY, label="Your marginal benefit")
    ax.bar(x + w/2, MC, w, color=DANGER, label="Neighbor's marginal cost")
    for xi, (b, c) in enumerate(zip(MB, MC)):
        ax.text(xi - w/2, b + 8, f"${b}", ha="center", color=SECONDARY, fontsize=10, fontweight="bold")
        ax.text(xi + w/2, c + 8, f"${c}", ha="center", color=DANGER, fontsize=10, fontweight="bold")
    # shade efficient region (hours 1-2: MB>MC)
    ax.axvspan(-0.5, 1.5, color=SUCCESS, alpha=0.10)
    ax.text(0.5, 470, "MB > MC\nefficient", ha="center", color=SUCCESS,
            fontweight="bold", fontsize=11)
    ax.text(2.5, 470, "MC > MB\nvalue destroyed", ha="center", color=DANGER,
            fontweight="bold", fontsize=11)
    ax.axvline(1.5, color=PRIMARY, ls="--", lw=1.5)
    ax.text(1.5, 530, "Efficient: 2 hrs", ha="center", color=PRIMARY, fontweight="bold", fontsize=11)
    ax.set_xticks(x); ax.set_xticklabels([f"Hour {h}" for h in hours])
    ax.set_ylim(0, 560)
    ax.set_ylabel("Value ($)", color=PRIMARY)
    ax.set_title("Coase bargaining: the efficient amount of barking", color=PRIMARY)
    ax.legend(loc="upper center", fontsize=10, frameon=False, ncol=2)
    style_ax(ax)
    save(fig, "fig-coase-barking.png")


# ============================================================
# 4. PIGOUVIAN TAX — tax shifts MPC up to MSC, Q 35 -> 25
# ============================================================
def fig_pigou():
    fig, ax = plt.subplots(figsize=(7.4, 5.2))
    Q = np.linspace(0, 60, 200)
    D = 200 - 2 * Q
    MPC = 60 + 2 * Q
    MSC = 100 + 2 * Q   # = MPC + $40 tax
    ax.plot(Q, D, color=PRIMARY, lw=2.6, label="Demand")
    ax.plot(Q, MPC, color=SECONDARY, lw=2.4, ls="--", label="MPC (before tax)")
    ax.plot(Q, MSC, color=SUCCESS, lw=2.8, label="MPC + $40 tax = MSC")

    Qs, Ps = 25, 150
    ax.plot([Qs, Qs], [0, Ps], color=SUCCESS, ls=":", lw=1.5)
    ax.plot([0, Qs], [Ps, Ps], color=SUCCESS, ls=":", lw=1.5)
    ax.scatter([35, Qs], [130, Ps], color=[SECONDARY, SUCCESS], zorder=5, s=55)
    ax.annotate("Before tax\nQ = 35", (35, 130), xytext=(37, 96),
                color=SECONDARY, fontweight="bold", fontsize=11)
    ax.annotate("After tax\nQ = 25", (Qs, Ps), xytext=(Qs - 22, Ps + 12),
                color=SUCCESS, fontweight="bold", fontsize=11)
    # tax wedge arrow
    ax.annotate("", xy=(15, 100 + 2*15), xytext=(15, 60 + 2*15),
                arrowprops=dict(arrowstyle="<->", color=ACCENT, lw=1.8))
    ax.text(16, 96, "tax = $40", color=ACCENT, fontsize=10.5, fontweight="bold")
    ax.set_xlim(0, 60); ax.set_ylim(0, 210)
    ax.set_xlabel("Quantity (thousand gallons / week)", color=PRIMARY)
    ax.set_ylabel("Price ($)", color=PRIMARY)
    ax.set_title("A Pigouvian tax internalizes the external cost", color=PRIMARY)
    ax.legend(loc="upper right", fontsize=9.5, frameon=False)
    style_ax(ax)
    save(fig, "fig-pigouvian-tax.png")


# ============================================================
# 5. CAP-AND-TRADE — total abatement cost with vs without trading
# ============================================================
def fig_captrade():
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    cats = ["Without trading", "With trading"]
    vals = [1800, 800]
    colors = [DANGER, SUCCESS]
    bars = ax.bar(cats, vals, color=colors, width=0.55)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 25, f"${v:,}", ha="center",
                fontweight="bold", color=PRIMARY, fontsize=14)
    ax.text(0, 1500, "Each plant cuts\n20 tons equally", ha="center", color="white",
            fontsize=10.5, fontweight="bold")
    ax.text(1, 640, "Plant A (cheap)\ncuts the most;\nothers buy permits", ha="center",
            color="white", fontsize=10.5, fontweight="bold")
    ax.annotate("Same 60-ton cut,\nless than half the cost", xy=(1, 800), xytext=(0.5, 1250),
                ha="center", color=SECONDARY, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SECONDARY, lw=1.6))
    ax.set_ylim(0, 2050)
    ax.set_ylabel("Total abatement cost ($)", color=PRIMARY)
    ax.set_title("Trading hits the cap at the lowest cost", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-cap-trade.png")


# ============================================================
# 6. GLOBAL CARBON PRICES vs Social Cost of Carbon ($190)
# ============================================================
def fig_carbon_prices():
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    labels = ["China\nETS", "California\nC&T", "Canada\ntax", "EU\nETS", "Social cost\nof carbon"]
    vals = [11, 28, 60, 82, 190]   # USD/ton (Canada C$80~US$60, EU €75~$82)
    colors = [SECONDARY, SECONDARY, SECONDARY, SECONDARY, ACCENT]
    bars = ax.bar(labels, vals, color=colors, width=0.62)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 4, f"${v}", ha="center",
                fontweight="bold", color=PRIMARY, fontsize=12)
    ax.axhline(190, color=ACCENT, ls="--", lw=1.6)
    ax.text(0.05, 196, "EPA social cost of carbon ≈ $190/ton", color=ACCENT,
            fontsize=10.5, fontweight="bold")
    ax.set_ylim(0, 215)
    ax.set_ylabel("Carbon price (US$ / ton CO₂)", color=PRIMARY)
    ax.set_title("Most of the world still under-prices carbon", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-carbon-prices.png")


# ============================================================
# 7. OPTIMAL POLLUTION — Marginal abatement cost vs marginal damage
#    Optimum where MAC = MD, NOT at zero pollution
# ============================================================
def fig_optimal():
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    # x = pollution reduced (abatement), 0..100% ; MAC rises steeply near 100% cleanup
    x = np.linspace(0, 100, 200)
    MAC = 0.008 * x**2 + 3        # rises sharply as you approach 100% cleanup
    MD = 80 - 0.6 * x             # marginal damage of remaining pollution falls as you abate more
    ax.plot(x, MAC, color=SECONDARY, lw=2.8, label="Marginal cost of abatement")
    ax.plot(x, MD, color=DANGER, lw=2.8, label="Marginal damage avoided")
    # intersection
    diff = np.abs(MAC - MD)
    ix = diff.argmin()
    xs, ys = x[ix], MAC[ix]
    ax.plot([xs, xs], [0, ys], color=SUCCESS, ls=":", lw=1.6)
    ax.scatter([xs], [ys], color=SUCCESS, zorder=5, s=60)
    ax.annotate("Optimal abatement\n(MAC = MD, not 100%)", (xs, ys), xytext=(xs + 6, ys + 20),
                color=SUCCESS, fontweight="bold", fontsize=11,
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.4))
    ax.text(98, 70, "Cleaning up the\nlast 1% would\ncost a fortune", ha="right",
            color=MUTED, fontsize=9.5)
    ax.set_xlim(0, 100); ax.set_ylim(0, 90)
    ax.set_xlabel("Pollution reduced (%)", color=PRIMARY)
    ax.set_ylabel("$ per unit", color=PRIMARY)
    ax.set_title("The optimal level of pollution is not zero", color=PRIMARY)
    ax.legend(loc="upper center", fontsize=10, frameon=False)
    style_ax(ax)
    save(fig, "fig-optimal-pollution.png")


if __name__ == "__main__":
    fig_negative()
    fig_positive()
    fig_coase()
    fig_pigou()
    fig_captrade()
    fig_carbon_prices()
    fig_optimal()
    print("done")
