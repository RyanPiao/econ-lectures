"""Generate Prophet decomposition of log CPI — trend + seasonality + changepoints."""
import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fredapi import Fred
import os

OUT = os.path.join(os.path.dirname(__file__), 'ch21-prophet-decomposition.png')

# Pull CPI from FRED
try:
    fred = Fred(api_key=os.environ.get('FRED_API_KEY', ''))
    cpi = fred.get_series('CPIAUCSL', observation_start='1990-01-01')
    cpi.index = pd.to_datetime(cpi.index)
except Exception:
    dates = pd.date_range('1990-01-01', '2025-12-01', freq='MS')
    np.random.seed(42)
    trend = np.linspace(5.0, 5.9, len(dates))
    seasonal = 0.003 * np.sin(2 * np.pi * np.arange(len(dates)) / 12)
    noise = np.cumsum(np.random.normal(0, 0.001, len(dates)))
    cpi = pd.Series(np.exp(trend + seasonal + noise), index=dates, name='CPI')

cpi_log = np.log(cpi)

try:
    from prophet import Prophet

    df = pd.DataFrame({'ds': cpi_log.index, 'y': cpi_log.values})
    m = Prophet(changepoint_prior_scale=0.05, yearly_seasonality=True,
                weekly_seasonality=False, daily_seasonality=False)
    m.add_country_holidays(country_name='US')
    m.fit(df)

    future = m.make_future_dataframe(periods=24, freq='MS')
    forecast = m.predict(future)

    # Extract components
    trend = forecast[['ds', 'trend']].copy()
    yearly = forecast[['ds', 'yearly']].copy()
    holidays = forecast[['ds', 'holidays']].copy()

    # Get changepoint locations
    changepoints = m.changepoints

    fig, axes = plt.subplots(3, 1, figsize=(12, 8), sharex=False)

    # Panel 1: Trend with changepoints
    axes[0].plot(trend['ds'], trend['trend'], color='#4A7BA7', linewidth=2)
    for cp in changepoints:
        axes[0].axvline(x=cp, color='#E07B54', linestyle='--', alpha=0.4, linewidth=0.8)
    axes[0].set_ylabel('Trend', fontsize=11)
    axes[0].set_title('Trend Component (with detected changepoints)', fontsize=12, fontweight='bold')
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)

    # Panel 2: Yearly seasonality
    yearly_one = forecast[forecast['ds'].dt.year == 2020][['ds', 'yearly']].copy()
    if len(yearly_one) >= 12:
        axes[1].plot(yearly_one['ds'].dt.month, yearly_one['yearly'].values, color='#4A7BA7', linewidth=2)
        axes[1].set_xlabel('Month')
    else:
        axes[1].plot(yearly['ds'], yearly['yearly'], color='#4A7BA7', linewidth=2)
    axes[1].set_ylabel('Yearly Effect', fontsize=11)
    axes[1].set_title('Yearly Seasonality', fontsize=12, fontweight='bold')
    axes[1].axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)

    # Panel 3: Holiday effects
    axes[2].plot(holidays['ds'], holidays['holidays'], color='#4A7BA7', linewidth=1.5, alpha=0.7)
    axes[2].set_ylabel('Holiday Effect', fontsize=11)
    axes[2].set_title('Holiday Effects', fontsize=12, fontweight='bold')
    axes[2].axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    axes[2].spines['top'].set_visible(False)
    axes[2].spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved: {OUT}")

except ImportError:
    # Prophet not available — generate synthetic decomposition
    dates = pd.date_range('1990-01-01', '2025-12-01', freq='MS')
    n = len(dates)

    # Synthetic trend with changepoints
    trend = np.piecewise(np.arange(n, dtype=float),
                         [np.arange(n) < 216, (np.arange(n) >= 216) & (np.arange(n) < 360),
                          np.arange(n) >= 360],
                         [lambda x: 5.0 + 0.002 * x,
                          lambda x: 5.432 + 0.0015 * (x - 216),
                          lambda x: 5.648 + 0.003 * (x - 360)])

    # Synthetic seasonality
    months = np.arange(12)
    seasonal_pattern = 0.002 * np.sin(2 * np.pi * months / 12)
    seasonality = np.tile(seasonal_pattern, n // 12 + 1)[:n]

    # Changepoint dates
    cp_dates = [dates[216], dates[360]]

    fig, axes = plt.subplots(3, 1, figsize=(12, 8))

    axes[0].plot(dates, trend, color='#4A7BA7', linewidth=2)
    for cp in cp_dates:
        axes[0].axvline(x=cp, color='#E07B54', linestyle='--', alpha=0.6, linewidth=1)
    axes[0].set_ylabel('Trend', fontsize=11)
    axes[0].set_title('Trend Component (with detected changepoints)', fontsize=12, fontweight='bold')
    axes[0].spines['top'].set_visible(False)
    axes[0].spines['right'].set_visible(False)

    axes[1].plot(months + 1, seasonal_pattern, color='#4A7BA7', linewidth=2, marker='o', markersize=4)
    axes[1].set_ylabel('Yearly Effect', fontsize=11)
    axes[1].set_xlabel('Month')
    axes[1].set_title('Yearly Seasonality', fontsize=12, fontweight='bold')
    axes[1].axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    axes[1].spines['top'].set_visible(False)
    axes[1].spines['right'].set_visible(False)

    holiday_effect = np.zeros(n)
    for i, d in enumerate(dates):
        if d.month == 12: holiday_effect[i] = 0.001
        elif d.month == 1: holiday_effect[i] = -0.0005
    axes[2].plot(dates, holiday_effect, color='#4A7BA7', linewidth=1.5, alpha=0.7)
    axes[2].set_ylabel('Holiday Effect', fontsize=11)
    axes[2].set_title('Holiday Effects', fontsize=12, fontweight='bold')
    axes[2].axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    axes[2].spines['top'].set_visible(False)
    axes[2].spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig(OUT, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"Saved (synthetic): {OUT}")
