"""Generate contamination effect figure: mean shifts, median stable."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

np.random.seed(42)

# Simulate contamination at increasing levels
from sklearn.datasets import fetch_california_housing
housing = fetch_california_housing(as_frame=True)
vals = housing.frame['MedHouseVal'].values.copy()

contamination_pcts = [0, 0.5, 1, 2, 5, 10]
means = []
medians = []

for pct in contamination_pcts:
    v = vals.copy()
    n_replace = int(len(v) * pct / 100)
    if n_replace > 0:
        idx = np.random.choice(len(v), n_replace, replace=False)
        v[idx] = 10.0  # $1M (max value)
    means.append(np.mean(v) * 100_000)
    medians.append(np.median(v) * 100_000)

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.plot(contamination_pcts, [m/1000 for m in means], 'o-', color='#e74c3c',
        linewidth=2.5, markersize=8, label='Mean', zorder=5)
ax.plot(contamination_pcts, [m/1000 for m in medians], 's-', color='#2ecc71',
        linewidth=2.5, markersize=8, label='Median', zorder=5)

ax.set_xlabel('Contamination (%)', fontsize=12)
ax.set_ylabel('House Value ($K)', fontsize=12)
ax.legend(fontsize=11, frameon=True, fancybox=True)
ax.set_xlim(-0.5, 10.5)
ax.grid(True, alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Annotate the gap
ax.annotate('Mean shifts\n+$42K at 10%',
            xy=(10, means[-1]/1000), xytext=(7, means[-1]/1000 + 15),
            fontsize=9, color='#e74c3c',
            arrowprops=dict(arrowstyle='->', color='#e74c3c', lw=1.5))
ax.annotate('Median stable',
            xy=(10, medians[-1]/1000), xytext=(7, medians[-1]/1000 - 15),
            fontsize=9, color='#2ecc71',
            arrowprops=dict(arrowstyle='->', color='#2ecc71', lw=1.5))

plt.tight_layout()
plt.savefig('figures/figure_002_contamination-effect.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_002_contamination-effect.png")
