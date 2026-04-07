"""Data Structures Taxonomy — Photo/Movie/Surveillance Grid visual with notation.
Slide-friendly: 6x4.5 (AR 1.33), 150 dpi, no baked-in title."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib
matplotlib.use("Agg")
from pathlib import Path

fig, axes = plt.subplots(1, 3, figsize=(6, 4.5))

# Colors
blue = "#1976d2"
orange = "#f57c00"
green = "#388e3c"
light_gray = "#f5f5f5"

# --- Panel 1: Cross-sectional (Photo) ---
ax = axes[0]
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")

# Draw a camera/photo icon metaphor: grid of dots (units) at one time
for i, y in enumerate([0.75, 0.60, 0.45, 0.30]):
    ax.add_patch(mpatches.FancyBboxPatch((0.25, y - 0.04), 0.5, 0.08,
                 boxstyle="round,pad=0.02", facecolor=blue, alpha=0.15 + 0.2 * (i == 0),
                 edgecolor=blue, linewidth=1))
    ax.text(0.5, y, f"Unit {i+1}", ha="center", va="center", fontsize=7, color=blue)

ax.text(0.5, 0.95, "Cross-Sectional", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(0.5, 0.12, r"$y_i$", ha="center", va="center", fontsize=14, color=blue, fontstyle="italic")
ax.text(0.5, 0.03, "Many units, one time", ha="center", va="center", fontsize=6, color="gray")

# --- Panel 2: Time Series (Movie) ---
ax = axes[1]
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")

# Draw timeline: one unit across periods
for i, x in enumerate([0.15, 0.35, 0.55, 0.75]):
    ax.add_patch(mpatches.FancyBboxPatch((x - 0.07, 0.45), 0.14, 0.14,
                 boxstyle="round,pad=0.02", facecolor=orange, alpha=0.15 + 0.2 * (i == 3),
                 edgecolor=orange, linewidth=1))
    ax.text(x, 0.52, f"t={i+1}", ha="center", va="center", fontsize=7, color=orange)

# Arrow connecting
ax.annotate("", xy=(0.82, 0.52), xytext=(0.12, 0.52),
            arrowprops=dict(arrowstyle="->", color=orange, lw=1.5, connectionstyle="arc3,rad=0"))

ax.text(0.5, 0.95, "Time Series", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(0.5, 0.28, r"$y_t$", ha="center", va="center", fontsize=14, color=orange, fontstyle="italic")
ax.text(0.5, 0.19, "One unit, many periods", ha="center", va="center", fontsize=6, color="gray")

# --- Panel 3: Panel (Surveillance Grid) ---
ax = axes[2]
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect("equal")
ax.axis("off")

# Draw grid
for i, y in enumerate([0.72, 0.56, 0.40]):
    for j, x in enumerate([0.2, 0.4, 0.6, 0.8]):
        alpha = 0.2 + 0.15 * (i + j)
        ax.add_patch(mpatches.FancyBboxPatch((x - 0.07, y - 0.05), 0.14, 0.1,
                     boxstyle="round,pad=0.01", facecolor=green, alpha=min(alpha, 0.8),
                     edgecolor=green, linewidth=0.8))

# Labels
for j, x in enumerate([0.2, 0.4, 0.6, 0.8]):
    ax.text(x, 0.84, f"t={j+1}", ha="center", va="center", fontsize=6, color="gray")
for i, y in enumerate([0.72, 0.56, 0.40]):
    ax.text(0.07, y, f"i={i+1}", ha="center", va="center", fontsize=6, color="gray")

ax.text(0.5, 0.95, "Panel", ha="center", va="center", fontsize=9, fontweight="bold")
ax.text(0.5, 0.23, r"$y_{it}$", ha="center", va="center", fontsize=14, color=green, fontstyle="italic")
ax.text(0.5, 0.14, "Same units, many periods", ha="center", va="center", fontsize=6, color="gray")

plt.tight_layout(w_pad=0.5)
out = Path(__file__).parent / "figure_003_data_structures_taxonomy.png"
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"OK: {out}")
