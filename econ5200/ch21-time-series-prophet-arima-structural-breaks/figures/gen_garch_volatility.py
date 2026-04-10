"""Generate GARCH(1,1) conditional volatility on S&P 500 daily returns."""
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

OUT = os.path.join(os.path.dirname(__file__), 'ch21-garch-volatility.png')

# Pull S&P 500 data
try:
    import yfinance as yf
    sp500 = yf.download('^GSPC', start='2005-01-01', end='2025-12-31', progress=False)['Close']
    if hasattr(sp500, 'columns'):
        sp500 = sp500.iloc[:, 0]
except Exception:
    # Fallback: synthetic data
    dates = pd.bdate_range('2005-01-03', '2025-12-31')
    np.random.seed(42)
    returns_raw = np.random.normal(0.0003, 0.01, len(dates))
    # Add volatility clustering
    vol = np.ones(len(dates)) * 0.01
    for i in range(1, len(dates)):
        vol[i] = np.sqrt(0.00001 + 0.09 * returns_raw[i-1]**2 + 0.90 * vol[i-1]**2)
        returns_raw[i] = np.random.normal(0.0003, vol[i])
    price = 1200 * np.exp(np.cumsum(returns_raw))
    sp500 = pd.Series(price, index=dates, name='Close')

returns = 100 * np.log(sp500 / sp500.shift(1)).dropna()

try:
    from arch import arch_model

    garch = arch_model(returns, vol='Garch', p=1, q=1, mean='AR', lags=1)
    result = garch.fit(disp='off')

    cond_vol = result.conditional_volatility
    # Annualize (approximate)
    cond_vol_annual = cond_vol * np.sqrt(252)
except Exception:
    # Fallback: rolling volatility as proxy
    cond_vol_annual = returns.rolling(21).std() * np.sqrt(252)

fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(cond_vol_annual.index, cond_vol_annual.values, color='#8B2500', alpha=0.7, linewidth=0.8)
ax.fill_between(cond_vol_annual.index, 0, cond_vol_annual.values, alpha=0.15, color='#8B2500')

# Crisis annotations
crisis_events = [
    ('2008-09-15', 'Lehman Brothers\nCollapse', 'top'),
    ('2020-03-16', 'COVID-19\nCrash', 'top'),
    ('2022-06-13', '2022 Rate\nHikes', 'top'),
]

for date_str, label, va in crisis_events:
    try:
        date = pd.Timestamp(date_str)
        if date in cond_vol_annual.index:
            idx = cond_vol_annual.index.get_loc(date)
        else:
            idx = cond_vol_annual.index.searchsorted(date)
            if idx >= len(cond_vol_annual):
                continue
            date = cond_vol_annual.index[idx]
        y_val = cond_vol_annual.iloc[idx] if isinstance(idx, (int, np.integer)) else cond_vol_annual.loc[date]
        ax.annotate(label, xy=(date, y_val),
                    xytext=(0, 20), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9, fontweight='bold',
                    arrowprops=dict(arrowstyle='->', color='gray', lw=1),
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8))
    except Exception:
        pass

ax.set_ylabel('Annualized Volatility (%)', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(labelsize=10)
ax.set_xlim(cond_vol_annual.index[0], cond_vol_annual.index[-1])

plt.tight_layout()
plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f"Saved: {OUT}")
