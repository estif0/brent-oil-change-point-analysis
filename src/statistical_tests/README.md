# Statistical Tests Module

This module provides statistical tests for time series analysis, particularly stationarity testing which is crucial for many time series models.

## Files

### `stationarity.py`
Contains the `StationarityTester` class for testing whether a time series is stationary.

**Key Features:**
- Augmented Dickey-Fuller (ADF) test
- Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test
- Human-readable interpretation of test results
- Comprehensive stationarity analysis combining both tests

**Core Methods:**
- `adf_test()` - Perform ADF test for stationarity
- `kpss_test()` - Perform KPSS test for stationarity
- `interpret_results()` - Get human-readable interpretation
- `comprehensive_stationarity_test()` - Run both tests and provide overall conclusion

**Usage Example:**
```python
from src.data import BrentDataLoader
from src.statistical_tests import StationarityTester

# Load data
loader = BrentDataLoader()
data = loader.load_data('data/raw/BrentOilPrices.csv')

# Test stationarity
tester = StationarityTester()

# Run comprehensive test
results = tester.comprehensive_stationarity_test(
    data['Price'],
    series_name="Brent Oil Prices"
)

print(results['conclusion'])
print(results['recommendation'])
print("\n" + results['adf_interpretation'])
print("\n" + results['kpss_interpretation'])

# Or run individual tests
adf_results = tester.adf_test(data['Price'])
kpss_results = tester.kpss_test(data['Price'])

if adf_results['is_stationary']:
    print(f"ADF test: Series is stationary (p={adf_results['p_value']:.4f})")
else:
    print(f"ADF test: Series is non-stationary (p={adf_results['p_value']:.4f})")
```

## Testing

Run tests with:
```bash
pytest tests/test_stationarity.py -v
```

All modules in this directory have corresponding test files in the `tests/` directory.

## Understanding Stationarity

### What is Stationarity?

A time series is **stationary** if its statistical properties (mean, variance, autocorrelation) remain constant over time. Stationarity is important because:
- Many time series models assume stationarity
- Non-stationary series can lead to spurious regressions
- Forecasting requires stable patterns

### The Two Tests

#### Augmented Dickey-Fuller (ADF) Test
- **Null Hypothesis (H0)**: Series has a unit root (non-stationary)
- **Alternative (H1)**: Series is stationary
- **Interpretation**: Low p-value (< 0.05) → Reject H0 → Series is stationary

#### KPSS Test
- **Null Hypothesis (H0)**: Series is stationary
- **Alternative (H1)**: Series has a unit root (non-stationary)
- **Interpretation**: High p-value (> 0.05) → Don't reject H0 → Series is stationary

**Note**: KPSS is the opposite of ADF!

### Interpreting Combined Results

| ADF Result     | KPSS Result    | Interpretation                           |
| -------------- | -------------- | ---------------------------------------- |
| Stationary     | Stationary     | ✅ Clearly stationary                     |
| Non-stationary | Non-stationary | ❌ Clearly non-stationary                 |
| Stationary     | Non-stationary | ⚠️ Trend-stationary (detrending may help) |
| Non-stationary | Stationary     | ⚠️ Mixed results (review data quality)    |

### Making Series Stationary

If a series is non-stationary, common transformations include:
1. **Differencing**: Subtract previous value from current value
2. **Log transformation**: Take natural logarithm of values
3. **Log returns**: `ln(P_t / P_{t-1})`
4. **Detrending**: Remove linear or polynomial trend

**Example:**
```python
# Test original prices
price_results = tester.comprehensive_stationarity_test(
    data['Price'],
    series_name="Prices"
)

# If non-stationary, try log returns
log_returns = np.log(data['Price'] / data['Price'].shift(1)).dropna()
returns_results = tester.comprehensive_stationarity_test(
    log_returns,
    series_name="Log Returns"
)
```

## Key Concepts

### Test Statistics
- **More negative ADF statistic** = More evidence for stationarity
- **Lower KPSS statistic** = More evidence for stationarity

### Critical Values
Both tests provide critical values at different significance levels (1%, 5%, 10%). If the test statistic is more extreme than the critical value, we reject the null hypothesis.

### P-values
- **p-value < 0.05**: Strong evidence against null hypothesis
- **p-value > 0.05**: Insufficient evidence to reject null hypothesis

### Lags
Both tests use lagged values to account for autocorrelation. The number of lags can be:
- Automatically selected (AIC, BIC)
- Manually specified
- Higher lags = more complex model but fewer observations
