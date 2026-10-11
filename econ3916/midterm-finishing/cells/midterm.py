# %% l1_read_fails
import pandas as pd
raw = pd.read_csv("data/wdi_extract.csv")
# %% l1_peek
with open("data/wdi_extract.csv") as f:
    for _ in range(5):
        print(f.readline().rstrip()[:60])
# %% l1_read
raw = pd.read_csv("data/wdi_extract.csv", skiprows=4)
print(raw.shape)
# %% l1_record
SOURCE = "https://databank.worldbank.org/source/world-development-indicators"
DOWNLOADED = "2025-08-15"          # the day you clicked Download
with open("data/wdi_extract.csv") as f:
    LAST_UPDATED = [next(f) for _ in range(3)][2].split(",")[1].strip('"')
print("source:", SOURCE)
print("last updated:", LAST_UPDATED, "| downloaded:", DOWNLOADED)
# %% l2_shape
print(raw.shape)
print(raw.columns[[0, 1, 2, 3, 4, -2, -1]].tolist())
print(raw[["Country Code", "Indicator Code", "2010"]].head(4))
# %% l2_unit
print(raw["Country Code"].nunique(), "countries x",
      raw["Indicator Code"].nunique(), "indicators =", len(raw), "rows")
# %% l2_melt
raw = raw.dropna(axis=1, how="all")      # the empty "Unnamed: 14"
ids = ["Country Name", "Country Code",
       "Indicator Name", "Indicator Code"]
long = raw.melt(id_vars=ids, var_name="year", value_name="value")
print(long.shape)
print(long["year"].dtype)
# %% l2_pivot
short = {"SL.TLF.CACT.FE.NE.ZS": "flfp",
         "NY.GDP.PCAP.KD": "gdp_pc",
         "SP.DYN.TFRT.IN": "fertility"}
long["var"] = long["Indicator Code"].map(short)
long = long.rename(columns={"Country Name": "country",
                            "Country Code": "code"})
panel = (long.pivot(index=["country", "code", "year"],
                    columns="var", values="value")
             .reset_index().rename_axis(columns=None))
panel["year"] = panel["year"].astype(int)
print(panel.shape)
print(panel.head(3).round(1).to_string(index=False))
# %% l2_why_int
leave = pd.read_csv("data/leave_weeks.csv")
panel.astype({"year": str}).merge(leave, on=["country", "year"])
# %% l2_check_unit
print(panel.duplicated(["code", "year"]).sum())
print(long.duplicated(["code", "year"]).sum())
# %% l3_count
print(panel.isna().sum())
# %% l3_where
vars3 = ["flfp", "gdp_pc", "fertility"]
gaps = panel.set_index(["code", "year"])[vars3].isna()
by_country = gaps.groupby("code").sum()
print(by_country[by_country.sum(axis=1) > 0])
g = gaps.reset_index()
for v in vars3:
    rows = g[g[v]]
    print(v, sorted(set(rows["code"])), rows["year"].tolist())
# %% l3_random
flfp_gap = panel.groupby("code")["flfp"].apply(lambda s: s.isna().any())
has_gap = panel["code"].map(flfp_gap).rename("has a flfp gap")
print(panel.groupby(has_gap)["gdp_pc"].median().round(0))
# %% l3_dropna
kept = panel.dropna()
print(len(panel), "->", len(kept))
print((panel.groupby("code").size() - kept.groupby("code").size())
      .loc[lambda s: s > 0])
# %% l4_naive
leave = pd.read_csv("data/leave_weeks.csv")
m = panel.merge(leave, on=["country", "year"])
print(len(panel), len(leave), len(m))
# %% l4_indicator
m = panel.merge(leave, on=["country", "year"], how="outer", indicator=True)
print(m["_merge"].value_counts())
print(sorted(m.loc[m["_merge"] == "left_only", "country"].unique()))
print(sorted(m.loc[m["_merge"] == "right_only", "country"].unique()))
# %% l4_fix
fix = {"Egypt": "Egypt, Arab Rep.", "South Korea": "Korea, Rep.",
       "Turkey": "Turkiye", "Vietnam": "Viet Nam"}
leave["country"] = leave["country"].replace(fix)
merged = panel.merge(leave, on=["country", "year"], how="outer",
                     indicator=True, validate="one_to_one")
print(merged["_merge"].value_counts())
merged = merged.drop(columns="_merge")
print(merged.shape)
# %% r_summary
df = merged.dropna().copy()
cols = {"flfp": "Female LFP (% of women 15+)", "gdp_pc": "GDP per capita (2015 US$)",
        "fertility": "Fertility (births per woman)", "leave_weeks": "Paid leave (weeks)"}
tab = df[list(cols)].describe().T[["count", "mean", "std", "min", "max"]]
tab.index = list(cols.values())
print(tab.round(1).to_string())
print(df["code"].nunique(), "countries,", df["year"].min(), "to", df["year"].max())
# %% r_figure
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(6.4, 4.0), dpi=150)
ax.scatter(df["gdp_pc"], df["flfp"], s=14, color="#2a5a8a", alpha=0.7)
ax.set_xscale("log")
ax.xaxis.set_major_locator(plt.FixedLocator([2000, 5000, 10000, 20000]))
ax.xaxis.set_minor_locator(plt.NullLocator())
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))
ax.set_xlabel("GDP per capita, constant 2015 US$ (log scale)")
ax.set_ylabel("Female labour force participation (%)")
ax.set_ylim(0, 100)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig("../figures/flfp_gdp.png")
cm = df.groupby("code")[["gdp_pc", "flfp"]].mean()
cm["third"] = pd.qcut(cm["gdp_pc"], 3, labels=["poorest", "middle", "richest"])
print(cm.groupby("third", observed=True)["flfp"].mean().round(1))
print(round(df[["flfp", "gdp_pc"]].corr().iloc[0, 1], 2),
      round(np.corrcoef(df["flfp"], np.log(df["gdp_pc"]))[0, 1], 2))
# %% r_model
import statsmodels.formula.api as smf
res = smf.ols("flfp ~ np.log(gdp_pc) + fertility + leave_weeks", data=df).fit(cov_type="HC1")
print(pd.DataFrame({"coef": res.params, "se": res.bse}).round(3))
print(int(res.nobs), round(res.rsquared, 3))
print(res.conf_int().round(2))
ci = res.conf_int().loc["np.log(gdp_pc)"] * np.log(1.10)
print(round(res.params["np.log(gdp_pc)"] * np.log(1.10), 2), ci.round(2).tolist())
# %% r_diag
from statsmodels.stats.diagnostic import het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor
plain = smf.ols("flfp ~ np.log(gdp_pc) + fertility + leave_weeks", data=df).fit()
print(f"{het_breuschpagan(plain.resid, plain.model.exog)[1]:.1e}")
X = plain.model.exog
print({n: round(float(variance_inflation_factor(X, i)), 2)
       for i, n in enumerate(plain.model.exog_names) if i > 0})
cook = plain.get_influence().cooks_distance[0]
print(round(float(cook.max()), 3), int((cook > 4 / len(df)).sum()), len(df))
big = cook > 4 / len(df)
print(df.loc[big, ["code", "year"]].to_string(index=False))
print(round(float(np.sqrt(variance_inflation_factor(X, 1))), 2))
refit = smf.ols("flfp ~ np.log(gdp_pc) + fertility + leave_weeks",
                data=df.loc[~big]).fit(cov_type="HC1")
print(round(res.params["np.log(gdp_pc)"], 3), "->", round(refit.params["np.log(gdp_pc)"], 3))
