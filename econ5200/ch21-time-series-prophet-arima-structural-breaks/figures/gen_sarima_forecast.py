"""Generate SARIMA(1,1,1)(1,1,1)[12] forecast on log CPI with 95% CI."""
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fredapi import Fred
from statsmodels.tsa.statespace.sarimax import SARIMAX
import os

OUT = os.path.join(os.path.dirname(__file__), 'ch21-sarima-cpi-forecast.png')

# Pull CPI from FRED
try:
    fred = Fred(api_key=os.environ.get('FRED_API_KEY', ''))
    cpi = fred.get_series('CPIAUCSL', observation_start='1990-01-01')
    cpi.index = pd.to_datetime(cpi.index)
except Exception:
    # Fallback: generate synthetic CPI-like data
    dates = pd.date_range('1990-01-01', '2025-12-01', freq='MS')
    np.random.seed(42)
    trend = np.linspace(5.0, 5.9, len(dates))
    seasonal = 0.003 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
    noise = np.cumsum(np.random.normal(0, 0.001, len(dates)))
    cpi = pd.Series(np.exp(trend + seasonal + noise), index=dates, name='CPI')

cpi_log = np.log(cpi)

# Fit SARIMA
model = SARIMAX(cpi_log, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False, enforce_invertibility=False)
fit = model.fit(disp=False, maxiter=200)

# Forecast 24 months
forecast = fit.get_forecast(steps=24)
pred_mean = forecast.predicted_mean
ci = forecast.conf_int(alpha=0.05)

# Plot last 60 months observed + 24-month forecast
fig, ax = plt.subplots(figsize=(12, 5))

obs_tail = cpi_log.iloc[-60:]
ax.plot(obs_tail.index, obs_tail.values, color='#4A7BA7', linewidth=2, label='Observed (log CPI)')
ax.plot(pred_mean.index, pred_mean.values, color='#E07B54', linewidth=2, label='SARIMA Forecast')
ax.fill_between(ci.index, ci.iloc[:, 0], ci.iloc[:, 1],
                alpha=0.2, color='#E07B54', label='95% Confidence Interval')

# Vertical line at forecast start
ax.axvline(x=obs_tail.index[-1], color='gray', linestyle='--', alpha=0.5, linewidth=1)

ax.set_xlabel('')
ax.set_ylabel('Log CPI', fontsize=12)
ax.legend(loc='upper left', frameon=True, fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(labelsize=10)

plt.tight_layout()
plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print(f"Saved: {OUT}")
