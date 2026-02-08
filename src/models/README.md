# Models Module

This module contains Bayesian statistical models for detecting change points in the Brent oil price time series.

## Overview

The `models` module provides implementations of Bayesian change point detection algorithms using PyMC for probabilistic programming and MCMC (Markov Chain Monte Carlo) sampling.

## Contents

### `bayesian_changepoint.py`

Contains the `BayesianChangePointModel` class for detecting a single change point in time series data.

**Key Features:**
- Bayesian inference using MCMC sampling
- Detects change point location (τ)
- Estimates before/after parameters (mean, standard deviation)
- Provides credible intervals for all parameters
- Includes convergence diagnostics

**Usage Example:**

```python
import pandas as pd
from src.models import BayesianChangePointModel

# Load your time series data (e.g., log returns)
data = pd.Series([...])  # Your data here

# Create and build model
model = BayesianChangePointModel(data)
model.build_model(min_segment_length=30, prior_std_scale=2.0)

# Fit model using MCMC
trace = model.fit(samples=2000, tune=1000, chains=2, random_seed=42)

# Get change point estimate
changepoint = model.get_changepoint_estimate(method='mean')
print(f"Change point detected at: {changepoint['date']}")

# Get parameter estimates
params = model.get_parameter_estimates()
print(f"Mean before: {params['mu_1']['mean']:.4f}")
print(f"Mean after: {params['mu_2']['mean']:.4f}")

# Get summary statistics
summary = model.get_summary()
print(summary)
```

## Mathematical Background

### Single Change Point Model

The model assumes a time series has a single change point τ where statistical properties change:

**Prior Distributions:**
```
τ ~ DiscreteUniform(min_segment, n - min_segment)
μ₁ ~ Normal(data_mean, data_std × scale)
μ₂ ~ Normal(data_mean, data_std × scale)
σ₁ ~ HalfNormal(data_std × scale)
σ₂ ~ HalfNormal(data_std × scale)
```

**Likelihood:**
```
For t < τ:  y_t ~ Normal(μ₁, σ₁)
For t ≥ τ:  y_t ~ Normal(μ₂, σ₂)
```

### Parameters

- **τ (tau)**: Index of the change point
- **μ₁ (mu_1)**: Mean of the series before the change point
- **μ₂ (mu_2)**: Mean of the series after the change point
- **σ₁ (sigma_1)**: Standard deviation before the change point
- **σ₂ (sigma_2)**: Standard deviation after the change point

## Model Assumptions

1. **Single Change Point**: The model assumes only one change point exists
2. **Normal Distribution**: Data within each segment follows a normal distribution
3. **Independent Observations**: Observations are independent (no autocorrelation modeling)
4. **Abrupt Change**: The change happens instantaneously at τ (no gradual transitions)

## Key Methods

### `build_model()`

Constructs the PyMC model structure.

**Parameters:**
- `prior_std_scale`: Scale factor for prior standard deviations (default: 2.0)
- `min_segment_length`: Minimum observations per segment (default: 30)

**Returns:** PyMC Model object

### `fit()`

Performs MCMC sampling to obtain posterior distributions.

**Parameters:**
- `samples`: Number of posterior samples per chain (default: 2000)
- `tune`: Number of tuning samples (discarded) (default: 1000)
- `chains`: Number of independent MCMC chains (default: 2)
- `target_accept`: Target acceptance rate for NUTS (default: 0.95)
- `random_seed`: Random seed for reproducibility (default: None)

**Returns:** ArViZ InferenceData object

### `get_changepoint_estimate()`

Returns point estimate of change point location.

**Parameters:**
- `method`: Estimation method - 'mean', 'median', or 'mode' (default: 'mean')

**Returns:** Dictionary with 'index', 'date' (if datetime index), and 'method'

### `get_parameter_estimates()`

Returns estimates for all model parameters.

**Returns:** Dictionary with mean, std, and HDI for each parameter

### `get_summary()`

Returns comprehensive summary statistics.

**Parameters:**
- `var_names`: List of variables to summarize (default: all)
- `hdi_prob`: Probability for HDI (default: 0.94)

**Returns:** pandas DataFrame with summary statistics

## Convergence Diagnostics

After fitting, always check convergence:

```python
summary = model.get_summary()

# Check R-hat values (should be < 1.01)
print(summary['r_hat'])

# Check effective sample size (should be > 100)
print(summary['ess_bulk'])
```

## Performance Considerations

- **Data Size**: Larger datasets take longer to sample
- **Chains**: More chains improve convergence diagnostics but increase runtime
- **Samples**: More samples improve posterior approximation but increase runtime
- **Typical Runtime**: 2-10 minutes for 1000-5000 observations with 2000 samples

## Testing

Run tests with:

```bash
# Fast tests only
pytest tests/test_bayesian_changepoint.py -m "not slow"

# All tests (including MCMC sampling)
pytest tests/test_bayesian_changepoint.py

# With coverage
pytest tests/test_bayesian_changepoint.py --cov=src/models
```

## Dependencies

- `pymc >= 5.0`: Probabilistic programming framework
- `arviz >= 0.23`: Bayesian inference diagnostics
- `numpy`: Numerical computing
- `pandas`: Data structures
- `pytensor`: Backend for PyMC

## References

1. Adams, R. P., & MacKay, D. J. (2007). Bayesian Online Changepoint Detection. arXiv:0710.3742
2. PyMC Documentation: https://www.pymc.io/
3. Bayesian Methods for Hackers: Chapter 1 (Change Point Detection)

## Future Enhancements

- Multi-change point detection
- Student-t likelihood for robust outlier handling
- Autoregressive models for time-dependent structures
- Variance change point detection without mean change
