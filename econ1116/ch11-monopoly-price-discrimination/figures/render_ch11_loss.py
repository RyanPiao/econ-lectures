"""Ch 11 — 'Monopoly is not a guarantee of profit' loss diagram (our style).
Demand lies BELOW ATC at every quantity, so the profit-max point (MR=MC) reads a
price P* < ATC -> the monopolist's best outcome is still a loss.
  D = 100 - Q ;  MR = 100 - 2Q ;  MC = AVC = 20 ;  ATC = 2000/Q + 20
  MR=MC at Q*=40 -> P*=$60 (on D), ATC=$70 -> Loss = (70-60)*40 = $400.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

NAVY='#0a2e5c'; BLUE='#2563eb'; GREEN='#16a34a'; RED='#b91c1c'; AMBER='#d97706'; INK='#1a1a1a'
plt.rcParams.update({'font.size': 12, 'figure.facecolor': 'white'})
plt.rcParams['text.parse_math'] = False

fig, ax = plt.subplots(figsize=(8.4, 6.0))
Q = np.linspace(0, 100, 400)
ax.plot(Q, 100 - Q, color=NAVY, lw=2.6, label='Demand (D)', zorder=5)
Qm = np.linspace(0, 50, 200)
ax.plot(Qm, 100 - 2*Qm, color=AMBER, lw=2.2, ls='--', label='MR', zorder=4)
ax.axhline(20, color=GREEN, lw=2.2, label='MC = AVC', zorder=3)
Qa = np.linspace(21, 100, 400)
ax.plot(Qa, 2000/Qa + 20, color=BLUE, lw=2.4, label='ATC', zorder=5)

Qs, Ps, As = 40, 60, 70
ax.add_patch(plt.Rectangle((0, Ps), Qs, As - Ps, facecolor=RED, alpha=0.20, zorder=1))
for yy in (Ps, As):
    ax.plot([0, Qs], [yy, yy], color='#888', ls=':', lw=1.1, zorder=2)
ax.plot([Qs, Qs], [0, As], color='#888', ls=':', lw=1.1, zorder=2)
ax.plot([Qs], [20], 'o', color=GREEN, mec='white', mew=1, ms=9, zorder=8)
ax.plot([Qs], [Ps], 'o', color=NAVY, mec='white', mew=1, ms=9, zorder=8)
ax.plot([Qs], [As], 'o', color=BLUE, mec='white', mew=1, ms=9, zorder=8)

ax.annotate('MR = MC\n→ Q* = 40', xy=(40, 20), xytext=(53, 31), fontsize=11, color=INK,
            ha='left', arrowprops=dict(arrowstyle='->', color='#666', lw=1.3))
ax.text(Qs/2, (Ps + As)/2, 'Loss = $400', ha='center', va='center', fontsize=12.5,
        weight='bold', color=RED, zorder=9)

ax.set_yticks([20, 60, 70]); ax.set_yticklabels(['$20 = MC', '$60 = P*', '$70 = ATC'])
ax.set_xticks([40]); ax.set_xticklabels(['Q* = 40'])
ax.set_xlim(0, 100); ax.set_ylim(0, 116)
ax.set_xlabel('Quantity', fontsize=12); ax.set_ylabel('Price / cost', fontsize=12)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.set_title('Demand below ATC everywhere → even a monopolist loses money',
             fontsize=13, weight='bold', pad=10)
ax.legend(loc='upper right', fontsize=10.5, frameon=True)
plt.tight_layout()
plt.savefig('fig-monopoly-loss.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print('saved fig-monopoly-loss.png')
