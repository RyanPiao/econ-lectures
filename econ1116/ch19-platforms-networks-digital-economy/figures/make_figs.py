#!/usr/bin/env python3
"""Ch 19 — Platforms, Networks & the Digital Economy: lecture figures (White Academia palette)."""
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
# 1. NETWORK DEMAND CURVE — upward then downward (the hump)
#    Willingness to pay rises with network size (core users),
#    then falls as casual, price-sensitive users join.
# ============================================================
def fig_network_demand():
    fig, ax = plt.subplots(figsize=(7.6, 5.2))
    q = np.linspace(0, 100, 400)
    # hump-shaped WTP: rises, peaks, then falls
    p = 10 + 0.95 * q - 0.0098 * q**2
    ax.plot(q, p, color=SECONDARY, lw=3.2)

    # peak
    qpk = q[np.argmax(p)]
    ppk = np.max(p)
    ax.scatter([qpk], [ppk], color=PRIMARY, zorder=6, s=45)
    ax.plot([qpk, qpk], [0, ppk], color=MUTED, ls=":", lw=1.2)

    # shade upward portion
    up = q <= qpk
    ax.fill_between(q[up], 0, p[up], color=SUCCESS, alpha=0.13)
    ax.fill_between(q[~up], 0, p[~up], color=ACCENT, alpha=0.13)

    ax.annotate("network effect dominates\n(core users build it)",
                xy=(22, 24), xytext=(2, 36), color=SUCCESS, fontsize=11,
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.5))
    ax.annotate("price effect dominates\n(casual users, price-sensitive)",
                xy=(80, 18), xytext=(52, 33), color=ACCENT, fontsize=11,
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.5))
    ax.text(qpk, ppk + 1.4, "tipping zone", ha="center", color=PRIMARY,
            fontsize=10.5, fontweight="bold")

    ax.set_xlim(0, 100); ax.set_ylim(0, 42)
    ax.set_xlabel("Network size (number of users)", color=PRIMARY)
    ax.set_ylabel("Willingness to pay ($)", color=PRIMARY)
    ax.set_title("The network demand curve: it rises before it falls", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-network-demand.png")


# ============================================================
# 2. TIPPING POINT — virtuous vs vicious adoption paths
#    Above critical mass -> S-curve to dominance; below -> collapse.
# ============================================================
def fig_tipping():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    t = np.linspace(0, 12, 400)
    # virtuous: logistic to 100
    virt = 100 / (1 + np.exp(-1.05 * (t - 5.2)))
    # vicious: decays toward 0 after a small start
    vic = 22 * np.exp(-0.42 * t) + 1.5
    ax.plot(t, virt, color=SUCCESS, lw=3.2, label="Above critical mass → virtuous cycle")
    ax.plot(t, vic, color=DANGER, lw=3.2, ls="--", label="Below critical mass → vicious cycle")

    # critical-mass threshold
    ax.axhline(20, color=MUTED, ls=":", lw=1.4)
    ax.text(0.2, 22, "tipping point (critical mass)", color=MUTED, fontsize=10.5,
            fontweight="bold")

    ax.annotate("Facebook, Amazon Prime", xy=(8.5, 95), xytext=(5.2, 70),
                color=SUCCESS, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.4))
    ax.annotate("Google+, MySpace", xy=(7.5, 2.8), xytext=(6.0, 22),
                color=DANGER, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.4))

    ax.set_xlim(0, 12); ax.set_ylim(0, 108)
    ax.set_xlabel("Time", color=PRIMARY)
    ax.set_ylabel("Users / value of the network", color=PRIMARY)
    ax.set_title("Tipping points: the same start, two destinies", color=PRIMARY)
    ax.legend(loc="center right", fontsize=10.5, frameon=False)
    style_ax(ax)
    save(fig, "fig-tipping.png")


# ============================================================
# 3. METCALFE'S LAW — network value scaling: n^2 vs n log n vs n
# ============================================================
def fig_metcalfe():
    fig, ax = plt.subplots(figsize=(7.6, 5.0))
    n = np.linspace(1, 100, 400)
    sq = n**2
    nlogn = n * np.log(n + 1) * (10000 / (100 * np.log(101)))   # rescaled to share top point
    lin = n * (10000 / 100)
    ax.plot(n, sq, color=SECONDARY, lw=3.2, label="Metcalfe:  V ∝ n²")
    ax.plot(n, nlogn, color=ACCENT, lw=3.0, ls="--", label="Odlyzko–Tilly:  V ∝ n·log n")
    ax.plot(n, lin, color=MUTED, lw=2.4, ls=":", label="Linear:  V ∝ n")

    ax.annotate("value explodes as\nusers are added", xy=(85, 85**2),
                xytext=(40, 8200), color=SECONDARY, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SECONDARY, lw=1.5))

    ax.set_xlim(0, 100); ax.set_ylim(0, 10500)
    ax.set_xlabel("Number of users (n)", color=PRIMARY)
    ax.set_ylabel("Network value (V)", color=PRIMARY)
    ax.set_title("Why size compounds: the value of a network", color=PRIMARY)
    ax.legend(loc="upper left", fontsize=10.5, frameon=False)
    style_ax(ax)
    save(fig, "fig-metcalfe.png")


# ============================================================
# 4. TAKE RATE — the platform's cut, across platforms
# ============================================================
def fig_take_rate():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    plats = ["Airbnb\n(host+guest)", "Apple App\nStore", "Uber\nrides",
             "Amazon 3P\n(effective)"]
    rates = [17, 30, 28, 45]
    colors = [SUCCESS, SECONDARY, ACCENT, DANGER]
    bars = ax.bar(plats, rates, width=0.6, color=colors)
    for b, r in zip(bars, rates):
        ax.text(b.get_x() + b.get_width()/2, r + 1.2, f"{r}%", ha="center",
                fontweight="bold", color=PRIMARY, fontsize=14)
    ax.axhline(0, color=MUTED, lw=1.0)
    ax.text(3, 39, "commissions + FBA\n+ ads bundled in", ha="center",
            color=DANGER, fontsize=9.5, fontweight="bold")
    ax.set_ylim(0, 52)
    ax.set_ylabel("Take rate (% of each transaction)", color=PRIMARY)
    ax.set_title("The take rate: how much of every dollar the platform keeps", color=PRIMARY)
    style_ax(ax)
    save(fig, "fig-take-rate.png")


# ============================================================
# 5. TWO-SIDED PRICING — subsidize the price-sensitive side,
#    extract from the value side (the price STRUCTURE).
# ============================================================
def fig_two_sided():
    fig, ax = plt.subplots(figsize=(8.0, 5.0))
    ax.axis("off")

    # platform box in the middle
    ax.add_patch(plt.Rectangle((0.40, 0.36), 0.20, 0.28, fc=SECONDARY,
                               ec=PRIMARY, lw=1.5, alpha=0.92))
    ax.text(0.50, 0.50, "PLATFORM", ha="center", va="center", color="white",
            fontsize=14, fontweight="bold")

    # left side: subsidized (consumers)
    ax.add_patch(plt.Rectangle((0.02, 0.36), 0.26, 0.28, fc=SUCCESS,
                               ec=PRIMARY, lw=1.4, alpha=0.85))
    ax.text(0.15, 0.555, "Side A — users", ha="center", color="white",
            fontsize=12.5, fontweight="bold")
    ax.text(0.15, 0.47, "price-sensitive\n→ subsidize\n(free / rewards)",
            ha="center", va="center", color="white", fontsize=11)

    # right side: monetized (advertisers/merchants)
    ax.add_patch(plt.Rectangle((0.72, 0.36), 0.26, 0.28, fc=ACCENT,
                               ec=PRIMARY, lw=1.4, alpha=0.88))
    ax.text(0.85, 0.555, "Side B — payers", ha="center", color="white",
            fontsize=12.5, fontweight="bold")
    ax.text(0.85, 0.47, "value-rich\n→ extract\n(fees / ads)",
            ha="center", va="center", color="white", fontsize=11)

    # arrows
    ax.annotate("", xy=(0.40, 0.50), xytext=(0.28, 0.50),
                arrowprops=dict(arrowstyle="<->", color=PRIMARY, lw=2.0))
    ax.annotate("", xy=(0.72, 0.50), xytext=(0.60, 0.50),
                arrowprops=dict(arrowstyle="<->", color=PRIMARY, lw=2.0))

    # cross-side effect loop
    ax.annotate("more A attract more B — and more B attract more A",
                xy=(0.5, 0.30), ha="center", color=MUTED, fontsize=11.5,
                fontweight="bold")
    ax.annotate("", xy=(0.74, 0.66), xytext=(0.26, 0.66),
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.8,
                                connectionstyle="arc3,rad=-0.35"))
    ax.annotate("", xy=(0.26, 0.34), xytext=(0.74, 0.34),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=1.8,
                                connectionstyle="arc3,rad=-0.35"))

    ax.text(0.5, 0.82, "Price STRUCTURE beats price LEVEL", ha="center",
            color=PRIMARY, fontsize=15, fontweight="bold")
    ax.text(0.5, 0.10, "Rochet & Tirole (2003): who pays matters more than how much",
            ha="center", color=MUTED, fontsize=11, fontstyle="italic")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    save(fig, "fig-two-sided.png")


# ============================================================
# 6. BUNDLING — separate sales vs bundle (heterogeneous tastes)
#    Aisha: A=$15, B=$5 ; Kaito: A=$6, B=$14 ; MC ~ 0
# ============================================================
def fig_bundling():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    labels = ["Sell separately\n(best uniform prices)", "Sell as a bundle\n($20 each)"]
    revenue = [40, 40]  # placeholder, recompute below
    # Separate: price A at $6 (both buy) = $12, price B at $5 (both buy) = $10 -> $22
    #   OR price A at $15 (1 buys)=$15, B at $14 (1 buys)=$14 -> $29. Best separate = $29.
    # Bundle at $20: Aisha values 20, Kaito values 20 -> both buy -> 2*20 = $40.
    revenue = [29, 40]
    bars = ax.bar(labels, revenue, width=0.5, color=[MUTED, SUCCESS])
    for b, r in zip(bars, revenue):
        ax.text(b.get_x() + b.get_width()/2, r + 0.8, f"${r}", ha="center",
                fontweight="bold", color=PRIMARY, fontsize=15)
    ax.annotate("+$11 from bundling\n(≈ 38% more)", xy=(1, 40), xytext=(0.30, 35),
                ha="center", color=SUCCESS, fontsize=11.5, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.6))
    ax.set_ylim(0, 48)
    ax.set_ylabel("Total revenue ($)", color=PRIMARY)
    ax.set_title("Bundling captures more when tastes diverge", color=PRIMARY)
    ax.text(0.5, -7.2, "Aisha values A=$15, B=$5  ·  Kaito values A=$6, B=$14  ·  MC ≈ $0",
            ha="center", color=MUTED, fontsize=10, transform=ax.transData)
    style_ax(ax)
    save(fig, "fig-bundling.png")


# ============================================================
# 7. AI COST STRUCTURE — huge fixed cost, near-zero marginal cost
#    -> falling LRAC = natural-oligopoly tendency
# ============================================================
def fig_ai_cost():
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    q = np.linspace(0.5, 100, 400)   # billions of queries
    FC = 191.0   # $M training (Gemini-ish)
    mc = 0.02    # near-zero marginal cost per (billion) queries, falling
    atc = FC / q + mc
    ax.plot(q, atc, color=SECONDARY, lw=3.2, label="LRAC = fixed ÷ queries + (~0 MC)")
    ax.axhline(mc, color=ACCENT, lw=2.4, ls="--", label="Marginal cost ≈ 0 (inference, ↓280×)")

    ax.annotate("enormous fixed cost\n(train the model: ~$191M)",
                xy=(6, FC/6 + mc), xytext=(22, 26),
                color=DANGER, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=1.5))
    ax.annotate("cost per query → ~0\nas scale grows",
                xy=(80, FC/80 + mc), xytext=(48, 12),
                color=SUCCESS, fontsize=11, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SUCCESS, lw=1.5))

    ax.set_xlim(0, 100); ax.set_ylim(0, 32)
    ax.set_xlabel("Queries served (billions)", color=PRIMARY)
    ax.set_ylabel("Average cost ($ per billion queries)", color=PRIMARY)
    ax.set_title("AI economics: pay once to train, serve forever for ~nothing", color=PRIMARY)
    ax.legend(loc="upper right", fontsize=10.5, frameon=False)
    style_ax(ax)
    save(fig, "fig-ai-cost.png")


if __name__ == "__main__":
    fig_network_demand()
    fig_tipping()
    fig_metcalfe()
    fig_take_rate()
    fig_two_sided()
    fig_bundling()
    fig_ai_cost()
    print("done")
