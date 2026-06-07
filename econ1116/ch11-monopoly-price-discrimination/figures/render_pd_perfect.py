"""Ch 11 — first-degree (perfect) price discrimination diagram (replicates the reference exactly).
The perfect price discriminator captures the WHOLE surplus triangle Pt-b-Pc as producer surplus:
output expands to the competitive Qc (no DWL), but all CS is transferred to PS.
  D = 100 - Q ; MR = 100 - 2Q ; MC = ATC = 20.  Consistent: Pm = (Pt+Pc)/2 = 60, Qm = Qc/2 = 40.
  a = (Qm, Pm) on D ; b = (Qc, Pc) on D∩MC ; c = (Qm, Pc) on MR∩MC.
Shading (matches reference): DARK top triangle Pt-a-Pm  +  DARK right triangle a-b-c  (captured CS+DWL),
LIGHT rectangle Pm-a-c-Pc (the single-price monopoly profit a single-price firm already gets).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

RED='#d23b3b'; ORANGE='#f0a23c'; GREEN='#6f9a3a'; INK='#222'
DARK='#4f93cc'; LIGHT='#dbeaf6'; GREY='#8a8a8a'
plt.rcParams.update({'font.size': 13, 'figure.facecolor': 'white'})

fig, ax = plt.subplots(figsize=(7.4, 7.0))
PT, PM, PC = 100, 60, 20
QM, QC = 40, 80

# ---- shaded surplus regions ----
ax.add_patch(plt.Polygon([(0,PT),(0,PM),(QM,PM)], facecolor=DARK,  edgecolor='none', zorder=1))   # top triangle (dark)
ax.add_patch(plt.Polygon([(0,PM),(QM,PM),(QM,PC),(0,PC)], facecolor=LIGHT, edgecolor='none', zorder=1))  # rectangle (light)
ax.add_patch(plt.Polygon([(QM,PM),(QC,PC),(QM,PC)], facecolor=DARK, edgecolor='none', zorder=1))   # right triangle (dark)

# ---- dashed guides ----
ax.plot([0, QM], [PM, PM], color=GREY, ls='--', lw=1.2, zorder=2)   # Pm -> a
ax.plot([QM, QM], [0, PM], color=GREY, ls='--', lw=1.2, zorder=2)   # Qm -> a
ax.plot([QC, QC], [0, PC], color=GREY, ls='--', lw=1.2, zorder=2)   # Qc -> b

# ---- curves ----
Q = np.linspace(0, 96, 400)
ax.plot(Q, 100 - Q,  color=RED,    lw=2.8, zorder=5)                # Demand
Qm = np.linspace(0, 50, 200); ax.plot(Qm, 100 - 2*Qm, color=ORANGE, lw=2.4, zorder=4)  # MR
ax.plot([0, 98], [PC, PC], color=GREEN, lw=2.6, zorder=4)          # MC = ATC

# ---- labelled points (open circles) ----
def dot(x, y):
    ax.plot([x], [y], 'o', color='white', mec=INK, mew=1.7, ms=11, zorder=8)
for (x, y) in [(0,PT),(0,PM),(0,PC),(QM,PM),(QC,PC),(QM,PC)]:
    dot(x, y)
ax.text(QM+1.8, PM+3.5, 'a', fontsize=16, style='italic', color=INK, zorder=9)
ax.text(QC+1.5, PC+5,   'b', fontsize=16, style='italic', color=INK, zorder=9)
ax.text(QM-4.5, PC-7,   'c', fontsize=16, style='italic', color=INK, zorder=9)

# ---- curve labels ----
ax.text(95, 100-95-3, 'D',  color=RED,    fontsize=16, weight='bold', style='italic', va='top')
ax.text(45, 5,        'MR', color=ORANGE, fontsize=15, weight='bold', style='italic')
ax.text(88, PC+4,     'MC = ATC', color=GREEN, fontsize=14.5, weight='bold', style='italic', ha='left')

# ---- axis labels / ticks (mathtext subscripts) ----
ax.set_yticks([PC, PM, PT]); ax.set_yticklabels(['$P_C$', '$P_M$', '$P_T$'], fontsize=16)
ax.set_xticks([QM, QC]);     ax.set_xticklabels(['$Q_M$', '$Q_C$'], fontsize=16)
ax.text(-3.2, -6.5, '0', fontsize=14, color=INK, ha='center', va='center')
ax.set_xlabel('Output', fontsize=15, labelpad=8)
ax.set_ylabel('Price and Cost', fontsize=15, labelpad=8)

ax.set_xlim(0, 102); ax.set_ylim(0, 108)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.spines['left'].set_color('#555');  ax.spines['left'].set_linewidth(1.8)
ax.spines['bottom'].set_color('#555'); ax.spines['bottom'].set_linewidth(1.8)
ax.tick_params(length=0)
plt.tight_layout()
plt.savefig('fig-pd-perfect.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close(); print('saved fig-pd-perfect.png')
