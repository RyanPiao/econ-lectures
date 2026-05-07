"""
Figure 005: Embedding Space Visualization
Shows how semantically similar economic terms cluster in embedding space.
2D projection using simulated embeddings for illustration.
"""
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

# Simulated 2D embedding clusters for economic terms
clusters = {
    "Monetary Policy": {
        "terms": ["federal funds rate", "interest rates", "tightening",
                  "accommodative", "rate hike", "rate cut"],
        "center": (2.5, 3.0),
        "color": "#2563eb"
    },
    "Inflation": {
        "terms": ["inflation", "price stability", "CPI",
                  "price pressures", "disinflation", "deflation"],
        "center": (5.5, 4.5),
        "color": "#dc2626"
    },
    "Labor Market": {
        "terms": ["unemployment", "job gains", "payrolls",
                  "labor force", "hiring", "wages"],
        "center": (1.5, 6.5),
        "color": "#16a34a"
    },
    "Economic Activity": {
        "terms": ["GDP growth", "expansion", "recession",
                  "output gap", "economic slowdown", "recovery"],
        "center": (6.0, 1.5),
        "color": "#9333ea"
    }
}

fig, ax = plt.subplots(figsize=(6, 4.5), dpi=150)

for cluster_name, info in clusters.items():
    cx, cy = info["center"]
    n = len(info["terms"])
    xs = cx + np.random.randn(n) * 0.45
    ys = cy + np.random.randn(n) * 0.45

    ax.scatter(xs, ys, c=info["color"], s=60, alpha=0.85, zorder=3,
               edgecolors='white', linewidths=0.5)

    for i, term in enumerate(info["terms"]):
        ax.annotate(term, (xs[i], ys[i]), fontsize=6.5,
                    ha='center', va='bottom', color=info["color"],
                    fontweight='medium',
                    xytext=(0, 4), textcoords='offset points')

    ax.annotate(cluster_name, (cx, cy - 0.9), fontsize=8,
                ha='center', va='top', color=info["color"],
                fontweight='bold', fontstyle='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                          edgecolor=info["color"], alpha=0.8))

ax.set_xlabel("Embedding Dimension 1 (projected)", fontsize=9)
ax.set_ylabel("Embedding Dimension 2 (projected)", fontsize=9)
ax.set_xlim(-0.5, 8.5)
ax.set_ylim(-0.5, 8.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.15)
ax.tick_params(labelsize=7)

# Remove top/right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
plt.savefig("figures/figure_005_embedding_space.png",
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("OK: figure_005_embedding_space.png")
