"""Generate correlation floor comparison figure: Bagging vs Random Forest variance."""
import matplotlib.pyplot as plt
import numpy as np

sigma2 = 0.50
rho_bag = 0.85
rho_rf = 0.40
B = 100

# Bagging components
bag_floor = rho_bag * sigma2
bag_reducible = (1 - rho_bag) / B * sigma2
bag_total = bag_floor + bag_reducible

# RF components
rf_floor = rho_rf * sigma2
rf_reducible = (1 - rho_rf) / B * sigma2
rf_total = rf_floor + rf_reducible

fig, ax = plt.subplots(figsize=(6, 4.5))

x = np.array([0, 1])
labels = ['Bagging\n($\\rho = 0.85$)', 'Random Forest\n($\\rho = 0.40$)']

# Stacked bars
bars_floor = ax.bar(x, [bag_floor, rf_floor], width=0.5,
                     color='#e74c3c', alpha=0.85, label='Correlation floor ($\\rho\\sigma^2$)')
bars_red = ax.bar(x, [bag_reducible, rf_reducible], width=0.5,
                   bottom=[bag_floor, rf_floor],
                   color='#3498db', alpha=0.85, label='Reducible $\\frac{(1-\\rho)}{B}\\sigma^2$')

# Annotations
ax.annotate(f'{bag_total:.3f}', xy=(0, bag_total), ha='center', va='bottom',
            fontsize=12, fontweight='bold')
ax.annotate(f'{rf_total:.3f}', xy=(1, rf_total), ha='center', va='bottom',
            fontsize=12, fontweight='bold')

# Arrow showing reduction
ax.annotate('', xy=(0.7, rf_total), xytext=(0.7, bag_total),
            arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2))
ax.text(0.82, (bag_total + rf_total) / 2, '52%\nlower',
        ha='left', va='center', fontsize=10, color='#2c3e50', fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.set_ylabel('Ensemble Variance', fontsize=12)
ax.set_ylim(0, 0.55)
ax.legend(loc='upper right', fontsize=9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig('figure_009_correlation_floor_comparison.png', dpi=150, bbox_inches='tight',
            facecolor='white')
print('OK: figure_009_correlation_floor_comparison.png')
