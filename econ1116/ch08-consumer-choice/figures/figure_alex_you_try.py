"""You Try — Alex's $150 entertainment budget: games at $80, Uber Eats at $30.
   Empty axes for student to draw the budget line on paper (or a partial setup with prompts)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 5.6))

# Empty axes with labels but no budget line drawn — students fill it in
ax.set_xlabel(r'$\mathrm{Q_{Uber\,Eats}}$    (meals, \$30 each)', fontsize=12, weight='bold')
ax.set_ylabel(r'$\mathrm{Q_{Games}}$    (games, \$80 each)', fontsize=12, weight='bold')

# Faint grid for reference
ax.set_xlim(0, 6)
ax.set_ylim(0, 2.5)
ax.set_xticks([0, 1, 2, 3, 4, 5])
ax.set_yticks([0, 0.5, 1, 1.5, 2])
ax.grid(alpha=0.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#374151')
ax.spines['bottom'].set_color('#374151')
ax.spines['left'].set_linewidth(1.6)
ax.spines['bottom'].set_linewidth(1.6)

# Big "?" placeholder where the budget line should be
ax.text(3.0, 1.25, '?',
        fontsize=140, color='#cbd5e1', ha='center', va='center',
        weight='bold', zorder=2)
ax.text(3.0, 0.32, 'Draw the budget line\non paper',
        fontsize=14, color='#64748b', ha='center', va='center',
        style='italic', zorder=3)

plt.tight_layout()
plt.savefig('figures/figure_alex_you_try.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_alex_you_try.png")
