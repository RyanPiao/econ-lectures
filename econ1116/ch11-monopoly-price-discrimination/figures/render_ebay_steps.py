"""Ch 11 — eBay producer-surplus staircase, rendered in THREE aligned layers so the green
PS bars sit INSCRIBED under a straight demand line (each bar's top-right corner touches D,
with a small blue sliver above — exactly like the ebay_pd.png reference).

  Layer 1  ebay-base.png   : axes, title, Pt/Pc labels            (opaque, always visible, BOTTOM)
  Layer 2  ebay-ps-{i}.png : one green PS bar + blue sliver + label (transparent, reveal fragments)
  Layer 3  ebay-top.png    : demand D, MR, MC=ATC lines + labels   (transparent, always visible, TOP)

All three use the SAME fixed canvas (add_axes + identical xlim/ylim + savefig WITHOUT
bbox_inches='tight') so they overlay pixel-aligned when stacked as <img> layers.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

RED='#dc2626'; ORANGE='#e0742f'; MCLINE='#6f8f3f'; PSG='#1e9e4a'; BLUE='#5b9bd5'; INK='#1a1a1a'
plt.rcParams.update({'figure.facecolor':'white'})
plt.rcParams['text.parse_math'] = False          # PS labels contain literal "$" — keep math off

WTP = [39, 38, 35, 31, 30, 22]                    # bid labels (annotations on each bar)
MC  = 13
PT  = 43.0                                         # demand y-intercept (choke price)
QC  = 7.0                                          # demand hits MC=ATC here (point b)
m   = (PT - MC) / QC                               # slope magnitude (~4.29)
def D(q): return PT - m * q                        # straight demand line
FIG = (6.6, 5.9)

def new_ax():
    fig = plt.figure(figsize=FIG)
    ax = fig.add_axes([0.10, 0.10, 0.86, 0.86])
    ax.set_xlim(0, 10); ax.set_ylim(0, 46); ax.axis('off')
    return fig, ax

# ---- Layer 1: base (axes, title, Pt/Pc) ----
fig, ax = new_ax()
ax.plot([0, 0],   [0, 46], color=INK, lw=1.6)      # y-axis
ax.plot([0, 9.6], [0, 0],  color=INK, lw=1.6)      # x-axis
ax.text(-0.12, PT, 'Pᴛ', ha='right', va='center', fontsize=13, color=INK)
ax.text(-0.12, MC, 'Pc', ha='right', va='center', fontsize=13, color=INK)
ax.set_title('Producer surplus: each bidder’s max WTP, captured one by one',
             fontsize=12, weight='bold', pad=6)
fig.savefig('ebay-base.png', dpi=150, facecolor='white')
plt.close(fig); print('saved ebay-base.png')

# ---- Layer 2: 6 transparent overlays — one inscribed green bar + blue sliver each ----
for i in range(6):
    fig, ax = new_ax()
    h = D(i + 1)                                   # bar top = demand at the bar's RIGHT edge (on the line)
    # blue sliver above the bar: (i,h)-(i,D(i))-(i+1,h)  (hypotenuse rides the demand line)
    ax.add_patch(Polygon([(i, h), (i, D(i)), (i + 1, h)], facecolor=BLUE, alpha=0.55,
                         edgecolor='none', zorder=2))
    # green PS bar, MC up to the demand line
    ax.add_patch(Rectangle((i, MC), 1, h - MC, facecolor=PSG, edgecolor='white', lw=1.2, zorder=3))
    ax.text(i + 0.5, MC + (h - MC) * 0.36, f'PS\n${WTP[i]}', ha='center', va='center',
            fontsize=10.5, weight='bold', color='white', zorder=4)
    fig.savefig(f'ebay-ps-{i}.png', dpi=150, transparent=True)
    plt.close(fig); print(f'saved ebay-ps-{i}.png')

# ---- Layer 3: top (demand, MR, MC) drawn OVER the bars ----
fig, ax = new_ax()
ax.plot([0, 8], [D(0), D(8)], color=RED, lw=3, zorder=6)           # Demand (straight)
ax.text(8.1, D(8) - 0.6, 'D', color=RED, fontsize=16, style='italic', weight='bold', va='top')
ax.plot([0, 5], [PT, PT - 2 * m * 5], color=ORANGE, lw=2.2, zorder=5)   # MR (slope = 2× demand)
ax.text(3.5, 7, 'MR', color=ORANGE, fontsize=12.5, style='italic', weight='bold')
ax.plot([0, 9.4], [MC, MC], color=MCLINE, lw=2.4, zorder=5)        # MC = ATC
ax.text(7.4, MC + 1.6, 'MC = ATC', color=MCLINE, fontsize=11.5, style='italic', ha='left')
fig.savefig('ebay-top.png', dpi=150, transparent=True)
plt.close(fig); print('saved ebay-top.png')
print('--- ebay steps done ---')
