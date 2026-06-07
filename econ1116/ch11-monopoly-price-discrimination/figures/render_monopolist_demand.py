"""Ch 11 — simple "Monopolist's Demand Curve" intro figure (recreates the user's screenshot in our palette).
A single downward-sloping demand line; market demand = firm's demand; marked at $200 / Q=50 (the airline)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
NAVY='#0a2e5c'; GOLD='#f59e0b'; INK='#1a1a1a'; GREY='#9ca3af'
plt.rcParams['text.parse_math'] = False

fig, ax = plt.subplots(figsize=(8.4, 6.0))
# demand line: P = 300 - 2Q  → passes through (50, 200)
qx = [12, 96]; py = [276, 108]
ax.plot(qx, py, color=NAVY, lw=3.2, zorder=5)
ax.text(98, 104, 'D', fontsize=20, weight='bold', color=NAVY, va='center')

# mark $200 at Q = 50
ax.plot([50, 50], [0, 200], color=GREY, ls=':', lw=1.6, zorder=2)
ax.plot([0, 50], [200, 200], color=GREY, ls=':', lw=1.6, zorder=2)

ax.set_xlim(0, 108); ax.set_ylim(0, 300)
ax.set_xticks([50]); ax.set_xticklabels(['50'], fontsize=15)
ax.set_yticks([200]); ax.set_yticklabels(['$200'], fontsize=15)
ax.set_xlabel('Q', fontsize=18, weight='bold', loc='right')
ax.set_ylabel('P', fontsize=18, weight='bold', rotation=0, loc='top', labelpad=10)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.6); ax.spines['bottom'].set_linewidth(1.6)
plt.tight_layout()
plt.savefig('fig-monopolist-demand.png', dpi=150, bbox_inches='tight', facecolor='white')
print('saved fig-monopolist-demand.png')
