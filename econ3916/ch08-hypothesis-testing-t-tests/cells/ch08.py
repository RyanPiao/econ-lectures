# Cells for the deck's mocked slides, copied verbatim by mock_cells.py pull.
# notebook: https://colab.research.google.com/github/RyanPiao/econ3916-student-notebooks/blob/cb83a4e73597232201bf8e62024ba8019a8d66ca/3916/lab-ch08-guided.ipynb
# published: RyanPiao/econ3916-student-notebooks main @ cb83a4e (file last changed in 84f4107, 9 Oct; blob 1f5794c, 47 cells),
#   the copy the room opens. The book copy (49 cells) is HELD until 21 Oct, so cells come from this file.
# source: /Users/openclaw/econ-lectures/econ3916/ch08-hypothesis-testing-t-tests/cells/lab-ch08-guided.published-cb83a4e.ipynb
# shown: 8 16 21 25 40   (the others run first, as the student's do; 30-38 are skipped: 32 has blanks,
#   37 is the Write-it-yourself stub, 38 its CHECK; 40 sets its own seed, so skipping them changes nothing)

# %% 3 nb=3
# GUIDED — run as-is
# Step 1: install pingouin, then import libraries
!pip install -q pingouin statsmodels

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import pingouin as pg
from statsmodels.stats.power import TTestIndPower
from statsmodels.stats.multitest import multipletests
from pathlib import Path

# savefig will not create a folder, and a fresh Colab session has no figures/ folder
Path("figures").mkdir(exist_ok=True)

print("Setup complete.")

# %% 5 nb=5
# GUIDED — run as-is
# Step 2: load the NSW experimental sample

# Dehejia & Wahba (2002) version of LaLonde's data, served by NBER; .dta is a Stata file
url = "https://users.nber.org/~rdehejia/data/nsw_dw.dta"
df = pd.read_stata(url)

print(f"Shape: {df.shape}")
print(f"\nColumns: {list(df.columns)}")
# treat is 1 for a trainee and 0 for a control; True counts as 1 in a sum, so each sum counts rows
print(f"\nTreatment group: {(df['treat'] == 1).sum()} treated, {(df['treat'] == 0).sum()} control")
print("\nFirst 5 rows:")
df.head()

# %% 6 nb=6
# GUIDED — run as-is
# Step 3: summary statistics by treatment status

# re78 is earnings in 1978, the outcome; .values turns a column into a plain NumPy array
treated = df[df["treat"] == 1]["re78"].values
control = df[df["treat"] == 0]["re78"].values

# ,.2f prints commas between thousands and 2 decimals.
# ddof=1 divides by n - 1, which gives the sample standard deviation; plain np.std divides by n
print("1978 earnings")
print(f"Treatment group (n={len(treated)}):")
print(f"  Mean:   ${np.mean(treated):,.2f}")
print(f"  Median: ${np.median(treated):,.2f}")
print(f"  Std:    ${np.std(treated, ddof=1):,.2f}")
print(f"\nControl group (n={len(control)}):")
print(f"  Mean:   ${np.mean(control):,.2f}")
print(f"  Median: ${np.median(control):,.2f}")
print(f"  Std:    ${np.std(control, ddof=1):,.2f}")
print(f"\nRaw difference in means: ${np.mean(treated) - np.mean(control):,.2f}")

# %% 8 nb=8
# GUIDED — run as-is
# Step 4: the two earnings distributions, side by side

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# alpha=0.6 makes the bars see-through, so the overlap between the groups shows
axes[0].hist(treated, bins=30, alpha=0.6, color="steelblue", label=f"Treatment (n={len(treated)})")
axes[0].hist(control, bins=30, alpha=0.6, color="peru", label=f"Control (n={len(control)})")
axes[0].axvline(np.mean(treated), color="navy", linestyle="--", label=f"Treat mean: ${np.mean(treated):,.0f}")
axes[0].axvline(np.mean(control), color="saddlebrown", linestyle="--", label=f"Control mean: ${np.mean(control):,.0f}")
axes[0].set_xlabel("1978 Earnings ($)")
axes[0].set_ylabel("Frequency")
axes[0].set_title("Earnings Distribution by Treatment Status")
axes[0].legend()

axes[1].boxplot([treated, control], tick_labels=["Treatment", "Control"])
axes[1].set_ylabel("1978 Earnings ($)")
axes[1].set_title("Earnings Box Plot by Treatment Status")

plt.tight_layout()
plt.savefig("figures/ch08_lalonde_distributions.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 14 nb=14
# GUIDED — run as-is
# Step 5: one-sample t-test
# H0: mean control earnings = $5,000.   H1: mean control earnings != $5,000

hypothesized_mean = 5000
t_stat_1, p_value_1 = stats.ttest_1samp(control, popmean=hypothesized_mean)

# :, in {hypothesized_mean:,} adds the thousands comma
print("One-sample t-test")
print(f"H0: Average control group earnings = ${hypothesized_mean:,}")
print(f"H1: Average control group earnings != ${hypothesized_mean:,}")
print(f"\nSample mean:  ${np.mean(control):,.2f}")
print(f"T-statistic:  {t_stat_1:.4f}")
print(f"P-value:      {p_value_1:.4f}")
# The one-line if/else from the note above
print(f"\nDecision at alpha=0.05: {'Reject H0' if p_value_1 < 0.05 else 'Fail to reject H0'}")

# %% 16 nb=16
# GUIDED — run as-is
# Step 6: two-sample t-test, Welch's version, which does not assume equal variances
# H0: mu_treatment - mu_control = 0.   H1: mu_treatment - mu_control != 0

# equal_var=False picks Welch's test. treated comes first, so a positive t means trainees earned more
t_stat_2, p_value_2 = stats.ttest_ind(
    treated, control,
    equal_var=False,
    alternative="two-sided"
)

mean_diff = np.mean(treated) - np.mean(control)

print("Two-sample Welch's t-test")
print(f"H0: Treatment earnings = Control earnings (no training effect)")
print(f"H1: Treatment earnings != Control earnings")
print(f"\nTreatment mean: ${np.mean(treated):,.2f}")
print(f"Control mean:   ${np.mean(control):,.2f}")
print(f"Difference:     ${mean_diff:,.2f}")
print(f"\nT-statistic:  {t_stat_2:.4f}")
print(f"P-value:      {p_value_2:.4f}")
print(f"\nDecision at alpha=0.05: {'Reject H0' if p_value_2 < 0.05 else 'Fail to reject H0'}")

# %% 21 nb=21
# GUIDED — run as-is
# Step 7: Cohen's d, the difference in means measured in standard deviations

# By hand: pool the two SDs into one, weighting each group by its n - 1
n1, n2 = len(treated), len(control)
s1, s2 = np.std(treated, ddof=1), np.std(control, ddof=1)
s_pooled = np.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2) / (n1 + n2 - 2))
d_manual = (np.mean(treated) - np.mean(control)) / s_pooled

print("Effect size: Cohen's d")
print(f"Pooled std:  ${s_pooled:,.2f}")
print(f"Cohen's d:   {d_manual:.4f}")

# The same number from pingouin, as a check on the hand calculation
d_pg = pg.compute_effsize(treated, control, paired=False, eftype="cohen")
print(f"Cohen's d (pingouin): {d_pg:.4f}")

print("\nBenchmarks: small d = 0.2, medium d = 0.5, large d = 0.8")
# abs() drops the sign; the chained if/else from the note above picks the band
print(f"Our d = {d_manual:.2f} -> {'Small' if abs(d_manual) < 0.5 else 'Medium' if abs(d_manual) < 0.8 else 'Large'} effect")
print(f"The ${mean_diff:,.0f} earnings difference represents {abs(d_manual):.2f} standard deviations.")

# %% 23 nb=23
# GUIDED — run as-is
# Step 8: power analysis, for our study and for a planned one

power_analysis = TTestIndPower()

# Power: the chance the test detects an effect of size d, with our two group sizes.
# ratio is the second group's size divided by the first's
achieved_power = power_analysis.solve_power(
    effect_size=abs(d_manual),
    nobs1=n1,
    alpha=0.05,
    ratio=n2 / n1,
    alternative="two-sided"
)
print("Power of our study")
print(f"Effect size (d):     {abs(d_manual):.3f}")
print(f"Treatment n:         {n1}")
print(f"Control n:           {n2}")
print(f"Achieved power:      {achieved_power:.3f} ({achieved_power*100:.1f}%)")
print(f"Target:              0.800 (80%)")

# solve_power solves for the one argument you leave out: here nobs1, the n per group
n_required_03 = power_analysis.solve_power(
    effect_size=0.3,
    alpha=0.05,
    power=0.80,
    ratio=1.0,
    alternative="two-sided"
)
print("\nRequired sample size")
print(f"To detect d=0.3 (small-medium) with 80% power:")
print(f"  n per group = {n_required_03:.0f}")
print(f"  Total participants = {2 * n_required_03:.0f}")

# %% 25 nb=25
# GUIDED — run as-is
# Step 9: power curves, the power for each n per group, at five effect sizes

fig, ax = plt.subplots(figsize=(10, 6))
sample_sizes = np.arange(10, 500)      # 10, 11, ..., 499 per group

# Each tuple is one curve: its effect size, its legend label, and its colour
for d, label, color in [
    (0.2, "Small (d=0.2)", "peru"),
    (abs(d_manual), f"Our effect (d={abs(d_manual):.2f})", "navy"),
    (0.3, "d=0.3", "lightsteelblue"),
    (0.5, "Medium (d=0.5)", "steelblue"),
    (0.8, "Large (d=0.8)", "seagreen"),
]:
    # The list comprehension from the note above: one power for every n in sample_sizes
    powers = [power_analysis.solve_power(
        effect_size=d, nobs1=n, alpha=0.05,
        ratio=1.0, alternative="two-sided"
    ) for n in sample_sizes]
    ax.plot(sample_sizes, powers, label=label, linewidth=2, color=color)

ax.axhline(y=0.80, color="gray", linestyle="--", label="80% power target")
ax.axvline(x=n1, color="red", linestyle=":", label=f"Our n={n1}")
ax.set_xlabel("Sample Size per Group")
ax.set_ylabel("Statistical Power")
ax.set_title("Power Curves — How Sample Size Determines Detectable Effects")
ax.legend(loc="lower right")
ax.set_ylim(0, 1.05)
plt.tight_layout()
plt.savefig("figures/ch08_power_curves.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 40 nb=40
# EXTENSION — run as-is
# Simulate p-values when the null is true, and when it is false

np.random.seed(42)          # the same random draws on every run
n_simulations = 2000
n_per_group = 50

# Simulation 1: both groups come from the SAME distribution, so the null is true.
# _ stands for a value we never use: the loop counter, and the t-statistic
p_values_null = []
for _ in range(n_simulations):
    group_a = np.random.normal(loc=100, scale=15, size=n_per_group)
    group_b = np.random.normal(loc=100, scale=15, size=n_per_group)
    _, p = stats.ttest_ind(group_a, group_b, equal_var=False)
    p_values_null.append(p)

# Simulation 2: group B's mean is 7.5 higher, half of the SD of 15, so d = 0.5 and the null is false
p_values_alt = []
for _ in range(n_simulations):
    group_a = np.random.normal(loc=100, scale=15, size=n_per_group)
    group_b = np.random.normal(loc=107.5, scale=15, size=n_per_group)
    _, p = stats.ttest_ind(group_a, group_b, equal_var=False)
    p_values_alt.append(p)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(p_values_null, bins=20, color="steelblue", edgecolor="white")
# 20 bars share 2,000 p-values, so a flat histogram has 100 in each
axes[0].axhline(y=n_simulations / 20, color="red", linestyle="--", label="Expected if uniform")
axes[0].set_xlabel("P-value")
axes[0].set_ylabel("Frequency")
axes[0].set_title("P-values When Null Is TRUE")
axes[0].legend()

axes[1].hist(p_values_alt, bins=20, color="peru", edgecolor="white")
axes[1].set_xlabel("P-value")
axes[1].set_ylabel("Frequency")
axes[1].set_title("P-values When Null Is FALSE (d=0.5)")

plt.tight_layout()
plt.savefig("figures/ch08_pvalue_distributions.png", dpi=150, bbox_inches="tight")
plt.show()

# p < 0.05 is True or False for each run, so the mean is the share of runs below 0.05
false_positive_rate = np.mean(np.array(p_values_null) < 0.05)
true_positive_rate = np.mean(np.array(p_values_alt) < 0.05)
print(f"False positive rate (null true):   {false_positive_rate:.3f}")
print(f"True positive rate (null false):   {true_positive_rate:.3f}")
