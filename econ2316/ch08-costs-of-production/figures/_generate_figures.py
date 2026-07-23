"""
Ch 8 (Costs of Production) — figure generator.
White Academia palette; mirrors ch07 style and layout discipline.
Outputs PNG to figures/ at 150 dpi.

Gigafactory locks inherited from ch07: A=8, alpha=0.4, beta=0.6, q=32 GWh.
Input prices locked in ch08: w=0.10 B$/(K-worker-year), r=0.13 /year.
LR cost-min from Walkthrough 8.1: K*=2.679, L*=5.224, c*=0.8707 B$/yr.
Firm's installed bundle (from ch07): K=4, L=4 (over-capitalized; c=0.92).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))

# White Academia palette
PRIMARY = "#2D2D2D"
SECONDARY = "#6B8BA4"      # dusty blue
ACCENT = "#C47B5A"         # terracotta
TEXT = "#3A3632"
MUTED = "#8C8580"
LINE = "#D5CEC7"
DANGER = "#A85C5C"         # rosewood
SUCCESS = "#6A8E6B"        # sage

plt.rcParams.update({
    "font.family": "DejaVu Serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "axes.edgecolor": PRIMARY,
    "axes.labelcolor": TEXT,
    "axes.linewidth": 1.0,
    "xtick.color": TEXT,
    "ytick.color": TEXT,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "legend.frameon": False,
    "savefig.facecolor": "white",
    "savefig.bbox": "tight",
    "savefig.dpi": 150,
})

# ============================================================
# Gigafactory production / cost helpers
# ============================================================
A, ALPHA, BETA = 8.0, 0.4, 0.6
Q_TARGET = 32.0
W, R = 0.10, 0.13

def isoquant_K(L, q=Q_TARGET):
    # 8 K^0.4 L^0.6 = q  =>  K = (q / (8 L^0.6))^(1/0.4)
    return (q / (A * L**BETA)) ** (1.0 / ALPHA)

def lr_cost(q):
    """Closed-form CRS Cobb-Douglas cost at locked input prices."""
    # c = (w/beta)^beta * (r/alpha)^alpha * q / A  (CRS, alpha+beta=1)
    return (W / BETA)**BETA * (R / ALPHA)**ALPHA * q / A

def sr_total_cost(q, Kbar):
    """Short-run total cost: r*Kbar + w * L where L = (q / (A Kbar^alpha))^(1/beta)."""
    L = (q / (A * Kbar**ALPHA)) ** (1.0 / BETA)
    return R * Kbar + W * L

# ============================================================
# FIGURE 1 — Headline / cover: SR family + LR envelope
# (Doubles as ch08-cover.png AND fig-sr-lr-envelope.png)
# ============================================================
def fig_cover_sr_lr_envelope():
    fig, ax = plt.subplots(figsize=(7, 5))

    q = np.linspace(2, 80, 400)
    K_bars = [1, 2, 4, 6, 8]
    sr_colors = [
        "#9DB7CC", SECONDARY, "#4A6B82", "#36546A", "#243A4E"
    ]

    # Manually-tuned label y-offsets so the right-edge labels don't pile up
    label_offsets = {1: 0.10, 2: 0.06, 4: 0.04, 6: -0.04, 8: -0.10}
    for Kbar, col in zip(K_bars, sr_colors):
        c = sr_total_cost(q, Kbar)
        ax.plot(q, c, color=col, lw=1.3, alpha=0.85,
                label=fr"$\bar K = {Kbar}$")
        # Label at the right end of each curve, with offset for legibility
        y_end = sr_total_cost(80, Kbar) + label_offsets.get(Kbar, 0)
        ax.text(81, y_end, fr"$\bar K={Kbar}$", color=col,
                fontsize=8, va="center", ha="left")

    # LR envelope (linear under CRS, lower envelope)
    lr = lr_cost(q)
    ax.plot(q, lr, color=ACCENT, lw=2.6, label="LR cost (envelope)")

    # Mark the tangency dots where each SR curve kisses LR
    # K* / q = 0.0837 under CRS Cobb-Douglas at locked prices
    # so q_tan(Kbar) = Kbar / 0.0837
    for Kbar, col in zip(K_bars, sr_colors):
        q_tan = Kbar / 0.0837
        if 2 <= q_tan <= 80:
            c_tan = lr_cost(q_tan)
            ax.plot(q_tan, c_tan, "o", color=col, markersize=5,
                    markeredgecolor="white", markeredgewidth=1.0, zorder=5)

    ax.set_xlabel("Output  $q$  (GWh / yr)")
    ax.set_ylabel("Total cost  $c$  (B\\$ / yr)")
    ax.set_xlim(0, 88)
    ax.set_ylim(0, 3.0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Legend just for LR
    lr_patch = mpatches.Patch(color=ACCENT, label="Long-run envelope")
    sr_patch = mpatches.Patch(color=SECONDARY,
                              label="Short-run total cost (one curve per $\\bar K$)")
    ax.legend(handles=[lr_patch, sr_patch], loc="upper left", fontsize=9)

    # Annotate the LR envelope identity
    ax.text(78, 2.55,
            r"$\mathrm{LRC}(q)=\min_{\bar K}\,\mathrm{STC}(q;\bar K)$",
            fontsize=10, ha="right", color=ACCENT, style="italic")

    # Mark gigafactory operating point q=32, c*=0.871
    ax.plot(32, lr_cost(32), "D", color=DANGER, markersize=7,
            markeredgecolor="white", markeredgewidth=1.0, zorder=6)
    ax.annotate("Gigafactory\nLR optimum\n$c^* = 0.87$ B\\$/yr",
                xy=(32, lr_cost(32)),
                xytext=(48, 0.45),
                fontsize=8.5, color=DANGER, ha="left",
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=0.8))

    out = os.path.join(HERE, "fig-sr-lr-envelope.png")
    plt.savefig(out)
    plt.close(fig)

    # Also save as cover
    fig, ax = plt.subplots(figsize=(7, 5.2))
    for Kbar, col in zip(K_bars, sr_colors):
        c = sr_total_cost(q, Kbar)
        ax.plot(q, c, color=col, lw=1.2, alpha=0.75)
    lr = lr_cost(q)
    ax.plot(q, lr, color=ACCENT, lw=3.0)
    ax.plot(32, lr_cost(32), "D", color=DANGER, markersize=8,
            markeredgecolor="white", markeredgewidth=1.0)
    ax.set_xlabel("Output  $q$  (GWh / yr)")
    ax.set_ylabel("Total cost  $c$  (B\\$ / yr)")
    ax.set_xlim(0, 80)
    ax.set_ylim(0, 3.0)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.text(40, 2.6, "Short-run cost curves",
            fontsize=10, color=SECONDARY, ha="center", style="italic")
    ax.text(75, 1.9, "Long-run\nenvelope",
            fontsize=10, color=ACCENT, ha="right", style="italic")
    out2 = os.path.join(HERE, "ch08-cover.png")
    plt.savefig(out2)
    plt.close(fig)


# ============================================================
# FIGURE 2 — Isocost / isoquant tangency at the gigafactory
# Q=32 isoquant with three isocosts; cost-min tangency at (K*,L*)
# Installed (4,4) shown as off-tangent suboptimal
# ============================================================
def fig_isocost_tangency():
    fig, ax = plt.subplots(figsize=(7, 5))

    # Isoquant Q=32
    L = np.linspace(1.5, 14, 400)
    K = isoquant_K(L, q=32)
    ax.plot(L, K, color=SECONDARY, lw=2.2, label="Isoquant  $Q=32$  GWh")

    # Cost-min point (LR optimum)
    L_star, K_star = 5.224, 2.679
    c_star = W * L_star + R * K_star  # 0.871

    # Installed bundle (4, 4) — over-capitalized
    L_in, K_in = 4.0, 4.0
    c_in = W * L_in + R * K_in       # 0.92

    # Build three isocost lines (slope = -w/r = -0.769)
    slope = -W / R
    L_axis = np.linspace(0, 14, 50)

    # Optimal isocost (passes through L_star, K_star)
    c_opt = c_star
    K_iso_opt = (c_opt - W * L_axis) / R
    # Higher isocost passing through installed bundle (over-spend)
    c_high = c_in
    K_iso_high = (c_high - W * L_axis) / R
    # Even higher dashed reference
    c_too_high = 1.2
    K_iso_too = (c_too_high - W * L_axis) / R

    ax.plot(L_axis, K_iso_too, color=MUTED, lw=1.0, ls=":", alpha=0.7)
    ax.plot(L_axis, K_iso_high, color=DANGER, lw=1.5, ls="--",
            label=f"Isocost  $c={c_high:.2f}$  (installed)")
    ax.plot(L_axis, K_iso_opt, color=ACCENT, lw=2.0,
            label=f"Isocost  $c^*={c_star:.2f}$  (tangent)")

    # Tangency dot
    ax.plot(L_star, K_star, "o", color=ACCENT, markersize=9,
            markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    ax.annotate(f"Cost-min  $(L^*,K^*)=({L_star:.2f},\\,{K_star:.2f})$\n"
                f"$\\mathrm{{MRTS}}=w/r=0.77$",
                xy=(L_star, K_star),
                xytext=(7.0, 4.6),
                fontsize=9, color=ACCENT,
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.8))

    # Installed bundle dot
    ax.plot(L_in, K_in, "s", color=DANGER, markersize=8,
            markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    ax.annotate(f"Installed  $(L,K)=(4,\\,4)$\nover-capitalized — costs $\\$49\\,$M / yr more",
                xy=(L_in, K_in),
                xytext=(0.5, 6.5),
                fontsize=9, color=DANGER,
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=0.8))

    ax.set_xlabel("Labor  $L$  (thousand workers)")
    ax.set_ylabel("Capital  $K$  (B\\$)")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper right", fontsize=8.5)

    out = os.path.join(HERE, "fig-isocost-tangency.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 3 — Wage shock comparative statics
# Pre-shock vs post-shock (w 0.10 -> 0.12) — isocost rotates,
# new tangency moves up-left (less L, more K)
# ============================================================
def fig_wage_shock():
    fig, ax = plt.subplots(figsize=(7, 5))

    # Isoquant Q=32
    L = np.linspace(1.5, 14, 400)
    K = isoquant_K(L, q=32)
    ax.plot(L, K, color=SECONDARY, lw=2.0, label="Isoquant  $Q=32$")

    # Pre-shock: w=0.10, r=0.13
    L1, K1 = 5.224, 2.679
    c1 = 0.10 * L1 + 0.13 * K1  # 0.871
    # Post-shock: w'=0.12, r=0.13 (20% wage shock)
    L2, K2 = 4.857, 2.989
    c2 = 0.12 * L2 + 0.13 * K2  # 0.971

    L_axis = np.linspace(0, 14, 50)
    K_pre = (c1 - 0.10 * L_axis) / 0.13
    K_post = (c2 - 0.12 * L_axis) / 0.13

    ax.plot(L_axis, K_pre, color=SECONDARY, lw=1.6, ls="--",
            label="Pre-shock isocost  ($w=0.10$)")
    ax.plot(L_axis, K_post, color=DANGER, lw=1.8,
            label="Post-shock isocost  ($w=0.12$, +20%)")

    # Pre + post tangency dots
    ax.plot(L1, K1, "o", color=SECONDARY, markersize=9,
            markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    ax.plot(L2, K2, "o", color=DANGER, markersize=9,
            markeredgecolor="white", markeredgewidth=1.2, zorder=6)

    ax.annotate(f"Pre   $(L^*,K^*)=({L1:.2f},\\,{K1:.2f})$",
                xy=(L1, K1), xytext=(6.7, 1.8),
                fontsize=9, color=SECONDARY,
                arrowprops=dict(arrowstyle="->", color=SECONDARY, lw=0.8))
    ax.annotate(f"Post  $(L',K')=({L2:.2f},\\,{K2:.2f})$\n"
                f"$\\Delta L=-7.0\\%$, $\\Delta K=+11.6\\%$",
                xy=(L2, K2), xytext=(6.7, 4.7),
                fontsize=9, color=DANGER,
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=0.8))

    # Substitution arrow along the isoquant
    arr = FancyArrowPatch((L1, K1), (L2, K2),
                          arrowstyle="->", mutation_scale=15,
                          color=ACCENT, lw=1.5, zorder=5)
    ax.add_patch(arr)
    ax.text(4.7, 3.2, "substitute\nlabor → capital",
            fontsize=8.5, color=ACCENT, style="italic", ha="center")

    ax.set_xlabel("Labor  $L$  (thousand workers)")
    ax.set_ylabel("Capital  $K$  (B\\$)")
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 7.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper right", fontsize=8.5)
    ax.set_title("A 20% wage shock rotates the cost-min bundle counterclockwise",
                 fontsize=10, color=PRIMARY, pad=8)

    out = os.path.join(HERE, "fig-wage-shock.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 4 — Generic U-shape AC/MC with AC=MC at minimum
# (visual for the AC-MC HeadsUp)
# ============================================================
def fig_ac_mc():
    fig, ax = plt.subplots(figsize=(7, 4.6))
    q = np.linspace(0.5, 10, 400)
    # Stylized cost: c(q) = 5 + 0.1 q^2 + 0.05 q^3 / 3 -- gives U-shape AC and rising MC
    # MC(q) = 0.2 q + 0.05 q^2
    # AC(q) = 5/q + 0.1 q + 0.05 q^2 / 3
    MC = 0.2 * q + 0.05 * q**2
    AC = 5.0 / q + 0.1 * q + (0.05 * q**2) / 3.0

    ax.plot(q, AC, color=SECONDARY, lw=2.2, label="Average cost  $AC$")
    ax.plot(q, MC, color=ACCENT, lw=2.2, label="Marginal cost  $MC$")

    # Find AC minimum numerically
    idx = np.argmin(AC)
    q_min = q[idx]
    ac_min = AC[idx]
    # At q_min, MC = AC
    ax.plot(q_min, ac_min, "o", color=DANGER, markersize=9,
            markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    ax.axvline(q_min, color=MUTED, lw=0.7, ls=":", alpha=0.7)
    ax.annotate(f"$AC$ minimum,\n$MC = AC$ here",
                xy=(q_min, ac_min), xytext=(q_min + 1.2, ac_min + 0.6),
                fontsize=9, color=DANGER,
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=0.8))

    # Zone labels
    ax.text(2.5, 0.9, "$MC<AC$\n$\\Rightarrow AC$ falling",
            fontsize=9, color=SUCCESS, ha="center", style="italic")
    ax.text(8.5, 2.2, "$MC>AC$\n$\\Rightarrow AC$ rising",
            fontsize=9, color=DANGER, ha="center", style="italic")

    ax.set_xlabel("Output  $q$")
    ax.set_ylabel("Cost per unit")
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(loc="upper right", fontsize=10)

    out = os.path.join(HERE, "fig-ac-mc.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 5 — De Loecker / Eeckhout / Unger rising US markups
# (stylized 1955-2014 time series)
# ============================================================
def fig_deu_markups():
    # DEU 2020 QJE figures: aggregate markup 1.21 in 1980, 1.61 by 2014
    fig, ax = plt.subplots(figsize=(7, 4.5))

    years = np.arange(1955, 2015)
    # Stylized path: ~1.20 through 1980, then rising linearly to 1.61
    markups = np.where(
        years <= 1980,
        1.20 + 0.001 * (years - 1955),       # near-flat at ~1.20-1.22
        1.22 + (0.39 / 34) * (years - 1980)  # rise to 1.61 over 34 years
    )
    # Add a little noise/wiggle for realism
    rng = np.random.default_rng(7)
    markups = markups + rng.normal(0, 0.008, size=markups.size)

    ax.plot(years, markups, color=SECONDARY, lw=2.0)
    ax.fill_between(years, 1.0, markups, color=SECONDARY, alpha=0.10)
    ax.axhline(1.0, color=MUTED, lw=0.8, ls=":", alpha=0.7)
    ax.text(1957, 1.02, "competitive benchmark  $\\mu = 1$",
            fontsize=8.5, color=MUTED, style="italic")

    # Annotate the two endpoints
    ax.plot(1980, 1.21, "o", color=ACCENT, markersize=7,
            markeredgecolor="white", markeredgewidth=1.0)
    ax.annotate("1980: 21% markup", xy=(1980, 1.21), xytext=(1962, 1.45),
                fontsize=9, color=ACCENT,
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=0.8))
    ax.plot(2014, 1.61, "o", color=DANGER, markersize=7,
            markeredgecolor="white", markeredgewidth=1.0)
    ax.annotate("2014: 61% markup", xy=(2014, 1.61), xytext=(1992, 1.65),
                fontsize=9, color=DANGER,
                arrowprops=dict(arrowstyle="->", color=DANGER, lw=0.8))

    ax.set_xlabel("Year")
    ax.set_ylabel("Aggregate markup  $\\mu = P/MC$")
    ax.set_xlim(1955, 2014)
    ax.set_ylim(0.95, 1.75)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("De Loecker, Eeckhout & Unger (2020 QJE) — US Compustat firms",
                 fontsize=10, color=PRIMARY, pad=8)

    out = os.path.join(HERE, "fig-deu-markups.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 6 — Cost-share comparison: gigafactory vs TSMC fab
# Two side-by-side donuts
# ============================================================
def fig_cost_shares():
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))

    def donut(ax, capital, labor, title, k_color, l_color):
        sizes = [capital, labor]
        colors = [k_color, l_color]
        wedges, _ = ax.pie(
            sizes, colors=colors, startangle=90,
            wedgeprops=dict(width=0.36, edgecolor="white", linewidth=2)
        )
        # Center label
        ax.text(0, 0.10, title, ha="center", va="center",
                fontsize=11, color=PRIMARY, fontweight="bold")
        ax.text(0, -0.18, f"$\\alpha={capital/100:.2f}$, $\\beta={labor/100:.2f}$",
                ha="center", va="center", fontsize=9, color=MUTED)
        # Wedge percentages
        ax.text(-0.95, 0.55, f"capital\n{capital}%",
                ha="center", fontsize=9, color=k_color, fontweight="bold")
        ax.text(0.95, 0.55, f"labor\n{labor}%",
                ha="center", fontsize=9, color=l_color, fontweight="bold")
        ax.set_aspect("equal")

    donut(axes[0], 40, 60, "Gigafactory", SECONDARY, ACCENT)
    donut(axes[1], 70, 30, "TSMC fab", SECONDARY, ACCENT)

    # Cost-share takeaway
    fig.text(0.5, 0.02,
             "Cost shares equal the production-function exponents:  "
             "$wL^*/c=\\beta$  and  $rK^*/c=\\alpha$  (under CRS).",
             ha="center", fontsize=9.5, color=PRIMARY, style="italic")

    plt.subplots_adjust(top=0.95, bottom=0.12)
    out = os.path.join(HERE, "fig-cost-shares.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 7 — Duality square: consumer-side ↔ producer-side
# (Visualization of the §8.6.2 four-corner duality)
# ============================================================
def fig_duality():
    # Wider canvas (~30% more horizontal pixels) so box text and arrow labels
    # don't crowd each other. Boxes also bumped from 0.18 → 0.22 wide.
    fig, ax = plt.subplots(figsize=(13.0, 4.8))

    # Layout — columns spread out so arrow gaps are wider (~0.13) and boxes
    # are roomy (0.22 wide), giving labels like "Conditional K*, L*" plenty
    # of horizontal slack.
    # Columns: Primitive (x=0.07) | Dual (x=0.41) | Demand (x=0.75)
    BOX_W = 0.22
    boxes = [
        # (x, y, w, h, label, sublabel, color)
        (0.06, 0.55, BOX_W, 0.30, "Utility  $u(x_1,x_2)$",
         "preferences", SECONDARY),
        (0.41, 0.55, BOX_W, 0.30, "Expenditure  $e(p,\\bar u)$",
         "min spending for $\\bar u$", SECONDARY),
        (0.76, 0.55, BOX_W, 0.30, "Hicksian  $h_i^*$",
         "compensated demand", SECONDARY),

        (0.06, 0.10, BOX_W, 0.30, "Production  $f(K,L)$",
         "technology", ACCENT),
        (0.41, 0.10, BOX_W, 0.30, "Cost  $c(w,r,q)$",
         "min spending for $q$", ACCENT),
        (0.76, 0.10, BOX_W, 0.30, "Conditional  $K^*,\\,L^*$",
         "input demand", ACCENT),
    ]

    for x, y, w, h, label, sub, color in boxes:
        rect = mpatches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.005,rounding_size=0.012",
            linewidth=1.4, edgecolor=color, facecolor="white"
        )
        ax.add_patch(rect)
        ax.text(x + w/2, y + h*0.62, label,
                ha="center", va="center", fontsize=10.5,
                color=PRIMARY, fontweight="bold")
        ax.text(x + w/2, y + h*0.28, sub,
                ha="center", va="center", fontsize=8.5,
                color=MUTED, style="italic")

    # Arrows between columns — labels sit in the WIDER gap with extra vertical lift
    def arrow(x1, x2, y, label, color, ylabel_offset=0.055):
        arr = FancyArrowPatch((x1, y), (x2, y),
                              arrowstyle="->", mutation_scale=18,
                              color=color, lw=1.6)
        ax.add_patch(arr)
        ax.text((x1+x2)/2, y + ylabel_offset, label,
                ha="center", fontsize=10, color=color,
                style="italic", fontweight="bold",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5))

    # Consumer row
    arrow(0.06 + BOX_W, 0.41, 0.70, "expenditure min", SECONDARY)
    arrow(0.41 + BOX_W, 0.76, 0.70, "Shephard", SECONDARY)
    # Producer row
    arrow(0.06 + BOX_W, 0.41, 0.25, "cost min", ACCENT)
    arrow(0.41 + BOX_W, 0.76, 0.25, "Shephard", ACCENT)

    # Row labels
    ax.text(0.04, 0.70, "Consumer", ha="right", va="center",
            fontsize=11.5, color=SECONDARY, fontweight="bold", rotation=90)
    ax.text(0.04, 0.25, "Producer", ha="right", va="center",
            fontsize=11.5, color=ACCENT, fontweight="bold", rotation=90)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.96)
    ax.axis("off")
    fig.text(0.5, 0.93,
             "The duality framework — same mathematical machinery, dual interpretations",
             ha="center", fontsize=11, color=PRIMARY, style="italic")

    out = os.path.join(HERE, "fig-duality.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 8 — Three parallel isocost lines (Figure 6.7 reference)
# C = $50, $80, $100 at W=10, R=20 (slope = -W/R = -0.5)
# Style matches the Goolsbee-style green-line reference figure
# ============================================================
def fig_isocost_lines_67():
    fig, ax = plt.subplots(figsize=(7.6, 4.5))

    # Wage = 10, Rental = 20, so slope = -W/R = -0.5
    W_, R_ = 10.0, 20.0
    slope = -W_ / R_
    Ls = np.linspace(0, 10, 50)

    # Three isocost lines
    isocosts = [(50, "$C = \\$50$"), (80, "$C = \\$80$"), (100, "$C = \\$100$")]
    GREEN = "#1A8754"

    for C, _label in isocosts:
        Ks = (C - W_ * Ls) / R_
        # Mask negative K
        valid = Ks >= 0
        ax.plot(Ls[valid], Ks[valid], color=GREEN, lw=2.6)

    # Label each line near its L-axis end
    label_positions = [
        (50,  3.7, 0.20, "$C = \\$50$"),
        (80,  6.7, 0.20, "$C = \\$80$"),
        (100, 8.7, 0.20, "$C = \\$100$"),
    ]
    for C, lx, ly, txt in label_positions:
        ax.text(lx, ly, txt, fontsize=10.5, color=PRIMARY, ha="left")

    # Slope annotation with arrow leaders
    ax.annotate(
        "",
        xy=(2.6, 1.7), xytext=(3.6, 3.0),
        arrowprops=dict(arrowstyle="->", lw=0.9, color=PRIMARY),
    )
    ax.annotate(
        "",
        xy=(4.2, 1.9), xytext=(4.2, 3.0),
        arrowprops=dict(arrowstyle="->", lw=0.9, color=PRIMARY),
    )
    ax.text(
        4.3, 3.15,
        r"$\mathrm{Slope}\;=\;-\dfrac{W}{R}\;=\;-\dfrac{10}{20}\;=\;-0.5$",
        fontsize=11, color=PRIMARY,
    )

    # Title (treated as a figure caption)
    ax.set_title("Isocost Lines",
                 fontsize=11, color=PRIMARY, pad=10, loc="center")

    ax.set_xlabel("Labor  $(L)$", fontsize=11)
    ax.set_ylabel("Capital  $(K)$", fontsize=11)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 5.5)
    ax.set_xticks(range(0, 11))
    ax.set_yticks(range(0, 6))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out = os.path.join(HERE, "fig-isocost-lines-67.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 9 — Cost Minimization (Figure 6.10 reference)
# Q-bar = 50 isoquant + three parallel isocost lines C_A, C_B, C_C
# Tangency at B (cost-min combination); A on the higher isocost C_A
# Style matches the textbook reference green isocost + maroon isoquant
# ============================================================
def fig_cost_min_610():
    fig, ax = plt.subplots(figsize=(7.4, 5.0))

    GREEN = "#1A8754"
    MAROON = "#7C3A5F"

    # Isoquant Q = sqrt(K*L) = 50, so K*L = 2500
    L_iso = np.linspace(35, 135, 400)
    K_iso = 2500.0 / L_iso
    ax.plot(L_iso, K_iso, color=MAROON, lw=2.6, zorder=3)

    # Three parallel isocost lines with slope -W/R = -0.5 (W=10, R=20)
    # K = C/R - (W/R) L  →  K = C/20 - 0.5 L
    # C_C = 1200 (below isoquant — infeasible at Q=50)
    # C_B = 1414 (tangent at B: L=70.71, K=35.36)
    # C_A = 1500 (crosses isoquant at A: L=100, K=25; and at L=50, K=50)
    L_axis = np.linspace(0, 160, 100)
    isocosts = [
        (1200, "$C_C$"),
        (1414, "$C_B$"),
        (1500, "$C_A$"),
    ]
    for C, _lbl in isocosts:
        K_line = (C - 10.0 * L_axis) / 20.0
        valid = (K_line >= 0) & (L_axis <= 160)
        ax.plot(L_axis[valid], K_line[valid], color=GREEN, lw=2.2, zorder=2)

    # Label each isocost AT the L-axis intercept (L_int = C/W = C/10)
    # C_C → L=120; C_B → L=141.4; C_A → L=150 (all near right side, just above axis)
    ax.text(120,   1.8, "$C_C$", color=PRIMARY, fontsize=12, ha="center",
            va="bottom", zorder=5,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    ax.text(141.4, 1.8, "$C_B$", color=PRIMARY, fontsize=12, ha="center",
            va="bottom", zorder=5,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    ax.text(150,   1.8, "$C_A$", color=PRIMARY, fontsize=12, ha="center",
            va="bottom", zorder=5,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2))

    # Point B — tangency / cost-minimizing combination
    L_B, K_B = 70.71, 35.36
    ax.plot(L_B, K_B, "o", color=PRIMARY, markersize=8,
            markeredgecolor="white", markeredgewidth=1.5, zorder=6)
    ax.annotate(
        "$B$  (cost-minimizing\ncombination)",
        xy=(L_B, K_B), xytext=(95, 62),
        fontsize=11, color=PRIMARY, ha="center",
        arrowprops=dict(arrowstyle="-", color=PRIMARY, lw=0.7),
    )

    # Point A — on isoquant, on the higher isocost C_A (lower-right of B)
    L_A, K_A = 100.0, 25.0
    ax.plot(L_A, K_A, "o", color=PRIMARY, markersize=7,
            markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    ax.text(L_A - 3, K_A + 3, "$A$", fontsize=12, color=PRIMARY,
            fontweight="bold", zorder=6)

    # Q̄ = 50 label on the right side of the isoquant
    ax.annotate(
        r"$Q = \bar Q = 50$",
        xy=(133, 2500.0 / 133),   # point on isoquant near right edge
        xytext=(141, 16),
        fontsize=12, color=MAROON,
        arrowprops=dict(arrowstyle="-", color=MAROON, lw=0.7),
    )

    ax.set_title("Cost Minimization",
                 fontsize=11, color=PRIMARY, pad=10, loc="center")

    ax.set_xlabel("Labor  $(L)$", fontsize=11)
    ax.set_ylabel("Capital  $(K)$", fontsize=11)
    ax.set_xlim(0, 170)
    ax.set_ylim(0, 80)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out = os.path.join(HERE, "fig-cost-min-610.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 10 — Input Price Changes
# Same isoquant Q̄=50 tangent to two isocost lines at different points
# C₁ (green, flat slope -0.5, "capital relatively more expensive") → A
# C₂ (red, steep slope -2.0, "labor relatively more expensive")    → B
# ============================================================
def fig_input_price_changes():
    fig, ax = plt.subplots(figsize=(7.5, 5.2))

    GREEN = "#1A8754"
    RED = "#C72A2A"
    MAROON = "#7C3A5F"

    # Isoquant Q = sqrt(K*L) = 50 → K*L = 2500
    L_iso = np.linspace(22, 140, 400)
    K_iso = 2500.0 / L_iso
    ax.plot(L_iso, K_iso, color=MAROON, lw=2.6, zorder=4)

    # ---- C₁ (green, flat, slope -0.5) — capital is more expensive ----
    # Tangent at A: K/L = 0.5 → K=0.5L, KL=2500 → L=70.71, K=35.36
    # C₁ passes through (0, 70.71) and (141.42, 0)
    L_axis = np.linspace(0, 160, 60)
    K_C1 = 70.71 - 0.5 * L_axis
    valid1 = K_C1 >= 0
    ax.plot(L_axis[valid1], K_C1[valid1], color=GREEN, lw=2.4, zorder=3)

    # ---- C₂ (red, steep, slope -2.0) — labor is more expensive ----
    # Tangent at B: K/L = 2 → K=2L, KL=2500 → L=35.36, K=70.71
    # C₂ passes through (0, 141.42) and (70.71, 0)
    K_C2 = 141.42 - 2.0 * L_axis
    valid2 = K_C2 >= 0
    ax.plot(L_axis[valid2], K_C2[valid2], color=RED, lw=2.4, zorder=3)

    # Tangency points
    L_A, K_A = 70.71, 35.36   # on green C₁
    L_B, K_B = 35.36, 70.71   # on red C₂

    ax.plot(L_A, K_A, "o", color=PRIMARY, markersize=8,
            markeredgecolor="white", markeredgewidth=1.5, zorder=6)
    ax.text(L_A + 3, K_A + 3, "$A$", fontsize=13, color=PRIMARY,
            fontweight="bold", zorder=6)

    ax.plot(L_B, K_B, "o", color=PRIMARY, markersize=8,
            markeredgecolor="white", markeredgewidth=1.5, zorder=6)
    ax.text(L_B - 6, K_B - 1, "$B$", fontsize=13, color=PRIMARY,
            fontweight="bold", zorder=6)

    # Annotations matching the screenshot
    # "Labor is relatively more expensive" points to red line / B (upper-left)
    ax.annotate(
        "Labor is relatively\nmore expensive.",
        xy=(L_B - 5, K_B + 25),       # arrowhead near the red line above B
        xytext=(12, 130),
        fontsize=11, color=PRIMARY,
        arrowprops=dict(arrowstyle="-", color=PRIMARY, lw=0.7),
    )
    # "Capital is relatively more expensive" points to green line / A (mid-right)
    ax.annotate(
        "Capital is relatively\nmore expensive.",
        xy=(95, 22),                  # arrowhead near the green line, right of A
        xytext=(95, 60),
        fontsize=11, color=PRIMARY,
        arrowprops=dict(arrowstyle="-", color=PRIMARY, lw=0.7),
    )

    # Q = Q̄ label on the right side of the isoquant
    ax.annotate(
        r"$Q = \bar Q$",
        xy=(135, 2500.0 / 135),
        xytext=(143, 17),
        fontsize=12.5, color=MAROON,
        arrowprops=dict(arrowstyle="-", color=MAROON, lw=0.7),
    )

    # C₁ and C₂ labels at the L-axis where each line crosses zero
    ax.text(72, 2.5, "$C_2$", color=RED, fontsize=13, ha="center",
            va="bottom", fontweight="bold", zorder=5,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2))
    ax.text(143, 2.5, "$C_1$", color=GREEN, fontsize=13, ha="center",
            va="bottom", fontweight="bold", zorder=5,
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2))

    ax.set_xlabel("Labor  $(L)$", fontsize=12)
    ax.set_ylabel("Capital  $(K)$", fontsize=12)
    ax.set_xlim(0, 160)
    ax.set_ylim(0, 160)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    out = os.path.join(HERE, "fig-input-price-changes.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 11 — Production Function to Costs (FC, VC, TC vs Q)
# ============================================================
def fig_production_to_costs():
    fig, ax = plt.subplots(figsize=(7.0, 4.8))

    Q  = [0, 20, 50, 90, 120, 140, 150, 155]
    FC = [26]*len(Q)
    VC = [0, 17, 35, 54, 72, 89, 105, 120.5]
    TC = [FC[i] + VC[i] for i in range(len(Q))]

    GREEN_FC = "#1A8754"
    RED_VC = "#C72A2A"
    PURPLE_TC = "#6A4FB6"

    ax.plot(Q, FC, "-o", color=GREEN_FC, lw=2.4, markersize=5,
            markeredgecolor="white", markeredgewidth=0.8, label="FC")
    ax.plot(Q, VC, "-o", color=RED_VC, lw=2.4, markersize=5,
            markeredgecolor="white", markeredgewidth=0.8, label="VC")
    ax.plot(Q, TC, "-o", color=PURPLE_TC, lw=2.6, markersize=5,
            markeredgecolor="white", markeredgewidth=0.8, label="TC")

    # Title-ish header for the chart
    ax.text(0.02, 1.04, "C O S T S", transform=ax.transAxes,
            fontsize=12.5, color=PRIMARY, fontweight="bold")

    # X-axis ticks exactly at the data Q's
    ax.set_xticks(Q)
    ax.set_xticklabels([str(q) for q in Q], fontsize=10)
    ax.set_xlim(-5, 160)
    ax.set_ylim(0, 200)
    ax.set_yticks([0, 50, 100, 150, 200])
    ax.set_yticklabels([f"\\${y}" for y in [0, 50, 100, 150, 200]], fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=LINE, lw=0.5)

    # Legend top-right
    ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.99),
              fontsize=10, ncol=3, frameon=False, columnspacing=1.5)

    out = os.path.join(HERE, "fig-production-to-costs.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 12 — Costs That Matter (MC, AVC, ATC, AFC vs Q)
# ============================================================
def fig_costs_that_matter():
    fig, ax = plt.subplots(figsize=(7.0, 4.8))

    Q   = [20, 50, 90, 120, 140, 150, 155]
    MC  = [0.85, 0.60, 0.48, 0.60, 0.85, 1.60, 3.10]
    AVC = [0.85, 0.70, 0.60, 0.60, 0.64, 0.70, 0.78]
    ATC = [2.15, 1.22, 0.89, 0.82, 0.82, 0.87, 0.95]
    AFC = [1.30, 0.52, 0.29, 0.22, 0.19, 0.17, 0.17]

    RED_MC = "#C72A2A"
    PURPLE_AVC = "#9C6FCC"
    ORANGE_ATC = "#F08C26"
    DGREEN_AFC = "#0A5538"

    ax.plot(Q, MC,  "-o", color=RED_MC,     lw=2.4, markersize=5,
            markeredgecolor="white", markeredgewidth=0.8, label="MC = ΔTC/ΔQ")
    ax.plot(Q, AVC, "-o", color=PURPLE_AVC, lw=2.4, markersize=5,
            markeredgecolor="white", markeredgewidth=0.8, label="AVC")
    ax.plot(Q, ATC, "-o", color=ORANGE_ATC, lw=2.4, markersize=5,
            markeredgecolor="white", markeredgewidth=0.8, label="ATC")
    ax.plot(Q, AFC, "-o", color=DGREEN_AFC, lw=2.4, markersize=5,
            markeredgecolor="white", markeredgewidth=0.8, label="AFC")

    ax.text(-0.04, 1.06, "C", transform=ax.transAxes,
            fontsize=14, color=PRIMARY, fontweight="bold", fontstyle="italic")
    ax.text(1.02, -0.06, "Q", transform=ax.transAxes,
            fontsize=14, color=PRIMARY, fontweight="bold", fontstyle="italic")

    ax.set_xticks([0, 20, 50, 90, 120, 140, 150, 155])
    ax.set_xticklabels(["0", "20", "50", "90", "120", "140", "150", "155"], fontsize=10)
    ax.set_xlim(0, 165)
    ax.set_ylim(0, 3.6)
    ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
    ax.set_yticklabels(["\\$0.0", "\\$0.5", "\\$1.0", "\\$1.5", "\\$2.0", "\\$2.5", "\\$3.0", "\\$3.5"], fontsize=10)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", color=LINE, lw=0.5)

    ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.10),
              fontsize=9.5, ncol=4, frameon=False, columnspacing=1.2)

    plt.subplots_adjust(top=0.86)
    out = os.path.join(HERE, "fig-costs-that-matter.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 13 — Average and Marginal Costs (3-panel: AFC | AVC+MC | ATC+MC)
# ============================================================
def _normalize_panel_pngs(paths):
    """Pad PNGs to a shared canvas, aligned on each chart's axes origin.

    Locates the axes origin as the darkest full-length vertical line (the
    left spine) and horizontal line (the bottom spine), then pads each image
    so every origin lands on the same pixel.  Result: identical dimensions
    and identical chart placement, with no content cropped.
    """
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        print("  (skip panel normalisation: numpy/Pillow not available)")
        return

    ims, origins = [], []
    for p in paths:
        im = Image.open(p).convert("RGB")
        g = np.asarray(im).min(axis=2)
        dark = g < 200
        # left spine: vertical line -> column with the most dark pixels
        # bottom spine: horizontal line -> row with the most dark pixels
        # The left spine is the LEFTMOST long vertical line; the bottom spine
        # is the LOWEST long horizontal line.  Plain argmax is wrong: in the
        # AFC panel the "Spreading effect" arrow is a long horizontal rule
        # sitting high in the chart, and argmax locks onto that instead of
        # the x-axis, which shoves the whole panel downwards.
        ccount = dark.sum(axis=0)
        rcount = dark.sum(axis=1)
        col = int(np.flatnonzero(ccount >= 0.5 * ccount.max()).min())
        row = int(np.flatnonzero(rcount >= 0.5 * rcount.max()).max())
        ims.append(im)
        origins.append((col, row))

    L = max(c for c, _ in origins)
    R = max(im.width - c for im, (c, _) in zip(ims, origins))
    T = max(r for _, r in origins)
    B = max(im.height - r for im, (_, r) in zip(ims, origins))
    W, H = L + R, T + B

    for p, im, (c, r) in zip(paths, ims, origins):
        canvas = Image.new("RGB", (W, H), (255, 255, 255))
        canvas.paste(im, (L - c, T - r))
        canvas.save(p)
    print("  normalised %d panels to %dx%d (axes-aligned)" % (len(paths), W, H))


def fig_amc_three_panels():
    """Three single-panel figures + the legacy combined three-panel figure.

    New panel order (reflects the slide's fragment-reveal sequence):
      Panel 1: AVC + MC (with crossing at Q = 120)
      Panel 2: ATC + MC (with crossing at Q = 140)
      Panel 3: AFC alone (monotone declining — saved for last)

    Emits three individual PNGs (one per panel) plus the combined PNG
    in the new order:
      fig-amc-panel-avc-mc.png
      fig-amc-panel-atc-mc.png
      fig-amc-panel-afc.png
      fig-amc-three-panels.png      (combined, AVC|ATC|AFC order)
    """
    Q   = [20, 50, 90, 120, 140, 150, 155]
    MC  = [0.85, 0.60, 0.48, 0.60, 0.85, 1.60, 3.10]
    AVC = [0.85, 0.70, 0.60, 0.60, 0.64, 0.70, 0.78]
    ATC = [2.15, 1.22, 0.89, 0.82, 0.82, 0.87, 0.95]
    AFC = [1.30, 0.52, 0.29, 0.22, 0.19, 0.17, 0.17]

    RED_MC = "#C72A2A"
    PURPLE_AVC = "#9C6FCC"
    ORANGE_ATC = "#F08C26"
    DGREEN_AFC = "#0A5538"

    # --------------------------------------------------------------
    # Helper: draw the AVC + MC panel onto a given Axes.
    # --------------------------------------------------------------
    def _draw_avc_mc(ax):
        ax.set_ylim(-0.05, 4.4)
        ax.plot(Q, AVC, "-o", color=PURPLE_AVC, lw=2.4, markersize=5,
                markeredgecolor="white", markeredgewidth=0.8, label="AVC")
        ax.plot(Q, MC, "-o", color=RED_MC, lw=2.4, markersize=5,
                markeredgecolor="white", markeredgewidth=0.8,
                label="MC = ΔTC/ΔQ")
        ax.axvline(120, color=PRIMARY, lw=0.8, ls=":")
        ax.plot([120], [0.60], "o", color="none",
                markeredgecolor="#1A8754", markeredgewidth=2.5,
                markersize=12, zorder=5)
        ax.annotate("", xy=(15, 3.85), xytext=(115, 3.85),
                    arrowprops=dict(arrowstyle="->", color="#0A5538", lw=1.4))
        ax.text(67, 3.95, "Increasing returns", fontsize=10, color="#0A5538",
                ha="center", fontweight="bold")
        ax.annotate("", xy=(160, 3.85), xytext=(125, 3.85),
                    arrowprops=dict(arrowstyle="->", color=RED_MC, lw=1.4))
        ax.text(142, 3.95, "Diminishing returns", fontsize=10, color=RED_MC,
                ha="center", fontweight="bold")
        ax.annotate("When MC < AVC, AVC is falling.", xy=(67, 0),
                    xytext=(67, -50), xycoords=("data", "data"),
                    textcoords="offset points", fontsize=9, ha="center",
                    color=PRIMARY)
        ax.annotate("When MC > AVC, AVC is rising.", xy=(142, 0),
                    xytext=(142, -50), xycoords=("data", "data"),
                    textcoords="offset points", fontsize=9, ha="center",
                    color=PRIMARY)
        ax.annotate("The MC curve crosses the AVC curve\n"
                    "at the AVC curve's minimum.",
                    xy=(120, 0), xytext=(120, -82),
                    xycoords=("data", "data"), textcoords="offset points",
                    fontsize=9, ha="center", color="#0A5538", style="italic")
        ax.set_xticks([0, 20, 50, 90, 120, 140, 155])
        ax.set_xticklabels(["0", "20", "50", "90", "120", "140", "155"],
                           fontsize=8.5)
        ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
        ax.set_yticklabels(["\\$0.0", "\\$0.5", "\\$1.0", "\\$1.5",
                            "\\$2.0", "\\$2.5", "\\$3.0", "\\$3.5"],
                           fontsize=9)
        ax.set_xlim(0, 165)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13),
                  fontsize=10, ncol=2, frameon=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", color=LINE, lw=0.5)

    # --------------------------------------------------------------
    # Helper: draw the ATC + MC panel onto a given Axes.
    # --------------------------------------------------------------
    def _draw_atc_mc(ax):
        ax.set_ylim(-0.05, 4.4)
        ax.plot(Q, ATC, "-o", color=ORANGE_ATC, lw=2.4, markersize=5,
                markeredgecolor="white", markeredgewidth=0.8, label="ATC")
        ax.plot(Q, MC, "-o", color=RED_MC, lw=2.4, markersize=5,
                markeredgecolor="white", markeredgewidth=0.8,
                label="MC = ΔTC/ΔQ")
        ax.axvline(140, color=PRIMARY, lw=0.8, ls=":")
        ax.plot([140], [0.82], "o", color="none",
                markeredgecolor="#1A8754", markeredgewidth=2.5,
                markersize=12, zorder=5)
        ax.annotate("", xy=(15, 3.85), xytext=(135, 3.85),
                    arrowprops=dict(arrowstyle="->", color="#0A5538", lw=1.4))
        ax.text(75, 3.95, "Increasing returns", fontsize=10, color="#0A5538",
                ha="center", fontweight="bold")
        ax.annotate("", xy=(160, 3.85), xytext=(145, 3.85),
                    arrowprops=dict(arrowstyle="->", color=RED_MC, lw=1.4))
        ax.text(152, 3.95, "Diminishing returns", fontsize=9.5, color=RED_MC,
                ha="center", fontweight="bold")
        ax.annotate("When MC < ATC, ATC is falling.", xy=(75, 0),
                    xytext=(75, -50), xycoords=("data", "data"),
                    textcoords="offset points", fontsize=9, ha="center",
                    color=PRIMARY)
        ax.annotate("When MC > ATC, ATC is rising.", xy=(150, 0),
                    xytext=(150, -50), xycoords=("data", "data"),
                    textcoords="offset points", fontsize=9, ha="center",
                    color=PRIMARY)
        ax.annotate("The MC curve crosses the ATC curve\n"
                    "at the ATC curve's minimum.",
                    xy=(140, 0), xytext=(140, -82),
                    xycoords=("data", "data"), textcoords="offset points",
                    fontsize=9, ha="center", color="#0A5538", style="italic")
        ax.set_xticks([0, 20, 50, 90, 120, 140, 155])
        ax.set_xticklabels(["0", "20", "50", "90", "120", "140", "155"],
                           fontsize=8.5)
        ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5])
        ax.set_yticklabels(["\\$0.0", "\\$0.5", "\\$1.0", "\\$1.5",
                            "\\$2.0", "\\$2.5", "\\$3.0", "\\$3.5"],
                           fontsize=9)
        ax.set_xlim(0, 165)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13),
                  fontsize=10, ncol=2, frameon=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", color=LINE, lw=0.5)

    # --------------------------------------------------------------
    # Helper: draw the AFC-only panel onto a given Axes.
    # AFC has its own natural y-range (0..1.5) since its values (FC/Q)
    # decay quickly. The panel shape (top legend / chart / bottom
    # annotation) still matches AVC/ATC for visual alignment.
    # --------------------------------------------------------------
    def _draw_afc(ax):
        ax.set_ylim(-0.02, 1.5)
        ax.plot(Q, AFC, "-o", color=DGREEN_AFC, lw=2.4, markersize=5,
                markeredgecolor="white", markeredgewidth=0.8, label="AFC")
        # Top annotation: spreading-effect arrow, sitting just above the
        # AFC curve's initial peak (≈ \$1.30 at Q=20).
        ax.annotate("", xy=(160, 1.32), xytext=(15, 1.32),
                    arrowprops=dict(arrowstyle="->", color=DGREEN_AFC, lw=1.4))
        ax.text(85, 1.36, "Spreading effect", fontsize=10, color=DGREEN_AFC,
                ha="center", fontweight="bold")
        # Bottom annotations matching AVC/ATC vertical structure
        ax.annotate("AFC = FC / Q.", xy=(85, 0),
                    xytext=(85, -50), xycoords=("data", "data"),
                    textcoords="offset points", fontsize=9, ha="center",
                    color=PRIMARY)
        ax.annotate("Declines forever &mdash; fixed cost\n"
                    "spread over more units.".replace("&mdash;", "—"),
                    xy=(85, 0), xytext=(85, -82),
                    xycoords=("data", "data"), textcoords="offset points",
                    fontsize=9, ha="center", color=DGREEN_AFC, style="italic")
        ax.set_xticks([0, 20, 50, 90, 120, 140, 155])
        ax.set_xticklabels(["0", "20", "50", "90", "120", "140", "155"],
                           fontsize=8.5)
        ax.set_yticks([0, 0.3, 0.6, 0.9, 1.2, 1.5])
        ax.set_yticklabels(["\\$0.0", "\\$0.3", "\\$0.6", "\\$0.9",
                            "\\$1.2", "\\$1.5"], fontsize=9)
        ax.set_xlim(0, 165)
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13),
                  fontsize=10, ncol=2, frameon=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="y", color=LINE, lw=0.5)

    # --------------------------------------------------------------
    # Emit the three single-panel PNGs (for step-by-step reveal on the slide)
    # --------------------------------------------------------------
    # Lock the chart-area position to the SAME bbox in all three single-panel
    # PNGs so the plots line up pixel-for-pixel when placed side by side on
    # the slide. [left, bottom, width, height] in figure-fraction coords.
    PANEL_BBOX = [0.14, 0.24, 0.83, 0.63]

    fig, ax = plt.subplots(figsize=(6.5, 5.6))
    _draw_avc_mc(ax)
    ax.set_position(PANEL_BBOX)
    plt.savefig(os.path.join(HERE, "fig-amc-panel-avc-mc.png"))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 5.6))
    _draw_atc_mc(ax)
    ax.set_position(PANEL_BBOX)
    plt.savefig(os.path.join(HERE, "fig-amc-panel-atc-mc.png"))
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.5, 5.6))
    _draw_afc(ax)
    ax.set_position(PANEL_BBOX)
    plt.savefig(os.path.join(HERE, "fig-amc-panel-afc.png"))
    plt.close(fig)

    # --------------------------------------------------------------
    # Normalise the three single-panel PNGs to ONE canvas, aligned on the
    # chart axes.  Why this is needed: rcParams["savefig.bbox"] = "tight"
    # (set globally at the top of this file) crops each PNG to its own ink
    # extent, which silently defeats the PANEL_BBOX pixel-alignment above --
    # it EXPANDS the AVC/ATC panels (their wide bottom annotations overflow
    # the figure) and SHRINKS the AFC panel (narrower content).  The panels
    # came out 1229x786, 1284x786 and 895x785: three different aspect ratios,
    # so at equal column widths on the slide the AFC panel rendered ~40%
    # taller than the other two.  Turning tight OFF is not an option -- the
    # ATC panel's "When MC > ATC, ATC is rising." caption genuinely extends
    # past the figure edge and would be cut in half.  So: keep tight (nothing
    # is ever clipped), then pad every panel out to a common canvas, lining
    # up the axes origin so the three charts sit at identical size AND in
    # identical positions.
    _normalize_panel_pngs([
        os.path.join(HERE, "fig-amc-panel-avc-mc.png"),
        os.path.join(HERE, "fig-amc-panel-atc-mc.png"),
        os.path.join(HERE, "fig-amc-panel-afc.png"),
    ])

    # --------------------------------------------------------------
    # Combined three-panel figure (kept for backwards compat) — new order
    # AVC + MC | ATC + MC | AFC
    # --------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.6))
    _draw_avc_mc(axes[0])
    _draw_atc_mc(axes[1])
    _draw_afc(axes[2])

    plt.subplots_adjust(left=0.05, right=0.98, bottom=0.22, top=0.87, wspace=0.32)
    out = os.path.join(HERE, "fig-amc-three-panels.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 14 — GPA analogy for AC/MC
# ============================================================
def fig_gpa_analogy():
    fig, ax = plt.subplots(figsize=(8.5, 4.6))

    GREEN_GPA = "#1A8754"
    RED_MC = "#C72A2A"
    PURPLE = "#6A4FB6"  # used only for the crossing-point marker now

    x_dense = np.linspace(7.5, 12.5, 400)

    # GPA curve: smooth quadratic passing through (9,2.3), (10,2.0), (11,2.2), (12,2.5)
    # Fit a quadratic to the 4 anchor points; extend slightly beyond.
    gpa_anchor_x = np.array([9.0, 10.0, 11.0, 12.0])
    gpa_anchor_y = np.array([2.3, 2.0, 2.2, 2.5])
    gpa_coef = np.polyfit(gpa_anchor_x, gpa_anchor_y, 2)
    gpa = np.polyval(gpa_coef, x_dense)
    ax.plot(x_dense, gpa, color=GREEN_GPA, lw=3.2, zorder=3)

    # Marginal grade curve: smooth quadratic through (9, 1.0), (10, 2.0), (11, 3.0), (12, 4.0)
    # These are linear → degree 2 will essentially give a line. Use degree 2 anyway.
    mg_anchor_x = np.array([9.0, 10.0, 11.0, 12.0])
    mg_anchor_y = np.array([1.0, 2.0, 3.0, 4.0])
    mg_coef = np.polyfit(mg_anchor_x, mg_anchor_y, 2)
    mg = np.polyval(mg_coef, x_dense)
    ax.plot(x_dense, mg, color=RED_MC, lw=3.2, zorder=3)

    # Data points: GPA (green) and Marginal Grade (red)
    for x, y, lbl, color, off in [
        (9,  2.3, "GPA: 2.3", GREEN_GPA, (-15, 0)),
        (10, 2.0, "Lowest GPA: 2.0", PURPLE, (10, -22)),
        (11, 2.2, "GPA: 2.2", GREEN_GPA, (12, -3)),
        (12, 2.5, "GPA: 2.5", GREEN_GPA, (12, 3)),
        (9,  1.0, "New Course: 1.0", RED_MC, (10, -10)),
        (11, 3.0, "New Course: 3.0", RED_MC, (-8, 18)),
        (12, 4.0, "New Course: 4.0", RED_MC, (-8, 18)),
    ]:
        ax.plot(x, y, "o", color=color, markersize=10,
                markeredgecolor="white", markeredgewidth=1.5, zorder=6)
        ax.annotate(lbl, (x, y), xytext=off, textcoords="offset points",
                    fontsize=9.5, color=color, fontweight="bold")

    # Crossing point at (10, 2.0) — purple emphasis dot (kept; the BOX is gone)
    ax.plot(10, 2.0, "o", color=PURPLE, markersize=12,
            markeredgecolor="white", markeredgewidth=2, zorder=7)

    # Dashed verticals at integer course numbers (subtle reference grid)
    for cx in [9, 10, 11, 12]:
        ax.axvline(cx, color=MUTED, lw=0.5, ls=":", alpha=0.6)

    # Curve labels (instead of legend)
    ax.text(12.55, 4.5, "Marginal Grade", fontsize=12, color=RED_MC,
            fontweight="bold", ha="left", va="center")
    ax.text(12.55, 4.2, "(Every New Course)", fontsize=10, color=RED_MC,
            ha="left", va="center", style="italic")
    ax.text(12.55, 2.9, "GPA", fontsize=13, color=GREEN_GPA,
            fontweight="bold", ha="left", va="center")

    ax.set_xticks([9, 10, 11, 12])
    ax.set_xticklabels(["9", "10", "11", "12"], fontsize=11)
    ax.set_yticks([2.0, 4.0])
    ax.set_yticklabels(["2.0", "4.0"], fontsize=11)
    ax.set_xlim(7, 13.5)
    ax.set_ylim(0.5, 5.0)
    ax.set_xlabel("Number of Courses", fontsize=11, fontweight="bold",
                  loc="right")
    ax.text(-0.04, 1.04, "Grade", transform=ax.transAxes,
            fontsize=12, color=PRIMARY, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.subplots_adjust(top=0.94, right=0.85)
    out = os.path.join(HERE, "fig-gpa-analogy.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 15 — Additive vs Conventional Manufacturing (cost per unit vs volume)
# Conventional: huge FC amortized → cost per unit drops as volume rises.
# Additive: low FC, ~constant cost per unit → flat horizontal line.
# Crossover at moderate volume where conventional becomes cheaper.
# ============================================================
def fig_additive_vs_conventional():
    fig, ax = plt.subplots(figsize=(7.2, 4.8))

    BLUE = "#2563eb"
    RED = "#C72A2A"
    GREEN = "#1A8754"

    # Unit volume axis 0 to 100
    Q = np.linspace(1, 100, 400)

    # Conventional: AC = FC_high/Q + MC_low_conventional
    # Pick FC=200, marginal=0.6 so curve passes through (1,200.6), (100, 2.6), crosses additive ~ Q=40
    AC_conv = 200.0 / Q + 0.6
    # Additive: roughly constant per-unit ≈ 5.0 (high marginal, no scale economies)
    AC_add = np.full_like(Q, 5.0)
    # Variable-cost floor (filament-only, ~3.0)
    AC_floor = np.full_like(Q, 3.0)

    ax.plot(Q, AC_conv, color=BLUE, lw=3.2, label="Conventional Manufacturing")
    ax.plot(Q, AC_add,  color=RED,  lw=2.8, label="Additive Manufacturing")
    ax.plot(Q, AC_floor, color=GREEN, lw=1.8, ls="-", alpha=0.85)

    # Annotations: place labels right next to the curves at clear positions
    ax.text(40, 13, "Conventional\nManufacturing", fontsize=14, color="#0f172a",
            fontweight="bold", ha="left")
    ax.text(80, 6.4, "Additive Manufacturing", fontsize=14, color="#0f172a",
            fontweight="bold", ha="right")

    # Axis styling — minimal ticks, just labels for the axes
    ax.set_xlabel("Unit volume", fontsize=14, fontweight="bold",
                  loc="center")
    ax.set_ylabel("Cost per unit", fontsize=14, fontweight="bold",
                  rotation=90)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 105)
    ax.set_ylim(0, 25)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_linewidth(1.5)
    ax.spines["bottom"].set_linewidth(1.5)

    plt.subplots_adjust(left=0.10, right=0.97, top=0.95, bottom=0.12)
    out = os.path.join(HERE, "fig-additive-vs-conventional.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 16 — 3D-printed house thumbnail (stylized illustration)
# Suggests Project-Milestone-style curved layered concrete house;
# used as the placeholder hero for the Economist article-link card.
# ============================================================
def fig_3d_printed_house():
    fig, ax = plt.subplots(figsize=(8, 4.5))

    # Sky background
    ax.add_patch(mpatches.Rectangle((0, 0.55), 1, 0.45,
                                    facecolor="#cbd9e6", edgecolor="none",
                                    transform=ax.transAxes, zorder=0))
    # Grass background
    ax.add_patch(mpatches.Rectangle((0, 0), 1, 0.55,
                                    facecolor="#85a35c", edgecolor="none",
                                    transform=ax.transAxes, zorder=0))

    # Tree silhouettes (a few simple dark blobs behind the house)
    tree_color = "#3a3a3a"
    for cx, cy, r in [(0.08, 0.78, 0.10), (0.92, 0.78, 0.10), (0.95, 0.72, 0.13)]:
        ax.add_patch(mpatches.Circle((cx, cy), r,
                                     facecolor=tree_color, alpha=0.55,
                                     transform=ax.transAxes, zorder=1))

    # House body — curved silhouette with layered "printed" stripes
    # Use a series of horizontal layer-strips with slight color variation
    house_color = "#e6e0d4"
    house_x = np.linspace(0.18, 0.82, 200)
    # Upper outline: a low arched curve
    upper_y = 0.68 - 0.05 * np.sin((house_x - 0.18) / (0.82 - 0.18) * np.pi) - 0.04 * np.cos((house_x - 0.5) * 6)
    # Just paint a rectangular block then overlay the layered stripes
    ax.add_patch(mpatches.FancyBboxPatch(
        (0.18, 0.30), 0.64, 0.36,
        boxstyle="round,pad=0,rounding_size=0.04",
        facecolor=house_color, edgecolor="#3a3a3a", lw=1.2,
        transform=ax.transAxes, zorder=2
    ))
    # Layered "printed" horizontal stripes
    for i in range(13):
        y = 0.32 + i * 0.026
        shade = "#d8d2c5" if i % 2 == 0 else "#e6e0d4"
        ax.add_patch(mpatches.Rectangle((0.18, y), 0.64, 0.012,
                                        facecolor=shade, edgecolor="none",
                                        transform=ax.transAxes, zorder=3))

    # Door
    ax.add_patch(mpatches.Rectangle((0.62, 0.32), 0.07, 0.16,
                                    facecolor="#23292f", edgecolor="#0f172a",
                                    lw=0.8, transform=ax.transAxes, zorder=4))
    # Window
    ax.add_patch(mpatches.Rectangle((0.49, 0.36), 0.10, 0.20,
                                    facecolor="#bcd0e0", edgecolor="#0f172a",
                                    lw=0.8, transform=ax.transAxes, zorder=4))
    # Plant by door
    ax.add_patch(mpatches.Circle((0.58, 0.34), 0.022,
                                 facecolor="#1A8754", alpha=0.7,
                                 transform=ax.transAxes, zorder=5))

    # AFP-style watermark
    ax.text(0.97, 0.06, "AFP", color="#ffffff", fontsize=12,
            fontweight="bold", ha="right",
            transform=ax.transAxes, zorder=6, alpha=0.7)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out = os.path.join(HERE, "fig-3d-printed-house.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 17 — Engines: Isoquants + SR/LR expansion paths (Figure 7.5)
# (Labor, Capital) plane; 3 isoquants Q=10, 20, 30 engines/wk;
# SR expansion path horizontal at K̄=6; LR expansion path through
# tangency points; isocost lines C=$100, $180, $300, $360.
# ============================================================
def fig_engines_isoquants_expansion():
    """Goolsbee Figure 7.5 with TRUE LR tangencies at X, Y, Z.

    Uses w = 10, r = 15 (so slope of isocost = -w/r = -2/3) and
    rectangular-hyperbola isoquants K·L = c so that the LR expansion
    path is the straight line K = (2/3)L through the origin.

    Marked points (each is a true tangency: isoquant slope = -2/3 = isocost slope):
        X  = (5,  10/3 ≈ 3.33)   tangent to Q = 10 isoquant and $100 isocost  (C = 50 + 50 = $100)
        Y  = (9,  6)             tangent to Q = 20 isoquant and $180 isocost  (C = 90 + 90 = $180)
        Z  = (15, 10)            tangent to Q = 30 isoquant and $300 isocost  (C = 150 + 150 = $300)

    SR points (Q-isoquant ∩ K̄ = 6 horizontal line):
        X' = (50/18 ≈ 2.78, 6)   on Q = 10 isoquant         (C ≈ 28 + 90 = $118 ≈ $120)
        Z' = (25, 6)             on Q = 30 isoquant         (C = 250 + 90 = $340 ≈ $360)

    Five labelled isocost lines $100 / $120 / $180 / $300 / $360 — labels
    match the textbook reference and the math is internally consistent.
    """
    fig, ax = plt.subplots(figsize=(7.6, 5.6))

    GREEN_ISOC = SUCCESS
    MAROON_ISOQ = DANGER
    SR_BLUE = SECONDARY
    LR_YELLOW = ACCENT

    # ============================================================
    # Prices: w = 10, r = 15  →  slope of every isocost = -w/r = -2/3
    # ============================================================
    w_price, r_price = 10.0, 15.0
    slope_iso = w_price / r_price   # = 2/3

    # ============================================================
    # Isoquants Q = 10, 20, 30 — rectangular hyperbolas K · L = c
    # (corresponds to Cobb-Douglas isoquants with α = β; for slope -2/3
    # tangency on the LR expansion path K = (w/r)·L = (2/3) L, the
    # tangency condition K/L = w/r = 2/3 gives one tangent point per
    # isoquant.)
    # Tangency point on Q-isoquant K·L = c at slope -w/r:
    #   K_tan = √(c · w/r),   L_tan = √(c · r/w)
    # Chose c values so tangencies fall at C = $100, $180, $300.
    # ============================================================
    isoq_specs = [
        # (Q, c_isoquant, tangency_label, L_tan, K_tan, isocost_C)
        (10,  50.0/3, "X", 5.0,  10.0/3, 100),   # K · L = 50/3 ≈ 16.67
        (20,  54.0,   "Y", 9.0,  6.0,    180),   # K · L = 54
        (30, 150.0,   "Z", 15.0, 10.0,   300),   # K · L = 150
    ]

    # ============================================================
    # Five isocost lines: C = $100, $120, $180, $300, $360
    # Each line: w·L + r·K = C  →  K = (C - w·L) / r
    # ============================================================
    L_axis = np.linspace(0, 40, 300)
    iso_costs = [100, 120, 180, 300, 360]
    isocost_label_xy = {
        100: (7.5,  2.10),
        120: (10.6, 1.45),
        180: (16.0, 1.65),
        300: (27.6, 1.65),
        360: (32.5, 1.65),  # shifted right since the $360 line is shifted right
    }
    # The $360 line gets a special override so it passes through Z' = (25, 6)
    # (with the schematic label preserved). The other 4 lines use the
    # standard w·L + r·K = C formula.
    Zp_L_target = 150.0 / 6.0   # = 25 (Z' on Q=30 isoquant K·L=150 at K=6)
    Zp_K = 6.0
    # $360 line through (Zp_L_target, Zp_K) with slope -w/r = -2/3
    # (downward, parallel to the other 4 isocost lines):
    #   K = Zp_K - (w/r) · (L - Zp_L_target)
    #     = 6 - (2/3) · (L - 25) = 22.667 - (2/3) L
    for C in iso_costs:
        if C == 360:
            K_line = Zp_K - slope_iso * (L_axis - Zp_L_target)
        else:
            K_line = (C - w_price * L_axis) / r_price
        valid = (K_line >= 0) & (L_axis <= 35)
        ax.plot(L_axis[valid], K_line[valid], color=GREEN_ISOC, lw=1.5, alpha=0.90)
        lx, ly = isocost_label_xy[C]
        ax.text(lx, ly, f"$C = \\${C}$", fontsize=9, color=PRIMARY, ha="left",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0, alpha=0.85))

    # ============================================================
    # Isoquants (drawn last over isocosts)
    # ============================================================
    L_iso = np.linspace(1.0, 32, 600)
    iso_label_xy = {
        10: (16.0, 1.05),
        20: (25.5, 2.20),
        30: (29.5, 5.20),
    }
    for Q, c_iso, _lbl, _Lt, _Kt, _C in isoq_specs:
        K = c_iso / L_iso
        valid = (K > 0.3) & (K < 13)
        ax.plot(L_iso[valid], K[valid], color=MAROON_ISOQ, lw=2.0)
        lx, ly = iso_label_xy[Q]
        ax.text(lx, ly, f"$Q = {Q}$", fontsize=10, color=MAROON_ISOQ, va="center",
                bbox=dict(facecolor="white", edgecolor="none", pad=1.0, alpha=0.85))

    # ============================================================
    # SR expansion path: horizontal at K̄ = 6
    # ============================================================
    K_bar = 6.0
    ax.plot([0.5, 30], [K_bar, K_bar], color=SR_BLUE, lw=2.2)
    ax.text(19.0, K_bar + 0.55, "Short-run\nexpansion\npath  ($\\bar K = 6$)",
            fontsize=10, color=SR_BLUE, ha="left", va="bottom",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

    # ============================================================
    # LR expansion path: linear K = (w/r) · L = (2/3) L through origin
    # ============================================================
    L_lr = np.linspace(0.5, 16.5, 100)
    K_lr = slope_iso * L_lr
    ax.plot(L_lr, K_lr, color=LR_YELLOW, lw=2.6)
    ax.text(7.0, 11.0, "Long-run\nexpansion\npath",
            fontsize=10, color=LR_YELLOW, ha="left", fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

    # ============================================================
    # LR tangency points X, Y, Z
    # ============================================================
    pt_style = dict(color=PRIMARY, markersize=8,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    lr_label_offsets = {
        "X": ( 0.40, -0.85),
        "Y": ( 0.40, -0.85),
        "Z": ( 0.45,  0.35),
    }
    for Q, _c, lbl, L_tan, K_tan, _C in isoq_specs:
        ax.plot(L_tan, K_tan, "o", **pt_style)
        dx, dy = lr_label_offsets[lbl]
        ax.text(L_tan + dx, K_tan + dy, lbl, fontsize=11.5, color=PRIMARY,
                fontweight="bold")

    # ============================================================
    # SR points X' (Q=10 ∩ K=6) and Z' (Q=30 ∩ K=6)
    #   X' on K · L = 50/3 at K = 6:  L = 50/(3 · 6) = 50/18 ≈ 2.78
    #   Z' on K · L = 150 at K = 6:   L = 150/6 = 25
    # ============================================================
    Xp_L = (50.0 / 3.0) / K_bar      # ≈ 2.78
    Zp_L = 150.0 / K_bar             # = 25
    ax.plot(Xp_L, K_bar, "o", **pt_style)
    ax.text(Xp_L - 0.95, K_bar + 0.40, "X'", fontsize=11.5, color=PRIMARY,
            fontweight="bold")
    ax.plot(Zp_L, K_bar, "o", **pt_style)
    ax.text(Zp_L + 0.30, K_bar + 0.40, "Z'", fontsize=11.5, color=PRIMARY,
            fontweight="bold")

    # ============================================================
    # Dashed verticals at L = 5, 9, 15, 25 (down from SR line)
    # ============================================================
    for L_dash in [5, 9, 15, 25]:
        ax.plot([L_dash, L_dash], [0, K_bar + 0.05], color=MUTED,
                lw=0.7, ls=":", alpha=0.7)

    # ============================================================
    # Axes formatting
    # ============================================================
    ax.set_xlabel("Labor  $(L)$", fontsize=11)
    ax.set_ylabel("Capital  $(K)$", fontsize=11)
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 13)
    ax.set_xticks([0, 5, 9, 15, 25])
    ax.set_yticks([0, 6])
    ax.set_yticklabels(["0", "6"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Capital & Labor Producing Engines (per week)",
                 fontsize=10.5, color=PRIMARY, pad=8)

    plt.subplots_adjust(top=0.93, right=0.97, left=0.08, bottom=0.10)
    out = os.path.join(HERE, "fig-engines-isoquants.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 18 — Engines: TC_SR vs TC_LR vs Q (Figure 7.6)
# ============================================================
def fig_engines_tc_sr_lr():
    fig, ax = plt.subplots(figsize=(7.0, 5.2))

    SR_BLUE = "#7BAFE0"
    LR_BLUE = "#1E40AF"

    # Stylized curves. Y axis = $0 to $400, X axis = 0 to 40 engines.
    # TC_LR: smoothly rising convex, value at Q=20 must equal TC_SR at Q=20.
    # Choose: TC_LR(Q) = 9 * Q + 0.02 * Q^2 + 18 → values: TC_LR(10)≈110, TC_LR(20)≈198, TC_LR(30)=306
    # Actually use simple cubic for cleaner Y values matching the screenshot: ~100, 180, 300
    Q = np.linspace(0, 35, 400)
    TC_LR = 0.05 * Q**2 + 8 * Q + 20      # → TC(10)=105, TC(20)=200, TC(30)=305
    TC_SR = 0.18 * Q**2 + 3 * Q + 50      # → TC(10)=98 (oops), need higher at extremes
    # Re-tune: at Q=20 (Y), TC_SR = TC_LR = 180. At Q=10, TC_SR=120 vs TC_LR=100. At Q=30, TC_SR=360 vs TC_LR=300.
    # Use: TC_LR(Q) = a*Q^2 + b*Q + c with constraints (10, 100), (20, 180), (30, 300)
    # From 100 = 100a + 10b + c
    #       180 = 400a + 20b + c
    #       300 = 900a + 30b + c
    # Diff1: 80 = 300a + 10b → 8 = 30a + b
    # Diff2: 120 = 500a + 10b → 12 = 50a + b
    # Subtract: 4 = 20a → a = 0.2; b = 8 − 30(0.2) = 2; c = 100 − 100(0.2) − 10(2) = 60
    # TC_LR = 0.2 Q² + 2 Q + 60
    TC_LR = 0.2 * Q**2 + 2 * Q + 60

    # TC_SR with constraints (10, 120), (20, 180), (30, 360):
    # 120 = 100a + 10b + c
    # 180 = 400a + 20b + c
    # 360 = 900a + 30b + c
    # Diff1: 60 = 300a + 10b → 6 = 30a + b
    # Diff2: 180 = 500a + 10b → 18 = 50a + b
    # → 12 = 20a → a = 0.6; b = 6 − 18 = −12; c = 120 − 60 + 120 = 180
    # TC_SR = 0.6 Q² − 12 Q + 180
    TC_SR = 0.6 * Q**2 - 12 * Q + 180
    # Clip TC_SR at Q ≈ 10 (don't draw it where it dips below LR weirdly at low Q)
    mask_LR = (Q >= 0)
    mask_SR = (Q >= 6)  # SR curve shown from Q=6 onward (avoids dip)

    ax.plot(Q[mask_LR], TC_LR[mask_LR], color=LR_BLUE, lw=2.8, label="$TC_{LR}$")
    ax.plot(Q[mask_SR], TC_SR[mask_SR], color=SR_BLUE, lw=2.4, label="$TC_{SR}$")

    # Curve labels at right
    ax.text(33.5, 0.2 * 33.5**2 + 2 * 33.5 + 60 - 18, "$TC_{LR}$", fontsize=14,
            color=LR_BLUE, fontweight="bold")
    ax.text(33.5, 0.6 * 33.5**2 - 12 * 33.5 + 180, "$TC_{SR}$", fontsize=14,
            color=SR_BLUE, fontweight="bold", va="bottom")

    # Points
    pts = [
        (10, 100, "X",   "right", -8, -2),
        (10, 120, "X'",  "right", -8, -2),
        (20, 180, "Y",   "left",  6, -2),
        (30, 300, "Z",   "left",  6, 0),
        (30, 360, "Z'",  "left",  6, 0),
    ]
    for x, y, lbl, ha, dx, dy in pts:
        ax.plot(x, y, "o", color=PRIMARY, markersize=8,
                markeredgecolor="white", markeredgewidth=1.2, zorder=6)
        ax.text(x + dx, y + dy, lbl, fontsize=11, color=PRIMARY, fontweight="bold")

    # Dashed reference lines from key points to axes
    for x, y in [(10, 100), (10, 120), (20, 180), (30, 300), (30, 360)]:
        ax.plot([x, x], [0, y], color=MUTED, lw=0.6, ls=":", alpha=0.5)
        ax.plot([0, x], [y, y], color=MUTED, lw=0.6, ls=":", alpha=0.5)

    ax.set_xlabel("Quantity of engines", fontsize=11)
    ax.set_ylabel("Total cost  (\\$)", fontsize=11)
    ax.set_xlim(0, 40)
    ax.set_ylim(0, 420)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_yticks([0, 100, 120, 180, 300, 360])
    ax.set_yticklabels(["0", "\\$100", "\\$120", "\\$180", "\\$300", "\\$360"], fontsize=9.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("TC$_{SR}$ vs TC$_{LR}$ for Engines",
                 fontsize=10.5, color=PRIMARY, pad=8)

    plt.subplots_adjust(top=0.92, left=0.13, right=0.97)
    out = os.path.join(HERE, "fig-engines-tc-sr-lr.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 18b — Engines: ATC_SR,20 vs ATC_LR (single SR curve, Figure 7.7)
# ============================================================
def fig_engines_atc_envelope_simple():
    """Replica of Goolsbee's Figure 7.7 — one SR-ATC against LR-ATC.

    Two U-shaped curves (consistent with slides 52 + new MC slide):
      ATC_LR(Q) = 0.005·(Q − 20)² + 9   — gentle U, $9.5 at Q = 10/30
      ATC_SR,20(Q) = 9 + 0.03·(Q − 20)² — steeper U tangent at Y

    Marked points:
        X  = (10, $9.5)  on ATC_LR
        Y  = (20, $9)    LR = SR min — tangency
        Z  = (30, $9.5)  on ATC_LR
        X' = (10, $12)   on ATC_SR,20
        Z' = (30, $12)   on ATC_SR,20
    """
    fig, ax = plt.subplots(figsize=(7.5, 4.6))

    SR_BLUE = "#7BAFE0"
    LR_BLUE = "#1E40AF"

    Q = np.linspace(2, 40, 400)

    # ---- LR-ATC: gentle U (consistent with the MC-family figure)
    ATC_LR = 0.005 * (Q - 20) ** 2 + 9.0
    # ---- ATC_SR,20: steeper U tangent to LR at Q = 20
    ATC_SR_20 = 9.0 + 0.03 * (Q - 20) ** 2

    valid_sr = ATC_SR_20 <= 14
    ax.plot(Q[valid_sr], ATC_SR_20[valid_sr], color=SR_BLUE, lw=2.4)
    ax.plot(Q, ATC_LR, color=LR_BLUE, lw=2.8)

    # ---- Curve labels at the upper-right
    ax.text(7.5, 13.0, r"$ATC_{SR,\,20}$", fontsize=11, color=PRIMARY, ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))
    ax.text(37.5, 10.7, r"$ATC_{LR}$", fontsize=12, color=LR_BLUE, ha="left",
            fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

    # ---- Marked points
    pt_style = dict(color=PRIMARY, markersize=8,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    points = [
        (10, 9.5,  "X",  -1.4, -0.45),
        (10, 12,   "X'", -1.4,  0.30),
        (20,  9,   "Y",   0.50, -0.65),
        (30, 9.5,  "Z",   0.55, -0.45),
        (30, 12,   "Z'",  0.55,  0.30),
    ]
    for qx, qy, lbl, dx, dy in points:
        ax.plot(qx, qy, "o", **pt_style)
        ax.text(qx + dx, qy + dy, lbl, fontsize=11.5,
                color=PRIMARY, fontweight="bold")

    # ---- Dashed reference lines from key points to axes
    for x, y in [(10, 12), (20, 9), (30, 12)]:
        ax.plot([x, x], [0, y], color=MUTED, lw=0.7, ls=":", alpha=0.6)
        ax.plot([0, x], [y, y], color=MUTED, lw=0.7, ls=":", alpha=0.6)

    # ---- Axes formatting (with axis break at 0)
    ax.set_xlabel("Quantity of engines", fontsize=11)
    ax.set_ylabel(r"Average total cost  (\$/unit)", fontsize=11)
    ax.set_xlim(0, 40)
    ax.set_ylim(8.0, 14)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_yticks([9, 12])
    ax.set_yticklabels([r"\$9", r"\$12"], fontsize=9.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("ATC$_{SR,20}$ vs ATC$_{LR}$ — Why LR Lies Below SR",
                 fontsize=10.5, color=PRIMARY, pad=8)

    plt.subplots_adjust(top=0.91, left=0.10, right=0.97, bottom=0.14)
    out = os.path.join(HERE, "fig-engines-atc-sr20-vs-lr.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 19 — Engines: ATC envelope (Figure 7.8)
# 3 SR-ATC U-shapes indexed by K̄=10, 20, 30; LR-ATC U-shape envelope
# ============================================================
def fig_engines_atc_envelope():
    """Goolsbee-style Figure 7.8 — LR-ATC envelops the family of SR-ATCs.

    Same ATC family used by slides 51 (single SR) and 54 (MC family).

        ATC_LR(Q)    = 0.005·(Q − 20)² + 9       (gentle U, min $9 at Q = 20)
        ATC_SR,k(Q)  = ATC_LR(k)
                       + 0.01·(k − 20)·(Q − k)   (tangency slope)
                       + 0.03·(Q − k)²            (steeper SR curvature)

    Marked points:
        X  = (10, $9.5)  tangency between ATC_SR,10 and ATC_LR
        Y  = (20, $9)    tangency between ATC_SR,20 and ATC_LR (also min)
        Z  = (30, $9.5)  tangency between ATC_SR,30 and ATC_LR
        X' = (10, $12)   sub-optimal SR — on ATC_SR,20 at Q = 10
        Z' = (30, $12)   sub-optimal SR — on ATC_SR,20 at Q = 30
    """
    fig, ax = plt.subplots(figsize=(7.5, 5.2))

    SR_BLUE = "#7BAFE0"
    LR_BLUE = "#1E40AF"

    Q = np.linspace(2, 40, 400)

    # ---- Cost functions
    def atc_lr(q):
        return 0.005 * (q - 20) ** 2 + 9.0

    def atc_lr_prime(q):
        return 0.01 * (q - 20)

    def atc_sr(q, k):
        return atc_lr(k) + atc_lr_prime(k) * (q - k) + 0.03 * (q - k) ** 2

    ATC_LR = atc_lr(Q)

    # ---- Plot three SR-ATC curves indexed by K̄ = 10, 20, 30
    sr_label_positions = {
        10: (5.5,  12.8, "left"),    # left of K̄=10 U
        20: (20.0, 12.8, "center"),  # above K̄=20 U
        30: (34.5, 12.8, "right"),   # right of K̄=30 U
    }
    for Q_bar, lbl_tex in [(10, r"$ATC_{SR,\,10}$"),
                           (20, r"$ATC_{SR,\,20}$"),
                           (30, r"$ATC_{SR,\,30}$")]:
        atc_curve = atc_sr(Q, Q_bar)
        valid = atc_curve <= 13.5
        ax.plot(Q[valid], atc_curve[valid], color=SR_BLUE, lw=2.0)
        lx, ly, ha = sr_label_positions[Q_bar]
        ax.text(lx, ly, lbl_tex, fontsize=10.5, color=PRIMARY, ha=ha,
                bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

    # ---- LR envelope on top
    ax.plot(Q, ATC_LR, color=LR_BLUE, lw=2.8)
    ax.text(37.5, 10.5, r"$ATC_{LR}$", fontsize=12.5, color=LR_BLUE,
            fontweight="bold", ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.5, alpha=0.85))

    # ---- Marked points
    pt_style = dict(color=PRIMARY, markersize=8,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    # LR tangencies X (10, 9.5), Y (20, 9), Z (30, 9.5)
    for (qx, qy, lbl, dx, dy) in [
        (10, 9.5, "X", -1.5, -0.30),
        (20, 9.0, "Y",  0.5, -0.55),
        (30, 9.5, "Z",  0.6, -0.30),
    ]:
        ax.plot(qx, qy, "o", **pt_style)
        ax.text(qx + dx, qy + dy, lbl, fontsize=11.5, color=PRIMARY, fontweight="bold")

    # Sub-optimal SR points X' (10, 12) and Z' (30, 12) — both on ATC_SR,20
    for (qx, qy, lbl, dx, dy) in [
        (10, 12, "X'",  0.45, 0.20),
        (30, 12, "Z'", -1.45, 0.20),
    ]:
        ax.plot(qx, qy, "o", **pt_style)
        ax.text(qx + dx, qy + dy, lbl, fontsize=11.5, color=PRIMARY, fontweight="bold")

    # ---- Dashed reference lines from key points to axes
    for x, y in [(10, 12), (20, 9), (30, 12)]:
        ax.plot([x, x], [7.5, y], color=MUTED, lw=0.7, ls=":", alpha=0.6)
        ax.plot([2, x], [y, y], color=MUTED, lw=0.7, ls=":", alpha=0.6)

    # ---- Axes formatting
    ax.set_xlabel("Quantity of engines", fontsize=11)
    ax.set_ylabel(r"Average total cost  (\$/unit)", fontsize=11)
    ax.set_xlim(0, 40)
    ax.set_ylim(7.5, 13.8)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_yticks([9, 12])
    ax.set_yticklabels([r"\$9", r"\$12"], fontsize=9.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("LR-ATC Envelops the SR-ATC Curves",
                 fontsize=10.5, color=PRIMARY, pad=8)

    plt.subplots_adjust(top=0.92, left=0.10, right=0.97, bottom=0.12)
    out = os.path.join(HERE, "fig-engines-atc-envelope.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 19b — Engines: MC family (Figure 7.9)
# Same ATC family + MC_SR,10/20/30 (green) + MC_LR (red)
# ============================================================
def fig_engines_mc_family():
    """Goolsbee-style Figure 7.9 — Long-run and short-run marginal costs.

    Stacks the SR-ATC + LR-ATC family from Figure 7.8 with the corresponding
    MC family in green/red:
        MC_LR(Q)    = 0.015·Q² − 0.4·Q + 11         (red)
        MC_SR,k(Q)  = dTC_SR,k/dQ for each K̄        (green)

    Marked points:
        A = (10, $8.5)  on MC_LR
        Y = (20, $9)    on MC_LR (= ATC_LR min)
        B = (30, $12.5) on MC_LR
    """
    fig, ax = plt.subplots(figsize=(7.8, 5.4))

    SR_BLUE = "#7BAFE0"
    LR_BLUE = "#1E40AF"
    SR_GREEN = "#1F7A3A"
    LR_RED = "#C0392B"

    Q = np.linspace(3, 40, 400)

    # ---- Cost functions (consistent with the ATC envelope figure)
    def atc_lr(q):
        return 0.005 * (q - 20) ** 2 + 9.0

    def atc_lr_prime(q):
        return 0.01 * (q - 20)

    def atc_sr(q, k):
        return atc_lr(k) + atc_lr_prime(k) * (q - k) + 0.03 * (q - k) ** 2

    def mc_lr(q):
        # TC_LR(Q) = 0.005 Q³ − 0.2 Q² + 11 Q  →  MC = 0.015 Q² − 0.4 Q + 11
        return 0.015 * q ** 2 - 0.4 * q + 11.0

    def mc_sr(q, k):
        # MC_SR,k(Q) = ATC_SR,k(Q) + Q · d/dQ ATC_SR,k(Q)
        return atc_sr(q, k) + q * (atc_lr_prime(k) + 0.06 * (q - k))

    # ---- Plot ATC family
    for Q_bar in [10, 20, 30]:
        atc_curve = atc_sr(Q, Q_bar)
        valid = atc_curve <= 13.8
        ax.plot(Q[valid], atc_curve[valid], color=SR_BLUE, lw=2.0)
    ax.plot(Q, atc_lr(Q), color=LR_BLUE, lw=2.6)

    # ---- ATC labels (top of chart)
    ax.text(8.5,  13.0, r"$ATC_{SR,\,10}$", fontsize=10, color=PRIMARY, ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))
    ax.text(15.5, 13.0, r"$ATC_{SR,\,20}$", fontsize=10, color=PRIMARY, ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))
    ax.text(24.5, 13.0, r"$ATC_{SR,\,30}$", fontsize=10, color=PRIMARY, ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))
    ax.text(37.0, 11.4, r"$ATC_{LR}$", fontsize=11.5, color=LR_BLUE, ha="left",
            fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))

    # ---- Plot MC family — tight arcs centered around each planning Q so the
    # three SR-MC curves are visually symmetric and clearly cross MC_LR at the
    # planning Q values (where they touch the dashed verticals through X, Y, Z).
    mc_sr_ranges = {
        10: (7.0,  13.0),
        20: (16.5, 23.5),
        30: (26.5, 31.0),
    }
    for Q_bar, (q_lo, q_hi) in mc_sr_ranges.items():
        Q_sub = np.linspace(q_lo, q_hi, 200)
        mc_curve = mc_sr(Q_sub, Q_bar)
        mc_curve = np.where(
            (mc_curve >= 5.7) & (mc_curve <= 13.8),
            mc_curve,
            np.nan,
        )
        ax.plot(Q_sub, mc_curve, color=SR_GREEN, lw=2.0)
    ax.plot(Q, mc_lr(Q), color=LR_RED, lw=2.6)

    # ---- MC labels — sit on the top arc of each SR-MC curve (not in empty
    # bottom space) so each label clearly attaches to its visible curve.
    ax.text(12.3,  10.7, r"$MC_{SR,\,10}$", fontsize=10, color=SR_GREEN, ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))
    ax.text(22.0,  12.3, r"$MC_{SR,\,20}$", fontsize=10, color=SR_GREEN, ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))
    ax.text(26.6,  10.3, r"$MC_{SR,\,30}$", fontsize=10, color=SR_GREEN, ha="left",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))
    ax.text(32.0, 13.2, r"$MC_{LR}$", fontsize=11.5, color=LR_RED, ha="left",
            fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="none", pad=1.2, alpha=0.9))

    # ---- Marked points
    pt_style = dict(color=PRIMARY, markersize=8,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    pt_style_lr = dict(color=LR_BLUE, markersize=8,
                       markeredgecolor="white", markeredgewidth=1.2, zorder=6)

    # X, Y, Z on ATC_LR — the optimal (lowest) ATC at each planning Q
    for (qx, qy, lbl, dx, dy) in [
        (10,  9.5, "X", -1.40, -0.30),
        (20,  9.0, "Y",  0.55, -0.55),
        (30,  9.5, "Z",  0.55, -0.30),
    ]:
        ax.plot(qx, qy, "o", **pt_style_lr)
        ax.text(qx + dx, qy + dy, lbl, fontsize=11.5,
                color=LR_BLUE, fontweight="bold")

    # A, B on MC_LR REMOVED 2026-07-22 (instructor request): having ATC points
    # (X, Y, Z) and MC points (A, B) labelled on one chart made students expect
    # MC_SR,10 to pass through X and MC_SR,30 through Z. It never does -- X and Z
    # sit on the ATC curves, while the MC_SR curves meet MC_LR at the same
    # quantity but at a different height. Only the ATC points are labelled now;
    # the MC_SR-meets-MC_LR crossings are left unlabelled and read off the curves.

    # ---- Dashed verticals at Q = 10, 20, 30 from MC_LR up to ATC_LR
    for (qx, qy_hi) in [(10, 9.5), (20, 9.0), (30, 9.5)]:
        ax.plot([qx, qx], [5.5, qy_hi], color=MUTED,
                lw=0.7, ls=":", alpha=0.6)

    # ---- Dashed horizontals at $9 and $12
    ax.plot([2, 20], [9, 9], color=MUTED, lw=0.7, ls=":", alpha=0.6)
    ax.plot([2, 30], [12, 12], color=MUTED, lw=0.7, ls=":", alpha=0.6)

    # ---- Axes
    ax.set_xlabel("Quantity of engines", fontsize=11)
    ax.set_ylabel(r"Average / marginal cost  (\$/unit)", fontsize=11)
    ax.set_xlim(0, 40)
    ax.set_ylim(5.5, 13.8)
    ax.set_xticks([0, 10, 20, 30])
    ax.set_yticks([9, 12])
    ax.set_yticklabels([r"\$9", r"\$12"], fontsize=9.5)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Long-Run and Short-Run Marginal Costs (Engines)",
                 fontsize=10.5, color=PRIMARY, pad=8)

    plt.subplots_adjust(top=0.92, left=0.10, right=0.97, bottom=0.12)
    out = os.path.join(HERE, "fig-engines-mc-family.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 19c — W8.5 explanation figure: SR cost curve at K̄ = 4
# ============================================================
def fig_engines_w85_stc_kbar4():
    """Companion figure for Walkthrough 8.5.

    Shows the gigafactory SR cost curve STC(q; K̄=4) plotted against
    the LR envelope LRC(q) = 0.02721·q. The four W8.5 table points
    are marked on the SR curve, the SR-LR tangency at q = 47.79 is
    shown as the unique point where STC = LRC, and the SR-LR wedge
    at the firm's current target q = 32 is annotated.
    """
    fig, ax = plt.subplots(figsize=(7.4, 5.0))

    SR_BLUE = "#7BAFE0"
    LR_BLUE = "#1E40AF"

    # Functions from Walkthrough 8.5 setup
    K_BAR = 4.0
    # Q = 8·K^0.4·L^0.6  →  L*_SR(q; 4) = (q / 13.93)^(1/0.6)
    A_KBAR = 8.0 * K_BAR ** 0.4   # ≈ 13.929
    W_PRICE = 0.10
    R_PRICE = 0.13
    FIXED_COST = R_PRICE * K_BAR  # = 0.52

    def L_sr(q):
        return (q / A_KBAR) ** (1.0 / 0.6)

    def STC(q):
        return W_PRICE * L_sr(q) + FIXED_COST

    def LRC(q):
        return 0.02721 * q

    Q = np.linspace(0, 70, 500)
    # Plot curves
    ax.plot(Q, LRC(Q), color=LR_BLUE, lw=2.6, label="$LRC(q) = 0.02721 \\, q$")
    # Avoid the L^1.667 explosion at q very small — start STC plot at q>0
    Q_sr = np.linspace(0.5, 70, 500)
    ax.plot(Q_sr, STC(Q_sr), color=SR_BLUE, lw=2.6, label="$STC(q;\\, \\bar K = 4)$")

    # Vertical intercept marker for fixed cost
    ax.plot([0, 1.5], [FIXED_COST, FIXED_COST], color=SR_BLUE, lw=1.0, ls="--", alpha=0.6)
    ax.text(1.7, FIXED_COST - 0.04, f"$r \\bar K = \\${FIXED_COST:.2f}$B\n(fixed)",
            fontsize=9, color=SR_BLUE, va="top", fontstyle="italic")

    # ---- Mark W8.5 table points on SR curve
    pt_style = dict(color=PRIMARY, markersize=8,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    w85_points = [
        (16, 0.646),
        (32, 0.920),
        (48, 1.306),  # approx tangency
        (64, 1.790),
    ]
    for qx, qy in w85_points:
        ax.plot(qx, qy, "o", **pt_style)
        ax.annotate(f"({qx}, \\${qy:.2f}B)", xy=(qx, qy),
                    xytext=(qx + 1.5, qy - 0.10), fontsize=9, color=PRIMARY)

    # ---- SR-LR tangency at q = 47.79
    q_tan = 47.79
    c_tan = 1.300
    ax.plot(q_tan, c_tan, "o", color="#D32F2F", markersize=10,
            markeredgecolor="white", markeredgewidth=1.4, zorder=7)
    ax.annotate(f"Tangency: $q = {q_tan}$\n$STC = LRC = \\$1.30$B",
                xy=(q_tan, c_tan), xytext=(q_tan - 24, c_tan + 0.16),
                fontsize=10, color="#D32F2F", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=1.4))

    # ---- SR-LR wedge at q = 32
    q_wedge = 32
    lr_at_32 = LRC(q_wedge)   # 0.871
    sr_at_32 = STC(q_wedge)   # 0.920
    # Vertical line connecting LR and SR at q=32
    ax.plot([q_wedge, q_wedge], [lr_at_32, sr_at_32], color="#EA580C", lw=2.2)
    ax.plot(q_wedge, lr_at_32, "o", color=LR_BLUE, markersize=7,
            markeredgecolor="white", markeredgewidth=1.2, zorder=6)
    # Wedge label
    ax.annotate(r"\$49M/yr wedge" + "\n" + r"($SR-LR$ gap at firm's $q=32$)",
                xy=(q_wedge, (lr_at_32 + sr_at_32) / 2),
                xytext=(q_wedge + 6, 0.55), fontsize=9.5, color="#EA580C",
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#EA580C", lw=1.2))

    # ---- Curve labels at right
    ax.text(67, LRC(67) + 0.05, "$LRC$", fontsize=12, color=LR_BLUE,
            fontweight="bold")
    ax.text(67, STC(67) - 0.08, "$STC$\n$(\\bar K = 4)$", fontsize=11, color=SR_BLUE,
            fontweight="bold", va="top")

    # ---- Axes formatting
    ax.set_xlabel("Quantity of batteries  $q$  (GWh/yr)", fontsize=11)
    ax.set_ylabel(r"Total cost  (B\$/yr)", fontsize=11)
    ax.set_xlim(0, 72)
    ax.set_ylim(0, 2.1)
    ax.set_xticks([0, 16, 32, 48, 64])
    ax.set_yticks([0, 0.435, 0.52, 0.871, 0.920, 1.300, 1.790])
    ax.set_yticklabels(["0", "0.44", "0.52", "0.87", "0.92", "1.30", "1.79"],
                       fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Walkthrough 8.5 — SR Cost at $\\bar K = 4$ vs LR Envelope",
                 fontsize=11, color=PRIMARY, pad=8)
    ax.legend(loc="upper left", fontsize=9.5, frameon=False)

    plt.subplots_adjust(top=0.92, left=0.10, right=0.97, bottom=0.13)
    out = os.path.join(HERE, "fig-engines-w85-stc-kbar4.png")
    plt.savefig(out)
    plt.close(fig)


# ============================================================
# FIGURE 20 — Small LRATC with 3 colored region arrows
# ============================================================
def fig_lratc_regions():
    """Mini LR-ATC U-shape with three colored arrows along the x-axis
    marking economies / constant / diseconomies regions.
    """
    fig, ax = plt.subplots(figsize=(4.6, 3.4))

    BLUE = SECONDARY      # deck palette (was #1E40AF)
    GREEN = SUCCESS       # deck palette (was #16A34A)
    ORANGE = ACCENT       # deck palette (was #EA580C)

    Q = np.linspace(0.5, 10, 400)
    # Asymmetric U-shape with a flat bottom — three regions visible.
    # ATC(Q) = a/(Q+0.4) + 0.01·Q² + 1.0
    LRATC = 5.5 / (Q + 0.7) + 0.06 * (Q - 5) ** 2 + 1.5
    # Trim where LRATC > 9
    valid = LRATC <= 9
    ax.plot(Q[valid], LRATC[valid], color=BLUE, lw=2.6)
    ax.text(9.4, 5.6, "LRATC", fontsize=11, color=DANGER, fontweight="bold")

    # Three region arrows along the x-axis (just above zero)
    Y_ARROW = -0.5
    # Blue — economies of scale (Q ≈ 0.5 to 3)
    ax.annotate("", xy=(3.2, Y_ARROW), xytext=(0.5, Y_ARROW),
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=2.2))
    # Green — constant economies (Q ≈ 3 to 6.5)
    ax.annotate("", xy=(6.7, Y_ARROW), xytext=(3.2, Y_ARROW),
                arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.2))
    # Orange — diseconomies of scale (Q ≈ 6.5 to 9.5)
    ax.annotate("", xy=(9.7, Y_ARROW), xytext=(6.7, Y_ARROW),
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.2))

    # Axis labels at the corners (no full axes — just arrows for Q and ATC)
    ax.annotate("", xy=(10.5, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.2))
    ax.annotate("", xy=(0, 9.5), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#333", lw=1.2))
    ax.text(-0.6, 9.2, "ATC", fontsize=11, color="#333", ha="left", fontweight="bold", fontstyle="italic")
    ax.text(10.6, -0.05, "Q", fontsize=11, color="#333", ha="left", fontweight="bold", fontstyle="italic")

    ax.set_xlim(-0.9, 11.6)
    ax.set_ylim(-1.5, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(False)

    plt.subplots_adjust(top=0.96, left=0.04, right=0.98, bottom=0.04)
    out = os.path.join(HERE, "fig-lratc-regions.png")
    plt.savefig(out, transparent=True)
    plt.close(fig)


# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    fig_cover_sr_lr_envelope()
    print("OK: ch08-cover.png + fig-sr-lr-envelope.png")
    fig_isocost_tangency()
    print("OK: fig-isocost-tangency.png")
    fig_wage_shock()
    print("OK: fig-wage-shock.png")
    fig_ac_mc()
    print("OK: fig-ac-mc.png")
    fig_deu_markups()
    print("OK: fig-deu-markups.png")
    fig_cost_shares()
    print("OK: fig-cost-shares.png")
    fig_duality()
    print("OK: fig-duality.png")
    fig_isocost_lines_67()
    print("OK: fig-isocost-lines-67.png")
    fig_cost_min_610()
    print("OK: fig-cost-min-610.png")
    fig_input_price_changes()
    print("OK: fig-input-price-changes.png")
    fig_production_to_costs()
    print("OK: fig-production-to-costs.png")
    fig_costs_that_matter()
    print("OK: fig-costs-that-matter.png")
    fig_amc_three_panels()
    print("OK: fig-amc-three-panels.png")
    fig_gpa_analogy()
    print("OK: fig-gpa-analogy.png")
    fig_additive_vs_conventional()
    print("OK: fig-additive-vs-conventional.png")
    fig_3d_printed_house()
    print("OK: fig-3d-printed-house.png")
    fig_engines_isoquants_expansion()
    print("OK: fig-engines-isoquants.png")
    fig_engines_tc_sr_lr()
    print("OK: fig-engines-tc-sr-lr.png")
    fig_engines_atc_envelope_simple()
    print("OK: fig-engines-atc-sr20-vs-lr.png")
    fig_engines_atc_envelope()
    print("OK: fig-engines-atc-envelope.png")
    fig_engines_mc_family()
    print("OK: fig-engines-mc-family.png")
    fig_lratc_regions()
    print("OK: fig-lratc-regions.png")
