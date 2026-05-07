"""Figure 4: DML vs Naive LASSO — Side-by-side ATE comparison."""
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(6, 4.5))

methods = ['True ATE', 'DML\n(cross-fitting)', 'Naive LASSO', 'Naive OLS\n(no controls)']
estimates = [5.0, 5.03, 4.12, 5.0]
colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12']
errors = [0, 0.15, 0.0, 0.0]  # Only DML has a CI to show

bars = ax.barh(methods, estimates, color=colors, edgecolor='white', linewidth=1.5, height=0.55)
ax.axvline(x=5.0, color='#2ecc71', linestyle='--', linewidth=1.5, alpha=0.7, label='True ATE = 5.0')

# Add value labels
for bar, val in zip(bars, estimates):
    ax.text(val + 0.1, bar.get_y() + bar.get_height()/2, f'{val:.2f}',
            va='center', fontsize=11, fontweight='bold')

# Bias annotation
ax.annotate('Regularization\nbias = −0.88',
            xy=(4.12, 1), xytext=(2.5, 1.5),
            fontsize=9, color='#e74c3c', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5))

ax.set_xlabel('Estimated ATE', fontsize=12)
ax.set_xlim(0, 6.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.legend(fontsize=10, loc='lower right')
plt.tight_layout()
plt.savefig('figures/figure_004_dml_vs_naive.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('OK: figure_004_dml_vs_naive.png')
