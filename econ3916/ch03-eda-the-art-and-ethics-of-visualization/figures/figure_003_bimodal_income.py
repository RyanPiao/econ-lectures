"""Bimodal Income Distribution: Histogram + KDE."""
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
low_income = np.random.normal(35000, 8000, 600)
high_income = np.random.normal(85000, 15000, 400)
income = np.concatenate([low_income, high_income])

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

# Histogram alone
axes[0].hist(income / 1000, bins=30, color="#2196F3", edgecolor="white",
             density=True, alpha=0.85)
axes[0].set_title("Histogram (30 bins)", fontsize=12, fontweight="bold")
axes[0].set_xlabel("Household Income ($K)")
axes[0].set_ylabel("Density")
axes[0].axvline(np.mean(income) / 1000, color="#E53935", linestyle="--",
                linewidth=2, label=f"Mean = ${np.mean(income)/1000:.0f}K")
axes[0].legend(frameon=False)
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)

# KDE alone
from scipy.stats import gaussian_kde
kde = gaussian_kde(income / 1000)
x_range = np.linspace(0, 140, 300)
axes[1].fill_between(x_range, kde(x_range), color="#FF9800", alpha=0.3)
axes[1].plot(x_range, kde(x_range), color="#FF9800", linewidth=2)
axes[1].set_title("KDE (Gaussian Kernel)", fontsize=12, fontweight="bold")
axes[1].set_xlabel("Household Income ($K)")
axes[1].set_ylabel("Density")
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)

# Both overlaid
axes[2].hist(income / 1000, bins=30, color="#2196F3", edgecolor="white",
             density=True, alpha=0.5)
axes[2].plot(x_range, kde(x_range), color="#FF9800", linewidth=2)
axes[2].axvline(np.mean(income) / 1000, color="#E53935", linestyle="--",
                linewidth=2, label=f"Mean = ${np.mean(income)/1000:.0f}K")
axes[2].set_title("Both: The Mean Misses It", fontsize=12, fontweight="bold")
axes[2].set_xlabel("Household Income ($K)")
axes[2].legend(frameon=False)
axes[2].spines["top"].set_visible(False)
axes[2].spines["right"].set_visible(False)

plt.tight_layout()
plt.savefig("figures/figure_003_bimodal_income.png", dpi=150,
            bbox_inches="tight", facecolor="white")
plt.close()
print("OK: figure_003_bimodal_income.png")
