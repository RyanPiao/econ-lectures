"""Gains from Trade — before/after consumption comparison for Ch3 lecture."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

fig, axes = plt.subplots(1, 2, figsize=(6, 4.5))

# --- U.S. Panel ---
ax1 = axes[0]
categories = ['Smartphones', 'Avocados\n(tons)']
before = [500, 250]
after = [700, 300]
x = np.arange(len(categories))
width = 0.35

bars1 = ax1.bar(x - width/2, before, width, label='Before Trade', color='#94a3b8', alpha=0.9)
bars2 = ax1.bar(x + width/2, after, width, label='After Trade', color='#2563eb', alpha=0.9)

ax1.set_title('United States', fontsize=13, fontweight='bold', pad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=10)
ax1.set_ylim(0, 850)
ax1.legend(fontsize=8)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for bar in bars1:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 10, f'{int(h)}', ha='center', fontsize=9, fontweight='bold')
for bar in bars2:
    h = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., h + 10, f'{int(h)}', ha='center', fontsize=9, fontweight='bold', color='#2563eb')

# Gains annotations
ax1.annotate('+200', xy=(0 + width/2, 720), fontsize=10, color='#16a34a', fontweight='bold', ha='center')
ax1.annotate('+50', xy=(1 + width/2, 315), fontsize=10, color='#16a34a', fontweight='bold', ha='center')

# --- Mexico Panel ---
ax2 = axes[1]
before_mx = [100, 200]
after_mx = [300, 100]

bars3 = ax2.bar(x - width/2, before_mx, width, label='Before Trade', color='#94a3b8', alpha=0.9)
bars4 = ax2.bar(x + width/2, after_mx, width, label='After Trade', color='#16a34a', alpha=0.9)

ax2.set_title('Mexico', fontsize=13, fontweight='bold', pad=10)
ax2.set_xticks(x)
ax2.set_xticklabels(categories, fontsize=10)
ax2.set_ylim(0, 400)
ax2.legend(fontsize=8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for bar in bars3:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 5, f'{int(h)}', ha='center', fontsize=9, fontweight='bold')
for bar in bars4:
    h = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., h + 5, f'{int(h)}', ha='center', fontsize=9, fontweight='bold', color='#16a34a')

# Gains annotations
ax2.annotate('+200', xy=(0 + width/2, 310), fontsize=10, color='#2563eb', fontweight='bold', ha='center')
ax2.annotate('−100', xy=(1 + width/2, 112), fontsize=10, color='#dc2626', fontweight='bold', ha='center')

fig.suptitle('Both Countries Gain from Trade', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
outpath = os.path.join(os.path.dirname(__file__), 'ch03-gains-bar.png')
plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {outpath}')
