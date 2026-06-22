#!/usr/bin/env python3
"""Circular-flow diagram (concentric loops) for ECON 2316 Ch 1 — the simplified economy.
Outer red loop = money ($); inner teal loop = real flows (goods & inputs).
Firms (left) and Households (right) sit on the loop; outputs on top, inputs on bottom.
2316 variant: factor market labelled LABOR & CAPITAL; loop legend in the upper-right.
Run from this directory: ``python3 render_circular_flow.py``."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc

OUT = os.path.dirname(os.path.abspath(__file__))

CHAR="#2D2D2D"; TEAL="#5C9AA3"; RED="#B0524F"; TERRA="#C47B5A"; MUTED="#8C8580"; BLUE="#6B8BA4"
plt.rcParams.update({"font.family":"sans-serif",
    "font.sans-serif":["Source Sans 3","Helvetica Neue","Arial","DejaVu Sans"],"text.color":CHAR})

fig, ax = plt.subplots(figsize=(8.8, 6.2))
ax.set_xlim(0,10); ax.set_ylim(0,8.6); ax.axis("off")
C=(5.0, 4.2)

# ---- concentric loops ----
for R,col in [(2.65,RED),(1.78,TEAL)]:
    ax.add_patch(Arc(C, 2*R, 2*R, theta1=0, theta2=360, lw=4.0, edgecolor=col, zorder=2))

def head(angle_deg, R, clockwise, col):
    th=np.radians(angle_deg)
    p=np.array([C[0]+R*np.cos(th), C[1]+R*np.sin(th)])
    tang=np.array([np.sin(th),-np.cos(th)]) * (1 if clockwise else -1)
    ax.add_patch(FancyArrowPatch(p-tang*0.04, p+tang*0.04, arrowstyle="-|>",
        mutation_scale=30, color=col, lw=0, zorder=3))

# red money loop: clockwise; teal real loop: counter-clockwise
head(90, 2.65, True, RED);  head(270, 2.65, True, RED)
head(90, 1.78, False, TEAL); head(270, 1.78, False, TEAL)

# ---- Firms / Households boxes on the loop ----
def box(cx, label, sub, edge):
    ax.add_patch(FancyBboxPatch((cx-1.18, C[1]-0.82), 2.36, 1.64,
        boxstyle="round,pad=0.02,rounding_size=0.16", linewidth=2.6,
        edgecolor=edge, facecolor="#f8f6f3", zorder=5))
    ax.text(cx, C[1]+0.26, label, ha="center", va="center", fontsize=15.5, fontweight="bold", color=CHAR, zorder=6)
    ax.text(cx, C[1]-0.36, sub, ha="center", va="center", fontsize=9.5, color=MUTED, zorder=6)
box(2.05, "Firms", "(Businesses)", TERRA)
box(7.95, "Households", "(You)", BLUE)

ax.text(C[0], C[1]+0.02, "Circular\nFlow", ha="center", va="center", fontsize=12.5,
        fontstyle="italic", color=MUTED, zorder=4, linespacing=1.05)

# ---- top: outputs / product market ----
ax.text(5.0, 7.95, "PRODUCT MARKET", ha="center", fontsize=11.5, fontweight="bold", color=MUTED)
ax.text(5.0, 7.45, "Outputs: goods & services", ha="center", fontsize=12.5, color=CHAR)

# ---- bottom: inputs / factor (labor & capital) market, highlighted ----
ax.add_patch(FancyBboxPatch((1.4, 0.12), 7.2, 1.15,
    boxstyle="round,pad=0.02,rounding_size=0.12", linewidth=2.2,
    edgecolor=TERRA, facecolor=(196/255,123/255,90/255,0.09), zorder=1))
ax.text(5.0, 0.92, "FACTOR  (LABOR & CAPITAL)  MARKET", ha="center", fontsize=12.5, fontweight="bold", color=TERRA)
ax.text(5.0, 0.42, "Inputs:  labor • capital • land • entrepreneurship", ha="center", fontsize=11.5, color=CHAR)

# ---- loop legend, upper-right corner ----
ax.add_patch(FancyArrowPatch((7.05,8.15),(7.65,8.15), arrowstyle="-|>", mutation_scale=16, color=RED, lw=3))
ax.text(7.75, 8.15, "money ($)", va="center", fontsize=9.5, color=RED, fontweight="bold")
ax.add_patch(FancyArrowPatch((7.05,7.62),(7.65,7.62), arrowstyle="-|>", mutation_scale=16, color=TEAL, lw=3))
ax.text(7.75, 7.62, "goods & inputs", va="center", fontsize=9.5, color=TEAL, fontweight="bold")

fig.savefig(os.path.join(OUT, "fig-circular-flow.png"), dpi=200, bbox_inches="tight", facecolor="white")
print("wrote fig-circular-flow.png")
