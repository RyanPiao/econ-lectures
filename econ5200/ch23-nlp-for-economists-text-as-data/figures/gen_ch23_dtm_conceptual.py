"""Generate a conceptual document-term matrix diagram for Ch 23 lecture slides."""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.family'] = 'sans-serif'

fig, ax = plt.subplots(figsize=(6, 4.5))

# Data for a small DTM example
words = ['inflation', 'rate', 'committee', 'labor', 'tapering', 'growth']
docs = ['Jan 2023\nFOMC', 'Mar 2023\nFOMC', 'Sep 2013\nFOMC']
data = np.array([
    [15, 8, 50, 3, 0, 5],
    [12, 10, 48, 6, 0, 8],
    [4, 5, 52, 2, 18, 3],
])

# Create table
colors = plt.cm.YlOrRd(data / data.max() * 0.7 + 0.1)
table = ax.table(
    cellText=data,
    rowLabels=docs,
    colLabels=words,
    cellColours=colors,
    loc='center',
    cellLoc='center'
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.8)

# Style header cells
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(fontweight='bold', fontsize=9)
        cell.set_facecolor('#E8E8E8')
    if col == -1:
        cell.set_text_props(fontweight='bold', fontsize=8)
        cell.set_facecolor('#E8E8E8')
        cell.set_width(0.18)

ax.axis('off')

# Annotations
ax.annotate('n = documents\n(FOMC meetings)', xy=(0.01, 0.5), fontsize=8,
            ha='center', va='center', color='#555',
            rotation=90, transform=ax.transAxes)
ax.annotate('p = vocabulary (features)', xy=(0.55, 0.97), fontsize=8,
            ha='center', va='center', color='#555',
            transform=ax.transAxes)
ax.annotate('"tapering" only in 2013\n→ high TF-IDF for that meeting',
            xy=(0.78, 0.08), fontsize=7, ha='center', color='#B33',
            style='italic', transform=ax.transAxes)

plt.tight_layout()
plt.savefig('figures/ch23-dtm-conceptual.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('OK: ch23-dtm-conceptual.png')
