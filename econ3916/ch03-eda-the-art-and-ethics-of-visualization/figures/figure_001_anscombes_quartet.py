"""Anscombe's Quartet: Same Stats, Different Stories."""
import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset("anscombe")

fig, axes = plt.subplots(2, 2, figsize=(10, 8), sharex=True, sharey=True)
for ax, dataset in zip(axes.flatten(), ["I", "II", "III", "IV"]):
    subset = df[df["dataset"] == dataset]
    ax.scatter(subset["x"], subset["y"], color="#2196F3", edgecolors="white",
               s=80, zorder=3)
    ax.plot([4, 14], [5, 10], color="#FF9800", linewidth=2, linestyle="--",
            alpha=0.8, zorder=2)
    ax.set_title(f"Dataset {dataset}", fontsize=13, fontweight="bold")
    ax.set_xlim(3, 20)
    ax.set_ylim(2, 14)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

fig.text(0.5, 0.02, "x", ha="center", fontsize=12)
fig.text(0.02, 0.5, "y", va="center", rotation="vertical", fontsize=12)
plt.tight_layout(rect=[0.03, 0.03, 1, 0.95])
plt.savefig("figures/figure_001_anscombes_quartet.png", dpi=150,
            bbox_inches="tight", facecolor="white")
plt.close()
print("OK: figure_001_anscombes_quartet.png")
