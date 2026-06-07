"""Ch 11 — "Self-sorting captures the entire demand curve" (Netflix versioning).
A smooth decreasing S-shaped demand curve with a cyan->white vertical gradient fill underneath
(cyan at the high-price top-left, fading to white at the low-price bottom-right). Clean, no axes;
text annotations + caption are added in HTML on the slide.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.colors import LinearSegmentedColormap

fig, ax = plt.subplots(figsize=(9.6, 5.0))
x = np.linspace(0, 10, 500)
y = 0.6 + 8.6 / (1 + np.exp(1.3 * (x - 4.3)))          # decreasing logistic: ~9.2 -> ~0.6

# vertical gradient (white at bottom -> cyan at top), clipped to the area under the curve
cmap = LinearSegmentedColormap.from_list('cyanfade', ['#ffffff', '#15dff5'])
grad = np.linspace(0, 1, 256).reshape(-1, 1)
im = ax.imshow(grad, extent=[0, 10, 0, 10], origin='lower', aspect='auto', cmap=cmap, zorder=1)
verts = np.column_stack([np.concatenate([x, [10, 0]]), np.concatenate([y, [0, 0]])])
clip = Polygon(verts, closed=True, facecolor='none', edgecolor='none', transform=ax.transData)
ax.add_patch(clip)
im.set_clip_path(clip)

ax.plot(x, y, color='#2b2b2b', lw=3.4, zorder=5, solid_capstyle='round')  # demand curve

ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis('off')
plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
plt.savefig('fig-netflix-curve.png', dpi=150, transparent=True)
print('saved fig-netflix-curve.png')
