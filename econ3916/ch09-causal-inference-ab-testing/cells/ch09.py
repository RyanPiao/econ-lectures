# Cells for the deck's mocked slides, copied verbatim by mock_cells.py pull.
# notebook: https://colab.research.google.com/github/RyanPiao/econ3916-student-notebooks/blob/main/3916/lab-ch09-guided.ipynb
# source: /Users/openclaw/Resilio Sync/documents/econ-project-book/econ-data-machine-learning/book/3916/labs/lab-ch09-guided.ipynb
# shown: 32   (the others run first, as the student's do)

# %% 3 nb=3
# GUIDED — run as-is
# Step 1: install statsmodels, then import libraries
!pip install -q statsmodels

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.power import TTestIndPower
from pathlib import Path

# Every resampling call below uses this seed, so your numbers match the expected output
RANDOM_STATE = 42

# savefig will not create a folder, and a fresh Colab session has no figures/ folder
Path("figures").mkdir(exist_ok=True)

print("Setup complete.")

# %% 5 nb=5
# GUIDED — run as-is
# Step 2: load the NSW experiment and compute the experimental ATE

# Dehejia & Wahba (2002) version of LaLonde's data, served by NBER; .dta is a Stata file
url = "https://users.nber.org/~rdehejia/data/nsw_dw.dta"
df = pd.read_stata(url)

# treat is 1 for a trainee and 0 for a control; re78 is earnings in 1978, the outcome
treated = df[df["treat"] == 1]
control = df[df["treat"] == 0]

ate_experimental = treated["re78"].mean() - control["re78"].mean()

# ,.2f prints commas between thousands and 2 decimals
print(f"Shape: {df.shape}")
print(f"Treatment group: n={len(treated)}, Control group: n={len(control)}")
print("\nExperimental Average Treatment Effect")
print(f"Mean earnings (treated):  ${treated['re78'].mean():,.2f}")
print(f"Mean earnings (control):  ${control['re78'].mean():,.2f}")
print(f"ATE (experimental):       ${ate_experimental:,.2f}")

# %% 7 nb=7
# GUIDED — run as-is
# Step 3: a simulated observational comparison group, and the selection bias it brings

np.random.seed(42)          # the same made-up earnings on every run

# lognormal draws are e raised to a normal draw, so mean=np.log(15000) puts the median at $15,000
n_comparison = len(control)
comparison_earnings = np.random.lognormal(mean=np.log(15000), sigma=0.8, size=n_comparison)

# The same trainees, compared with the simulated group instead of the randomized controls
ate_observational = treated["re78"].mean() - comparison_earnings.mean()
selection_bias = ate_observational - ate_experimental

# >10,.2f right-aligns each number in 10 characters, so the column lines up
print("Selection Bias Decomposition")
print(f"Experimental ATE (causal):    ${ate_experimental:>10,.2f}")
print(f"Observational ATE (biased):   ${ate_observational:>10,.2f}")
print(f"Selection Bias:               ${selection_bias:>10,.2f}")
print(f"\nFormula: Obs. ATE = True ATE + Selection Bias")
print(f"         {ate_observational:,.0f}  =  {ate_experimental:,.0f}  +  ({selection_bias:,.0f})")

# %% 9 nb=9
# GUIDED — run as-is
# Step 4: the three earnings distributions, and the two estimates of one effect

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# density=True scales each histogram to area 1, so groups of different sizes compare fairly;
# alpha=0.5 makes the bars see-through, so the overlap shows
axes[0].hist(treated["re78"], bins=30, alpha=0.5, density=True, color="steelblue",
             label=f"Treated (n={len(treated)})")
axes[0].hist(control["re78"], bins=30, alpha=0.5, density=True, color="peru",
             label=f"Exp. Control (n={len(control)})")
axes[0].hist(comparison_earnings, bins=30, alpha=0.5, density=True, color="navy",
             label=f"Obs. Comparison (n={n_comparison})")
axes[0].set_xlabel("1978 Earnings ($)")
axes[0].set_ylabel("Density")
axes[0].set_title("Treatment vs. Control vs. Comparison Group")
axes[0].legend()

axes[1].bar(["Experimental\n(Causal)", "Observational\n(Biased)"],
            [ate_experimental, ate_observational], color=["steelblue", "peru"], width=0.5)
axes[1].axhline(y=0, color="gray", linewidth=0.5)
# An arrow from the label to the top of the observational bar
axes[1].annotate(f"Selection Bias\n= ${selection_bias:,.0f}", xy=(1, ate_observational),
                 xytext=(0.5, ate_experimental / 2), color="red",
                 arrowprops={"arrowstyle": "->", "color": "red"})
axes[1].set_ylabel("Estimated ATE ($)")
axes[1].set_title("Why Random Assignment Matters")

plt.tight_layout()
plt.savefig("figures/ch09_selection_bias.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 14 nb=14
# GUIDED — run as-is
# Step 5: permutation test on the LaLonde experiment

def ate_statistic(x, y, axis):
    """Difference in means, x minus y, along axis."""
    return np.mean(x, axis=axis) - np.mean(y, axis=axis)


# .values turns a column into a plain NumPy array, which is what scipy expects
treated_earnings = treated["re78"].values
control_earnings = control["re78"].values

# "independent" shuffles the treat/control labels across all 445 people, 9,999 times
perm_result = stats.permutation_test(
    (treated_earnings, control_earnings),
    statistic=ate_statistic,
    permutation_type="independent",
    n_resamples=9999,
    random_state=RANDOM_STATE,
    alternative="two-sided"
)

print("Permutation Test")
print(f"Observed ATE:     ${ate_experimental:,.2f}")
print(f"Permutation p:    {perm_result.pvalue:.4f}")
print(f"N resamples:      {len(perm_result.null_distribution):,}")
print(f"\nDecision at alpha=0.05: {'Reject H0' if perm_result.pvalue < 0.05 else 'Fail to reject H0'}")

# %% 16 nb=16
# GUIDED — run as-is
# Step 6: the null distribution, with the observed ATE marked

fig, ax = plt.subplots(figsize=(10, 6))

# One ATE for each of the 9,999 shuffles: what chance alone produces
ax.hist(perm_result.null_distribution, bins=50, color="steelblue", edgecolor="white",
        label="Null distribution\n(shuffled labels)")
# A two-sided test counts both tails, so the mirror image of the observed ATE is marked too
ax.axvline(ate_experimental, color="peru", linewidth=2.5, linestyle="--",
           label=f"Observed ATE = ${ate_experimental:,.0f}")
ax.axvline(-ate_experimental, color="peru", linewidth=2.5, linestyle=":",
           label=f"Mirror = -${ate_experimental:,.0f}")
ax.set_xlabel("ATE Under Null ($)")
ax.set_ylabel("Frequency")
ax.set_title("Permutation Test: Null Distribution vs. Observed ATE")
ax.legend(loc="upper left")

plt.tight_layout()
plt.savefig("figures/ch09_permutation_null.png", dpi=150, bbox_inches="tight")
plt.show()

# np.abs drops the sign, so this counts both tails; True counts as 1 in a sum, and
# .1% multiplies by 100 and adds a percent sign
far = np.abs(perm_result.null_distribution) >= abs(ate_experimental)
print(f"Shuffled ATEs at least as far from zero as the observed one: {far.sum()} of {len(far):,} ({far.mean():.1%})")

# %% 18 nb=18
# GUIDED — run as-is
# Step 7: bootstrap 95% confidence interval for the ATE

# The permutation test asks whether the effect could be chance. The bootstrap asks how big it
# plausibly is: it resamples each group with replacement and recomputes the ATE each time.
# ate_statistic from Step 5 is the statistic again.
boot_result = stats.bootstrap(
    (treated_earnings, control_earnings),
    statistic=ate_statistic,
    n_resamples=9999,
    confidence_level=0.95,
    method="BCa",          # bias-corrected and accelerated: adjusts the interval for skewed data
    random_state=RANDOM_STATE
)

ci_low = boot_result.confidence_interval.low
ci_high = boot_result.confidence_interval.high

print("Bootstrap 95% BCa Confidence Interval")
print(f"Point estimate (ATE):  ${ate_experimental:,.2f}")
print(f"95% CI:                [${ci_low:,.2f}, ${ci_high:,.2f}]")

# %% 23 nb=23
# GUIDED — run as-is
# Step 8: Cohen's d, and the power our study achieved

power_analysis = TTestIndPower()

# Cohen's d, as in Lab 8. pandas' .std() divides by n - 1, the sample standard deviation
n_t, n_c = len(treated), len(control)
s_t = treated["re78"].std()
s_c = control["re78"].std()
s_pooled = np.sqrt(((n_t - 1) * s_t**2 + (n_c - 1) * s_c**2) / (n_t + n_c - 2))
d_lalonde = ate_experimental / s_pooled

# The chance our test detects an effect of size d, with our group sizes; ratio is n_c / n_t
achieved_power = power_analysis.solve_power(
    effect_size=abs(d_lalonde),
    nobs1=n_t,
    alpha=0.05,
    ratio=n_c / n_t,
    alternative="two-sided"
)

print("Power of the LaLonde Study")
print(f"Cohen's d:           {d_lalonde:.3f}")
print(f"Treatment n:         {n_t}")
print(f"Control n:           {n_c}")
print(f"Achieved power:      {achieved_power:.3f} ({achieved_power*100:.1f}%)")
print(f"Target:              0.800 (80%)")

# %% 25 nb=25
# GUIDED — run as-is
# Step 8, continued: the sample size needed for three dollar effects

# Leave nobs1 out and give power instead: solve_power then solves for the n per group.
# n_by_effect is a dictionary: n_by_effect[500] will hold the n for a $500 effect
print(f"Required Sample Size per Group (80% power, alpha=0.05)")
n_by_effect = {}
for dollar_effect in [500, 1000, 2000]:
    d_target = dollar_effect / s_pooled
    n_required = power_analysis.solve_power(
        effect_size=d_target,
        alpha=0.05,
        power=0.80,
        ratio=1.0,
        alternative="two-sided"
    )
    n_by_effect[dollar_effect] = n_required
    # >5, pads to 5 characters with a thousands comma; >6,.0f does the same with no decimals
    print(f"  To detect ${dollar_effect:>5,} effect (d={d_target:.3f}): n = {n_required:>6,.0f} per group ({2*n_required:,.0f} total)")

print(f"\nn for a $500 effect / n for a $2,000 effect: {n_by_effect[500] / n_by_effect[2000]:.0f}")

# %% 27 nb=27
# GUIDED — run as-is
# Step 9: power curves, the power for each n per group, at three dollar effects

fig, ax = plt.subplots(figsize=(10, 6))
sample_sizes = np.arange(20, 1000)      # 20, 21, ..., 999 per group

for dollar_eff, color in [(500, "peru"), (1000, "navy"), (2000, "steelblue")]:
    d = dollar_eff / s_pooled
    # One power for every n in sample_sizes, as in Lab 8's power curves
    powers = [power_analysis.solve_power(
        effect_size=d, nobs1=n, alpha=0.05,
        ratio=1.0, alternative="two-sided"
    ) for n in sample_sizes]
    ax.plot(sample_sizes, powers, label=f"${dollar_eff:,} effect (d={d:.2f})", linewidth=2, color=color)

ax.axhline(y=0.80, color="gray", linestyle="--", label="80% power target")
ax.axvline(x=n_t, color="red", linestyle=":", label=f"Our n={n_t}")
ax.set_xlabel("Sample Size per Group")
ax.set_ylabel("Statistical Power")
ax.set_title("Power Curves — Planning an A/B Test Before You Run It")
ax.legend(loc="right")
ax.set_ylim(0, 1.05)

plt.tight_layout()
plt.savefig("figures/ch09_power_curves.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 32 nb=32
# GUIDED — run as-is
# Step 10: load the Cookie Cats data

cookie_url = "https://raw.githubusercontent.com/Saikushal185/ab-testing-analytics/main/data/cookie_cats.csv"
cc = pd.read_csv(cookie_url)

print(f"Shape: {cc.shape}")
print(f"\nGroup sizes:")
print(cc["version"].value_counts())
print(f"\nFirst 5 rows:")
cc.head()
