"""Regenerate fig-gpa-analogy.png with non-overlapping labels.

Previous version (imported from 2316 ch08) had labels stacked directly on top
of the curves: "GPA: 2.3", "GPA: 2.2", "GPA: 2.5" overlapped the green line;
"New Course: 1.0/3.0/4.0" overlapped the red line; "Lowest GPA: 2.0" overlapped
the crossing point. This version uses white-bbox labels placed off the curves
with short leader-line arrows.

Story: 4 semesters (courses 9 → 12). Cumulative GPA (green, average) reacts to
each new course's grade (red, marginal). Sub-GPA next courses pull GPA down;
above-GPA ones pull it up. They cross at the GPA minimum (course 10).
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# Data
courses = np.array([9, 10, 11, 12])
gpa     = np.array([2.3, 2.0, 2.2, 2.5])
new_grade = np.array([1.0, 2.0, 3.0, 4.0])

# Smooth curves through the 4 points (quadratic + linear)
xs = np.linspace(8.6, 12.4, 200)
gpa_coef = np.polyfit(courses, gpa, 2)
gpa_smooth = np.polyval(gpa_coef, xs)
new_smooth = np.polyval(np.polyfit(courses, new_grade, 1), xs)

# Figure
GREEN = '#1A8754'
RED   = '#C72A2A'
PURPLE = '#6A4FB6'
GRID  = '#dcdcd6'

fig, ax = plt.subplots(figsize=(8.0, 5.3))
ax.plot(xs, gpa_smooth, color=GREEN, linewidth=3.0, label='GPA  (cumulative — average)', zorder=3)
ax.plot(xs, new_smooth, color=RED,   linewidth=3.0, label='New course grade  (marginal)', zorder=3)

# Data points
ax.scatter(courses, gpa, color=GREEN, s=80, zorder=5, edgecolor='white', linewidth=1.5)
ax.scatter(courses, new_grade, color=RED, s=80, zorder=5, edgecolor='white', linewidth=1.5)

# Crossing point (course 10)
ax.scatter([10], [2.0], color=PURPLE, s=170, zorder=6, edgecolor='white', linewidth=2.0)


def label(ax, txt, xy, xytext, color, fontsize=11, weight='bold'):
    ax.annotate(txt, xy=xy, xytext=xytext, fontsize=fontsize, color=color,
                fontweight=weight, ha='center',
                bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                          edgecolor=color, linewidth=1.4),
                arrowprops=dict(arrowstyle='-', color=color, lw=1.0,
                                connectionstyle='arc3,rad=0'),
                zorder=10)


# GPA labels (placed BELOW or ABOVE the green curve so they don't overlap it)
label(ax, 'GPA: 2.3',  xy=(9, 2.3),  xytext=(8.65, 2.65), color=GREEN)
label(ax, 'GPA: 2.2',  xy=(11, 2.2), xytext=(11.45, 1.75), color=GREEN)
label(ax, 'GPA: 2.5',  xy=(12, 2.5), xytext=(12.30, 3.05), color=GREEN)

# Crossing point label (placed below, in purple)
label(ax, 'Lowest GPA = 2.0\n(MC crosses ATC here)',
      xy=(10, 2.0), xytext=(10, 0.85), color=PURPLE, fontsize=10.5)

# Marginal-grade labels (placed AWAY from red line)
label(ax, 'New course: 1.0\n(below GPA → pulls down)',
      xy=(9, 1.0), xytext=(8.85, 0.20), color=RED, fontsize=10)
label(ax, 'New course: 3.0\n(above GPA → pulls up)',
      xy=(11, 3.0), xytext=(10.10, 3.65), color=RED, fontsize=10)
label(ax, 'New course: 4.0',
      xy=(12, 4.0), xytext=(11.10, 4.45), color=RED, fontsize=10)

# Curve "name" labels on the right edge (just text, no arrow)
ax.text(12.55, 2.45, 'GPA', color=GREEN, fontsize=13, fontweight='bold',
        ha='left', va='center')
ax.text(12.55, 4.10, 'Marginal Grade', color=RED, fontsize=13, fontweight='bold',
        ha='left', va='center')

# Axes
ax.set_xlim(8.4, 13.6)
ax.set_ylim(-0.4, 5.0)
ax.set_xticks([9, 10, 11, 12])
ax.set_yticks([1, 2, 3, 4])
ax.set_xlabel('Number of courses taken', fontsize=12, fontweight='bold')
ax.set_ylabel('Grade', fontsize=12, fontweight='bold')
ax.grid(True, color=GRID, linewidth=0.7, alpha=0.7)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Legend in upper-left, away from data
ax.legend(loc='upper left', fontsize=10.5, frameon=True, framealpha=0.95)

plt.tight_layout()
plt.savefig('fig-gpa-analogy.png', dpi=160, bbox_inches='tight', facecolor='white')
print('saved fig-gpa-analogy.png')
