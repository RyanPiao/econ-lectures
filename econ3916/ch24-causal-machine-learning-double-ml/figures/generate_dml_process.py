"""Generate DML 3-step process flow diagram."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 4)
ax.axis('off')

# Colors
blue = '#2980B9'
red = '#E74C3C'
green = '#27AE60'
gray = '#7F8C8D'

# Step boxes
box_style = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=gray, linewidth=2)

# Step 1
ax.text(1.5, 3, 'Step 1', fontsize=14, fontweight='bold', ha='center', va='center',
        color=blue)
ax.text(1.5, 2.2, 'Predict Y from X\n(ML model $\\hat{g}$)', fontsize=11, ha='center',
        va='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#EBF5FB', edgecolor=blue, linewidth=2))
ax.text(1.5, 1.0, '$\\tilde{Y} = Y - \\hat{g}(X)$', fontsize=12, ha='center', va='center',
        color=blue, fontweight='bold')

# Arrow 1→2
ax.annotate('', xy=(3.5, 2.2), xytext=(2.8, 2.2),
            arrowprops=dict(arrowstyle='->', color=gray, lw=2))

# Step 2
ax.text(5, 3, 'Step 2', fontsize=14, fontweight='bold', ha='center', va='center',
        color=red)
ax.text(5, 2.2, 'Predict D from X\n(ML model $\\hat{m}$)', fontsize=11, ha='center',
        va='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#FDEDEC', edgecolor=red, linewidth=2))
ax.text(5, 1.0, '$\\tilde{D} = D - \\hat{m}(X)$', fontsize=12, ha='center', va='center',
        color=red, fontweight='bold')

# Arrow 2→3
ax.annotate('', xy=(7, 2.2), xytext=(6.3, 2.2),
            arrowprops=dict(arrowstyle='->', color=gray, lw=2))

# Step 3
ax.text(8.5, 3, 'Step 3', fontsize=14, fontweight='bold', ha='center', va='center',
        color=green)
ax.text(8.5, 2.2, 'Regress residuals\n(OLS: $\\tilde{Y}$ on $\\tilde{D}$)', fontsize=11, ha='center',
        va='center', bbox=dict(boxstyle='round,pad=0.4', facecolor='#EAFAF1', edgecolor=green, linewidth=2))
ax.text(8.5, 1.0, '$\\hat{\\theta}_{DML}$', fontsize=14, ha='center', va='center',
        color=green, fontweight='bold')

# Bottom label
ax.text(5, 0.2, 'Cross-fitting: train on folds $\\neq k$, predict on fold $k$, stack all residuals',
        fontsize=10, ha='center', va='center', color=gray, style='italic')

plt.tight_layout()
plt.savefig('figures/ch24-dml-process-flow.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print('OK: ch24-dml-process-flow.png')
