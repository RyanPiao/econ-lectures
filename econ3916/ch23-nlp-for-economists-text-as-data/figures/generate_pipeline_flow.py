"""Generate text preprocessing pipeline flow diagram for Ch23 lecture slides."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')

# Colors
box_color = '#6B8BA4'  # dusty blue (White Academia theme)
arrow_color = '#2c3e50'
accent_color = '#C47B5A'  # terracotta

# Box positions (x_center, y_center)
boxes = [
    (1.0, 2.0, 'Raw Text\n"The Fed raised\nthe federal\nfunds rate..."'),
    (3.2, 2.0, 'Tokenize\n["The", "Fed",\n"raised", "the",\n"federal", ...]'),
    (5.4, 2.0, 'Remove\nStop Words\n["Fed", "raised",\n"federal", "funds",\n"rate"]'),
    (7.6, 2.0, 'TF-IDF\nWeighting'),
    (9.2, 2.0, 'Document-\nTerm\nMatrix X'),
]

box_w, box_h = 1.8, 2.4

for i, (x, y, label) in enumerate(boxes):
    color = accent_color if i == 3 else box_color  # highlight TF-IDF
    rect = mpatches.FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.1",
        facecolor=color, edgecolor=arrow_color, linewidth=1.5, alpha=0.15
    )
    ax.add_patch(rect)
    rect_border = mpatches.FancyBboxPatch(
        (x - box_w/2, y - box_h/2), box_w, box_h,
        boxstyle="round,pad=0.1",
        facecolor='none', edgecolor=color, linewidth=2
    )
    ax.add_patch(rect_border)
    ax.text(x, y, label, ha='center', va='center', fontsize=8,
            fontweight='bold' if i == 3 else 'normal',
            color=arrow_color, family='sans-serif')

# Arrows between boxes
for i in range(len(boxes) - 1):
    x1 = boxes[i][0] + box_w/2 + 0.02
    x2 = boxes[i+1][0] - box_w/2 - 0.02
    ax.annotate('', xy=(x2, 2.0), xytext=(x1, 2.0),
                arrowprops=dict(arrowstyle='->', color=arrow_color,
                                lw=2, connectionstyle='arc3,rad=0'))

# Stage labels below
stage_labels = ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Output']
for i, (x, y, _) in enumerate(boxes):
    ax.text(x, y - box_h/2 - 0.15, stage_labels[i],
            ha='center', va='top', fontsize=7, color='#7f8c8d',
            style='italic')

plt.tight_layout()
output_path = Path(__file__).parent / 'ch23-preprocessing-pipeline.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
print(f'Saved: {output_path}')
plt.close()
