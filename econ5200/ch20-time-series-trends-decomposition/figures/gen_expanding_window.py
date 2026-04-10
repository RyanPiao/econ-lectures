"""Generate expanding window cross-validation diagram for slides."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(6, 4.5))

n_folds = 5
total_periods = 30
colors_train = '#3498db'
colors_test = '#e74c3c'
colors_unused = '#ecf0f1'

ax.set_xlim(-1, total_periods + 1)
ax.set_ylim(-0.5, n_folds + 1.5)
ax.set_xlabel('Time Period', fontsize=10)
ax.set_title('Expanding Window Cross-Validation', fontsize=13, fontweight='bold', pad=15)

# Draw timeline arrow
ax.annotate('', xy=(total_periods + 0.5, -0.2), xytext=(-0.5, -0.2),
            arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=1.5))

for fold in range(n_folds):
    y = n_folds - fold
    # Train/test split: expanding train, fixed-size test
    train_end = 10 + fold * 4
    test_end = train_end + 4

    # Unused
    for t in range(total_periods):
        if t >= test_end:
            rect = mpatches.Rectangle((t, y - 0.35), 0.9, 0.7,
                                       facecolor=colors_unused, edgecolor='#bdc3c7', linewidth=0.5)
            ax.add_patch(rect)

    # Train
    for t in range(train_end):
        rect = mpatches.Rectangle((t, y - 0.35), 0.9, 0.7,
                                   facecolor=colors_train, alpha=0.7, edgecolor='white', linewidth=0.5)
        ax.add_patch(rect)

    # Test
    for t in range(train_end, min(test_end, total_periods)):
        rect = mpatches.Rectangle((t, y - 0.35), 0.9, 0.7,
                                   facecolor=colors_test, alpha=0.7, edgecolor='white', linewidth=0.5)
        ax.add_patch(rect)

    ax.text(-0.8, y, f'Fold {fold + 1}', ha='right', va='center', fontsize=9, fontweight='bold')

# Legend
train_patch = mpatches.Patch(color=colors_train, alpha=0.7, label='Training')
test_patch = mpatches.Patch(color=colors_test, alpha=0.7, label='Test')
unused_patch = mpatches.Patch(color=colors_unused, edgecolor='#bdc3c7', label='Unused')
ax.legend(handles=[train_patch, test_patch, unused_patch], loc='upper right', fontsize=9)

ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/ch20-expanding-window-cv.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print('OK: ch20-expanding-window-cv.png')
