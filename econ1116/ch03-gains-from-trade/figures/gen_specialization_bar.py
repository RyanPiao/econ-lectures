"""Before vs After Specialization bar chart for Ch3 lecture slides."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

fig, axes = plt.subplots(1, 2, figsize=(6, 4.5))

# Data
categories = ['Before\nTrade', 'After\nSpecialization']
us_smartphones = [500, 1000]
mexico_smartphones = [100, 0]
us_avocados = [250, 0]
mexico_avocados = [200, 400]

x = np.arange(len(categories))
width = 0.35

# Smartphones panel
ax1 = axes[0]
bars1 = ax1.bar(x - width/2, us_smartphones, width, label='United States', color='#2563eb', alpha=0.85)
bars2 = ax1.bar(x + width/2, mexico_smartphones, width, label='Mexico', color='#16a34a', alpha=0.85)
ax1.set_ylabel('Smartphones', fontsize=11, fontweight='bold')
ax1.set_title('Smartphones', fontsize=12, fontweight='bold', pad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=9)
ax1.set_ylim(0, 1150)
ax1.legend(fontsize=8, loc='upper left')
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Add value labels
for bar in bars1:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 20, f'{int(h)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar in bars2:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 20, f'{int(h)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Avocados panel
ax2 = axes[1]
bars3 = ax2.bar(x - width/2, us_avocados, width, label='United States', color='#2563eb', alpha=0.85)
bars4 = ax2.bar(x + width/2, mexico_avocados, width, label='Mexico', color='#16a34a', alpha=0.85)
ax2.set_ylabel('Avocados (tons)', fontsize=11, fontweight='bold')
ax2.set_title('Avocados (tons)', fontsize=12, fontweight='bold', pad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=9)
ax2.set_ylim(0, 480)
ax2.legend(fontsize=8, loc='upper left')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for bar in bars3:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 8, f'{int(h)}', ha='center', va='bottom', fontsize=9, fontweight='bold')
for bar in bars4:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 8, f'{int(h)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

# World totals annotation
ax1.annotate('World: 600 → 1,000\n(+67%)', xy=(0.5, 0.92), xycoords='axes fraction',
             fontsize=8, color='#dc2626', fontweight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#fef2f2', edgecolor='#dc2626', alpha=0.9))
ax2.annotate('World: 450 → 400\n(−11%)', xy=(0.5, 0.92), xycoords='axes fraction',
             fontsize=8, color='#9333ea', fontweight='bold', ha='center',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#faf5ff', edgecolor='#9333ea', alpha=0.9))

plt.tight_layout()
outpath = os.path.join(os.path.dirname(__file__), 'ch03-specialization-bar.png')
plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {outpath}')
