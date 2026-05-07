"""Figure 2: TF-IDF vs Embeddings — sparse scattered vs semantic clusters."""
import matplotlib.pyplot as plt
import numpy as np

# White Academia palette
CHARCOAL = '#2D2D2D'
DUSTY_BLUE = '#6B8BA4'
TERRACOTTA = '#C47B5A'
SAGE = '#6A8E6B'
ROSEWOOD = '#A85C5C'
LIGHT_BG = '#F8F6F3'
DECORATIVE = '#D5CEC7'

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'font.family': 'sans-serif',
    'font.size': 11,
})

np.random.seed(42)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4.5))

# --- Left panel: TF-IDF (sparse, scattered) ---
n = 30
# Monetary policy documents (scattered because sparse vectors don't cluster well by meaning)
x1 = np.random.uniform(0, 1, n)
y1 = np.random.uniform(0, 1, n)
labels1 = ['monetary'] * 10 + ['fiscal'] * 10 + ['trade'] * 10
colors1 = [DUSTY_BLUE] * 10 + [TERRACOTTA] * 10 + [SAGE] * 10

ax1.scatter(x1, y1, c=colors1, s=40, alpha=0.7, edgecolors='white', linewidths=0.5)
ax1.set_title('TF-IDF (Sparse)', fontsize=13, color=CHARCOAL, fontweight='bold')
ax1.set_xlabel('Dimension 1', fontsize=10, color=CHARCOAL)
ax1.set_ylabel('Dimension 2', fontsize=10, color=CHARCOAL)

# --- Right panel: Embeddings (clustered by meaning) ---
# Monetary cluster
mx, my = 0.3, 0.7
ex_m = mx + np.random.normal(0, 0.06, 10)
ey_m = my + np.random.normal(0, 0.06, 10)

# Fiscal cluster
fx, fy = 0.7, 0.3
ex_f = fx + np.random.normal(0, 0.06, 10)
ey_f = fy + np.random.normal(0, 0.06, 10)

# Trade cluster
tx, ty = 0.7, 0.75
ex_t = tx + np.random.normal(0, 0.06, 10)
ey_t = ty + np.random.normal(0, 0.06, 10)

ax2.scatter(ex_m, ey_m, c=DUSTY_BLUE, s=40, alpha=0.7, edgecolors='white', linewidths=0.5, label='Monetary policy')
ax2.scatter(ex_f, ey_f, c=TERRACOTTA, s=40, alpha=0.7, edgecolors='white', linewidths=0.5, label='Fiscal policy')
ax2.scatter(ex_t, ey_t, c=SAGE, s=40, alpha=0.7, edgecolors='white', linewidths=0.5, label='Trade policy')

# Draw cluster boundaries (light ellipses)
from matplotlib.patches import Ellipse
for cx, cy, color in [(mx, my, DUSTY_BLUE), (fx, fy, TERRACOTTA), (tx, ty, SAGE)]:
    ellipse = Ellipse((cx, cy), 0.25, 0.25, fill=False, edgecolor=color, linestyle='--', alpha=0.5, linewidth=1.5)
    ax2.add_patch(ellipse)

ax2.set_title('Embeddings (Dense)', fontsize=13, color=CHARCOAL, fontweight='bold')
ax2.set_xlabel('Dimension 1', fontsize=10, color=CHARCOAL)
ax2.legend(fontsize=8, loc='lower left', framealpha=0.9)

for ax in [ax1, ax2]:
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.05)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(DECORATIVE)
    ax.spines['left'].set_color(DECORATIVE)
    ax.tick_params(colors=CHARCOAL, labelsize=9)

plt.tight_layout()
plt.savefig(
    __file__.replace('.py', '.png'),
    dpi=150, bbox_inches='tight', facecolor='white'
)
plt.close()
print("OK: figure_002_tfidf_vs_embeddings.png")
