"""White Academia figure defaults, shared by every ch11 figure script."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PRIMARY = "#2D2D2D"; SECONDARY = "#6B8BA4"; ACCENT = "#C47B5A"
TEXT = "#3A3632"; MUTED = "#8C8580"; LINE = "#D5CEC7"
DANGER = "#A85C5C"; SUCCESS = "#6A8E6B"

def style():
    plt.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.dpi": 150,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10, "axes.labelsize": 10.5, "axes.titlesize": 11,
        "axes.edgecolor": LINE, "axes.labelcolor": TEXT,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.spines.top": False, "axes.spines.right": False,
        "legend.frameon": False, "legend.fontsize": 9.5,
        "grid.color": LINE, "grid.linewidth": 0.7, "grid.alpha": 0.6,
    })
