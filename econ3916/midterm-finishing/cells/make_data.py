"""Write the two synthetic files the deck's worked examples read.

    python3 make_data.py          (run from this folder; writes data/)

Real country names, WDI country and indicator codes and the WDI bulk-download layout
(four metadata lines, years as columns, a trailing comma). Every number is generated
with a fixed seed. Nothing here is real data, and the slides say so.
"""
import csv
from pathlib import Path

import numpy as np

rng = np.random.default_rng(3916)
YEARS = list(range(2010, 2020))
# WDI name, ISO3, rough 2010 GDP per capita, rough fertility, country shift in female LFP
COUNTRIES = [
    ("Brazil", "BRA", 8700, 1.8, 2),
    ("Chile", "CHL", 12800, 1.8, -2),
    ("Egypt, Arab Rep.", "EGY", 3100, 3.2, -22),
    ("India", "IND", 1350, 2.5, -20),
    ("Indonesia", "IDN", 3100, 2.4, 4),
    ("Korea, Rep.", "KOR", 25000, 1.2, -6),
    ("Mexico", "MEX", 9300, 2.2, -8),
    ("Nigeria", "NGA", 2300, 5.6, 14),
    ("Poland", "POL", 11300, 1.4, -3),
    ("Turkiye", "TUR", 8700, 2.1, -16),
    ("Viet Nam", "VNM", 2200, 1.9, 18),
    ("South Africa", "ZAF", 6600, 2.4, 0),
]
IND = [
    ("Labor force participation rate, female (% of female population ages 15+) (national estimate)",
     "SL.TLF.CACT.FE.NE.ZS"),
    ("GDP per capita (constant 2015 US$)", "NY.GDP.PCAP.KD"),
    ("Fertility rate, total (births per woman)", "SP.DYN.TFRT.IN"),
]
# the gaps the deck teaches from: (ISO3, indicator code, years)
GAPS = [
    ("IND", "SL.TLF.CACT.FE.NE.ZS", range(2010, 2014)),   # series starts late
    ("NGA", "SL.TLF.CACT.FE.NE.ZS", range(2010, 2013)),
    ("NGA", "NY.GDP.PCAP.KD", range(2017, 2020)),         # series stops
    ("BRA", "SP.DYN.TFRT.IN", [2014]),                    # scattered single cells
    ("POL", "SP.DYN.TFRT.IN", [2011]),
    ("VNM", "SP.DYN.TFRT.IN", [2018]),
]
gap = {(c, i, y) for c, i, ys in GAPS for y in ys}

rows, leave = [], []
for name, iso, g0, f0, shift in COUNTRIES:
    growth = rng.normal(0.022, 0.01)
    gdp = [g0 * np.exp(growth * t + rng.normal(0, 0.015)) for t in range(len(YEARS))]
    fert = [max(1.0, f0 - 0.025 * t + rng.normal(0, 0.04)) for t in range(len(YEARS))]
    weeks0 = int(rng.choice([12, 14, 16, 18, 26]))
    lw = [weeks0 + (4 if (iso in ("CHL", "IND", "VNM") and y >= 2015) else 0) for y in YEARS]
    flfp = [min(80, max(15, 6.0 * np.log(g) - 6.5 * f + 0.25 * w + shift + 12 + rng.normal(0, 1.2)))
            for g, f, w in zip(gdp, fert, lw)]
    series = {"SL.TLF.CACT.FE.NE.ZS": (flfp, 3), "NY.GDP.PCAP.KD": (gdp, 1), "SP.DYN.TFRT.IN": (fert, 3)}
    for iname, code in IND:
        vals, nd = series[code]
        cells = ["" if (iso, code, y) in gap else f"{v:.{nd}f}" for y, v in zip(YEARS, vals)]
        rows.append([name, iso, iname, code] + cells)
    leave_name = {"Egypt, Arab Rep.": "Egypt", "Korea, Rep.": "South Korea",
                  "Turkiye": "Turkey", "Viet Nam": "Vietnam"}.get(name, name)
    leave += [[leave_name, y, w] for y, w in zip(YEARS, lw)]

out = Path("data"); out.mkdir(exist_ok=True)
with open(out / "wdi_extract.csv", "w", newline="") as fh:
    fh.write('"Data Source","World Development Indicators",\n\n')
    fh.write('"Last Updated Date","2025-07-01",\n\n')
    w = csv.writer(fh, quoting=csv.QUOTE_ALL, lineterminator=",\n")
    w.writerow(["Country Name", "Country Code", "Indicator Name", "Indicator Code"] + [str(y) for y in YEARS])
    for r in rows:
        w.writerow(r)
with open(out / "leave_weeks.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["country", "year", "leave_weeks"])
    w.writerows(leave)
print("wrote", out / "wdi_extract.csv", len(rows), "rows;", out / "leave_weeks.csv", len(leave), "rows")
