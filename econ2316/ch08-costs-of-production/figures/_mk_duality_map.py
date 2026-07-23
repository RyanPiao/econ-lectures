"""ch08 duality map — producer/consumer parallel, styled to match
   ECON 2316 ch06's figure-6-duality-map.png (rich boxes, named arrows
   carrying their formula, and the envelope theorem as the foundation)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import os

HERE = os.path.dirname(os.path.abspath(__file__))
PRIMARY="#2D2D2D"; SECONDARY="#6B8BA4"; ACCENT="#C47B5A"
MUTED="#8C8580"; DANGER="#A85C5C"; SUCCESS="#3F7A4F"
plt.rcParams.update({"figure.facecolor":"white","savefig.facecolor":"white",
                     "savefig.bbox":"tight","savefig.dpi":150})

fig, ax = plt.subplots(figsize=(14.6, 7.5))
ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")

def box(cx, cy, w, h, edge, face, title, sym, gloss):
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
        boxstyle="round,pad=0.008,rounding_size=0.016",
        linewidth=2.0, edgecolor=edge, facecolor=face, zorder=3))
    ax.text(cx, cy+h*0.235, title, ha="center", va="center", fontsize=14,
            fontweight="bold", color=edge, zorder=4)
    ax.text(cx, cy-h*0.045, sym, ha="center", va="center", fontsize=16,
            color=PRIMARY, zorder=4)
    ax.text(cx, cy-h*0.325, gloss, ha="center", va="center", fontsize=9.8,
            color=MUTED, fontstyle="italic", zorder=4)

def arrow(x0, x1, y, color, label, formula):
    ax.add_patch(FancyArrowPatch((x0, y), (x1, y),
        arrowstyle="-|>", mutation_scale=20, linewidth=2.2,
        color=color, zorder=4))
    ax.text((x0+x1)/2, y+0.040, label, ha="center", va="bottom",
            fontsize=11, fontweight="bold", color=color, zorder=5, linespacing=1.25)
    ax.text((x0+x1)/2, y-0.036, formula, ha="center", va="top",
            fontsize=10.5, color=PRIMARY, zorder=5)

W, H = 0.200, 0.170
CX = [0.170, 0.505, 0.840]
Y_C, Y_P = 0.655, 0.355

# ---------- top banner ----------
ax.add_patch(FancyBboxPatch((0.055, 0.845), 0.895, 0.125,
    boxstyle="round,pad=0.006,rounding_size=0.014",
    linewidth=2.0, edgecolor=DANGER, facecolor="#FBEFEF", zorder=3))
ax.text(0.5025, 0.938, "One problem, two readings  —  minimize spending subject to hitting a target",
        ha="center", va="center", fontsize=15, fontweight="bold", color=DANGER, zorder=4)
ax.text(0.5025, 0.882,
        r"consumer:  $\min\ p\cdot x$  s.t.  $u(x)=\bar u$          "
        r"producer:  $\min\ wL+rK$  s.t.  $f(K,L)=q$",
        ha="center", va="center", fontsize=13, color=PRIMARY, zorder=4)

# ---------- row labels ----------
ax.text(0.032, Y_C, "CONSUMER\nCh 6", ha="center", va="center", fontsize=12,
        fontweight="bold", color=SECONDARY, rotation=90, linespacing=1.5)
ax.text(0.032, Y_P, "PRODUCER\nCh 8", ha="center", va="center", fontsize=12,
        fontweight="bold", color=ACCENT, rotation=90, linespacing=1.5)

# ---------- consumer row ----------
box(CX[0], Y_C, W, H, SECONDARY, "#EEF3F7", "Utility",     r"$u(x_1,x_2)$",  "preferences  —  primitive")
box(CX[1], Y_C, W, H, SECONDARY, "#EEF3F7", "Expenditure", r"$e(p,\bar u)$", r"min spending to reach $\bar u$")
box(CX[2], Y_C, W, H, SECONDARY, "#EEF3F7", "Hicksian",    r"$h_i(p,\bar u)$","compensated demand")

arrow(CX[0]+W/2, CX[1]-W/2, Y_C, SECONDARY, "expenditure\nmin", r"$\min\ p\cdot x$")
arrow(CX[1]+W/2, CX[2]-W/2, Y_C, SECONDARY, "Shephard",        r"$h_i=\partial e/\partial p_i$")

# ---------- producer row ----------
box(CX[0], Y_P, W, H, ACCENT, "#FDF3EC", "Production", r"$f(K,L)$",    "technology  —  primitive")
box(CX[1], Y_P, W, H, ACCENT, "#FDF3EC", "Cost",       r"$c(w,r,q)$",  r"min spending to make $q$")
box(CX[2], Y_P, W, H, ACCENT, "#FDF3EC", "Conditional", r"$K^*,\ L^*$","input demand")

arrow(CX[0]+W/2, CX[1]-W/2, Y_P, ACCENT, "cost min",  r"$\min\ wL+rK$")
arrow(CX[1]+W/2, CX[2]-W/2, Y_P, ACCENT, "Shephard",  r"$L^*=\partial c/\partial w$")

# ---------- dashed recovery arrow: c recovers f ----------
_ry = Y_P - H/2 - 0.048
ax.add_patch(FancyArrowPatch((CX[1], _ry), (CX[0], _ry),
    arrowstyle="-|>", mutation_scale=15, linewidth=1.6, linestyle=(0,(5,3)),
    color=MUTED, zorder=4))
for _x in (CX[0], CX[1]):
    ax.plot([_x, _x], [_ry, Y_P - H/2], linestyle=(0,(2,3)), linewidth=1.2,
            color=MUTED, zorder=2)
ax.text((CX[0]+CX[1])/2, _ry - 0.038,
        r"$c$ recovers $f$  —  same firm, two descriptions",
        ha="center", va="center", fontsize=10.5, color=MUTED, fontstyle="italic", zorder=5)

# ---------- foundation banner ----------
ax.add_patch(FancyBboxPatch((0.145, 0.022), 0.715, 0.100,
    boxstyle="round,pad=0.006,rounding_size=0.014",
    linewidth=2.0, edgecolor=SUCCESS, facecolor="#EDF7EF", zorder=3))
ax.text(0.5025, 0.096, "Envelope theorem  —  the one result behind BOTH Shephard arrows",
        ha="center", va="center", fontsize=13.5, fontweight="bold", color=SUCCESS, zorder=4)
ax.text(0.5025, 0.050, r"and behind  $\partial c/\partial q=\mu=MC$",
        ha="center", va="center", fontsize=11.5, color=PRIMARY, zorder=4)
plt.savefig(os.path.join(HERE, "fig-duality.png"))
plt.close(fig)
print("wrote fig-duality.png")
