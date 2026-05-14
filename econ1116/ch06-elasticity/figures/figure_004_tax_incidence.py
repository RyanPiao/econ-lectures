"""Tax incidence diagram: tax wedge with burden split based on relative elasticities."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, axes = plt.subplots(1, 2, figsize=(6, 4))

def draw_tax_diagram(ax, title, d_slope, s_slope, tax=1.5):
    """Draw S&D with tax wedge."""
    q = np.linspace(0, 10, 200)

    # Supply: P = s_slope * Q + 1
    p_s = s_slope * q + 1
    # Demand: P = -d_slope * Q + 7
    p_d = -d_slope * q + 7

    # Find equilibrium without tax
    q_eq = (7 - 1) / (d_slope + s_slope)
    p_eq = -d_slope * q_eq + 7

    # With tax: S shifts up by tax amount
    p_s_tax = s_slope * q + 1 + tax
    # New equilibrium
    q_tax = (7 - 1 - tax) / (d_slope + s_slope)
    p_buyer = -d_slope * q_tax + 7
    p_seller = p_buyer - tax

    ax.plot(q, p_d, color='#2196F3', linewidth=2, label='Demand')
    ax.plot(q, p_s, color='#e74c3c', linewidth=2, label='Supply')
    ax.plot(q, p_s_tax, color='#e74c3c', linewidth=1.5, linestyle='--', alpha=0.6, label='Supply + Tax')

    # Tax wedge
    ax.plot([q_tax, q_tax], [p_seller, p_buyer], color='#333', linewidth=3, alpha=0.8)

    # Buyer burden (shaded)
    buyer_burden = p_buyer - p_eq
    seller_burden = p_eq - p_seller

    ax.fill_between([q_tax - 0.3, q_tax + 0.3], p_eq, p_buyer,
                    color='#2196F3', alpha=0.3)
    ax.fill_between([q_tax - 0.3, q_tax + 0.3], p_seller, p_eq,
                    color='#e74c3c', alpha=0.3)

    # Labels
    buyer_pct = buyer_burden / tax * 100
    seller_pct = seller_burden / tax * 100

    ax.annotate(f'Buyer pays\n{buyer_pct:.0f}%', xy=(q_tax + 0.5, (p_buyer + p_eq)/2),
                fontsize=7, color='#1565c0', weight='bold')
    ax.annotate(f'Seller pays\n{seller_pct:.0f}%', xy=(q_tax + 0.5, (p_seller + p_eq)/2),
                fontsize=7, color='#c62828', weight='bold')

    ax.set_title(title, fontsize=9, weight='bold')
    ax.set_xlabel('Quantity', fontsize=8)
    ax.set_ylabel('Price ($)', fontsize=8)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(fontsize=6, loc='upper right')

# Panel 1: Inelastic demand (cigarettes) — buyer bears most
draw_tax_diagram(axes[0], 'Inelastic Demand\n(Cigarettes)', d_slope=1.8, s_slope=0.5, tax=1.5)

# Panel 2: Elastic demand (soda) — more evenly split
draw_tax_diagram(axes[1], 'Elastic Demand\n(Soda)', d_slope=0.5, s_slope=0.8, tax=1.5)

plt.tight_layout()
plt.savefig('figures/figure_004_tax_incidence.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_004_tax_incidence.png")
