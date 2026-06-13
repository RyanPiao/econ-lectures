#!/usr/bin/env python3
"""Ch 17 — Public Goods, Commons & Government: lecture figures (White Academia palette)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.patches import FancyBboxPatch
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
# 1. GOODS MATRIX — rivalry x excludability 2x2
# ============================================================
def fig_matrix():
    fig, ax = plt.subplots(figsize=(8.4, 5.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis("off")

    cells = [
        # (x, y, fill, title, examples)
        (0.2, 5.2, "#eef2f5", "PRIVATE GOODS", "pizza · sneakers · a haircut", SECONDARY),
        (5.1, 5.2, "#fdf3f3", "COMMON RESOURCES", "ocean fish · clean air · a\ncongested road", DANGER),
        (0.2, 0.3, "#f3f0ea", "CLUB GOODS", "Netflix · toll roads · a gym\nmembership", ACCENT),
        (5.1, 0.3, "#eef5ee", "PUBLIC GOODS", "national defense · streetlights\nWikipedia · GPS", SUCCESS),
    ]
    for (x, y, fill, title, ex, c) in cells:
        box = FancyBboxPatch((x, y), 4.7, 4.4, boxstyle="round,pad=0.02,rounding_size=0.18",
                             linewidth=2.2, edgecolor=c, facecolor=fill)
        ax.add_patch(box)
        ax.text(x + 2.35, y + 3.5, title, ha="center", va="center",
                fontsize=14.5, fontweight="bold", color=c)
        ax.text(x + 2.35, y + 1.7, ex, ha="center", va="center",
                fontsize=11.5, color=PRIMARY)

    # axis labels
    ax.annotate("", xy=(10, -0.35), xytext=(0.2, -0.35),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4),
                annotation_clip=False)
    ax.text(2.55, -0.95, "EXCLUDABLE", ha="center", fontsize=11.5,
            fontweight="bold", color=MUTED)
    ax.text(7.45, -0.95, "NOT EXCLUDABLE", ha="center", fontsize=11.5,
            fontweight="bold", color=MUTED)
    ax.annotate("", xy=(-0.35, 10), xytext=(-0.35, 0.3),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.4),
                annotation_clip=False)
    ax.text(-0.95, 7.4, "RIVAL", ha="center", va="center", rotation=90,
            fontsize=11.5, fontweight="bold", color=MUTED)
    ax.text(-0.95, 2.5, "NOT RIVAL", ha="center", va="center", rotation=90,
            fontsize=11.5, fontweight="bold", color=MUTED)
    ax.set_title("Two questions classify every good in the economy",
                 color=PRIMARY, pad=14)
    save(fig, "fig-goods-matrix.png")


# ============================================================
# 2. PUBLIC GOOD DEMAND — vertical summation (Leo + Rachel snowplow)
#    Leo:  P = 6 - 0.5Q ;  Rachel: P = 4 - 0.5Q
#    Social (vertical sum) = 10 - Q ;  MC = $5  ->  Q* = 5
# ============================================================
def fig_public_demand():
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    Q = np.linspace(0, 10, 200)
    leo = np.clip(6 - 0.5 * Q, 0, None)
    rachel = np.clip(4 - 0.5 * Q, 0, None)
    social = np.clip(10 - 1.0 * Q, 0, None)
    ax.plot(Q, leo, color=SECONDARY, lw=2.4, label="Leo's willingness to pay")
    ax.plot(Q, rachel, color=ACCENT, lw=2.4, label="Rachel's willingness to pay")
    ax.plot(Q, social, color=PRIMARY, lw=3.0, label="Social WTP (vertical sum)")
    ax.axhline(5, color=DANGER, ls="--", lw=2.0, label="Marginal cost = $5")

    # optimum Q* = 5
    ax.plot([5, 5], [0, 5], color=SUCCESS, ls=":", lw=1.6)
    ax.scatter([5], [5], color=SUCCESS, zorder=5, s=60)
    ax.annotate("Efficient\nQ* = 5 days", (5, 5), xytext=(5.5, 6.4),
                color=SUCCESS, fontweight="bold", fontsize=11.5,
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.4))
    # vertical-sum illustration at Q=2
    ax.annotate("", xy=(2, 8), xytext=(2, 0),
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8, ls=":"))
    ax.text(2.15, 8.3, "add WTP\nvertically", color=MUTED, fontsize=9.5)

    ax.set_xlim(0, 10); ax.set_ylim(0, 11)
    ax.set_xlabel("Days of snowplowing (a public good)", color=PRIMARY)
    ax.set_ylabel("Willingness to pay ($ / day)", color=PRIMARY)
    ax.set_title("Public-good demand: sum WTP vertically, not quantities", color=PRIMARY)
    ax.legend(loc="upper right", fontsize=9.8, frameon=False)
    style_ax(ax)
    save(fig, "fig-public-demand.png")


# ============================================================
# 3. FREE-RIDER GAP — the neighborhood fountain
#    Social benefit $20,000 ; Cost $7,000 ; Voluntary $3,000
# ============================================================
def fig_free_rider():
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    cats = ["Total social\nbenefit", "Cost to\nbuild", "Voluntary\ncontributions"]
    vals = [20000, 7000, 3000]
    colors = [SUCCESS, SECONDARY, DANGER]
    bars = ax.bar(cats, vals, color=colors, width=0.58)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 350, f"${v:,}", ha="center",
                fontweight="bold", color=PRIMARY, fontsize=13)
    # cost line
    ax.axhline(7000, color=SECONDARY, ls="--", lw=1.4, alpha=0.7)
    ax.annotate("Passes the cost-benefit test\n($20k > $7k)...", xy=(0, 20000),
                xytext=(0.45, 16500), ha="center", color=SUCCESS,
                fontsize=10.5, fontweight="bold")
    ax.annotate("...but free-riding leaves\nit $4,000 short", xy=(2, 3000),
                xytext=(1.75, 9500), ha="center", color=DANGER, fontsize=10.5,
                fontweight="bold", arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.5))
    ax.set_ylim(0, 22500)
    ax.set_ylabel("Dollars", color=PRIMARY)
    ax.set_title("The free-rider problem: the fountain doesn't get built", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-free-rider.png")


# ============================================================
# 4. TRAGEDY OF THE COMMONS — total catch vs total fishing hours
#    20->160, 40->240, 60->240, 80->160, 100->100 (peak ~40-50)
# ============================================================
def fig_fishery():
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    hrs = np.array([0, 20, 40, 60, 80, 100])
    catch = np.array([0, 160, 240, 240, 160, 100])
    # smooth curve through points
    xs = np.linspace(0, 100, 200)
    coeffs = np.polyfit(hrs, catch, 3)
    ys = np.polyval(coeffs, xs)
    ax.plot(xs, ys, color=SECONDARY, lw=2.8)
    ax.scatter(hrs[1:], catch[1:], color=SECONDARY, zorder=5, s=45)

    # social optimum ~40 hrs (max sustainable yield)
    ax.plot([40, 40], [0, 240], color=SUCCESS, ls=":", lw=1.8)
    ax.scatter([40], [240], color=SUCCESS, zorder=6, s=80)
    ax.annotate("Social optimum\n40 hrs, 240 fish", (40, 240), xytext=(8, 255),
                color=SUCCESS, fontweight="bold", fontsize=11)
    # open-access equilibrium ~80 hrs
    ax.plot([80, 80], [0, 160], color=DANGER, ls=":", lw=1.8)
    ax.scatter([80], [160], color=DANGER, zorder=6, s=80)
    ax.annotate("Open-access\nover-fishing\n80+ hrs", (80, 160), xytext=(84, 120),
                color=DANGER, fontweight="bold", fontsize=11)
    ax.annotate("", xy=(78, 70), xytext=(42, 70),
                arrowprops=dict(arrowstyle="->", color=MUTED, lw=1.6))
    ax.text(60, 50, "each fisher's private\nincentive pushes here", ha="center",
            color=MUTED, fontsize=9.5)

    ax.set_xlim(0, 105); ax.set_ylim(0, 285)
    ax.set_xlabel("Total fishing hours (all 10 fishers)", color=PRIMARY)
    ax.set_ylabel("Total daily catch (fish)", color=PRIMARY)
    ax.set_title("Tragedy of the commons: rational use, collective ruin", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-fishery.png")


# ============================================================
# 5. MEDIAN VOTER — five voters' ideal park-spending points
# ============================================================
def fig_median():
    fig, ax = plt.subplots(figsize=(8.0, 4.4))
    voters = [0, 10, 20, 30, 100]      # thousands of $
    colors = [SECONDARY, SECONDARY, SUCCESS, SECONDARY, SECONDARY]
    sizes = [240, 240, 560, 240, 240]
    ax.scatter(voters, [1]*5, s=sizes, color=colors, zorder=5, edgecolor="white", linewidth=1.5)
    for v, c in zip(voters, colors):
        ax.annotate(f"${v}k", (v, 1), xytext=(v, 0.42), ha="center", color=PRIMARY,
                    fontsize=11.5, fontweight="bold")
    ax.annotate("Median voter", (20, 1), xytext=(20, 1.52), ha="center", color=SUCCESS,
                fontweight="bold", fontsize=12)
    # median line
    ax.axvline(20, color=SUCCESS, ls="--", lw=1.8)
    ax.annotate("Majority vote settles here →\nthe median voter wins", (20, 1),
                xytext=(33, 2.15), color=SUCCESS, fontweight="bold", fontsize=11.5,
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.5))
    ax.set_xlim(-8, 110); ax.set_ylim(0, 2.6)
    ax.set_yticks([])
    ax.set_xlabel("Preferred annual park spending ($ thousands)", color=PRIMARY)
    ax.set_title("The median voter theorem: the middle decides", color=PRIMARY)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=MUTED, labelsize=11)
    for lbl in ax.get_xticklabels():
        lbl.set_color(PRIMARY)
    save(fig, "fig-median-voter.png")


if __name__ == "__main__":
    fig_matrix()
    fig_public_demand()
    fig_free_rider()
    fig_fishery()
    fig_median()
    print("done")
