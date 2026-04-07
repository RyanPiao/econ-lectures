"""Figure 3: Big Mac Nominal vs. Real Prices 2000-2024."""
import matplotlib.pyplot as plt

# US Big Mac prices (selected years from The Economist Big Mac Index)
years = [2000, 2003, 2005, 2007, 2010, 2012, 2015, 2017, 2020, 2022, 2024]
nominal_price = [2.51, 2.71, 3.06, 3.41, 3.73, 4.33, 4.79, 5.30, 5.71, 5.15, 5.69]
# Corresponding CPI values (annual average, CPIAUCSL)
cpi_vals = [172.2, 184.0, 195.3, 207.3, 218.1, 229.6, 237.0, 245.1, 258.8, 292.7, 314.2]

# Deflate to 2020 dollars
base_cpi_2020 = 258.8
real_price = [(p / c) * base_cpi_2020 for p, c in zip(nominal_price, cpi_vals)]

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.plot(years, nominal_price, marker="o", markersize=5, label="Nominal Big Mac price",
        color="#2196F3", linewidth=2.5)
ax.plot(years, real_price, marker="s", markersize=5, label="Real Big Mac price (2020 $)",
        color="#FF9800", linewidth=2.5)

# Shade the gap
ax.fill_between(years, nominal_price, real_price, alpha=0.08, color="#9E9E9E")
ax.text(2011, 4.0, "≈75% of increase\nis inflation", fontsize=7, color="#616161",
        ha="center", style="italic")

ax.set_xlabel("Year", fontsize=10)
ax.set_ylabel("US Big Mac price ($)", fontsize=10)
ax.legend(frameon=False, fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(1999, 2025)
ax.set_ylim(0, 7)
plt.tight_layout()
plt.savefig("figures/figure_003_bigmac-real-nominal.png", dpi=150, bbox_inches="tight")
print("OK: figure_003_bigmac-real-nominal.png")
