"""Ch 11 — Monopoly & Price Discrimination: all custom analytical figures.

One consolidated script (mirrors ch10's render_ch10_figures.py). White background,
White-Academia deck palette. Everything is anchored to the textbook's remote-island
airline so the deck, the table (Table 11.1), and every figure agree:

    Demand:  P = 380 - 3.6 Q          (through the table's (Q,P) points)
    MC    :  $56  (constant marginal cost per passenger)
    ATC   :  2000/Q + 56              (FC = $2,000, VC = 56 Q)
    Monopoly  : Q* = 50,  P* = $200,  profit = $5,200   (table, 10-seat batches)
    Competitive: Q  = 90,  P  = $56                      (P = MC)

Figures:
  fig-monopoly-airline  — D, the MR ledger (from the table), MC; MR = MC at Q = 50
  fig-five-step         — the canonical smooth diagram + profit rectangle (5 steps)
  fig-dwl-monopoly      — competition vs monopoly: CS, the transfer, and DWL
  fig-hhi               — two industries, same CR4 = 85%, very different HHI
  fig-lerner            — the Lerner Index markup spectrum (appendix)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ---- White-Academia deck palette (shared with ch09 / ch10) ----
NAVY='#0a2e5c'; CYAN='#0891b2'; AMBER='#d97706'; GREEN='#16a34a'
SAGE='#6A8E6B'; GOLD='#f59e0b'; GREY='#9ca3af'; ORANGE='#e07a4f'
INK='#1a1a1a'; RED='#b91c1c'; BLUE='#2563eb'; TERRA='#C47B5A'; PLUM='#7C3A5F'
plt.rcParams.update({'font.size': 12, 'axes.titlesize': 13, 'figure.facecolor': 'white'})
# Render every literal "$" as a real dollar sign — never let matplotlib treat
# "$200 ... $56" as a math-mode span (the run-together-italics bug). No mathtext
# is used in this file, so we just turn parsing off globally.
plt.rcParams['text.parse_math'] = False

# ---- shared airline economics ----
def D(q):  return 380.0 - 3.6*q          # inverse demand
def MR(q): return 380.0 - 7.2*q          # smooth MR: same intercept, twice the slope
def ATC(q): return 2000.0/q + 56.0
MCv = 56.0

def style(ax, xl, yl, t):
    ax.set_xlabel(xl, fontsize=12)
    ax.set_ylabel(yl, fontsize=12)
    ax.set_title(t, fontsize=13, weight='bold', pad=8)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.16)


# ======================================================================
# FIG 1 — The monopoly airline: demand, the MR ledger, and MC
#         Faithful to Table 11.1 (10-seat batches): MR = MC = $56 at Q = 50.
# ======================================================================
def fig_airline():
    fig, ax = plt.subplots(figsize=(10.6, 6.0))
    q = np.linspace(0, 100, 300)
    ax.plot(q, D(q), color=NAVY, lw=2.8, label='Demand  (P)', zorder=5)

    # the MR ledger straight from the table's MR column
    qd  = np.array([20, 30, 40, 50, 60, 70, 80, 90, 100])
    mrd = np.array([272, 200, 128, 56, -16, -88, -160, -232, -304])
    ax.plot(qd, mrd, color=ORANGE, lw=2.2, ls='--', marker='D', ms=7,
            markeredgecolor='white', markeredgewidth=1.2,
            label='Marginal revenue  (from the table)', zorder=6)

    ax.axhline(MCv, color=GREEN, lw=2.6, label='MC = $56', zorder=4)
    ax.axhline(0, color='#cbd5e1', lw=1.0, zorder=1)

    # optimum: MR ledger meets MC at Q = 50
    ax.plot([50, 50], [0, 200], color=GREY, ls=':', lw=1.3, zorder=2)
    ax.plot([50], [56],  '*', color=GOLD, ms=24, markeredgecolor=INK,
            markeredgewidth=1.0, zorder=9)
    ax.plot([50], [200], 'o', color=NAVY, ms=12, markeredgecolor='white',
            markeredgewidth=1.7, zorder=9)
    ax.plot([0, 50], [200, 200], color=GREY, ls=':', lw=1.1, zorder=2)

    # the MR < P gap, made visible
    ax.annotate('', xy=(50, 196), xytext=(50, 60),
                arrowprops=dict(arrowstyle='<->', color=PLUM, lw=1.8))
    ax.text(53.5, 128, 'P = $200\nbut MR = $56\n→  MR < P', fontsize=11,
            color=PLUM, weight='bold', va='center')

    ax.text(50, 214, 'P* = $200', fontsize=12, color=NAVY, weight='bold', ha='center')
    ax.text(78, 70, 'MR = MC = $56\nat  Q* = 50', fontsize=11.5, color=GREEN,
            weight='bold', ha='center')

    ax.set_xlim(0, 100); ax.set_ylim(-120, 400)
    ax.set_xticks([20, 40, 50, 60, 80, 100])
    ax.set_yticks([0, 56, 100, 200, 300, 380])
    ax.set_yticklabels(['0', '$56', '$100', '$200', '$300', '$380'])
    ax.legend(loc='upper right', fontsize=10.5, frameon=True)
    style(ax, 'Quantity — seats sold', 'Price / revenue per seat',
          'The Monopoly Airline — to sell more, it must cut the price for everyone')
    fig.text(0.5, -0.02,
             'Each new batch of seats adds revenue (quantity effect) but lowers the price on all earlier seats '
             '(price effect) — so MR falls below P at every step.',
             ha='center', fontsize=9.5, color='#555', style='italic')
    plt.tight_layout()
    plt.savefig('fig-monopoly-airline.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print('saved fig-monopoly-airline.png')


# ======================================================================
# FIG 2 — The five-step method: the canonical smooth monopoly diagram.
#         Smooth MR (twice the slope) meets MC at Q ~ 45, P = $218.
# ======================================================================
def fig_five_step():
    fig, ax = plt.subplots(figsize=(10.6, 6.0))
    q = np.linspace(1, 100, 400)
    ax.plot(q, D(q),  color=NAVY,  lw=2.8, label='Demand (D)', zorder=5)
    ax.plot(q, MR(q), color=ORANGE, lw=2.4, ls='--', label='MR (twice the slope)', zorder=5)
    ax.axhline(MCv, color=GREEN, lw=2.6, label='MC = $56', zorder=4)
    qq = np.linspace(8, 100, 400)
    ax.plot(qq, ATC(qq), color=PLUM, lw=2.4, label='ATC', zorder=4)

    qs, ps, atc = 45.0, D(45.0), ATC(45.0)          # 45, $218, $100.4
    # profit rectangle (P - ATC) x Q*
    ax.fill_between([0, qs], atc, ps, color=GREEN, alpha=0.16, zorder=2)
    ax.text(qs/2, (ps+atc)/2, 'Profit\n≈ $5,290', fontsize=12.5, weight='bold',
            color='#0f5132', ha='center', va='center')

    # guides + markers
    ax.plot([qs, qs], [0, ps], color=GREY, ls=':', lw=1.2, zorder=1)
    ax.plot([0, qs], [ps, ps], color=GREY, ls=':', lw=1.1, zorder=1)
    ax.plot([0, qs], [atc, atc], color=GREY, ls=':', lw=1.1, zorder=1)
    ax.plot([qs], [MCv], '*', color=GOLD, ms=24, markeredgecolor=INK, markeredgewidth=1.0, zorder=9)
    ax.plot([qs], [ps],  'o', color=NAVY, ms=12, markeredgecolor='white', markeredgewidth=1.7, zorder=9)
    ax.plot([qs], [atc], 'o', color=PLUM, ms=10, markeredgecolor='white', markeredgewidth=1.5, zorder=9)

    # the five numbered steps
    ax.annotate('① MR = MC', xy=(qs, MCv), xytext=(60, 120),
                fontsize=11, color=GREEN, weight='bold',
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.6))
    ax.annotate('② read Q*', xy=(qs, 0), xytext=(qs+4, 28),
                fontsize=11, color=INK, weight='bold')
    ax.annotate('③ read P* off D', xy=(qs, ps), xytext=(58, 300),
                fontsize=11, color=NAVY, weight='bold',
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.6))
    ax.annotate('④ read ATC*', xy=(qs, atc), xytext=(60, 60),
                fontsize=11, color=PLUM, weight='bold',
                arrowprops=dict(arrowstyle='->', color=PLUM, lw=1.6))
    ax.text(8, 250, '⑤ Profit = (P* − ATC*) × Q*', fontsize=11, color='#0f5132', weight='bold')

    ax.set_xlim(0, 100); ax.set_ylim(0, 400)
    ax.set_xticks([45, 90]); ax.set_xticklabels(['Q*≈45', '90'])
    ax.set_yticks([56, atc, ps, 380]); ax.set_yticklabels(['MC $56', 'ATC ≈$100', 'P* $218', '$380'])
    ax.legend(loc='upper right', fontsize=10.5, frameon=True)
    style(ax, 'Quantity', 'Price / cost',
          'The Five-Step Method — find Q* where MR = MC, then read P* off demand')
    fig.text(0.5, -0.02,
             'Smooth curves land at Q* ≈ 45, P* = $218. Real planes come in 10-seat batches, '
             'so Table 11.1 rounds to Q = 50, P = $200 — same logic.',
             ha='center', fontsize=9.5, color='#555', style='italic')
    plt.tight_layout()
    plt.savefig('fig-five-step.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print('saved fig-five-step.png')


# ======================================================================
# FIG 3 — Welfare cost of monopoly: CS, the transfer, and DWL.
#         Competition: Q=90, P=$56.  Monopoly: Q=50, P=$200.
# ======================================================================
def fig_dwl():
    fig, ax = plt.subplots(figsize=(10.6, 6.0))
    q = np.linspace(0, 100, 300)
    ax.plot(q, D(q), color=NAVY, lw=2.8, label='Demand', zorder=6)
    ax.axhline(MCv, color=GREEN, lw=2.6, label='MC = Supply ($56)', zorder=5)

    Qm, Pm, Qc, Pc = 50.0, 200.0, 90.0, 56.0

    # consumer surplus that REMAINS under monopoly (above $200, up to demand)
    xs = np.linspace(0, Qm, 50)
    ax.fill_between(xs, Pm, D(xs), color=CYAN, alpha=0.22, zorder=2)
    ax.text(17, 300, 'Consumer\nsurplus', fontsize=11, color='#0e6b86', weight='bold', ha='center')

    # transfer: consumer surplus turned into producer surplus (the rectangle)
    ax.fill_between([0, Qm], Pc, Pm, color=ORANGE, alpha=0.20, zorder=2)
    ax.text(25, 128, 'Transfer  →  producer\n(was consumer surplus)', fontsize=10.5,
            color='#9a4a25', weight='bold', ha='center')

    # deadweight loss triangle (demand to MC, Qm..Qc)
    xd = np.linspace(Qm, Qc, 50)
    ax.fill_between(xd, MCv, D(xd), color=RED, alpha=0.22, hatch='///',
                    edgecolor=RED, linewidth=0.0, zorder=3)
    ax.annotate('Deadweight\nloss = $2,880', xy=(63, 100), xytext=(83, 230),
                fontsize=11, color=RED, weight='bold', ha='center',
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.7))

    # the two outcomes
    for (qx, px, col, lab) in [(Qm, Pm, NAVY, 'Monopoly'), (Qc, Pc, GREEN, 'Competition')]:
        ax.plot([qx, qx], [0, px], color=GREY, ls=':', lw=1.2, zorder=1)
        ax.plot([qx], [px], 'o', color=col, ms=12, markeredgecolor='white', markeredgewidth=1.7, zorder=9)
    ax.text(Qm, 214, 'Monopoly:  Q=50, P=$200', fontsize=11, color=NAVY, weight='bold', ha='center')
    ax.text(Qc+1, 70, 'Competition:\nQ=90, P=$56', fontsize=10.5, color='#0f5132', weight='bold', ha='left')

    ax.annotate('', xy=(52, 20), xytext=(88, 20),
                arrowprops=dict(arrowstyle='<->', color=GREY, lw=1.6))
    ax.text(70, 30, '40 trips never happen', fontsize=10, color='#555', ha='center', style='italic')

    ax.set_xlim(0, 100); ax.set_ylim(0, 400)
    ax.set_xticks([50, 90]); ax.set_xticklabels(['50  (monopoly)', '90  (competition)'])
    ax.set_yticks([56, 200, 380]); ax.set_yticklabels(['$56', '$200', '$380'])
    ax.legend(loc='upper right', fontsize=10.5, frameon=True)
    style(ax, 'Quantity — seats', 'Price',
          'The Welfare Cost of Monopoly — restricting output destroys mutually beneficial trades')
    plt.tight_layout()
    plt.savefig('fig-dwl-monopoly.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print('saved fig-dwl-monopoly.png')


# ======================================================================
# FIG 4 — CR4 hides what HHI reveals: two industries, same CR4 = 85%.
# ======================================================================
def fig_hhi():
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(12.4, 5.6), sharey=True)
    labels = ['Firm 1', 'Firm 2', 'Firm 3', 'Firm 4', 'Others']
    ind1 = [65, 10, 5, 5, 15]
    ind2 = [25, 20, 20, 20, 15]
    cols = [NAVY, CYAN, SAGE, AMBER, GREY]

    for ax, shares, title, hhi, tag in [
            (axA, ind1, 'Industry 1 — one dominant firm', 4600, 'Highly concentrated'),
            (axB, ind2, 'Industry 2 — four near-equals',  2050, 'Moderately concentrated')]:
        bars = ax.bar(labels, shares, color=cols, edgecolor='white', width=0.72, zorder=3)
        for b, s in zip(bars, shares):
            ax.text(b.get_x()+b.get_width()/2, s+1.5, f'{s}%', ha='center',
                    fontsize=11, weight='bold', color=INK)
        ax.set_ylim(0, 75)
        ax.set_title(title, fontsize=12.5, weight='bold', pad=8)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
        ax.grid(True, axis='y', alpha=0.16)
        boxcol = RED if hhi > 2500 else AMBER
        ax.text(0.5, 0.86, f'CR4 = 85%\nHHI = {hhi:,}\n{tag}',
                transform=ax.transAxes, ha='center', va='top', fontsize=12, weight='bold',
                color='white', bbox=dict(boxstyle='round,pad=0.5', facecolor=boxcol, alpha=0.92))
    axA.set_ylabel('Market share (%)', fontsize=12)
    fig.suptitle('Same CR4, different worlds — squaring the shares makes the leader visible',
                 fontsize=13.5, weight='bold', y=1.0)
    fig.text(0.5, -0.02,
             'CR4 just sums the top four shares (85% in both). HHI squares every share, so Industry 1’s '
             '65% giant (65² = 4,225) dwarfs Industry 2’s spread-out four.',
             ha='center', fontsize=9.5, color='#555', style='italic')
    plt.tight_layout()
    plt.savefig('fig-hhi.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print('saved fig-hhi.png')


# ======================================================================
# FIG 5 — The Lerner Index markup spectrum (appendix).
# ======================================================================
def fig_lerner():
    fig, ax = plt.subplots(figsize=(10.6, 5.2))
    names = ['Perfect\ncompetition', 'Airline\n(P=$200, MC=$56)',
             'Ozempic generic\n(India, $14)', 'Ozempic\n(US, $969)']
    L = [0.0, (200-56)/200, (14-5)/14, (969-5)/969]   # 0, 0.72, 0.643, 0.995
    cols = [SAGE, CYAN, AMBER, RED]
    bars = ax.barh(names, L, color=cols, edgecolor='white', height=0.62, zorder=3)
    for b, v in zip(bars, L):
        ax.text(v+0.012, b.get_y()+b.get_height()/2, f'L = {v:.3f}',
                va='center', fontsize=12, weight='bold', color=INK)
    ax.axvline(0, color='#cbd5e1', lw=1.0)
    ax.set_xlim(0, 1.12)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_title('The Lerner Index:  L = (P − MC) / P  — how much of the price is pure markup',
                 fontsize=12.5, weight='bold', pad=10)
    ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
    ax.grid(True, axis='x', alpha=0.16)
    ax.set_xlabel('Lerner Index    (0 = price-taker, P = MC      →      1 = total market power)', fontsize=11)
    fig.text(0.5, -0.04, 'Identity:  L = 1 / |elasticity|.  Inelastic demand → bigger markup. '
             'Patent protection is what separates the $969 US market from the $14 Indian one.',
             ha='center', fontsize=9.5, color='#555', style='italic')
    plt.tight_layout()
    plt.savefig('fig-lerner.png', dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print('saved fig-lerner.png')


if __name__ == '__main__':
    fig_airline()
    fig_five_step()
    fig_dwl()
    fig_hhi()
    fig_lerner()
    print('--- all ch11 figures rendered ---')
