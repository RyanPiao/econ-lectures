"""Ch 11 — Monopoly is NOT guaranteed profit: same airline, two seasons.
Identical cost curves in both panels (TC = 0.05Q^3 - 5.2Q^2 + 201Q + 1500),
tuned so MC = $56 at Q = 50 — matching the airline TABLE (MR = MC = $56).
  GOOD season (high demand): MR=MC at Q*=50, P*=$200 > ATC=$96  -> PROFIT $5,200
  STORM season (collapsed demand): MR=MC at Q*=30, P*=$80 < ATC=$140 -> LOSS $1,800
The storm's high ATC is honest: flying only ~30 seats spreads the fixed cost thin.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RED='#dc2626'; ORANGE='#e0742f'; BLUE='#2563eb'; GREEN='#16a34a'; INK='#1a1a1a'
CYAN='#35a7d4'; AMBER='#f2a93b'
plt.rcParams.update({'font.size': 12, 'figure.facecolor': 'white'})
plt.rcParams['text.parse_math'] = False

def MC(Q):  return 0.15*Q**2 - 10.4*Q + 201
def ATC(Q): return 0.05*Q**2 - 5.2*Q + 201 + 1500/Q

def panel(fname, dA, dB, Qs, Ps, As, mrmc, box_color, box_label, q_lab):
    """dA,dB: demand intercept/slope  (P = dA - dB*Q);  MR = dA - 2*dB*Q."""
    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    Q  = np.linspace(2, 74, 400)
    Qc = np.linspace(9, 74, 400)
    ax.plot(Q, dA - dB*Q,   color=RED,    lw=2.6, zorder=5)
    ax.plot(Q, dA - 2*dB*Q, color=ORANGE, lw=2.4, zorder=4)
    ax.plot(Qc, MC(Qc),     color=BLUE,   lw=2.6, zorder=5)
    ax.plot(Qc, ATC(Qc),    color=GREEN,  lw=2.6, zorder=5)

    # profit / loss rectangle (P* to ATC over 0..Q*)
    lo, hi = sorted((Ps, As))
    ax.add_patch(plt.Rectangle((0, lo), Qs, hi-lo, facecolor=box_color, alpha=0.85, zorder=3))
    ax.text(Qs/2, (lo+hi)/2, box_label, ha='center', va='center', fontsize=13,
            weight='bold', color='white', zorder=6)

    ax.plot([Qs, Qs], [0, max(Ps, As)], color='#888', ls=':', lw=1.2, zorder=2)
    for (yy, col) in [(Ps, RED), (As, GREEN), (mrmc, INK)]:
        ax.plot([Qs], [yy], 'o', color='black', ms=8, zorder=8)
    # axis value labels
    ax.set_yticks(sorted([Ps, As])); ax.set_yticklabels(['$'+str(int(min(Ps,As))), '$'+str(int(max(Ps,As)))])
    ax.set_xticks([Qs]); ax.set_xticklabels([q_lab])

    # curve labels near right end
    ax.text(74, dA-dB*74-4, 'D', color=RED, fontsize=14, weight='bold', style='italic', ha='left', va='top')
    ax.annotate('MR', xy=(0,0), xytext=(max(2,(dA/(2*dB))*0.62), 6), color=ORANGE, fontsize=13, weight='bold', style='italic')
    ax.text(70, MC(70)-2, 'MC', color=BLUE, fontsize=14, weight='bold', style='italic', ha='right', va='bottom')
    ax.text(72, ATC(72)+4, 'ATC', color=GREEN, fontsize=14, weight='bold', style='italic', ha='right', va='bottom')

    ax.set_xlim(0, 80); ax.set_ylim(0, 355)
    ax.set_xlabel('Q (passengers)', fontsize=12); ax.set_ylabel('P', fontsize=13, rotation=0, labelpad=12)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.tick_params(labelsize=12)
    plt.tight_layout()
    plt.savefig(fname, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(); print('saved', fname)

# GOOD season — high demand -> profit.   D = 344 - 2.88Q  (Q*=50, P*=200, ATC=96, MR=MC=56)
panel('fig-airline-profit.png', 344, 2.88, 50, 200, 96, 56, CYAN, 'PROFIT', '50')
# STORM season — demand collapses -> few fly -> ATC soars.  D = 136 - 1.867Q (Q*=30, P*=80, ATC=140, MR=MC=24)
panel('fig-airline-loss.png', 136, 1.867, 30, 80, 140, 24, AMBER, 'LOSS', '30')
print('--- profit-vs-loss panels done ---')
