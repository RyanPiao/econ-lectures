"""Model comparison: Single Tree vs Ridge vs Random Forest on California Housing."""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import fetch_california_housing
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['font.family'] = 'sans-serif'

# Fit models
data = fetch_california_housing()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

tree = DecisionTreeRegressor(random_state=42)
tree.fit(X_train, y_train)
ridge = Ridge(alpha=1.0)
ridge.fit(X_train, y_train)
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Scores
models = ['Single Tree', 'Ridge (Ch 16)', 'Random Forest']
train_r2 = [r2_score(y_train, m.predict(X_train)) for m in [tree, ridge, rf]]
test_r2 = [r2_score(y_test, m.predict(X_test)) for m in [tree, ridge, rf]]

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)

x = np.arange(len(models))
width = 0.32
bars1 = ax.bar(x - width/2, train_r2, width, label='Train R²', color='#6B8BA4', edgecolor='white', linewidth=0.5)
bars2 = ax.bar(x + width/2, test_r2, width, label='Test R²', color='#C47B5A', edgecolor='white', linewidth=0.5)

# Value labels
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9, color='#6B8BA4', fontweight='bold')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=9, color='#C47B5A', fontweight='bold')

ax.set_ylabel('R² Score', fontsize=11, color='#2D2D2D')
ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=10, color='#2D2D2D')
ax.set_ylim(0, 1.12)
ax.legend(fontsize=10, loc='upper left', framealpha=0.9)

# Overfitting gap annotation for tree
ax.annotate('', xy=(0 - width/2, test_r2[0] + 0.02), xytext=(0 - width/2, train_r2[0] - 0.02),
            arrowprops=dict(arrowstyle='<->', color='#A85C5C', lw=1.5))
ax.text(-0.35, (train_r2[0] + test_r2[0]) / 2, 'Overfit\ngap', fontsize=8, color='#A85C5C',
        ha='center', va='center', fontweight='bold')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#D5CEC7')
ax.spines['bottom'].set_color('#D5CEC7')
ax.tick_params(colors='#3A3632', labelsize=9)

plt.tight_layout()
plt.savefig('/Users/openclaw/Resilio Sync/Documents/econ-lecture-material/econ5200-applied-data-analytics/ch19-econ5200-tree-based-models-random-forests/figures/figure_003_model_comparison.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figure_003_model_comparison.png")
