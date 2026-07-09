"""Let's Visualize This — Maya's $16 budget line for pizza slices + ramen.
   Shows endpoints (4 pizza, 0 ramen) and (0 pizza, 16 ramen) + midpoint (2 pizza, 8 ramen)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'figure_lets_visualize.png')

fig, ax = plt.subplots(figsize=(9, 5.6))

# Budget line: 4*Q_pizza + 1*Q_ramen = 16
# Endpoints: (0, 4) and (16, 0)  -- x = Q_ramen, y = Q_pizza
x_line = [0, 16]
y_line = [4, 0]
ax.plot(x_line, y_line, color='#6d28d9', linewidth=4, zorder=5)

# Markers + labels (clip_on=False so axis-sitting markers aren't half-cut)
ax.plot(0, 4, 'o', color='#dc2626', markersize=18, zorder=10,
        markeredgecolor='#7f1d1d', markeredgewidth=1.5, clip_on=False)
ax.annotate('4 Pizza Slices', xy=(0, 4), xytext=(0.6, 4.25),
            fontsize=14, weight='bold', color='#dc2626', ha='left')

ax.plot(8, 2, 'o', color='#ea580c', markersize=18, zorder=10,
        markeredgecolor='#9a3412', markeredgewidth=1.5, clip_on=False)
ax.annotate('2 Slices\n+ 8 Ramen', xy=(8, 2), xytext=(8.4, 2.6),
            fontsize=12, weight='bold', color='#ea580c')

ax.plot(16, 0, 'o', color='#15803d', markersize=18, zorder=10,
        markeredgecolor='#14532d', markeredgewidth=1.5, clip_on=False)
ax.annotate('16 Ramen', xy=(16, 0), xytext=(14.9, 0.45),
            fontsize=14, weight='bold', color='#15803d')

# Dashed guide lines for the midpoint
ax.plot([0, 8], [2, 2], color='#9ca3af', linewidth=1.4, linestyle='--', zorder=2)
ax.plot([8, 8], [0, 2], color='#9ca3af', linewidth=1.4, linestyle='--', zorder=2)

# Title placement on plot
ax.text(8, 4.55, 'The Budget Line — $16 Budget', fontsize=14, weight='bold',
        ha='center', color='#1a1a1a')

# Axis labels (escape $ to avoid mathtext mangling the price labels)
ax.set_xlabel(r'$\mathrm{Q_{Ramen}}$    (ramen packs, \$1 each)', fontsize=12, weight='bold')
ax.set_ylabel(r'$\mathrm{Q_{Pizza}}$    (pizza slices, \$4 each)', fontsize=12, weight='bold')

# Axes anchored at (0, 0)
ax.set_xlim(0, 17.5)
ax.set_ylim(0, 4.9)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#374151')
ax.spines['bottom'].set_color('#374151')
ax.spines['left'].set_linewidth(1.6)
ax.spines['bottom'].set_linewidth(1.6)
ax.grid(alpha=0.18)

plt.tight_layout()
plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("OK:", OUT)
