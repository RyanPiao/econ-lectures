"""Income increase ($16 → $20) — budget line shifts OUTWARD parallel.
   Both intercepts scale by 20/16 = 1.25. Prices unchanged."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))

# ---- New budget ($20): endpoints (20, 0) and (0, 5)
x_new = [0, 20]
y_new = [5, 0]

# ---- Old budget ($16): endpoints (16, 0) and (0, 4)
x_old = [0, 16]
y_old = [4, 0]

# ---- Affordable regions
# Original (under old line) — soft green
ax.fill([0, 16, 0], [0, 0, 4], color='#bbf7d0', alpha=0.85, zorder=1)
# Added strip (between old and new lines) — bright green
# Polygon: (0,4) → (16,0) → (20,0) → (0,5) → (0,4)
ax.fill([0, 16, 20, 0], [4, 0, 0, 5], color='#86efac', alpha=0.7, zorder=2)

# Old line — dashed faded
ax.plot(x_old, y_old, color='#a78bfa', linewidth=3, linestyle='--',
        alpha=0.85, zorder=4)

# New line — solid
ax.plot(x_new, y_new, color='#6d28d9', linewidth=4, zorder=7,
        solid_capstyle='round')

# Shift arrows (parallel translation indicator)
ax.annotate('', xy=(0, 4.7), xytext=(0, 4.15),
            arrowprops=dict(arrowstyle='->', color='#111418', lw=2.0))
ax.annotate('', xy=(19.5, 0), xytext=(16.4, 0),
            arrowprops=dict(arrowstyle='->', color='#111418', lw=2.0))

# ---- Markers (clip_on=False so axis-sitting markers aren't half-clipped)
# New y-intercept (0, 5)
ax.plot(0, 5, 'o', color='#dc2626', markersize=20, zorder=10,
        markeredgecolor='#7f1d1d', markeredgewidth=1.5, clip_on=False)
ax.annotate(r'$\dfrac{\$20}{\$4/\mathrm{lb}}$ = 5 lbs', xy=(0, 5),
            xytext=(-0.7, 5), fontsize=13, weight='bold',
            color='#dc2626', ha='right', va='center')

# Old y-intercept (0, 4) — faded
ax.plot(0, 4, 'o', color='#fca5a5', markersize=18, zorder=9,
        markeredgecolor='#dc2626', markeredgewidth=1.2, clip_on=False, alpha=0.7)
ax.annotate(r'$\dfrac{\$16}{\$4/\mathrm{lb}}$ = 4 lbs', xy=(0, 4),
            xytext=(-0.7, 4), fontsize=11, weight='bold',
            color='#9ca3af', ha='right', va='center')

# New x-intercept (20, 0)
ax.plot(20, 0, 'o', color='#15803d', markersize=20, zorder=10,
        markeredgecolor='#14532d', markeredgewidth=1.5, clip_on=False)
ax.annotate(r'$\dfrac{\$20}{\$1/\mathrm{avo}}$ = 20 avocados', xy=(20, 0),
            xytext=(20, 0.6), fontsize=13, weight='bold',
            color='#15803d', ha='center')

# Old x-intercept (16, 0) — faded
ax.plot(16, 0, 'o', color='#86efac', markersize=18, zorder=9,
        markeredgecolor='#15803d', markeredgewidth=1.2, clip_on=False, alpha=0.7)
ax.annotate(r'$\dfrac{\$16}{\$1/\mathrm{avo}}$ = 16', xy=(16, 0),
            xytext=(15.6, -0.85), fontsize=10, weight='bold',
            color='#9ca3af', ha='center', va='top')

# Budget-line labels w/ leader lines
ax.annotate('New budget line ($20)', xy=(13, 1.75),
            xytext=(15.0, 5.5), fontsize=12, weight='bold', color='#6d28d9',
            ha='center',
            arrowprops=dict(arrowstyle='->', color='#6d28d9', lw=1.4))
ax.annotate('Old budget line ($16)', xy=(8, 2),
            xytext=(4.5, 5.5), fontsize=11, weight='bold', color='#7c3aed',
            ha='center', alpha=0.9,
            arrowprops=dict(arrowstyle='->', color='#7c3aed', lw=1.2, alpha=0.8))

# Region labels
ax.text(4, 1.0, 'Original\nattainable', fontsize=11, weight='bold',
        color='#15803d', ha='center', va='center', alpha=0.85)
ax.text(14.3, 2.1, 'Newly\naffordable', fontsize=12, weight='bold',
        color='#047857', ha='center', va='center', style='italic')

# Title text in-plot (escape $ so mathtext doesn't eat the price strings)
ax.text(10, 6.6, r'Income Up: \$16 $\rightarrow$ \$20  (prices unchanged)',
        fontsize=15, weight='bold', ha='center', color='#1a1a1a')

# Axis labels
ax.set_xlabel(r'$\mathrm{Q_{Avocado}}$    (avocados, \$1 each)',
              fontsize=12, weight='bold')
ax.set_ylabel(r'$\mathrm{Q_{Beef}}$    (lbs of beef, \$4/lb)',
              fontsize=12, weight='bold')

# Axes anchored at (0, 0)
ax.set_xlim(0, 22)
ax.set_ylim(-1.4, 7)
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
plt.savefig('figures/figure_income_increase_shift.png', dpi=150,
            bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_income_increase_shift.png")
