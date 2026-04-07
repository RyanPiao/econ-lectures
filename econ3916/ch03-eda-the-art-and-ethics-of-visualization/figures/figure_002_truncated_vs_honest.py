"""Truncated vs Honest Bar Chart: Quarterly Revenue."""
import matplotlib.pyplot as plt
import numpy as np

quarters = ["Q1", "Q2", "Q3", "Q4"]
revenue = [98, 99, 100, 102]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# LEFT: Truncated (dishonest)
bars_l = axes[0].bar(quarters, revenue, color="#E53935", width=0.6,
                     edgecolor="white", linewidth=1.5)
axes[0].set_ylim(96, 104)
axes[0].set_title("Truncated Y-Axis\n(Lie Factor ≈ 49)", fontweight="bold",
                  fontsize=12, color="#E53935")
axes[0].set_ylabel("Revenue ($M)")
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)
for bar, val in zip(bars_l, revenue):
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                 f"${val}M", ha="center", fontsize=10, fontweight="bold")

# RIGHT: Full range (honest)
bars_r = axes[1].bar(quarters, revenue, color="#2196F3", width=0.6,
                     edgecolor="white", linewidth=1.5)
axes[1].set_ylim(0, 120)
axes[1].set_title("Full Y-Axis\n(Lie Factor ≈ 1.0)", fontweight="bold",
                  fontsize=12, color="#2196F3")
axes[1].set_ylabel("Revenue ($M)")
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)
for bar, val in zip(bars_r, revenue):
    axes[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                 f"${val}M", ha="center", fontsize=10, fontweight="bold")

plt.tight_layout()
plt.savefig("figures/figure_002_truncated_vs_honest.png", dpi=150,
            bbox_inches="tight", facecolor="white")
plt.close()
print("OK: figure_002_truncated_vs_honest.png")
