"""Brooks's Law illustration: 5-node complete graph (10 channels) next
to a 50-node complete graph (1,225 channels) with the n(n-1)/2 formula
in between. Mirrors the user's reference screenshot.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations

RED = '#E5402B'
BLACK = '#2D2D2D'

fig = plt.figure(figsize=(11.0, 4.6))

# ---------------- Panel 1: 5-node complete graph ----------------
ax1 = fig.add_axes([0.02, 0.05, 0.36, 0.90])
n1 = 5
angles = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, n1, endpoint=False)
x1 = np.cos(angles)
y1 = np.sin(angles)
# Draw all C(5,2)=10 edges
for i, j in combinations(range(n1), 2):
    ax1.plot([x1[i], x1[j]], [y1[i], y1[j]],
             color=BLACK, linewidth=1.6, alpha=0.85, zorder=2)
# Nodes
ax1.scatter(x1, y1, s=320, color=BLACK, zorder=5, edgecolor='white', linewidth=2.5)
ax1.set_xlim(-1.5, 1.5)
ax1.set_ylim(-1.5, 1.5)
ax1.set_aspect('equal')
ax1.axis('off')
ax1.text(0, -1.45, '5 People = 10 Channels',
         fontsize=16, color=BLACK, ha='center', va='top', fontweight='bold')

# ---------------- Panel 2: formula ----------------
ax2 = fig.add_axes([0.38, 0.05, 0.24, 0.90])
ax2.text(0.5, 0.55, r'$\dfrac{n\,(n-1)}{2}$',
         fontsize=44, ha='center', va='center', color=BLACK)
ax2.text(0.5, 0.18, 'channels grow\ncombinatorially',
         fontsize=12, ha='center', va='center', color=BLACK, fontstyle='italic')
ax2.axis('off')

# ---------------- Panel 3: 50-node complete graph ----------------
ax3 = fig.add_axes([0.62, 0.05, 0.36, 0.90])
n3 = 50
angles3 = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, n3, endpoint=False)
x3 = np.cos(angles3)
y3 = np.sin(angles3)
# Draw all C(50,2)=1,225 edges in red with low alpha to mimic the dense web
for i, j in combinations(range(n3), 2):
    ax3.plot([x3[i], x3[j]], [y3[i], y3[j]],
             color=RED, linewidth=0.45, alpha=0.30, zorder=2)
# Nodes (black dots around the rim)
ax3.scatter(x3, y3, s=70, color=BLACK, zorder=5, edgecolor='white', linewidth=1.2)
ax3.set_xlim(-1.4, 1.4)
ax3.set_ylim(-1.4, 1.4)
ax3.set_aspect('equal')
ax3.axis('off')
ax3.text(0, -1.32, '50 People = 1,225 Channels',
         fontsize=16, color=BLACK, ha='center', va='top', fontweight='bold')

plt.savefig('fig-brooks-law.png', dpi=160, bbox_inches='tight',
            facecolor='white')
print('saved fig-brooks-law.png')
