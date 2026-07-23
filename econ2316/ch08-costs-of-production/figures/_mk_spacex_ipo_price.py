"""SPCX daily closes since the 12 Jun 2026 IPO.
Data: Yahoo Finance chart API, pulled 2026-07-23. Closes are real, not modelled.
To refresh: re-pull the series and replace DATA below."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os

HERE=os.path.dirname(os.path.abspath(__file__))
PRIMARY="#2D2D2D"; SECONDARY="#6B8BA4"; ACCENT="#C47B5A"
MUTED="#8C8580"; LINE="#D5CEC7"; DANGER="#A85C5C"; SUCCESS="#3F7A4F"
plt.rcParams.update({"figure.facecolor":"white","savefig.facecolor":"white",
                     "savefig.bbox":"tight","savefig.dpi":150})

IPO_PRICE=135.00
DATA=[('2026-06-12', 160.95), ('2026-06-15', 192.5), ('2026-06-16', 211.39), ('2026-06-17', 191.82), ('2026-06-18', 185.0), ('2026-06-22', 154.6), ('2026-06-23', 156.11), ('2026-06-24', 154.54), ('2026-06-25', 153.0), ('2026-06-26', 153.23), ('2026-06-29', 164.19), ('2026-06-30', 170.86), ('2026-07-01', 157.54), ('2026-07-02', 162.0), ('2026-07-06', 160.42), ('2026-07-07', 149.47), ('2026-07-08', 148.3), ('2026-07-09', 152.16), ('2026-07-10', 145.3), ('2026-07-13', 139.14), ('2026-07-14', 136.08), ('2026-07-15', 135.27), ('2026-07-16', 131.11), ('2026-07-17', 123.99), ('2026-07-20', 119.85), ('2026-07-21', 123.54), ('2026-07-22', 115.26), ('2026-07-23', 111.83)]

dates=[datetime.strptime(d,"%Y-%m-%d") for d,_ in DATA]
close=[c for _,c in DATA]

fig,ax=plt.subplots(figsize=(8.6,4.7))

# shade above / below the IPO price
ax.fill_between(dates, close, IPO_PRICE, where=[c>=IPO_PRICE for c in close],
                color=SUCCESS, alpha=0.13, interpolate=True, zorder=1)
ax.fill_between(dates, close, IPO_PRICE, where=[c<IPO_PRICE for c in close],
                color=DANGER, alpha=0.13, interpolate=True, zorder=1)

ax.axhline(IPO_PRICE, color=SECONDARY, ls="--", lw=1.5, zorder=3)
ax.plot(dates, close, color=PRIMARY, lw=2.3, zorder=4)

imax=close.index(max(close))
pts=[(0,"Day-1 close",  52, -20, SUCCESS),
     (imax,"Peak",       0, 20, SUCCESS),
     (len(close)-1,"Today", -30, -36, DANGER)]
for i,lbl,dx,dy,col in pts:
    ax.plot(dates[i], close[i], "o", color=col, markersize=8,
            markeredgecolor="white", markeredgewidth=1.5, zorder=6)
    ax.annotate(f"{lbl}\n\\${close[i]:,.2f}", xy=(dates[i],close[i]),
                xytext=(dx,dy), textcoords="offset points",
                fontsize=10, fontweight="bold", color=col,
                ha="center", zorder=7, linespacing=1.35)

ax.text(dates[len(dates)//2], IPO_PRICE+3.5, r"IPO price  \$135",
        fontsize=10, color=SECONDARY, fontweight="bold",
        fontstyle="italic", ha="center", va="bottom", zorder=5)

ax.set_title("SPCX  ·  SpaceX on the Nasdaq since its 12 June 2026 IPO",
             fontsize=13.5, fontweight="bold", color=PRIMARY, pad=26)
ax.text(0.5,1.045, r"Raised \$75B at a \$1.77T valuation  ·  the largest IPO ever",
        transform=ax.transAxes, ha="center", va="bottom", fontsize=10, color=MUTED)
ax.set_ylabel("Share price (USD)", fontsize=10.5, fontstyle="italic")
ax.set_ylim(90, 236)
ax.set_yticks([100,135,160,185,210])
ax.set_yticklabels([r"\$100",r"\$135",r"\$160",r"\$185",r"\$210"], fontsize=9.5)
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=1))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
plt.setp(ax.get_xticklabels(), fontsize=9.5)
ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
ax.grid(axis="y", color=LINE, lw=0.6); ax.set_axisbelow(True)
ax.text(0.0,-0.20,"Daily closing prices, all %d trading days since listing.  Source: Yahoo Finance, 23 Jul 2026." % len(DATA),
        transform=ax.transAxes, ha="left", va="top", fontsize=8.5,
        color=MUTED, fontstyle="italic")
plt.savefig(os.path.join(HERE,"fig-spacex-ipo-price.png"))
plt.close(fig)
print("wrote fig-spacex-ipo-price.png")
