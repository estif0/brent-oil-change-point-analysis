# Brent Oil Change Point Analysis - Workflow Documentation

**Project**: Brent Oil Price Change Point Analysis  
**Client**: Birhan Energies  
**Date**: February 2026  
**Analysis Period**: May 1987 - September 2022

---

## Overview

This document outlines the complete workflow for analyzing Brent oil price changes using Bayesian change point detection. The analysis identifies how major geopolitical events, OPEC decisions, and economic shocks impact oil prices.

---

## Workflow Stages

### Stage 1: Data Acquisition and Validation

**Objective**: Load and validate historical Brent oil price data and event metadata.

#### 1.1 Price Data Loading
- **Input**: `data/raw/BrentOilPrices.csv`
- **Module**: `src.data.BrentDataLoader`
- **Process**:
  1. Load CSV file with date and price columns
  2. Parse dates using flexible date format detection
  3. Set dates as pandas DatetimeIndex
  4. Sort chronologically
  5. Convert prices to numeric type
  
- **Output**: DataFrame with DatetimeIndex and Price column
- **Validation Checks**:
  - File exists and is readable
  - Required columns present (Date, Price)
  - No duplicate dates
  - No negative prices
  - Missing values identified and documented
  
```python
from src.data import BrentDataLoader

loader = BrentDataLoader()
data = loader.load_data('data/raw/BrentOilPrices.csv')
validation = loader.validate_data()

if not validation['is_valid']:
    print("Warnings:", validation['warnings'])
```

#### 1.2 Event Data Loading
- **Input**: `data/events.csv`
- **Module**: `src.data.EventDataLoader`
- **Process**:
  1. Load events CSV with date, name, type, description, expected impact
  2. Parse event dates
  3. Sort chronologically
  4. Categorize by type (geopolitical, opec_decision, economic_shock, sanction)
  
- **Output**: DataFrame with event metadata
- **Event Types**:
  - Geopolitical: Wars, conflicts, political instability
  - OPEC Decision: Production quotas, policy changes
  - Economic Shock: Financial crises, disasters
  - Sanction: Trade restrictions, embargoes

```python
from src.data import EventDataLoader

event_loader = EventDataLoader()
events = event_loader.load_events('data/events.csv')
summary = event_loader.get_events_summary()
```

---

### Stage 2: Exploratory Data Analysis (EDA)

**Objective**: Understand the characteristics, patterns, and statistical properties of the price series.

#### 2.1 Price Series Visualization
- **Module**: `src.eda.TimeSeriesAnalyzer`
- **Process**:
  1. Plot raw price series over time
  2. Identify visual trends and patterns
  3. Note periods of high/low volatility
  4. Mark major historical events on timeline
  
- **Key Observations**:
  - Long-term trends (upward/downward/stationary)
  - Cyclical patterns
  - Structural breaks or regime changes
  - Outliers and extreme values

```python
from src.eda import TimeSeriesAnalyzer

analyzer = TimeSeriesAnalyzer(data)
fig = analyzer.plot_price_series()
```

#### 2.2 Returns Analysis
- **Process**:
  1. Calculate log returns: `ln(P_t / P_{t-1})`
  2. Plot returns time series
  3. Analyze returns distribution
  4. Calculate summary statistics (mean, std, skewness, kurtosis)
  
- **Why Log Returns?**:
  - Additive over time
  - Symmetric (treat gains/losses equally)
  - More suitable for statistical modeling
  - Closer to normal distribution

```python
log_returns = analyzer.calculate_log_returns()
fig = analyzer.plot_log_returns()
stats = analyzer.get_summary_statistics()
```

#### 2.3 Volatility Analysis
- **Process**:
  1. Calculate rolling mean (30, 60, 90 day windows)
  2. Calculate rolling standard deviation (price volatility)
  3. Calculate returns volatility
  4. Identify high/low volatility periods
  5. Correlate volatility spikes with known events
  
- **Insights**:
  - Volatility clustering (high volatility follows high volatility)
  - Event-driven volatility spikes
  - Periods of market stability vs. turbulence

```python
rolling_stats = analyzer.calculate_rolling_stats(window=60)
fig = analyzer.plot_volatility(window=60)
```

---

### Stage 3: Statistical Testing

**Objective**: Test statistical properties of the series, particularly stationarity.

#### 3.1 Stationarity Tests
- **Module**: `src.statistical_tests.StationarityTester`
- **Tests Performed**:
  1. **Augmented Dickey-Fuller (ADF) Test**
     - H0: Series has unit root (non-stationary)
     - H1: Series is stationary
     - Reject H0 if p-value < 0.05
  
  2. **KPSS Test**
     - H0: Series is stationary
     - H1: Series has unit root (non-stationary)
     - Reject H0 if p-value < 0.05

- **Process**:
  1. Test original price series
  2. Test log returns
  3. Compare results from both tests
  4. Determine if transformation is needed

```python
from src.statistical_tests import StationarityTester

tester = StationarityTester()

# Test prices
price_results = tester.comprehensive_stationarity_test(
    data['Price'],
    series_name='Brent Oil Prices'
)

# Test returns
log_returns = np.log(data['Price'] / data['Price'].shift(1)).dropna()
returns_results = tester.comprehensive_stationarity_test(
    log_returns,
    series_name='Log Returns'
)
```

#### 3.2 Expected Results
- **Raw Prices**: Typically non-stationary
  - Mean changes over time (trends)
  - Variance may be non-constant (heteroscedasticity)
  - Recommendation: Use log returns or differencing

- **Log Returns**: Typically stationary
  - Suitable for time series modeling
  - Can be used directly in Bayesian change point model

---

### Stage 4: Bayesian Change Point Modeling

**Objective**: Identify points in time where the statistical properties of the series change significantly.

#### 4.1 Model Specification
- **Module**: `src.models.BayesianChangePointModel`
- **Model Components**:
  1. **Change point (τ)**: Discrete uniform prior over time
  2. **Before parameters**: μ₁ (mean), σ₁ (std) before τ
  3. **After parameters**: μ₂ (mean), σ₂ (std) after τ
  4. **Likelihood**: Normal distribution with switching parameters

- **Mathematical Formulation**:
  ```
  τ ~ DiscreteUniform(0, T)
  μ₁, μ₂ ~ Normal(0, σ²)
  σ₁, σ₂ ~ HalfNormal(σ²)
  
  For t < τ:  y_t ~ Normal(μ₁, σ₁)
  For t ≥ τ:  y_t ~ Normal(μ₂, σ₂)
  ```

#### 4.2 Model Fitting
- **Inference Method**: Markov Chain Monte Carlo (MCMC)
- **Parameters**:
  - Samples: 2000-4000
  - Tuning steps: 1000-2000
  - Chains: 2-4 (for convergence checking)
  
- **Process**:
  1. Build PyMC model
  2. Run MCMC sampling
  3. Check convergence diagnostics (R-hat < 1.01)
  4. Extract posterior distributions

```python
from src.models import BayesianChangePointModel

model = BayesianChangePointModel(log_returns, n_changepoints=1)
model.build_model()
trace = model.fit(samples=2000, tune=1000, chains=4)
```

#### 4.3 Convergence Diagnostics
- **Module**: `src.models.diagnostics`
- **Checks**:
  1. R-hat values close to 1.0 (< 1.01)
  2. Trace plots show good mixing
  3. No divergences in sampling
  4. Effective sample size > 400

```python
from src.models import ModelDiagnostics

diagnostics = ModelDiagnostics()
convergence = diagnostics.check_convergence(trace)
diagnostics.plot_trace(trace, var_names=['tau', 'mu_1', 'mu_2'])
```

---

### Stage 5: Change Point Analysis

**Objective**: Extract and interpret change points, associate with events, and quantify impacts.

#### 5.1 Change Point Identification
- **Module**: `src.analysis.ChangePointAnalyzer`
- **Process**:
  1. Extract posterior distribution of τ
  2. Calculate posterior mode or mean
  3. Compute credible intervals (95% HDI)
  4. Convert index to date
  5. Identify top N change points if multiple

```python
from src.analysis import ChangePointAnalyzer

analyzer = ChangePointAnalyzer()
changepoints = analyzer.identify_changepoints(trace, confidence=0.95)
```

#### 5.2 Event Association
- **Process**:
  1. For each identified change point:
     - Search for events within ±30 day window
     - Rank events by proximity to change point
     - Consider event type and expected impact
  2. Create associations between change points and events
  3. Handle cases with multiple or no nearby events

```python
associations = analyzer.associate_with_events(
    changepoints,
    events,
    window_days=30
)
```

#### 5.3 Impact Quantification
- **Process**:
  1. Calculate before/after statistics:
     - Mean price/return before change point
     - Mean price/return after change point
     - Change in volatility
  2. Compute percentage change
  3. Estimate price shift magnitude
  4. Determine direction (increase/decrease)

```python
impact = analyzer.quantify_impact(trace, data, changepoint_date)
statement = analyzer.generate_impact_statement(changepoint_date, events)
```

#### 5.4 Impact Statement Example
```
Change Point: September 15, 2008
Associated Event: Global Financial Crisis (Lehman Brothers Collapse)
Impact: Price shifted from $96.50 to $76.20 USD/barrel (-21.0%)
Volatility: Increased by 85% following the event
Duration: Price remained depressed for 18 months
```

---

### Stage 6: Visualization and Reporting

**Objective**: Create clear, informative visualizations and written reports.

#### 6.1 Visualization Types
- **Module**: `src.visualization.plots`
- **Key Plots**:
  1. Price series with change points overlaid
  2. Event timeline with change points
  3. Posterior distribution of τ
  4. Before/after parameter comparisons
  5. Impact assessment plots

```python
from src.visualization import plots

fig1 = plots.plot_price_with_changepoints(data, changepoints, events)
fig2 = plots.plot_changepoint_distribution(trace)
fig3 = plots.plot_parameter_comparison(trace)
fig4 = plots.plot_event_impact(data, event_date, window=90)
```

#### 6.2 Report Generation
- **Outputs**:
  1. Executive summary (key findings)
  2. Methodology description
  3. Change point analysis results
  4. Event impact statements
  5. Recommendations for stakeholders

#### 6.3 Dashboard
- **Backend**: Flask API serving data, change points, events
- **Frontend**: React dashboard with interactive visualizations
- **Features**:
  - Date range filters
  - Event type filters
  - Change point exploration
  - Impact metrics display
  - Downloadable reports

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Stage 1: Data Loading                     │
│  • Load price data (BrentDataLoader)                        │
│  • Load event data (EventDataLoader)                        │
│  • Validate data quality                                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Stage 2: Exploratory Data Analysis              │
│  • Visualize price series                                   │
│  • Calculate log returns                                    │
│  • Analyze volatility patterns                              │
│  • Generate summary statistics                              │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               Stage 3: Statistical Testing                   │
│  • ADF test for stationarity                                │
│  • KPSS test for stationarity                               │
│  • Determine if transformation needed                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           Stage 4: Bayesian Change Point Modeling            │
│  • Build PyMC model                                         │
│  • Run MCMC sampling                                        │
│  • Check convergence diagnostics                            │
│  • Extract posterior distribution                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Stage 5: Change Point Analysis                  │
│  • Identify change points from posterior                    │
│  • Associate with events                                    │
│  • Quantify impacts (before/after stats)                    │
│  • Generate impact statements                               │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│          Stage 6: Visualization and Reporting                │
│  • Create plots and figures                                 │
│  • Generate written reports                                 │
│  • Build interactive dashboard                              │
│  • Present findings to stakeholders                         │
└─────────────────────────────────────────────────────────────┘
```

---

## Iteration and Refinement

The workflow is iterative. After initial results:
1. Review change points and their plausibility
2. Adjust model parameters if needed (priors, number of change points)
3. Test alternative model specifications
4. Validate findings against domain knowledge
5. Incorporate stakeholder feedback

---

## Tools and Technologies

- **Data Processing**: pandas, numpy
- **Statistical Testing**: statsmodels
- **Bayesian Modeling**: PyMC
- **Visualization**: matplotlib, seaborn, plotly
- **Dashboard Backend**: Flask, Flask-RESTful
- **Dashboard Frontend**: React, TypeScript, Recharts
- **Testing**: pytest
- **Version Control**: git

---

## Quality Assurance

Throughout the workflow:
- Unit tests for all code modules
- Data validation at each stage
- Convergence diagnostics for MCMC
- Visual inspection of results
- Peer review of findings
- Documentation of assumptions and limitations

---

## Timeline Estimate

For a single change point analysis:
- Stage 1 (Data Loading): 30 minutes
- Stage 2 (EDA): 1-2 hours
- Stage 3 (Statistical Testing): 30 minutes
- Stage 4 (Modeling): 2-4 hours (depending on convergence)
- Stage 5 (Analysis): 1-2 hours
- Stage 6 (Reporting): 2-3 hours

**Total**: 1-2 days for complete analysis

---

## Next Steps

After completing this workflow:
1. Extend to multiple change point models
2. Incorporate external factors (supply/demand data)
3. Build predictive models
4. Develop real-time monitoring system
5. Create scenario analysis tools

---

**Document Version**: 1.0  
**Last Updated**: February 8, 2026
