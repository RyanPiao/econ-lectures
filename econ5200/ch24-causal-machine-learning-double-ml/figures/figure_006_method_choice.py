"""Figure 6: Causal method choice decision tree."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.set_xlim(0, 10)
ax.set_ylim(0, 8)
ax.axis('off')

# Styles
box_style = dict(boxstyle='round,pad=0.4', facecolor='#ecf0f1', edgecolor='#2c3e50', linewidth=1.5)
decision_style = dict(boxstyle='round,pad=0.3', facecolor='#f9e79f', edgecolor='#f39c12', linewidth=1.5)
answer_style_green = dict(boxstyle='round,pad=0.3', facecolor='#d5f5e3', edgecolor='#27ae60', linewidth=1.5)
answer_style_blue = dict(boxstyle='round,pad=0.3', facecolor='#d6eaf8', edgecolor='#2980b9', linewidth=1.5)
answer_style_purple = dict(boxstyle='round,pad=0.3', facecolor='#e8daef', edgecolor='#8e44ad', linewidth=1.5)
answer_style_orange = dict(boxstyle='round,pad=0.3', facecolor='#fdebd0', edgecolor='#e67e22', linewidth=1.5)

# Decision nodes
ax.text(5, 7.2, 'Can you\nrandomize?', ha='center', va='center', fontsize=10, fontweight='bold', bbox=decision_style)
ax.text(2, 5.2, 'Low-dim\nconfounders?', ha='center', va='center', fontsize=9, fontweight='bold', bbox=decision_style)
ax.text(7.5, 5.2, 'A/B Test\n(Ch 9)', ha='center', va='center', fontsize=10, fontweight='bold', bbox=answer_style_green)
ax.text(0.8, 3.2, 'OLS\n(Ch 13)', ha='center', va='center', fontsize=9, fontweight='bold', bbox=answer_style_blue)
ax.text(3.5, 3.2, 'Instrument\navailable?', ha='center', va='center', fontsize=9, fontweight='bold', bbox=decision_style)
ax.text(2.0, 1.2, 'IV / 2SLS', ha='center', va='center', fontsize=9, fontweight='bold', bbox=answer_style_purple)
ax.text(5.5, 1.2, 'DML\n(Ch 24)', ha='center', va='center', fontsize=11, fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.4', facecolor='#fadbd8', edgecolor='#e74c3c', linewidth=2.5))

# Arrows with labels
def arrow(x1, y1, x2, y2, label, label_side='left'):
    ax.annotate('', xy=(x2, y2+0.4), xytext=(x1, y1-0.4),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=1.5))
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2
    offset = -0.35 if label_side == 'left' else 0.35
    ax.text(mid_x + offset, mid_y, label, fontsize=8, color='#7f8c8d', ha='center',
            fontstyle='italic')

arrow(5, 7.2, 2, 5.2, 'No', 'left')
arrow(5, 7.2, 7.5, 5.2, 'Yes', 'right')
arrow(2, 5.2, 0.8, 3.2, 'Yes', 'left')
arrow(2, 5.2, 3.5, 3.2, 'No (high-dim)', 'right')
arrow(3.5, 3.2, 2.0, 1.2, 'Yes', 'left')
arrow(3.5, 3.2, 5.5, 1.2, 'No', 'right')

plt.tight_layout()
plt.savefig('figures/figure_006_method_choice.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('OK: figure_006_method_choice.png')
