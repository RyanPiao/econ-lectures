"""Missing Data Heatmap — country x date presence/absence, highlighting Russia gap.
Slide-friendly: 6x4.5 (AR 1.33), 150 dpi, no baked-in title."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
matplotlib.use("Agg")
from pathlib import Path

url = "https://raw.githubusercontent.com/TheEconomist/big-mac-data/master/output-data/big-mac-raw-index.csv"
df = pd.read_csv(url, parse_dates=["date"])

# Select interesting countries (mix of complete + incomplete)
highlight = ["Switzerland", "United States", "Japan", "Brazil", "Russia",
             "Argentina", "China", "Britain", "India", "South Korea",
             "Turkey", "Egypt", "Venezuela", "Ukraine", "South Africa"]
df_sub = df.loc[df["name"].isin(highlight)]

# Create presence matrix
pivot = df_sub.pivot_table(index="name", columns="date", values="dollar_price", aggfunc="first")
presence = (~pivot.isnull()).astype(int)

# Sort by completeness (most complete at top)
presence = presence.loc[presence.sum(axis=1).sort_values(ascending=False).index]

fig, ax = plt.subplots(figsize=(6, 4.5))
cmap = matplotlib.colors.ListedColormap(["#ef5350", "#66bb6a"])
ax.imshow(presence.values, aspect="auto", cmap=cmap, interpolation="nearest")

# Y-axis: country names
ax.set_yticks(range(len(presence)))
ax.set_yticklabels(presence.index, fontsize=7)

# X-axis: selected years
dates = presence.columns
year_ticks = [i for i, d in enumerate(dates) if d.month == 1 and d.year % 5 == 0]
ax.set_xticks(year_ticks)
ax.set_xticklabels([dates[i].year for i in year_ticks], fontsize=8, rotation=45)

# Highlight Russia row
russia_idx = list(presence.index).index("Russia") if "Russia" in presence.index else None
if russia_idx is not None:
    ax.axhline(russia_idx - 0.5, color="white", linewidth=1.5)
    ax.axhline(russia_idx + 0.5, color="white", linewidth=1.5)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor="#66bb6a", label="Data present"),
                   Patch(facecolor="#ef5350", label="Data missing")]
ax.legend(handles=legend_elements, loc="lower right", fontsize=7, framealpha=0.9)

plt.tight_layout()
out = Path(__file__).parent / "figure_002_missing_data_heatmap.png"
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
plt.close()
print(f"OK: {out}")
