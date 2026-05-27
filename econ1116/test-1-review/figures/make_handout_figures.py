"""Generate handout-problem figures for the Test 1 Review deck.
Clean palette matching the deck theme.
"""
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT = Path(__file__).parent

# Clean palette (same as deck)
C_PRIMARY = "#0F172A"
C_ACCENT = "#2563EB"      # blue — demand
C_SECOND = "#059669"      # emerald — supply
C_CS_FILL = "#DBEAFE"     # light blue — CS
C_PS_FILL = "#D1FAE5"     # light green — PS
C_GRID = "#E2E8F0"


def setup_axes(ax, x_max, y_max, title):
    ax.set_xlim(0, x_max)
    ax.set_ylim(0, y_max)
    ax.set_xlabel("Quantity (Q, dozens)", fontsize=11, color=C_PRIMARY, fontweight="bold")
    ax.set_ylabel("Price (P, $/dozen)", fontsize=11, color=C_PRIMARY, fontweight="bold")
    ax.set_title(title, fontsize=13, color=C_PRIMARY, fontweight="bold", pad=14)
    ax.grid(True, linestyle="-", linewidth=0.5, color=C_GRID, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(C_PRIMARY)
    ax.spines["bottom"].set_color(C_PRIMARY)
    ax.tick_params(colors=C_PRIMARY)


# Ch 5 deck handout figure: artisanal donut market
# Demand: P = 12 - 0.1Q  (intercepts $12 at Q=0, Q=120 at P=0)
# Supply: P = 4 + 0.1Q  (intercept $4 at Q=0)
# Equilibrium: 12 - 0.1Q = 4 + 0.1Q → Q* = 40, P* = $8
# CS = ½ × 40 × (12 - 8) = $80
# PS = ½ × 40 × (8 - 4) = $80
# TS = $160
def fig_ch5_handout():
    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=150)
    Q = np.linspace(0, 120, 200)
    D = 12 - 0.1 * Q
    S = 4 + 0.1 * Q

    # Shade CS (above $8, below D, 0..40)
    Q_eq = np.linspace(0, 40, 100)
    D_eq = 12 - 0.1 * Q_eq
    ax.fill_between(Q_eq, 8, D_eq, color=C_CS_FILL, alpha=0.6, label="Consumer Surplus")
    # Shade PS (below $8, above S, 0..40)
    S_eq = 4 + 0.1 * Q_eq
    ax.fill_between(Q_eq, S_eq, 8, color=C_PS_FILL, alpha=0.6, label="Producer Surplus")

    ax.plot(Q, D, color=C_ACCENT, linewidth=2.5, label="Demand (D)")
    ax.plot(Q, S, color=C_SECOND, linewidth=2.5, label="Supply (S)")

    # Equilibrium marker
    ax.plot([40], [8], "o", color=C_PRIMARY, markersize=8)
    ax.plot([40, 40], [0, 8], "--", color=C_PRIMARY, linewidth=0.8, alpha=0.5)
    ax.plot([0, 40], [8, 8], "--", color=C_PRIMARY, linewidth=0.8, alpha=0.5)

    # Demand intercept marker
    ax.plot([0], [12], "o", color=C_ACCENT, markersize=6)
    # Supply intercept marker
    ax.plot([0], [4], "o", color=C_SECOND, markersize=6)

    # Annotations
    ax.annotate("P* = $8", xy=(40, 8), xytext=(60, 9.5),
                fontsize=11, color=C_PRIMARY, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_PRIMARY, lw=0.7))
    ax.annotate("Q* = 40", xy=(40, 0.3), xytext=(48, 1.2),
                fontsize=11, color=C_PRIMARY, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_PRIMARY, lw=0.7))
    ax.annotate("$12", xy=(0, 12), xytext=(-8, 12), fontsize=10,
                color=C_ACCENT, fontweight="bold", ha="right")
    ax.annotate("$4", xy=(0, 4), xytext=(-8, 4), fontsize=10,
                color=C_SECOND, fontweight="bold", ha="right")

    setup_axes(ax, 120, 13, "Cambridge Donut Market — Read CS, PS, TS")
    ax.legend(loc="upper right", framealpha=0.95, fontsize=9, edgecolor=C_GRID)
    plt.tight_layout()
    plt.savefig(OUT / "ch5-handout-donuts.png", bbox_inches="tight", facecolor="white", dpi=150)
    plt.close()
    print("✓ ch5-handout-donuts.png")


# Ch 7 deck handout figure: NYC rent control with binding ceiling
# Demand: P = 5000 - 2Q  (intercept $5000 at Q=0; Q=2500 at P=0)
# Supply: P = 1000 + 2Q
# Equilibrium: 5000 - 2Q = 1000 + 2Q → Q* = 1000, P* = $3000
# Ceiling at $2,000: Q_s = 500 (only this many supplied)
# Q_d at $2,000 = (5000-2000)/2 = 1500. Shortage = 1000.
# DWL = ½ × (1000 - 500) × (D - S at Q=500) = ½ × 500 × (4000 - 2000) = $500,000/month
def fig_ch7_handout():
    fig, ax = plt.subplots(figsize=(7, 4.8), dpi=150)
    Q = np.linspace(0, 2500, 200)
    D = 5000 - 2 * Q
    S = 1000 + 2 * Q

    # DWL triangle (Q=500 to Q=1000, between D and S)
    Q_dwl = np.linspace(500, 1000, 50)
    D_dwl = 5000 - 2 * Q_dwl
    S_dwl = 1000 + 2 * Q_dwl
    C_DWL_FILL = "#FEE2E2"
    ax.fill_between(Q_dwl, S_dwl, D_dwl, color=C_DWL_FILL, alpha=0.85, label="Deadweight Loss")

    # Shortage shading (Q=500 to Q=1500 at the ceiling level)
    C_SHORTAGE = "#FEF3C7"
    ax.fill_between([500, 1500], [2000, 2000], [2000.01, 2000.01],
                    color=C_SHORTAGE, alpha=0)  # just to register label
    # Draw shortage bar (horizontal segment at $2,000)
    ax.plot([500, 1500], [2000, 2000], color="#F59E0B", linewidth=4, alpha=0.7,
            label="Shortage (Q_d − Q_s)")

    # Curves
    ax.plot(Q, D, color=C_ACCENT, linewidth=2.5, label="Demand")
    ax.plot(Q, S, color=C_SECOND, linewidth=2.5, label="Supply")

    # Ceiling line
    ax.axhline(2000, color="#B91C1C", linewidth=2, linestyle="--", alpha=0.9,
               label="Rent Ceiling = $2,000")

    # Equilibrium marker
    ax.plot([1000], [3000], "o", color=C_PRIMARY, markersize=8)
    # Q_s marker (where supply meets ceiling)
    ax.plot([500], [2000], "o", color="#B91C1C", markersize=7)
    # Q_d marker
    ax.plot([1500], [2000], "o", color="#B91C1C", markersize=7)
    # Reference dashed lines
    ax.plot([1000, 1000], [0, 3000], "--", color=C_PRIMARY, linewidth=0.7, alpha=0.4)
    ax.plot([0, 1000], [3000, 3000], "--", color=C_PRIMARY, linewidth=0.7, alpha=0.4)
    ax.plot([500, 500], [0, 2000], ":", color="#B91C1C", linewidth=0.7, alpha=0.6)
    ax.plot([1500, 1500], [0, 2000], ":", color="#B91C1C", linewidth=0.7, alpha=0.6)

    # Annotations
    ax.annotate("P* = $3,000", xy=(1000, 3000), xytext=(1400, 3500),
                fontsize=10, color=C_PRIMARY, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_PRIMARY, lw=0.7))
    ax.annotate("Q* = 1000", xy=(1000, 100), xytext=(1100, 400),
                fontsize=10, color=C_PRIMARY, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=C_PRIMARY, lw=0.7))
    ax.text(500, -300, "Q_s=500", fontsize=9, color="#B91C1C",
            fontweight="bold", ha="center")
    ax.text(1500, -300, "Q_d=1500", fontsize=9, color="#B91C1C",
            fontweight="bold", ha="center")
    ax.text(750, 2700, "DWL", fontsize=10, color="#B91C1C", fontweight="bold", ha="center")

    ax.set_xlim(0, 2500)
    ax.set_ylim(-500, 5500)
    ax.set_xlabel("Apartments (Q, thousands)", fontsize=11, color=C_PRIMARY, fontweight="bold")
    ax.set_ylabel("Rent (P, $/month)", fontsize=11, color=C_PRIMARY, fontweight="bold")
    ax.set_title("NYC Apartment Market with $2,000 Rent Ceiling",
                 fontsize=13, color=C_PRIMARY, fontweight="bold", pad=14)
    ax.grid(True, linestyle="-", linewidth=0.5, color=C_GRID, alpha=0.7)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(C_PRIMARY)
    ax.spines["bottom"].set_color(C_PRIMARY)
    ax.tick_params(colors=C_PRIMARY)
    ax.legend(loc="upper right", framealpha=0.95, fontsize=8.5, edgecolor=C_GRID)
    plt.tight_layout()
    plt.savefig(OUT / "ch7-handout-rent-ceiling.png",
                bbox_inches="tight", facecolor="white", dpi=150)
    plt.close()
    print("✓ ch7-handout-rent-ceiling.png")


if __name__ == "__main__":
    fig_ch5_handout()
    fig_ch7_handout()
    print("Done.")
