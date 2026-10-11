# Cells for the deck's mocked slides, copied verbatim by mock_cells.py pull.
# notebook: https://colab.research.google.com/github/RyanPiao/econ3916-student-notebooks/blob/cb83a4e73597232201bf8e62024ba8019a8d66ca/3916/lab-ch08-guided.ipynb
# published: RyanPiao/econ3916-student-notebooks main @ cb83a4e (file last changed in 84f4107, 9 Oct; blob 1f5794c, 47 cells),
#   the copy the room opens. The book copy (49 cells) is HELD until 21 Oct, so cells come from this file.
# source: /Users/openclaw/econ-lectures/econ3916/ch08-hypothesis-testing-t-tests/cells/lab-ch08-guided.published-cb83a4e.ipynb
# shown: 16 21   (the others run first, as the student's do)

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
