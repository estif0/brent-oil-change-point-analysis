# Analysis Module

This module provides tools for analyzing detected change points from Bayesian models, associating them with historical events, and quantifying their impact.

## Classes

### ChangePointAnalyzer

Main class for comprehensive change point analysis.

**Key Features:**
- Identify change point locations with credible intervals
- Quantify impact (before/after statistics)
- Associate change points with historical events
- Generate human-readable impact statements
- Batch analysis pipeline

## Usage Examples

### Basic Analysis

```python
from src.analysis import ChangePointAnalyzer
from src.models import BayesianChangePointModel
from src.data import BrentDataLoader, EventDataLoader

# Load data
loader = BrentDataLoader()
data = loader.load_data()
log_returns = loader.calculate_log_returns()

# Load events
event_loader = EventDataLoader()
events = event_loader.load_events()

# Fit Bayesian model
model = BayesianChangePointModel(log_returns)
model.build_model()
trace = model.fit(samples=2000, tune=1000)

# Analyze change points
analyzer = ChangePointAnalyzer()
changepoints = analyzer.identify_changepoints(trace, log_returns)
impact = analyzer.quantify_impact(trace, log_returns)
associations = analyzer.associate_with_events(changepoints, events)

# Generate report
statement = analyzer.generate_impact_statement(
    changepoints[0], impact, associations[0]
)
print(statement)
```

### Batch Analysis

```python
# Complete analysis in one call
results = analyzer.batch_analyze(
    trace, log_returns, events, window_days=30
)

# Access all results
changepoints = results['changepoints']
impact = results['impact']
associations = results['associations']
statement = results['statement']

print(statement)
```

### Identifying Change Points

```python
# Identify with custom confidence level
changepoints = analyzer.identify_changepoints(
    trace, 
    data, 
    confidence=0.90,
    method='mean'
)

cp = changepoints[0]
print(f"Change point at: {cp['date']}")
print(f"Index: {cp['index']}")
print(f"90% Credible Interval: {cp['credible_interval']}")
```

### Quantifying Impact

```python
# Get detailed impact statistics
impact = analyzer.quantify_impact(trace, data, include_volatility=True)

print(f"Mean before: {impact['mu_before']:.4f}")
print(f"Mean after: {impact['mu_after']:.4f}")
print(f"Change: {impact['mean_change']:+.4f} ({impact['mean_change_pct']:+.2f}%)")
print(f"Direction: {impact['direction']}")
print(f"Magnitude: {impact['magnitude']}")

if 'sigma_before' in impact:
    print(f"\nVolatility before: {impact['sigma_before']:.4f}")
    print(f"Volatility after: {impact['sigma_after']:.4f}")
    print(f"Volatility direction: {impact['volatility_direction']}")
```

### Associating with Events

```python
# Find events near change points
associations = analyzer.associate_with_events(
    changepoints, 
    events, 
    window_days=30
)

for assoc in associations:
    if assoc['closest_event']:
        print(f"Change at {assoc['changepoint_date']}")
        print(f"Closest event: {assoc['closest_event']['event_name']}")
        print(f"Distance: {assoc['days_from_closest']} days")
        print(f"Events in window: {assoc['num_events_in_window']}")
```

## Output Examples

### Impact Statement

```
======================================================================
CHANGE POINT ANALYSIS SUMMARY
======================================================================

📍 Change Point Detected: 2008-09-15
   Index: 542
   94% Credible Interval: [2008-09-01, 2008-09-30]

📊 Impact on Mean:
   Before: 0.001234
   After:  -0.002456
   Change: -0.003690 (-299.03%)
   Direction: DECREASE
   Magnitude: LARGE

📈 Impact on Volatility:
   Before: 0.015234
   After:  0.028456
   Change: +0.013222 (+86.76%)
   Volatility: INCREASE

🌍 Associated Events:
   Event: Lehman Brothers Collapse
   Event Date: 2008-09-15
   Distance: 0 days
   Type: Financial Crisis
   Expected Impact: Negative

💡 Interpretation:
   Strong negative shift detected in the time series.
   Volatility increased, indicating higher market uncertainty.
   Timing closely aligns with major event (within 0 days).

======================================================================
```

### Change Point Dictionary

```python
{
    'index': 542,
    'date': Timestamp('2008-09-15'),
    'estimate_method': 'mean',
    'credible_interval': (535, 550),
    'ci_probability': 0.94,
    'posterior_std': 4.23,
    'posterior_samples': 4000,
    'ci_dates': (Timestamp('2008-09-01'), Timestamp('2008-09-30'))
}
```

### Impact Dictionary

```python
{
    'mu_before': 0.001234,
    'mu_after': -0.002456,
    'mu_before_ci': (0.000456, 0.002012),
    'mu_after_ci': (-0.003234, -0.001678),
    'mean_change': -0.003690,
    'mean_change_pct': -299.03,
    'direction': 'decrease',
    'magnitude': 'large',
    'magnitude_in_std': 1.85,
    'sigma_before': 0.015234,
    'sigma_after': 0.028456,
    'sigma_before_ci': (0.014123, 0.016345),
    'sigma_after_ci': (0.027123, 0.029789),
    'sigma_change': 0.013222,
    'sigma_change_pct': 86.76,
    'volatility_direction': 'increase'
}
```

### Association Dictionary

```python
{
    'changepoint_date': Timestamp('2008-09-15'),
    'changepoint_index': 542,
    'associated_events': [
        {
            'date': Timestamp('2008-09-15'),
            'event_name': 'Lehman Brothers Collapse',
            'event_type': 'Financial Crisis',
            'expected_impact': 'Negative',
            'days_from_changepoint': 0,
            'abs_days_from_changepoint': 0
        },
        # ... more events within window
    ],
    'closest_event': {
        'date': Timestamp('2008-09-15'),
        'event_name': 'Lehman Brothers Collapse',
        'event_type': 'Financial Crisis',
        'expected_impact': 'Negative',
        'days_from_changepoint': 0,
        'abs_days_from_changepoint': 0
    },
    'days_from_closest': 0,
    'num_events_in_window': 2
}
```

## Methods Reference

### identify_changepoints()

Extract change point locations from MCMC posterior.

**Parameters:**
- `trace` (InferenceData): MCMC samples
- `data` (pd.Series): Original time series
- `confidence` (float): Credible interval probability (default: 0.94)
- `method` (str): 'mean', 'median', or 'mode' (default: 'mean')

**Returns:** List of change point dictionaries

### quantify_impact()

Calculate before/after statistics and change magnitude.

**Parameters:**
- `trace` (InferenceData): MCMC samples
- `data` (pd.Series): Original time series
- `include_volatility` (bool): Include sigma analysis (default: True)

**Returns:** Dictionary with impact statistics

### associate_with_events()

Find events near change points.

**Parameters:**
- `changepoints` (list): Change point dictionaries
- `events` (pd.DataFrame): Historical events
- `window_days` (int): Search window in days (default: 30)
- `date_column` (str): Date column name (default: 'date')

**Returns:** List of association dictionaries

### generate_impact_statement()

Create human-readable report.

**Parameters:**
- `changepoint` (dict): Change point dictionary
- `impact` (dict): Impact dictionary
- `association` (dict, optional): Association dictionary

**Returns:** Formatted string

### batch_analyze()

Run complete analysis pipeline.

**Parameters:**
- `trace` (InferenceData): MCMC samples
- `data` (pd.Series): Original time series
- `events` (pd.DataFrame, optional): Historical events
- `window_days` (int): Search window (default: 30)

**Returns:** Dictionary with all results

## Design Considerations

### Change Point Identification

- Uses Highest Density Interval (HDI) for credible intervals
- Supports multiple point estimate methods (mean/median/mode)
- Returns both index and date (if available)
- Includes posterior standard deviation for uncertainty

### Impact Quantification

- Before/after means with credible intervals
- Absolute and percentage change calculations
- Direction classification (increase/decrease/minimal)
- Magnitude assessment based on standard deviations
  - Negligible: < 0.2σ
  - Small: 0.2-0.5σ
  - Moderate: 0.5-1.0σ
  - Large: 1.0-2.0σ
  - Very Large: > 2.0σ

### Event Association

- Time window-based search (default ±30 days)
- Distance metrics for all events in window
- Automatic identification of closest event
- Handles multiple events in window
- Flexible date column specification

### Impact Statements

- Structured format with clear sections
- Emoji visual markers for readability
- Quantitative information with context
- Interpretation guidelines based on magnitude
- Event causality assessment based on proximity

## Integration

This module integrates with:

- **src.models**: BayesianChangePointModel, ModelDiagnostics
- **src.data**: BrentDataLoader, EventDataLoader
- **src.visualization**: (Future) Plotting functions for change point analysis

## Testing

Comprehensive test suite in `tests/test_changepoint_analyzer.py`:
- 37 tests covering all methods
- Synthetic data with known change points
- Edge case and error handling tests
- Integration tests with full workflow

Run tests:
```bash
pytest tests/test_changepoint_analyzer.py -v
```
