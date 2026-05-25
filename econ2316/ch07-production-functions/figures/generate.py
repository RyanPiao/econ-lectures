"""Generate figures for ECON 2316 Ch 7 lecture slides (Production Functions).
White Academia palette: dusty blue, terracotta, sage, charcoal."""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path(__file__).parent

# White Academia palette
NAVY    = "#2D2D2D"
BLUE    = "#6B8BA4"
TERRA   = "#C47B5A"
SAGE    = "#6A8E6B"
ROSE    = "#A85C5C"
MUTED   = "#8C8580"
LINE    = "#D5CEC7"
PAPER   = "#F8F6F3"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": NAVY,
    "axes.labelcolor": NAVY,
    "xtick.color": NAVY,
    "ytick.color": NAVY,
    "axes.linewidth": 1.2,
})

# ---------- Cover image: stylized isoquant family at the gigafactory anchor ----------
def fig_cover():
    fig, ax = plt.subplots(figsize=(10, 7.5))
    L = np.linspace(0.5, 14, 400)
    # Cobb-Douglas Q = 8 K^0.4 L^0.6  =>  K = (Q/(8 L^0.6))^(1/0.4)
    for Q, alpha in [(16, 0.4), (24, 0.6), (32, 1.0), (40, 0.7), (48, 0.5)]:
        K_iso = (Q/(8*L**0.6))**(1/0.4)
        m = K_iso < 12
        ax.plot(L[m], K_iso[m], color=BLUE, linewidth=2.2, alpha=alpha)
        if Q == 32:
            ax.plot(L[m], K_iso[m], color=TERRA, linewidth=3.2, alpha=1.0)
    # Mark the gigafactory anchor
    ax.scatter([4], [4], s=260, color=TERRA, edgecolor="white", linewidth=3.5, zorder=5)
    ax.annotate("Tesla Nevada\nK=$4B,  L=4,000\nQ=32 GWh/yr",
                xy=(4, 4), xytext=(6.8, 7.2),
                fontsize=14, fontweight="bold", color=NAVY,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6),
                ha="left", va="center")
    ax.text(11.5, 0.8, "Q = 48", fontsize=12, color=BLUE)
    ax.text(11.5, 1.5, "Q = 40", fontsize=12, color=BLUE)
    ax.text(11.5, 2.5, "Q = 32", fontsize=13, color=TERRA, fontweight="bold")
    ax.text(11.5, 3.7, "Q = 24", fontsize=12, color=BLUE)
    ax.text(11.5, 6.3, "Q = 16", fontsize=12, color=BLUE)
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Labor, L  (thousand workers)", fontsize=14)
    ax.set_ylabel("Capital, K  (billion $)", fontsize=14)
    ax.set_title("Production Functions  ·  Q = 8 K$^{0.4}$ L$^{0.6}$",
                 fontsize=15, color=NAVY, pad=14)
    fig.patch.set_facecolor("white")
    plt.tight_layout()
    plt.savefig(OUT/"ch07-cover.png", dpi=160, bbox_inches="tight", facecolor="white")
    plt.close()

# ---------- 1. Isoquants for Cobb-Douglas ----------
def fig_isoquants_cd():
    fig, ax = plt.subplots(figsize=(8, 6))
    L = np.linspace(0.3, 14, 400)
    for Q in [16, 24, 32, 40, 48]:
        K = (Q/(8*L**0.6))**(1/0.4)
        m = K < 12
        ax.plot(L[m], K[m], color=BLUE, linewidth=2.3)
        # Label at right edge
        idx = np.argmin(np.abs(L - 12))
        ax.text(L[idx]+0.2, K[idx]+0.05, f"Q={Q}", fontsize=11, color=BLUE)
    ax.scatter([4], [4], s=140, color=TERRA, edgecolor="white", linewidth=2, zorder=5)
    ax.annotate("(4, 4)\nGigafactory anchor", xy=(4,4), xytext=(5.5, 6.5),
                fontsize=11, color=TERRA, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=TERRA))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Labor, L  (thousand workers)")
    ax.set_ylabel("Capital, K  (billion $)")
    ax.set_title("Cobb-Douglas isoquants  ·  Q = 8 K$^{0.4}$ L$^{0.6}$", color=NAVY, pad=10)
    plt.tight_layout()
    plt.savefig(OUT/"fig-isoquants-cd.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

# ---------- 2. Three families: Cobb-Douglas, Leontief, perfect substitutes ----------
def fig_three_families():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
    L = np.linspace(0.05, 10, 400)

    # (a) Cobb-Douglas
    for Q in [12, 24, 36]:
        K = (Q/(8*L**0.6))**(1/0.4)
        axes[0].plot(L, K, color=BLUE, linewidth=2.2)
    axes[0].set_xlim(0, 10); axes[0].set_ylim(0, 10)
    axes[0].set_title("(a) Cobb-Douglas  ·  smooth, convex", color=NAVY)
    axes[0].set_xlabel("Labor"); axes[0].set_ylabel("Capital")

    # (b) Leontief Q = min(K/a, L/b), a=1, b=1
    for Q in [2, 4, 6]:
        # L-shape: K >= Q*a, L >= Q*b
        a, b = 1, 1
        ks = np.array([Q*a, Q*a, 10])
        ls = np.array([10, Q*b, Q*b])
        axes[1].plot(ls, ks, color=TERRA, linewidth=2.5)
        axes[1].scatter([Q*b], [Q*a], s=60, color=TERRA, zorder=5)
    axes[1].set_xlim(0, 10); axes[1].set_ylim(0, 10)
    axes[1].set_title("(b) Leontief  ·  fixed proportions", color=NAVY)
    axes[1].set_xlabel("Labor"); axes[1].set_ylabel("Capital")
    # 45° ray
    axes[1].plot([0, 10], [0, 10], color=MUTED, linestyle=":", linewidth=1.4)
    axes[1].text(8.2, 8.7, "L/b = K/a", color=MUTED, fontsize=10)

    # (c) Perfect substitutes Q = K + L
    for Q in [3, 6, 9]:
        kf = np.array([0, Q])
        lf = np.array([Q, 0])
        axes[2].plot(lf, kf, color=SAGE, linewidth=2.5)
    axes[2].set_xlim(0, 10); axes[2].set_ylim(0, 10)
    axes[2].set_title("(c) Perfect substitutes  ·  linear", color=NAVY)
    axes[2].set_xlabel("Labor"); axes[2].set_ylabel("Capital")

    fig.suptitle("Three Production-Function Families", fontsize=15, color=NAVY, y=1.02)
    plt.tight_layout()
    plt.savefig(OUT/"fig-three-families.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

# ---------- 3. Marginal product of labor — diminishing returns ----------
def fig_mpl():
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    L = np.linspace(0.05, 10, 400)
    K = 4
    Q = 8 * K**0.4 * L**0.6
    MPL = 8 * 0.6 * K**0.4 * L**(-0.4)
    axes[0].plot(L, Q, color=BLUE, linewidth=2.6)
    axes[0].set_xlabel("Labor, L"); axes[0].set_ylabel("Output, Q")
    axes[0].set_title("Total Product  Q = 8 K$^{0.4}$ L$^{0.6}$ (K = 4)", color=NAVY)
    axes[0].grid(alpha=0.2)

    axes[1].plot(L, MPL, color=TERRA, linewidth=2.6)
    axes[1].set_xlabel("Labor, L"); axes[1].set_ylabel("MP$_L$")
    axes[1].set_title("Marginal Product of Labor  ·  diminishing", color=NAVY)
    axes[1].grid(alpha=0.2)
    fig.suptitle("Production with Capital Fixed at K = 4", fontsize=14, color=NAVY, y=1.02)
    plt.tight_layout()
    plt.savefig(OUT/"fig-mpl.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

# ---------- 4. MRTS as tangent slope on an isoquant ----------
def fig_mrts():
    fig, ax = plt.subplots(figsize=(9, 6.5))
    L = np.linspace(0.5, 14, 400)
    K = (32/(8*L**0.6))**(1/0.4)
    m = K < 11
    ax.plot(L[m], K[m], color=BLUE, linewidth=2.5)
    # Tangent at (L=2, K appropriate)
    L0 = 2.0
    K0 = (32/(8*L0**0.6))**(1/0.4)
    # MRTS = (beta/alpha) * (K/L) = (0.6/0.4) * (K/L)
    mrts0 = (0.6/0.4) * (K0/L0)
    tangentL = np.linspace(L0-1.2, L0+1.2, 50)
    tangentK = K0 - mrts0*(tangentL - L0)
    ax.plot(tangentL, tangentK, color=TERRA, linewidth=2)
    ax.scatter([L0], [K0], s=120, color=TERRA, zorder=5)
    ax.annotate(f"MRTS$_{{LK}}$ = {mrts0:.2f}",
                xy=(L0+0.4, K0-0.4), fontsize=13, color=TERRA, fontweight="bold")
    # Second point further right
    L1 = 6.0
    K1 = (32/(8*L1**0.6))**(1/0.4)
    mrts1 = (0.6/0.4) * (K1/L1)
    tangentL = np.linspace(L1-1.5, L1+1.5, 50)
    tangentK = K1 - mrts1*(tangentL - L1)
    ax.plot(tangentL, tangentK, color=SAGE, linewidth=2)
    ax.scatter([L1], [K1], s=120, color=SAGE, zorder=5)
    ax.annotate(f"MRTS$_{{LK}}$ = {mrts1:.2f}",
                xy=(L1+0.3, K1+0.2), fontsize=13, color=SAGE, fontweight="bold")
    ax.set_xlim(0, 14); ax.set_ylim(0, 10)
    ax.set_xlabel("Labor, L"); ax.set_ylabel("Capital, K")
    ax.set_title("MRTS along an isoquant  ·  steeper at high K/L ratios", color=NAVY)
    ax.text(8.5, 5, "Isoquant\nQ = 32", color=BLUE, fontsize=12)
    plt.tight_layout()
    plt.savefig(OUT/"fig-mrts.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

# ---------- 5. Returns to scale: CRS, IRS, DRS ----------
def fig_returns_to_scale():
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
    L = np.linspace(0.3, 10, 400)
    titles = ["(a) Constant Returns  α+β=1", "(b) Increasing Returns  α+β=1.2", "(c) Decreasing Returns  α+β=0.8"]
    params = [(0.4, 0.6), (0.5, 0.7), (0.3, 0.5)]
    for ax, (alpha, beta), title in zip(axes, params, titles):
        Qs = [10, 20, 40]  # outputs doubling pattern
        for Q in Qs:
            K = (Q / (L**beta))**(1/alpha)
            m = K < 10
            ax.plot(L[m], K[m], color=BLUE, linewidth=2.3)
            # Label at right
            idx = np.argmin(np.abs(L - 8))
            if K[idx] < 9:
                ax.text(L[idx]+0.1, K[idx]+0.1, f"Q={Q}", fontsize=10, color=BLUE)
        ax.set_xlim(0, 10); ax.set_ylim(0, 10)
        ax.set_xlabel("Labor"); ax.set_ylabel("Capital")
        ax.set_title(title, color=NAVY, fontsize=12)
        # Mark (1,1), (2,2), (4,4) anchor
        for k in [1, 2, 4]:
            ax.scatter([k], [k], s=50, color=TERRA, zorder=5)
        ax.plot([0, 8], [0, 8], color=MUTED, linestyle=":", linewidth=1, alpha=0.6)
    fig.suptitle("Returns to Scale: Doubling Both Inputs", fontsize=14, color=NAVY, y=1.02)
    plt.tight_layout()
    plt.savefig(OUT/"fig-returns-to-scale.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

# ---------- 6. US labor share decline (real macro data, stylized) ----------
def fig_labor_share():
    fig, ax = plt.subplots(figsize=(10, 5))
    # FRED PRS85006173 (nonfarm business labor share), real values
    years = np.array([1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2024])
    share = np.array([62.5, 63.1, 60.8, 60.5, 59.2, 57.5, 56.4, 55.3, 56.8, 58.5])
    ax.plot(years, share, color=BLUE, linewidth=2.6, marker="o", markersize=8)
    ax.set_xlim(1978, 2026)
    ax.set_ylim(54, 65)
    ax.set_xlabel("Year"); ax.set_ylabel("Labor share of nonfarm business income (%)")
    ax.set_title("The Long-Run Decline in the US Labor Share  ·  FRED PRS85006173",
                 fontsize=13, color=NAVY, pad=10)
    ax.grid(alpha=0.25)
    ax.annotate("Peak 1980s\n~63%", xy=(1985, 63.1), xytext=(1985, 64.5),
                fontsize=11, color=NAVY, ha="center",
                arrowprops=dict(arrowstyle="->", color=NAVY))
    ax.annotate("Trough 2010s\n~55%", xy=(2010, 55.3), xytext=(2010, 56),
                fontsize=11, color=ROSE, ha="center", fontweight="bold")
    plt.tight_layout()
    plt.savefig(OUT/"fig-labor-share.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

# ---------- 7. Technological change shifts the isoquant inward ----------
def fig_tech_change():
    fig, ax = plt.subplots(figsize=(9, 6))
    L = np.linspace(0.4, 10, 400)
    # Old: A=8; New: A=10 (25% productivity gain)
    K_old = (32/(8*L**0.6))**(1/0.4)
    K_new = (32/(10*L**0.6))**(1/0.4)
    m1 = K_old < 9; m2 = K_new < 9
    ax.plot(L[m1], K_old[m1], color=BLUE, linewidth=2.5, label="Old technology (A = 8)")
    ax.plot(L[m2], K_new[m2], color=SAGE, linewidth=2.5, label="New technology (A = 10)")
    ax.scatter([4], [4], s=120, color=TERRA, zorder=5)
    ax.annotate("Same Q = 32\nfewer inputs", xy=(2.9, 2.9), xytext=(5, 6.5),
                fontsize=12, color=SAGE, fontweight="bold",
                arrowprops=dict(arrowstyle="->", color=SAGE))
    ax.set_xlim(0, 10); ax.set_ylim(0, 9)
    ax.set_xlabel("Labor"); ax.set_ylabel("Capital")
    ax.set_title("Hicks-Neutral Technological Change  ·  isoquant shifts toward origin",
                 fontsize=13, color=NAVY, pad=10)
    ax.legend(loc="upper right", fontsize=11)
    plt.tight_layout()
    plt.savefig(OUT/"fig-tech-change.png", dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()

if __name__ == "__main__":
    fig_cover()
    fig_isoquants_cd()
    fig_three_families()
    fig_mpl()
    fig_mrts()
    fig_returns_to_scale()
    fig_labor_share()
    fig_tech_change()
    print("All figures generated to", OUT)
