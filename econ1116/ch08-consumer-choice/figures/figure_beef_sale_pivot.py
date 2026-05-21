"""Beef on sale ($4/lb → $2/lb) — budget line pivots outward on the beef axis.
   Original line dashed, new line solid + filled affordable region. $16 budget."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 6))

# ---- New (sale) budget line: $16, $2/lb beef, $1 avo → endpoints (16, 0) and (0, 8)
x_new = [0, 16]
y_new = [8, 0]

# ---- Affordable region under the NEW line
ax.fill([0, 16, 0], [0, 0, 8], color='#dcfce7', alpha=0.85, zorder=1)

# ---- Original budget line ($4/lb): endpoints (16, 0) and (0, 4) — dashed
x_old = [0, 16]
y_old = [4, 0]
ax.plot(x_old, y_old, color='#6d28d9', linewidth=3.2, linestyle='--',
        alpha=0.7, zorder=4)

# ---- New budget line — solid
ax.plot(x_new, y_new, color='#6d28d9', linewidth=4, zorder=7,
        solid_capstyle='round')

# Pivot-up arrow on the y-axis: from 4 to 8
ax.annotate('', xy=(0, 7.7), xytext=(0, 4.3),
            arrowprops=dict(arrowstyle='->', color='#111418', lw=2.0))

# ---- Markers (clip_on=False so axis-sitting ones aren't half-clipped)
# New y-intercept at (0, 8): red filled
ax.plot(0, 8, 'o', color='#dc2626', markersize=20, zorder=10,
        markeredgecolor='#7f1d1d', markeredgewidth=1.5, clip_on=False)
ax.annotate(r'$\dfrac{\$16}{\$2/\mathrm{lb}}$ = 8 lbs', xy=(0, 8),
            xytext=(-0.6, 8.1), fontsize=13, weight='bold',
            color='#dc2626', ha='right', va='center')

# Old y-intercept at (0, 4): faded marker + strikethrough-ish label
ax.plot(0, 4, 'o', color='#fca5a5', markersize=18, zorder=9,
        markeredgecolor='#dc2626', markeredgewidth=1.2, clip_on=False, alpha=0.7)
ax.annotate(r'$\dfrac{\$16}{\$4/\mathrm{lb}}$ = 4 lbs', xy=(0, 4),
            xytext=(-0.6, 4), fontsize=11, weight='bold',
            color='#9ca3af', ha='right', va='center')

# x-intercept (16, 0): green
ax.plot(16, 0, 'o', color='#15803d', markersize=20, zorder=10,
        markeredgecolor='#14532d', markeredgewidth=1.5, clip_on=False)
ax.annotate('16 Avocados', xy=(16, 0), xytext=(14.6, 0.7),
            fontsize=13, weight='bold', color='#15803d', ha='center')

# Budget-line labels w/ leader lines
ax.annotate('New budget line ($16)', xy=(11, 2.5),
            xytext=(14.0, 5.5), fontsize=12, weight='bold', color='#6d28d9',
            ha='center',
            arrowprops=dict(arrowstyle='->', color='#6d28d9', lw=1.4))
ax.annotate('Old budget line ($16)', xy=(6, 2.5),
            xytext=(3.5, 5.5), fontsize=11, weight='bold', color='#7c3aed',
            ha='center', alpha=0.9,
            arrowprops=dict(arrowstyle='->', color='#7c3aed', lw=1.2, alpha=0.8))

# Title text in-plot (escape $ so mathtext doesn't eat the price strings)
ax.text(7.5, 9.0, r'Beef on Sale: \$4/lb $\rightarrow$ \$2/lb',
        fontsize=15, weight='bold', ha='center', color='#1a1a1a')

# Axis labels
ax.set_xlabel(r'$\mathrm{Q_{Avocado}}$    (avocados, \$1 each)',
              fontsize=12, weight='bold')
ax.set_ylabel(r'$\mathrm{Q_{Beef}}$    (lbs of beef)',
              fontsize=12, weight='bold')

# Axes anchored at (0, 0)
ax.set_xlim(0, 18)
ax.set_ylim(0, 9.5)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#1f2937')
ax.spines['bottom'].set_color('#1f2937')
ax.spines['left'].set_linewidth(2.2)
ax.spines['bottom'].set_linewidth(2.2)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))

plt.tight_layout()
plt.savefig('figures/figure_beef_sale_pivot.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_beef_sale_pivot.png")
