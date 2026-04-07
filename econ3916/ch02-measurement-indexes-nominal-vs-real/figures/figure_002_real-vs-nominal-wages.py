"""Figure 2: Nominal vs. Real Wages 1964-2024 — the fifty-year divergence."""
import matplotlib.pyplot as plt
import numpy as np

# Average Hourly Earnings (production & nonsupervisory) — selected years
# Source: FRED series AHETPI
years = [1964, 1968, 1973, 1978, 1983, 1988, 1993, 1998, 2003, 2008,
         2013, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
nominal = [2.50, 2.85, 3.94, 5.69, 8.02, 9.28, 10.83, 12.77, 15.35, 18.08,
           20.13, 22.73, 23.51, 24.73, 26.00, 27.49, 29.00, 30.30]
# CPI values for those years (annual average, CPIAUCSL)
cpi_vals = [31.0, 34.8, 44.4, 65.2, 99.6, 118.3, 144.5, 163.0, 184.0, 215.3,
            233.0, 251.1, 255.7, 258.8, 271.0, 292.7, 304.7, 314.2]

# Deflate to 2020 dollars
base_cpi_2020 = 258.8
real = [(n / c) * base_cpi_2020 for n, c in zip(nominal, cpi_vals)]

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.plot(years, nominal, label="Nominal wage", color="#2196F3", linewidth=2.5, marker='o', markersize=3)
ax.plot(years, real, label="Real wage (2020 $)", color="#FF9800", linewidth=2.5, marker='s', markersize=3)

# Annotate the 1973 peak
peak_idx = years.index(1973)
ax.annotate("1973 peak\n(real)", xy=(1973, real[peak_idx]),
            xytext=(1980, real[peak_idx] + 3),
            fontsize=7, color="#E65100",
            arrowprops=dict(arrowstyle="->", color="#E65100", lw=0.8))

# Annotate divergence
ax.annotate("Money\nillusion\ngap", xy=(2010, 20), xytext=(2005, 13),
            fontsize=7, color="#757575",
            arrowprops=dict(arrowstyle="->", color="#757575", lw=0.8))

ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("Average hourly earnings ($)", fontsize=10)
ax.legend(frameon=False, fontsize=9, loc="upper left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(1962, 2026)
plt.tight_layout()
plt.savefig("figures/figure_002_real-vs-nominal-wages.png", dpi=150, bbox_inches="tight")
print("OK: figure_002_real-vs-nominal-wages.png")
