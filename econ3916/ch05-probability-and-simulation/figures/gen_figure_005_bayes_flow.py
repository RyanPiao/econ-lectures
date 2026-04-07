"""Bayes' Theorem flow diagram for slides."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(8, 4))
ax.set_xlim(0, 10)
ax.set_ylim(0, 5)
ax.axis('off')

# Boxes
box_style = dict(boxstyle='round,pad=0.5', facecolor='#e8f4fd', edgecolor='#1f77b4', linewidth=2)
highlight_style = dict(boxstyle='round,pad=0.5', facecolor='#fff3cd', edgecolor='#ff7f0e', linewidth=2)
result_style = dict(boxstyle='round,pad=0.5', facecolor='#d4edda', edgecolor='#28a745', linewidth=2)

# Prior
ax.text(1.5, 3.5, 'Prior\nP(H) = 0.001', ha='center', va='center',
        fontsize=11, fontweight='bold', bbox=box_style)

# Likelihood
ax.text(1.5, 1.5, 'Likelihood\nP(E|H) = 0.99', ha='center', va='center',
        fontsize=11, fontweight='bold', bbox=box_style)

# Evidence / Marginal
ax.text(5, 2.5, 'Evidence\nP(E) = 0.021', ha='center', va='center',
        fontsize=11, fontweight='bold', bbox=highlight_style)

# Posterior
ax.text(8.5, 2.5, 'Posterior\nP(H|E) = 0.047', ha='center', va='center',
        fontsize=12, fontweight='bold', bbox=result_style)

# Arrows
arrow_props = dict(arrowstyle='->', color='#555555', lw=2)
ax.annotate('', xy=(3.8, 2.8), xytext=(2.7, 3.3), arrowprops=arrow_props)
ax.annotate('', xy=(3.8, 2.2), xytext=(2.7, 1.7), arrowprops=arrow_props)
ax.annotate('', xy=(7.0, 2.5), xytext=(6.2, 2.5), arrowprops=arrow_props)

# Multiply symbol
ax.text(3.3, 2.5, '×', ha='center', va='center', fontsize=16, fontweight='bold', color='#555')

# Divide symbol
ax.text(6.6, 2.5, '÷', ha='center', va='center', fontsize=16, fontweight='bold', color='#555')

# Formula at bottom
ax.text(5, 0.5, r'$P(H|E) = \frac{P(E|H) \cdot P(H)}{P(E)}$',
        ha='center', va='center', fontsize=13, style='italic', color='#333')

plt.tight_layout()
plt.savefig('figure_005_bayes_flow.png', dpi=150, bbox_inches='tight',
            facecolor='white')
print("OK: figure_005_bayes_flow.png")
