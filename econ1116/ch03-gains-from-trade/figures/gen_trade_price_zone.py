"""Trade Price Zone diagram for Ch3 lecture — shows valid price range."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

fig, ax = plt.subplots(figsize=(6, 3))

# Price range
ax.barh(0, 2 - 0.5, left=0.5, height=0.4, color='#dbeafe', edgecolor='#2563eb', linewidth=2)

# Endpoints
ax.plot(0.5, 0, 'o', color='#2563eb', markersize=12, zorder=5)
ax.plot(2.0, 0, 'o', color='#16a34a', markersize=12, zorder=5)

# Example trade price
ax.plot(1.0, 0, 'D', color='#dc2626', markersize=10, zorder=6)

# Labels
ax.text(0.5, -0.35, 'U.S. OC\n0.5 avocados', ha='center', fontsize=9, fontweight='bold', color='#2563eb')
ax.text(2.0, -0.35, 'Mexico OC\n2.0 avocados', ha='center', fontsize=9, fontweight='bold', color='#16a34a')
ax.text(1.0, 0.32, 'Trade price = 1.0\n(both gain)', ha='center', fontsize=9, fontweight='bold', color='#dc2626')

# Zone label
ax.text(1.25, -0.65, 'Mutually beneficial trade zone', ha='center', fontsize=10, fontstyle='italic', color='#475569')

# Axis
ax.set_xlim(0, 2.5)
ax.set_ylim(-0.8, 0.6)
ax.set_xlabel('Price of 1 Smartphone (in tons of avocados)', fontsize=10, fontweight='bold')
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)

# Arrows showing "U.S. won't trade" and "Mexico won't trade" zones
ax.annotate('U.S. won\'t\ntrade here', xy=(0.15, 0), fontsize=7, ha='center', color='#94a3b8', fontstyle='italic')
ax.annotate('Mexico won\'t\ntrade here', xy=(2.35, 0), fontsize=7, ha='center', color='#94a3b8', fontstyle='italic')

plt.tight_layout()
outpath = os.path.join(os.path.dirname(__file__), 'ch03-trade-price-zone.png')
plt.savefig(outpath, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print(f'Saved: {outpath}')
