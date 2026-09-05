import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CHARCOAL = "#2D2D2D"; BLUE = "#6B8BA4"; TERRA = "#C47B5A"
SAGE = "#6A8E6B"; ROSE = "#A85C5C"; MUTED = "#8C8580"; LINE = "#D5CEC7"
TEXT = "#3A3632"

def setup():
    plt.rcParams.update({
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.dpi": 150,
        "font.family": "sans-serif",
        "font.sans-serif": ["Source Sans 3", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10, "text.color": TEXT,
        "axes.edgecolor": LINE, "axes.labelcolor": TEXT, "axes.labelsize": 10.5,
        "xtick.color": TEXT, "ytick.color": TEXT,
        "xtick.labelsize": 9.5, "ytick.labelsize": 9.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "legend.frameon": False, "legend.fontsize": 9.5,
    })
