"""Generate decision framework visual — which tool for which context."""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.axis('off')

# Table data
col_labels = ['Context', 'Location', 'Spread', 'Outlier\nDetection']
row_data = [
    ['Symmetric\n(rare in econ)', 'Mean', 'Std Dev', 'Z-score'],
    ['Right-skewed\n(income, housing)', 'Median /\nTrimmed Mean', 'IQR / MAD', 'Tukey\nFences'],
    ['High-dim,\nheavy-tailed', 'Trimmed\nMean', 'MAD', 'Isolation\nForest'],
    ['Growth rates\n/ returns', 'Geometric\nMean', '—', '—'],
]

table = ax.table(cellText=row_data, colLabels=col_labels,
                 loc='center', cellLoc='center')

# Style
table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 1.8)

# Header style
for j in range(4):
    cell = table[0, j]
    cell.set_facecolor('#2c3e50')
    cell.set_text_props(color='white', fontweight='bold', fontsize=10)

# Row colors (alternating)
colors = ['#ecf0f1', '#ffffff', '#ecf0f1', '#ffffff']
for i in range(4):
    for j in range(4):
        cell = table[i+1, j]
        cell.set_facecolor(colors[i])
        cell.set_edgecolor('#bdc3c7')

# Highlight the "most common in econ" row
for j in range(4):
    cell = table[2, j]
    cell.set_facecolor('#e8f8f5')
    cell.set_edgecolor('#1abc9c')

plt.tight_layout()
plt.savefig('figures/figure_005_decision-framework.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_005_decision-framework.png")
