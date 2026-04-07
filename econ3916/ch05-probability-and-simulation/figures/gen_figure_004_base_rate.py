"""Base rate fallacy visualization: 1000 transactions as dots."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

rng = np.random.default_rng(42)
n = 1000
# 1 actual fraud, ~20 false positives, ~979 true negatives
fraud_idx = 0
fp_rate = 0.02
is_legit = np.ones(n, dtype=bool)
is_legit[fraud_idx] = False

flagged = np.zeros(n, dtype=bool)
flagged[fraud_idx] = True  # True positive
for i in range(1, n):
    if rng.random() < fp_rate:
        flagged[i] = True

# Colors
colors = []
for i in range(n):
    if not is_legit[i] and flagged[i]:
        colors.append('#d62728')   # True positive (red)
    elif is_legit[i] and flagged[i]:
        colors.append('#ff7f0e')   # False positive (orange)
    else:
        colors.append('#2ca02c')   # True negative (green)

# Layout as grid
cols = 40
rows = 25
x = np.array([i % cols for i in range(n)])
y = np.array([i // cols for i in range(n)])

fig, ax = plt.subplots(figsize=(8, 5.5))
ax.scatter(x, y, c=colors, s=25, edgecolors='none', alpha=0.85)
ax.set_xlim(-1, cols)
ax.set_ylim(-1, rows)
ax.invert_yaxis()
ax.set_aspect('equal')
ax.axis('off')

# Legend
red_patch = mpatches.Patch(color='#d62728', label=f'True fraud: 1')
orange_patch = mpatches.Patch(color='#ff7f0e', label=f'False alarms: {sum(1 for c in colors if c == "#ff7f0e")}')
green_patch = mpatches.Patch(color='#2ca02c', label=f'True negatives: {sum(1 for c in colors if c == "#2ca02c")}')
ax.legend(handles=[red_patch, orange_patch, green_patch],
          loc='lower center', ncol=3, fontsize=10,
          bbox_to_anchor=(0.5, -0.08), frameon=False)

plt.tight_layout()
plt.savefig('figure_004_base_rate_fallacy.png', dpi=150, bbox_inches='tight',
            facecolor='white')
print("OK: figure_004_base_rate_fallacy.png")
