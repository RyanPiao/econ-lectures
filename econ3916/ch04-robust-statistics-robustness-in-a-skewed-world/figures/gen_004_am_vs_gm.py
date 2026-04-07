"""Generate AM vs GM visualization: zigzag vs smooth compound path."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4.5))

# Panel 1: The +100%/-50% trap
years = [0, 1, 2]
values = [100, 200, 100]
am_path = [100, 100 * 1.25, 100 * 1.25**2]

ax1.plot(years, values, 'o-', color='#e74c3c', linewidth=2.5, markersize=8, label='Actual ($100)')
ax1.plot(years, am_path, 's--', color='#95a5a6', linewidth=2, markersize=6, label='AM implies ($156)')
ax1.axhline(100, color='#2ecc71', linestyle=':', alpha=0.5, linewidth=1.5)

ax1.set_xlabel('Year', fontsize=10)
ax1.set_ylabel('Portfolio Value ($)', fontsize=10)
ax1.set_xticks([0, 1, 2])
ax1.legend(fontsize=8, frameon=True, loc='upper left')
ax1.set_ylim(50, 220)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.set_title('+100% then -50%', fontsize=11, fontweight='bold')

# Annotations
ax1.annotate('AM = +25%\nGM = 0%', xy=(1.5, 130), fontsize=9,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fff3e0', edgecolor='#e67e22'))

# Panel 2: S&P 500 20-year compounding
years_sp = np.arange(0, 21)
am_rate = 0.119
gm_rate = 0.104
am_growth = 10000 * (1 + am_rate) ** years_sp
gm_growth = 10000 * (1 + gm_rate) ** years_sp

ax2.plot(years_sp, am_growth / 1000, '-', color='#95a5a6', linewidth=2.5, label=f'AM (11.9%): ${am_growth[-1]/1000:.0f}K')
ax2.plot(years_sp, gm_growth / 1000, '-', color='#2ecc71', linewidth=2.5, label=f'GM (10.4%): ${gm_growth[-1]/1000:.0f}K')
ax2.fill_between(years_sp, am_growth/1000, gm_growth/1000, alpha=0.15, color='#e74c3c')

# Gap annotation
gap = (am_growth[-1] - gm_growth[-1])
ax2.annotate(f'Gap: ${gap/1000:.1f}K\n(variance drag)',
            xy=(15, (am_growth[15]+gm_growth[15])/2000), fontsize=8,
            color='#e74c3c',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#fce4ec', edgecolor='#e74c3c', alpha=0.8))

ax2.set_xlabel('Year', fontsize=10)
ax2.set_ylabel('Portfolio Value ($K)', fontsize=10)
ax2.legend(fontsize=8, frameon=True, loc='upper left')
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.set_title('S&P 500 (20yr)', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/figure_004_am-vs-gm.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print("OK: figure_004_am-vs-gm.png")
