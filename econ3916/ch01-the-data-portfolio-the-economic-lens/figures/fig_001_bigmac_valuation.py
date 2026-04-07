"""Big Mac Valuation Bar Chart — top 5 overvalued + top 5 undervalued currencies.
Slide-friendly: 6x4.5 (AR 1.33), 150 dpi, no baked-in title."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
from pathlib import Path

# Load data
url = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/output-data/big-mac-raw-index.csv"
df = pd.read_csv(url, parse_dates=["date"])
latest = df.loc[df["date"] == df["date"].max()].copy()
us_price = latest.loc[latest["iso_a3"] == "USA", "dollar_price"].values[0]
latest["valuation_pct"] = (
    (latest["local_price"] / us_price - latest["dollar_ex"])
    / latest["dollar_ex"] * 100
)

# Top 5 overvalued + top 5 undervalued
top5 = latest.nlargest(5, "valuation_pct")[["name", "valuation_pct"]]
bot5 = latest.nsmallest(5, "valuation_pct")[["name", "valuation_pct"]]
plot_df = pd.concat([top5, bot5]).sort_values("valuation_pct")

fig, ax = plt.subplots(figsize=(6, 4.5))
colors = ["#d32f2f" if v < 0 else "#1976d2" for v in plot_df["valuation_pct"]]
ax.barh(plot_df["name"], plot_df["valuation_pct"], color=colors, edgecolor="none", height=0.6)
ax.axvline(0, color="black", linewidth=0.8)
ax.set_xlabel("Currency Valuation vs USD (%)", fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.tick_params(labelsize=9)

# Add value labels
for i, (name, val) in enumerate(zip(plot_df["name"], plot_df["valuation_pct"])):
    offset = 2 if val >= 0 else -2
    ha = "left" if val >= 0 else "right"
    ax.text(val + offset, i, f"{val:+.0f}%", va="center", ha=ha, fontsize=8, fontweight="bold")

plt.tight_layout()
out = Path(__file__).parent / "figure_001_bigmac_valuation.png"
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"OK: {out}")
