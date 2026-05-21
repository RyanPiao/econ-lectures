"""Avocado price up ($1 → $2) — budget line pivots INWARD on the avocado axis.
   Original line dashed, new line solid + filled affordable region. $16 budget,
   beef still $4/lb."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 6))

# ---- Original line ($1 avo, $4 beef): endpoints (16, 0) and (0, 4) — dashed
x_old = [0, 16]
y_old = [4, 0]

# ---- New (higher avo price): $16, $2/avo, $4/lb beef → endpoints (8, 0) and (0, 4)
x_new = [0, 8]
y_new = [4, 0]

# ---- Affordable region under the NEW (smaller) line
ax.fill([0, 8, 0], [0, 0, 4], color='#dcfce7', alpha=0.85, zorder=1)

# ---- Lost-affordability sliver between new and old (light pink)
ax.fill([8, 16, 0, 0], [0, 0, 4, 4], color='#fee2e2', alpha=0.55, zorder=1)

# Old line (dashed)
ax.plot(x_old, y_old, color='#6d28d9', linewidth=3.2, linestyle='--',
        alpha=0.7, zorder=4)

# New line (solid)
ax.plot(x_new, y_new, color='#6d28d9', linewidth=4, zorder=7,
        solid_capstyle='round')

# Pivot-in arrow on the x-axis: from 16 to 8
ax.annotate('', xy=(8.3, 0), xytext=(15.7, 0),
            arrowprops=dict(arrowstyle='->', color='#111418', lw=2.0))

# ---- Markers (clip_on=False so axis-sitting ones aren't half-clipped)
# y-intercept unchanged at (0, 4)
ax.plot(0, 4, 'o', color='#dc2626', markersize=20, zorder=10,
        markeredgecolor='#7f1d1d', markeredgewidth=1.5, clip_on=False)
ax.annotate(r'$\dfrac{\$16}{\$4/\mathrm{lb}}$ = 4 lbs', xy=(0, 4),
            xytext=(-0.6, 4), fontsize=13, weight='bold',
            color='#dc2626', ha='right', va='center')

# New x-intercept at (8, 0)
ax.plot(8, 0, 'o', color='#15803d', markersize=20, zorder=10,
        markeredgecolor='#14532d', markeredgewidth=1.5, clip_on=False)
ax.annotate(r'$\dfrac{\$16}{\$2/\mathrm{avo}}$ = 8 avocados', xy=(8, 0),
            xytext=(7.5, 1.05), fontsize=13, weight='bold',
            color='#15803d', ha='right')

# Old x-intercept at (16, 0) — faded
ax.plot(16, 0, 'o', color='#86efac', markersize=18, zorder=9,
        markeredgecolor='#15803d', markeredgewidth=1.2, clip_on=False, alpha=0.7)
ax.annotate(r'$\dfrac{\$16}{\$1/\mathrm{avo}}$ = 16 avocados', xy=(16, 0),
            xytext=(15.6, 0.55), fontsize=11, weight='bold',
            color='#9ca3af', ha='center')

# Budget-line labels w/ leader lines
ax.annotate('New budget line ($16)', xy=(3.5, 2.25),
            xytext=(1.5, 5.4), fontsize=12, weight='bold', color='#6d28d9',
            ha='center',
            arrowprops=dict(arrowstyle='->', color='#6d28d9', lw=1.4))
ax.annotate('Old budget line ($16)', xy=(11, 1.4),
            xytext=(13.0, 5.0), fontsize=11, weight='bold', color='#7c3aed',
            ha='center', alpha=0.9,
            arrowprops=dict(arrowstyle='->', color='#7c3aed', lw=1.2, alpha=0.8))

# "No longer affordable" region annotation
ax.text(11.5, 2.2, 'No longer\naffordable', fontsize=12, weight='bold',
        color='#b91c1c', ha='center', va='center', style='italic')

# Title text in-plot (escape $ so mathtext doesn't eat the price strings)
ax.text(8, 6.0, r'Avocado Up: \$1 $\rightarrow$ \$2 each',
        fontsize=15, weight='bold', ha='center', color='#1a1a1a')

# Axis labels
ax.set_xlabel(r'$\mathrm{Q_{Avocado}}$    (avocados)',
              fontsize=12, weight='bold')
ax.set_ylabel(r'$\mathrm{Q_{Beef}}$    (lbs of beef, \$4/lb)',
              fontsize=12, weight='bold')

# Axes anchored at (0, 0)
ax.set_xlim(0, 18)
ax.set_ylim(0, 6.5)
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
plt.savefig('figures/figure_avocado_priceup_pivot.png', dpi=150,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_avocado_priceup_pivot.png")
