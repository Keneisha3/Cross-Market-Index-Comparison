import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

# Use dark background
plt.style.use('dark_background')

# Define tickers and date range
tickers = {'Nikkei 225': '^N225', 'DJIA': '^DJI'}
start_date = '2023-01-01'
end_date = '2025-06-30'

# Download closing price data
data = yf.download(list(tickers.values()), start=start_date, end=end_date)['Close']
data.columns = list(tickers.keys())

# Calculate daily returns
daily_returns = data.pct_change() * 100

# Monthly returns (resample to month-end)
monthly_returns = data.resample('ME').last().pct_change() * 100

# Calculate annual returns
annual_returns = {}
annual_lines = {}  # store start and end values for each year

for year in [2023, 2024, 2025]:
    if year == 2025:
        year_data = data.loc['2025-01-01':'2025-06-30'].dropna()
        end_date_str = '2025-06-30'
    else:
        year_data = data.loc[f'{year}-01-01':f'{year}-12-31'].dropna()
        end_date_str = f'{year}-12-31'
    
    if year_data.empty:
        continue

    first = year_data.iloc[0]
    last = year_data.iloc[-1]
    returns = ((last - first) / first * 100).round(2)
    annual_returns[str(year)] = returns

    # Store the return line segment for plotting
    for index in tickers.keys():
        if index not in annual_lines:
            annual_lines[index] = []
        annual_lines[index].append({
            'x': [pd.to_datetime(f'{year}-01-01'), pd.to_datetime(end_date_str)],
            'y': [0, ((last[index] - first[index]) / first[index]) * 100]
        })

# Convert to DataFrame
annual_df = pd.DataFrame(annual_returns).T.dropna().astype(float)
print("\nAnnual Return DataFrame:\n", annual_df)

# Plotting setup
fig, ax1 = plt.subplots(figsize=(16, 8))
ax2 = ax1.twinx()

colors = {'Nikkei 225': '#00FFCC', 'DJIA': '#FF4C4C'}
bar_width = 15  # days

# Plot daily returns
ax1.plot(daily_returns.index, daily_returns['Nikkei 225'], alpha=0.3, label='Nikkei 225 Daily', color=colors['Nikkei 225'])
ax1.plot(daily_returns.index, daily_returns['DJIA'], alpha=0.3, label='DJIA Daily', color=colors['DJIA'])

# Plot monthly returns as bars
dates = monthly_returns.index
ax1.bar(dates - pd.Timedelta(days=bar_width/2), monthly_returns['Nikkei 225'],
        width=bar_width, label='Nikkei 225 Monthly', color=colors['Nikkei 225'], alpha=0.5)
ax1.bar(dates + pd.Timedelta(days=bar_width/2), monthly_returns['DJIA'],
        width=bar_width, label='DJIA Monthly', color=colors['DJIA'], alpha=0.5)

# Plot annual return trajectory lines
for index_name, segments in annual_lines.items():
    for seg in segments:
        ax2.plot(seg['x'], seg['y'], linestyle='--', color=colors[index_name], linewidth=2, alpha=0.7)

# Plot annual return markers
label_added = {'Nikkei 225': False, 'DJIA': False}
for year_str in annual_df.index:
    if year_str == '2025':
        x = pd.to_datetime(year_str + "-06-30")
    else:
        x = pd.to_datetime(year_str + "-12-31")
    for index_name in ['Nikkei 225', 'DJIA']:
        y = annual_df.loc[year_str, index_name]
        label = None
        if not label_added[index_name]:
            label = f"{index_name} Annual"
            label_added[index_name] = True
        ax2.plot(x, y, marker='D', linestyle='None', markersize=10,
                 label=label, color=colors[index_name], zorder=10)

# Axis labels and formatting
ax1.set_title("Nikkei 225 vs DJIA - Daily, Monthly and Annual Returns (YTD June 30, 2025)", fontsize=16, color='white')
ax1.set_xlabel("Date", fontsize=12, color='white')
ax1.set_ylabel("Daily and Monthly Return (%)", fontsize=12, color='white')
ax2.set_ylabel("Annual Return (%)", fontsize=12, color='white')

# Monthly ticks
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))

# Colors
ax1.tick_params(axis='both', colors='white')
ax2.tick_params(axis='y', colors='white')

# Legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', facecolor='black', edgecolor='white', framealpha=0.8)

# Grid and layout
ax1.grid(True, linestyle='--', alpha=0.3)
plt.tight_layout()
plt.show()
