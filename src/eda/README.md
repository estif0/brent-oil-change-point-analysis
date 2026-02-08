# EDA Module

This module provides tools for exploratory data analysis of time series data, specifically designed for oil price analysis.

## Files

### `time_series_analysis.py`
Contains the `TimeSeriesAnalyzer` class for comprehensive time series analysis.

**Key Features:**
- Visualize raw price series with customizable styling
- Calculate and analyze log returns
- Compute rolling statistics (mean, standard deviation)
- Analyze volatility patterns over time
- Generate comprehensive summary statistics

**Core Methods:**
- `plot_price_series()` - Visualize price trends over time
- `calculate_log_returns()` - Compute logarithmic returns
- `plot_log_returns()` - Visualize returns distribution and time series
- `calculate_rolling_stats()` - Calculate rolling mean and standard deviation
- `plot_volatility()` - Comprehensive volatility analysis with multiple panels
- `get_summary_statistics()` - Generate detailed statistical summary

**Usage Example:**
```python
from src.data import BrentDataLoader
from src.eda import TimeSeriesAnalyzer
import matplotlib.pyplot as plt

# Load data
loader = BrentDataLoader()
data = loader.load_data('data/raw/BrentOilPrices.csv')

# Create analyzer
analyzer = TimeSeriesAnalyzer(data)

# Plot price series
fig1 = analyzer.plot_price_series()
plt.show()

# Calculate and plot log returns
log_returns = analyzer.calculate_log_returns()
fig2 = analyzer.plot_log_returns()
plt.show()

# Analyze volatility
fig3 = analyzer.plot_volatility(window=60)
plt.show()

# Get summary statistics
stats = analyzer.get_summary_statistics()
print(f"Mean price: ${stats['price_stats']['mean']:.2f}")
print(f"Volatility: {stats['returns_stats']['volatility']:.4f}")
```

## Testing

Run tests with:
```bash
pytest tests/test_time_series_analysis.py -v
```

All modules in this directory have corresponding test files in the `tests/` directory.

## Key Concepts

### Log Returns
Log returns are calculated as `ln(P_t / P_{t-1})` where P_t is the price at time t. Log returns have several advantages:
- They are additive over time
- They are symmetric (a gain of X% followed by a loss of X% returns to the original value)
- They are more suitable for statistical analysis

### Rolling Statistics
Rolling statistics are calculated over a moving window of specified size. They help identify:
- Trends (rolling mean)
- Volatility changes over time (rolling standard deviation)
- Regime changes in the data

### Volatility
Volatility measures the degree of price variation over time. We analyze:
- Price volatility (rolling standard deviation of prices)
- Returns volatility (rolling standard deviation of returns)
- Both help identify periods of market turbulence
