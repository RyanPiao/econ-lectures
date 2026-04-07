"""Figure 1: CPI Level 1947-2024 — upward curve with base period reference line."""
import matplotlib.pyplot as plt
import numpy as np

# CPI-U data points (annual averages, selected years from FRED CPIAUCSL)
years = [1947, 1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990,
         1995, 2000, 2005, 2010, 2015, 2020, 2021, 2022, 2023, 2024]
cpi = [22.3, 24.1, 26.8, 29.6, 31.5, 38.8, 53.8, 82.4, 107.6, 130.7,
       152.4, 172.2, 195.3, 218.1, 237.0, 258.8, 271.0, 292.7, 304.7, 314.2]

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.plot(years, cpi, color="#1565C0", linewidth=2.5, marker='o', markersize=3)
ax.axhline(y=100, color="gray", linestyle="--", alpha=0.5, linewidth=1)
ax.text(1950, 105, "Base period (1982-84 = 100)", fontsize=8, color="gray", alpha=0.7)

# Annotate key points
ax.annotate("9.1% peak\n(Jun 2022)", xy=(2022, 292.7), xytext=(2012, 290),
            fontsize=7, color="#D32F2F", arrowprops=dict(arrowstyle="->", color="#D32F2F", lw=0.8))
ax.annotate("Vibecession\nzone", xy=(2023, 304.7), xytext=(2016, 330),
            fontsize=7, color="#FF9800", arrowprops=dict(arrowstyle="->", color="#FF9800", lw=0.8))

ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("CPI (1982-84 = 100)", fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(1945, 2026)
ax.set_ylim(0, 350)
plt.tight_layout()
plt.savefig("figures/figure_001_cpi-level.png", dpi=150, bbox_inches="tight")
print("OK: figure_001_cpi-level.png")
