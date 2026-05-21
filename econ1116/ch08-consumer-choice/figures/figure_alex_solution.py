"""Solution — Alex's $150 entertainment budget: games at $80, Uber Eats at $30.
   Filled-in budget line for the You Try paper exercise."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 5.6))

# Budget line: 80 * Q_games + 30 * Q_meals = 150
# Endpoints (x = Q_meals, y = Q_games): (5, 0) and (0, 1.875)
x_line = [0, 5]
y_line = [1.875, 0]
ax.plot(x_line, y_line, color='#6d28d9', linewidth=4, zorder=7,
        solid_capstyle='round')

# Affordable region — green tint below the line
ax.fill([0, 5, 0], [0, 0, 1.875], color='#dcfce7', alpha=0.7, zorder=1)

# Endpoint markers (clip_on=False so axis-sitting markers aren't half-cut)
ax.plot(0, 1.875, 'o', color='#dc2626', markersize=18, zorder=10,
        markeredgecolor='#7f1d1d', markeredgewidth=1.5, clip_on=False)
ax.annotate('All games:\n1.875 games\n(can buy 1)', xy=(0, 1.875),
            xytext=(0.25, 2.4), fontsize=12, weight='bold',
            color='#dc2626', ha='left', va='top')

ax.plot(5, 0, 'o', color='#15803d', markersize=18, zorder=10,
        markeredgecolor='#14532d', markeredgewidth=1.5, clip_on=False)
ax.annotate('All meals:\n5 Uber Eats', xy=(5, 0), xytext=(5, 0.35),
            fontsize=12, weight='bold', color='#15803d', ha='center')

# Midpoint-ish marker: 1 game + (150-80)/30 = 1 game + 2.33 meals
# Pure midpoint by spending half on each: $75 → 0.94 games, $75 → 2.5 meals
ax.plot(2.5, 0.9375, 'o', color='#ea580c', markersize=18, zorder=6,
        markeredgecolor='#9a3412', markeredgewidth=1.5)
ax.annotate('$75 each:\n2.5 meals\n+ ~0.94 game', xy=(2.5, 0.9375),
            xytext=(2.8, 1.35), fontsize=11, weight='bold', color='#ea580c')

# Dashed guides to the midpoint
ax.plot([0, 2.5], [0.9375, 0.9375], color='#9ca3af', linewidth=1.4, linestyle='--', zorder=2)
ax.plot([2.5, 2.5], [0, 0.9375], color='#9ca3af', linewidth=1.4, linestyle='--', zorder=2)

# Slope annotation
ax.text(3.6, 1.85, r'Slope $=\dfrac{P_{meal}}{P_{game}}=\dfrac{30}{80}=0.375$',
        fontsize=13, color='#1a1a1a',
        bbox=dict(boxstyle='round,pad=0.45', facecolor='#fef9c3',
                  edgecolor='#ca8a04', linewidth=1.2))

# Title
ax.text(2.5, 2.45, "Alex's Budget Line — $150", fontsize=14, weight='bold',
        ha='center', color='#1a1a1a')

# Axis labels
ax.set_xlabel(r'$\mathrm{Q_{Uber\,Eats}}$    (meals, \$30 each)', fontsize=12, weight='bold')
ax.set_ylabel(r'$\mathrm{Q_{Games}}$    (games, \$80 each)', fontsize=12, weight='bold')

ax.set_xlim(0, 6)
ax.set_ylim(0, 2.6)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_yticks([0, 0.5, 1, 1.5, 2])
ax.grid(alpha=0.25)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#374151')
ax.spines['bottom'].set_color('#374151')
ax.spines['left'].set_linewidth(1.8)
ax.spines['bottom'].set_linewidth(1.8)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))

plt.tight_layout()
plt.savefig('figures/figure_alex_solution.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_alex_solution.png")
