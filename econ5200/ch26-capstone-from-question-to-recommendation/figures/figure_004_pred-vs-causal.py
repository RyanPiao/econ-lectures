"""Figure 4: Prediction vs Causation comparison — side-by-side framework."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4.5))

# Prediction side
pred_items = [
    ('Goal', 'Forecast $\\hat{y}$'),
    ('Method', 'RF, XGBoost, LASSO'),
    ('Features', 'Everything predictive'),
    ('Metric', 'RMSE, AUC, MASE'),
    ('Output', '"Predicts X with Y% accuracy"'),
]

ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.set_title('Prediction\n("Umbrella")', fontsize=13, fontweight='bold', color='#2980b9')
ax1.add_patch(mpatches.FancyBboxPatch((0.3, 0.3), 9.4, 9.4, boxstyle='round,pad=0.3',
              facecolor='#eaf2f8', edgecolor='#2980b9', linewidth=2))

for i, (label, value) in enumerate(pred_items):
    y = 8.5 - i * 1.7
    ax1.text(1, y, label, fontsize=9, fontweight='bold', color='#2c3e50')
    ax1.text(1, y - 0.7, value, fontsize=8, color='#555', style='italic')

ax1.axis('off')

# Causation side
causal_items = [
    ('Goal', 'Estimate $\\hat{\\tau}$ of T on Y'),
    ('Method', 'RCT, DiD, DML'),
    ('Features', 'Only exogenous controls'),
    ('Metric', 'CI for $\\hat{\\tau}$, balance'),
    ('Output', '"T caused Z-unit change (CI)"'),
]

ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_title('Causation\n("Rain Dance")', fontsize=13, fontweight='bold', color='#c0392b')
ax2.add_patch(mpatches.FancyBboxPatch((0.3, 0.3), 9.4, 9.4, boxstyle='round,pad=0.3',
              facecolor='#fdedec', edgecolor='#c0392b', linewidth=2))

for i, (label, value) in enumerate(causal_items):
    y = 8.5 - i * 1.7
    ax2.text(1, y, label, fontsize=9, fontweight='bold', color='#2c3e50')
    ax2.text(1, y - 0.7, value, fontsize=8, color='#555', style='italic')

ax2.axis('off')

plt.tight_layout()
plt.savefig('figure_004_pred-vs-causal.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('OK: figure_004_pred-vs-causal.png')
