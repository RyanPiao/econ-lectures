"""Four Visualizations of Real Wages: Same Data, Different Arguments.

Uses static data (approximate FRED AHETPI deflated to 2020 dollars)
to avoid API dependency in the slide build pipeline.
"""
import numpy as np
import matplotlib.pyplot as plt

# Approximate real hourly earnings (2020$), annual averages 1964-2024
years = np.arange(1964, 2025)
# Stylized trajectory: rise to 1973, stagnation to 2015, rise to 2020, dip, recovery
real_wages = np.array([
    22.3, 22.7, 23.1, 23.0, 23.5, 23.8, 23.5, 23.7, 24.1, 24.1,  # 1964-73
    23.5, 23.0, 23.2, 23.5, 23.3, 22.8, 22.5, 22.6, 22.4, 22.5,  # 1974-83
    22.3, 22.2, 22.5, 22.4, 22.5, 22.3, 22.1, 22.0, 22.2, 22.4,  # 1984-93
    22.3, 22.5, 22.6, 22.9, 23.3, 23.7, 24.0, 23.8, 23.9, 24.0,  # 1994-03
    23.8, 23.9, 24.0, 24.1, 23.9, 24.3, 24.5, 24.4, 24.3, 24.5,  # 2004-13
    24.7, 25.0, 25.3, 25.5, 25.8, 26.3, 27.0, 27.5, 27.8, 28.2,  # 2014-23
    28.6                                                            # 2024
])

fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# Panel A: Honest (full range, y starts at 0)
axes[0, 0].plot(years, real_wages, color="#2196F3", linewidth=2.5)
axes[0, 0].set_ylim(0, 35)
axes[0, 0].set_title("A: Full Range (Honest)", fontweight="bold", fontsize=12,
                     color="#2196F3")
axes[0, 0].set_ylabel("Real Wage (2020 $)")
axes[0, 0].spines["top"].set_visible(False)
axes[0, 0].spines["right"].set_visible(False)

# Panel B: Truncated y-axis (starts at $20)
axes[0, 1].plot(years, real_wages, color="#E53935", linewidth=2.5)
axes[0, 1].set_ylim(20, 30)
axes[0, 1].set_title("B: Truncated Y-Axis\n(Exaggerates Variation)",
                     fontweight="bold", fontsize=12, color="#E53935")
axes[0, 1].set_ylabel("Real Wage (2020 $)")
axes[0, 1].spines["top"].set_visible(False)
axes[0, 1].spines["right"].set_visible(False)

# Panel C: Cherry-picked window (2015-2024)
mask = years >= 2015
axes[1, 0].plot(years[mask], real_wages[mask], color="#FF9800", linewidth=2.5)
axes[1, 0].set_ylim(0, 35)
axes[1, 0].set_title("C: Cherry-Picked Window\n(Hides 50-Year Stagnation)",
                     fontweight="bold", fontsize=12, color="#FF9800")
axes[1, 0].set_ylabel("Real Wage (2020 $)")
axes[1, 0].spines["top"].set_visible(False)
axes[1, 0].spines["right"].set_visible(False)

# Panel D: Log scale
axes[1, 1].plot(years, real_wages, color="#4CAF50", linewidth=2.5)
axes[1, 1].set_yscale("log")
axes[1, 1].set_ylim(10, 40)
axes[1, 1].set_title("D: Log Scale\n(Smooths Structural Breaks)",
                     fontweight="bold", fontsize=12, color="#4CAF50")
axes[1, 1].set_ylabel("Real Wage (2020 $, log)")
axes[1, 1].spines["top"].set_visible(False)
axes[1, 1].spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("figures/figure_004_wage_redesigns.png", dpi=150,
            bbox_inches="tight", facecolor="white")
plt.close()
print("OK: figure_004_wage_redesigns.png")
