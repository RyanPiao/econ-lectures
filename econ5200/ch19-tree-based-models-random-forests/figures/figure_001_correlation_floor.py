"""Correlation floor comparison: Bagging vs Random Forest variance reduction."""
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'

# Parameters
sigma2 = 0.50
B_values = np.arange(1, 501)
rho_bagging = 0.85
rho_rf = 0.40

# Variance formulas
var_bagging = rho_bagging * sigma2 + (1 - rho_bagging) / B_values * sigma2
var_rf = rho_rf * sigma2 + (1 - rho_rf) / B_values * sigma2

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)

ax.plot(B_values, var_bagging, color='#C47B5A', linewidth=2.5, label=f'Bagging (ρ = {rho_bagging})')
ax.plot(B_values, var_rf, color='#6B8BA4', linewidth=2.5, label=f'Random Forest (ρ = {rho_rf})')

# Correlation floors
ax.axhline(y=rho_bagging * sigma2, color='#C47B5A', linestyle='--', alpha=0.5, linewidth=1.2)
ax.axhline(y=rho_rf * sigma2, color='#6B8BA4', linestyle='--', alpha=0.5, linewidth=1.2)

# Annotations
ax.annotate(f'Bagging floor: ρσ² = {rho_bagging * sigma2:.3f}',
            xy=(400, rho_bagging * sigma2), fontsize=9, color='#C47B5A',
            va='bottom', ha='right')
ax.annotate(f'RF floor: ρσ² = {rho_rf * sigma2:.3f}',
            xy=(400, rho_rf * sigma2), fontsize=9, color='#6B8BA4',
            va='bottom', ha='right')

# Arrow showing 52% reduction
mid_y = (rho_bagging * sigma2 + rho_rf * sigma2) / 2
ax.annotate('', xy=(450, rho_rf * sigma2 + 0.005), xytext=(450, rho_bagging * sigma2 - 0.005),
            arrowprops=dict(arrowstyle='<->', color='#6A8E6B', lw=1.5))
ax.text(460, mid_y, '52%\nlower', fontsize=8, color='#6A8E6B', va='center', fontweight='bold')

ax.set_xlabel('Number of Trees (B)', fontsize=11, color='#2D2D2D')
ax.set_ylabel('Ensemble Variance', fontsize=11, color='#2D2D2D')
ax.set_xlim(1, 500)
ax.set_ylim(0, 0.55)
ax.legend(fontsize=10, loc='upper right', framealpha=0.9)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#D5CEC7')
ax.spines['bottom'].set_color('#D5CEC7')
ax.tick_params(colors='#3A3632', labelsize=9)
ax.grid(axis='y', alpha=0.3, color='#D5CEC7')

plt.tight_layout()
plt.savefig('/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/econ5200-applied-data-analytics/ch19-econ5200-tree-based-models-random-forests/figures/figure_001_correlation_floor.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figure_001_correlation_floor.png")
