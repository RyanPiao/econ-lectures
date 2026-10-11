# Cells for the deck's mocked slides, copied verbatim by mock_cells.py pull.
# notebook: https://colab.research.google.com/github/RyanPiao/econ3916-student-notebooks/blob/main/3916/lab-ch14-guided.ipynb
# source: /Users/openclaw/Resilio Sync/documents/econ-project-book/econ-data-machine-learning/book/3916/labs/lab-ch14-guided.ipynb
# shown: 7 28   (the others run first, as the student's do)

# %% 3 nb=3
# GUIDED — run as-is
# Step 1: imports and the random generator
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan   # used in Step 5
from statsmodels.stats.stattools import jarque_bera          # used in Step 5
from sklearn.datasets import fetch_california_housing
from pathlib import Path

rng = np.random.default_rng(seed=42)    # Steps 2 and 4 and the Extension draw from rng, in order

# savefig will not create a folder, and a fresh Colab session has no figures/ folder
Path("figures").mkdir(exist_ok=True)

print("Setup complete.")

# %% 5 nb=5
# GUIDED — run as-is
# Step 2: errors whose spread grows with x, fitted with classical and with robust standard errors
n = 2_000
x = rng.uniform(1, 10, n)
TRUE_SLOPE = 2.0
y = 5 + TRUE_SLOPE * x + rng.normal(0, 0.5 * x, n)    # the error's standard deviation is 0.5 * x

fit = sm.OLS(y, sm.add_constant(x)).fit()                              # classical
rob = sm.OLS(y, sm.add_constant(x)).fit(cov_type="HC3", use_t=True)    # robust (HC3)

# <22 pads text to 22 characters; >10.4f right-aligns a number in 10, with 4 decimals
print(f"{'':<22}{'estimate':>10}{'std err':>10}{'95% CI':>22}")
print("-" * 66)
for label, res in [("classical", fit), ("robust (HC3)", rob)]:    # one (label, results) pair per pass
    lo, hi = res.conf_int()[1]
    ci = f"[{lo:.4f}, {hi:.4f}]"
    print(f"{label:<22}{res.params[1]:>10.4f}{res.bse[1]:>10.4f}{ci:>22}")
print(f"\nTrue slope: {TRUE_SLOPE}")

# %% 7 nb=7
# GUIDED — run as-is
# Step 3: how often does each interval contain the true slope? 400 simulated samples
TRIALS = 400
covered_classical = 0
covered_robust = 0
for i in range(TRIALS):
    r = np.random.default_rng(1000 + i)          # a fresh generator for each trial
    xi = r.uniform(1, 10, 400)
    yi = 5 + TRUE_SLOPE * xi + r.normal(0, 0.5 * xi, 400)
    Xi = sm.add_constant(xi)

    lo, hi = sm.OLS(yi, Xi).fit().conf_int()[1]
    covered_classical += lo <= TRUE_SLOPE <= hi   # True adds 1, False adds 0
    lo, hi = sm.OLS(yi, Xi).fit(cov_type="HC3", use_t=True).conf_int()[1]
    covered_robust += lo <= TRUE_SLOPE <= hi

# 6.1% prints a share as a percentage, 6 characters wide with 1 decimal: 0.918 prints as 91.8%
for label, count in [("classical", covered_classical), ("robust", covered_robust)]:
    p = count / TRIALS
    mc_se = np.sqrt(p * (1 - p) / TRIALS)
    print(f"{label:>10} interval covers the truth {p:6.1%}  (MC SE {mc_se:.1%})   nominal 95%")

# %% 12 nb=12
# GUIDED — run as-is
# Step 4: four residual patterns, four different problems
n = 600
xg = rng.uniform(0, 10, n)
panels = {
    "well behaved":      5 + 2 * xg + rng.normal(0, 1.5, n),
    "heteroskedastic":   5 + 2 * xg + rng.normal(0, 0.4 * xg, n),
    "missing curvature": 5 + 2 * xg - 0.25 * xg**2 + rng.normal(0, 1.5, n),
    "an outlier":        5 + 2 * xg + rng.normal(0, 1.5, n),
}
panels["an outlier"][0] = 60        # row 0's outcome, forced far above the line

fig, axes = plt.subplots(1, 4, figsize=(16, 3.6))
# zip pairs each of the four panels with one (name, outcome) pair
for ax, (name, yv) in zip(axes, panels.items()):
    res = sm.OLS(yv, sm.add_constant(xg)).fit()
    ax.scatter(res.fittedvalues, res.resid, s=6, alpha=0.5, color="darkslategray")
    ax.axhline(0, color="firebrick", lw=1)
    ax.set_title(name)
    ax.set_xlabel("fitted")
axes[0].set_ylabel("residual")
plt.tight_layout()
plt.savefig("figures/ch14_residual_patterns.png", dpi=150, bbox_inches="tight")
plt.show()

# %% 14 nb=14
# GUIDED — run as-is
# Step 5: a formal test beside each picture
for name, yv in panels.items():
    res = sm.OLS(yv, sm.add_constant(xg)).fit()
    bp = het_breuschpagan(res.resid, res.model.exog)
    jb = jarque_bera(res.resid)
    # <8.4f left-aligns the number in 8 characters, so the second test lines up
    print(f"{name:<20} Breusch-Pagan p={bp[1]:<8.4f} Jarque-Bera p={jb[1]:.4f}")

# %% 19 nb=19
# GUIDED — run as-is
# Step 6: leverage, standardised residual and Cook's distance for the outlier panel
yo = panels["an outlier"]
fit_o = sm.OLS(yo, sm.add_constant(xg)).fit()
infl = fit_o.get_influence()
lev = infl.hat_matrix_diag
std_resid = infl.resid_studentized_internal
cooks = infl.cooks_distance[0]

order = np.argsort(cooks)[::-1][:5]       # the five largest Cook's distances, largest first

print(f"{'obs':>6}{'leverage':>11}{'std resid':>12}{'Cook D':>10}")
print("-" * 40)
for i in order:
    print(f"{i:>6}{lev[i]:>11.4f}{std_resid[i]:>12.3f}{cooks[i]:>10.4f}")

# %% 21 nb=21
# GUIDED — run as-is
# Step 7: delete the most influential row and fit again
top = order[0]                             # the row with the largest Cook's distance
without = sm.OLS(np.delete(yo, top), sm.add_constant(np.delete(xg, top))).fit()

label_with = f"with obs {top}"
label_without = f"without obs {top}"
print(f"{'':<22}{'slope':>10}{'std err':>10}")
print("-" * 42)
print(f"{label_with:<22}{fit_o.params[1]:>10.4f}{fit_o.bse[1]:>10.4f}")
print(f"{label_without:<22}{without.params[1]:>10.4f}{without.bse[1]:>10.4f}")

shift = abs(fit_o.params[1] - without.params[1])
# .0% prints a share as a whole percentage: 0.33 prints as 33%
print(f"\nthe slope moved      {shift:.4f}, which is {shift / fit_o.bse[1]:.2f} of its own standard error")
print(f"the standard error   fell {1 - without.bse[1] / fit_o.bse[1]:.0%}, "
      f"from {fit_o.bse[1]:.4f} to {without.bse[1]:.4f}")

# %% 26 nb=26
# GUIDED — run as-is
# Step 8: one real regression, classical and robust standard errors side by side
data = fetch_california_housing(as_frame=True)
ca = data.frame.rename(columns={"MedHouseVal": "value"})    # the outcome gets the shorter name

feat = ["MedInc", "HouseAge", "AveRooms", "AveOccup"]
fit_ca = sm.OLS(ca["value"], sm.add_constant(ca[feat])).fit()
fit_ca_hc3 = sm.OLS(ca["value"], sm.add_constant(ca[feat])).fit(cov_type="HC3", use_t=True)

print(f"{'term':<12}{'coef':>10}{'classical SE':>14}{'HC3 SE':>10}{'ratio':>8}")
print("-" * 54)
for name in fit_ca.params.index:
    ratio = fit_ca_hc3.bse[name] / fit_ca.bse[name]
    print(f"{name:<12}{fit_ca.params[name]:>10.4f}{fit_ca.bse[name]:>14.4f}"
          f"{fit_ca_hc3.bse[name]:>10.4f}{ratio:>8.2f}")

# %% 28 nb=28
# GUIDED — run as-is
# Step 9: residuals against fitted values, and the districts at the 5.0 ceiling
fig, ax = plt.subplots(figsize=(9, 4.5))
ax.scatter(fit_ca.fittedvalues, fit_ca.resid, s=3, alpha=0.15, color="darkslategray")
ax.axhline(0, color="firebrick", lw=1)
ax.set_xlabel("fitted value")
ax.set_ylabel("residual")
ax.set_title("California Housing: residuals vs fitted")
plt.tight_layout()
plt.savefig("figures/ch14_california_residuals.png", dpi=150, bbox_inches="tight")
plt.show()

at_ceiling = (ca["value"] > 5).sum()
below = ca[ca["value"] <= 5]          # every district not at the ceiling
# .2% prints a share as a percentage with 2 decimals; :, adds a thousands comma
print(f"{at_ceiling} of {len(ca):,} districts sit at the ceiling ({at_ceiling / len(ca):.2%})")
print(f"{len(below):,} districts are below it")
