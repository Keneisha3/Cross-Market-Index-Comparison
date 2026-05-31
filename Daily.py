import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Use dark background style
plt.style.use('dark_background')

# Define tickers and date range
tickers = {'Nikkei 225': '^N225', 'DJIA': '^DJI'}
start_date = '2023-01-01'
end_date = '2025-06-30'

# Download daily data (default frequency)
data = yf.download(list(tickers.values()), start=start_date, end=end_date)['Close']
data.columns = list(tickers.keys())

# Plot setup
fig, ax = plt.subplots(figsize=(14, 7))

# Bright custom colors
colors = {
    'Nikkei 225': '#00FFCC',  # bright cyan
    'DJIA': '#FF6F61',        # bright coral
}

# Plot each index
for index in data.columns:
    ax.plot(data.index, data[index], label=index, linewidth=1.5, color=colors.get(index, 'white'))

# Format x-axis with daily ticks spaced for clarity
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))  # Show a tick every 3 months
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.xticks(rotation=45, ha='right')

# Styling
ax.set_title('📈 Daily Index Performance: Nikkei 225 vs DJIA (Jan 2023 – Jun 2025)', fontsize=16, fontweight='bold', color='white')
ax.set_xlabel('Date', fontsize=12, color='white')
ax.set_ylabel('Index Value', fontsize=12, color='white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(fontsize=12, loc='upper left', facecolor='black', edgecolor='white')

# Optimize layout
plt.tight_layout()
plt.show()
