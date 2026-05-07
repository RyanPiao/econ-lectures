"""Figure 5: Propensity score overlap — treated vs control distributions."""
import numpy as np
import matplotlib.pyplot as plt

# Simulate propensity scores for illustration
rng = np.random.default_rng(42)
n = 5000
ps_control = np.clip(rng.beta(2, 5, n), 0.02, 0.98)
ps_treated = np.clip(rng.beta(5, 3, n), 0.02, 0.98)

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.hist(ps_control, bins=50, alpha=0.6, label='Control (D=0)', color='#3498db', density=True)
ax.hist(ps_treated, bins=50, alpha=0.6, label='Treated (D=1)', color='#e74c3c', density=True)

# Shade overlap region
ax.axvspan(0.15, 0.85, alpha=0.08, color='#2ecc71', label='Good overlap region')

# Danger zones
ax.axvspan(0, 0.05, alpha=0.15, color='#e74c3c')
ax.axvspan(0.95, 1.0, alpha=0.15, color='#e74c3c')
ax.text(0.025, ax.get_ylim()[1]*0.85, 'Danger\nzone', fontsize=8, color='#e74c3c',
        ha='center', fontweight='bold')
ax.text(0.975, ax.get_ylim()[1]*0.85, 'Danger\nzone', fontsize=8, color='#e74c3c',
        ha='center', fontweight='bold')

ax.set_xlabel('Estimated Propensity Score P(D=1|X)', fontsize=12)
ax.set_ylabel('Density', fontsize=12)
ax.legend(fontsize=10)
ax.set_xlim(0, 1)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figures/figure_005_overlap_propensity.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('OK: figure_005_overlap_propensity.png')
