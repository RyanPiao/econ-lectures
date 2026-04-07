"""Generate California Housing boxplot with Tukey Fences marked."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

from sklearn.datasets import fetch_california_housing
housing = fetch_california_housing(as_frame=True)
vals = housing.frame['MedHouseVal'].values * 100_000

q1 = np.percentile(vals, 25)
q3 = np.percentile(vals, 75)
iqr = q3 - q1
lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

fig, ax = plt.subplots(figsize=(6, 4.5))

bp = ax.boxplot(vals / 1000, vert=False, widths=0.5,
                patch_artist=True,
                boxprops=dict(facecolor='#3498db', alpha=0.4, linewidth=1.5),
                medianprops=dict(color='#e74c3c', linewidth=2),
                whiskerprops=dict(linewidth=1.5),
                capprops=dict(linewidth=1.5),
                flierprops=dict(marker='o', markersize=3, alpha=0.3, color='#7f8c8d'))

# Mark the fences
ax.axvline(upper_fence / 1000, color='#e67e22', linestyle='--', linewidth=2, label=f'Upper Fence (${upper_fence/1000:.0f}K)')
ax.axvline(q1 / 1000, color='#9b59b6', linestyle=':', linewidth=1.5, alpha=0.7)
ax.axvline(q3 / 1000, color='#9b59b6', linestyle=':', linewidth=1.5, alpha=0.7)

# Count outliers
n_outliers = np.sum(vals > upper_fence)
pct_outliers = n_outliers / len(vals) * 100

ax.set_xlabel('Median House Value ($K)', fontsize=12)
ax.set_yticks([])

# Annotations
ax.annotate(f'Q1\n${q1/1000:.0f}K', xy=(q1/1000, 0.7), fontsize=9, ha='center', color='#9b59b6')
ax.annotate(f'Q3\n${q3/1000:.0f}K', xy=(q3/1000, 0.7), fontsize=9, ha='center', color='#9b59b6')
ax.annotate(f'Upper Fence\n${upper_fence/1000:.0f}K', xy=(upper_fence/1000, 1.35),
            fontsize=9, ha='center', color='#e67e22')
ax.annotate(f'{n_outliers} outliers\n({pct_outliers:.1f}%)',
            xy=(480, 1.15), fontsize=9, ha='center', color='#e74c3c',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fce4ec', edgecolor='#e74c3c', alpha=0.8))

ax.legend(loc='upper right', fontsize=9, frameon=True)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('figures/figure_003_boxplot-tukey-fences.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_003_boxplot-tukey-fences.png")
