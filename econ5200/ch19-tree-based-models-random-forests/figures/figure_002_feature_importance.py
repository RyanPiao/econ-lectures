"""Feature importance bar chart for California Housing Random Forest."""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'

# Fit the model
data = fetch_california_housing()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Sort importances
indices = np.argsort(rf.feature_importances_)[::-1]
names = [data.feature_names[i] for i in indices]
values = rf.feature_importances_[indices]

# White Academia colors
colors = ['#6B8BA4' if i == 0 else '#C47B5A' if i == 1 else '#8C8580' for i in range(len(names))]

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)
bars = ax.barh(range(len(names)), values, color=colors, height=0.65, edgecolor='white', linewidth=0.5)

ax.set_yticks(range(len(names)))
ax.set_yticklabels(names, fontsize=10, color='#2D2D2D')
ax.invert_yaxis()
ax.set_xlabel('Mean Decrease in Impurity (MDI)', fontsize=11, color='#2D2D2D')

# Value labels
for i, v in enumerate(values):
    ax.text(v + 0.005, i, f'{v:.3f}', va='center', fontsize=9, color='#3A3632')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#D5CEC7')
ax.spines['bottom'].set_color('#D5CEC7')
ax.tick_params(colors='#3A3632', labelsize=9)
ax.set_xlim(0, max(values) * 1.2)

plt.tight_layout()
plt.savefig('/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/econ5200-applied-data-analytics/ch19-econ5200-tree-based-models-random-forests/figures/figure_002_feature_importance.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figure_002_feature_importance.png")
