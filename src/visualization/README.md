# Visualization Module

This module provides plotting functions for Bayesian change point analysis. All functions return matplotlib Figure objects for customization and saving.

## Functions

### plot_price_with_changepoints()

Overlay change points and events on time series.

**Features:**
- Plot original price/returns series
- Mark detected change points with credible intervals
- Show historical events with type-based coloring
- Highlight events near change points differently
- Customizable styling and layout

**Parameters:**
- `data` (pd.Series): Time series with datetime index
- `changepoints` (list, optional): Change point dictionaries
- `events` (pd.DataFrame, optional): Historical events
- `figsize` (tuple): Figure size (default: (14, 6))
- `title` (str, optional): Custom title
- `show_ci` (bool): Show credible intervals (default: True)
- `event_window` (int): Days for highlighting events (default: 30)

**Example:**
```python
from src.visualization import plot_price_with_changepoints

fig = plot_price_with_changepoints(
    data=log_returns,
    changepoints=changepoints,
    events=events,
    title='Brent Oil Price Change Points'
)
fig.savefig('changepoints.png', dpi=300, bbox_inches='tight')
```

### plot_changepoint_distribution()

Plot posterior distribution of change point (τ).

**Features:**
- Histogram of posterior samples
- Point estimates (MAP, mean)
- Credible interval (HDI)
- Date labels on secondary x-axis
- Uncertainty visualization

**Parameters:**
- `trace` (InferenceData): MCMC samples
- `data` (pd.Series): Original time series
- `bins` (int): Histogram bins (default: 50)
- `figsize` (tuple): Figure size (default: (10, 6))
- `show_map` (bool): Show mode/MAP (default: True)
- `show_mean` (bool): Show mean (default: True)
- `show_hdi` (bool): Show HDI (default: True)
- `hdi_prob` (float): HDI probability (default: 0.94)

**Example:**
```python
from src.visualization import plot_changepoint_distribution

fig = plot_changepoint_distribution(
    trace=trace,
    data=log_returns,
    hdi_prob=0.94
)
fig.savefig('tau_posterior.png', dpi=300, bbox_inches='tight')
```

### plot_parameter_comparison()

Compare before/after parameter distributions.

**Features:**
- Violin plots for μ₁ vs μ₂ and σ₁ vs σ₂
- KDE posterior distributions
- Credible intervals (HDI shaded regions)
- Side-by-side comparison
- Optional volatility parameters

**Parameters:**
- `trace` (InferenceData): MCMC samples
- `figsize` (tuple): Figure size (default: (12, 8))
- `hdi_prob` (float): HDI probability (default: 0.94)
- `include_sigma` (bool): Include volatility (default: True)

**Example:**
```python
from src.visualization import plot_parameter_comparison

fig = plot_parameter_comparison(
    trace=trace,
    include_sigma=True
)
fig.savefig('parameter_comparison.png', dpi=300, bbox_inches='tight')
```

### plot_event_impact()

Visualize price behavior around specific event.

**Features:**
- Time series before and after event
- Event marker line
- Shaded before/after regions
- Statistical comparison (mean, volatility)
- Percentage changes
- Optional statistics text box

**Parameters:**
- `data` (pd.Series): Time series with datetime index
- `event_date` (pd.Timestamp): Event date
- `window_days` (int): Days before/after (default: 60)
- `figsize` (tuple): Figure size (default: (12, 6))
- `event_name` (str, optional): Event name for title
- `show_stats` (bool): Display statistics (default: True)

**Example:**
```python
from src.visualization import plot_event_impact

fig = plot_event_impact(
    data=log_returns,
    event_date=pd.Timestamp('2008-09-15'),
    window_days=90,
    event_name='Lehman Brothers Collapse'
)
fig.savefig('event_impact.png', dpi=300, bbox_inches='tight')
```

## Usage Examples

### Complete Visualization Workflow

```python
from src.data import BrentDataLoader, EventDataLoader
from src.models import BayesianChangePointModel
from src.analysis import ChangePointAnalyzer
from src.visualization import (
    plot_price_with_changepoints,
    plot_changepoint_distribution,
    plot_parameter_comparison,
    plot_event_impact,
)

# Load data
loader = BrentDataLoader()
data = loader.load_data()
log_returns = loader.calculate_log_returns()

event_loader = EventDataLoader()
events = event_loader.load_events()

# Fit model
model = BayesianChangePointModel(log_returns)
model.build_model()
trace = model.fit(samples=2000, tune=1000)

# Analyze
analyzer = ChangePointAnalyzer()
results = analyzer.batch_analyze(trace, log_returns, events)

# Visualize
# 1. Overview plot
fig1 = plot_price_with_changepoints(
    log_returns,
    results['changepoints'],
    events,
    title='Brent Oil Log Returns with Change Points'
)
fig1.savefig('figures/01_overview.png', dpi=300, bbox_inches='tight')

# 2. Change point posterior
fig2 = plot_changepoint_distribution(trace, log_returns)
fig2.savefig('figures/02_tau_posterior.png', dpi=300, bbox_inches='tight')

# 3. Parameter comparison
fig3 = plot_parameter_comparison(trace)
fig3.savefig('figures/03_parameters.png', dpi=300, bbox_inches='tight')

# 4. Event impact
if results['associations'][0]['closest_event']:
    event = results['associations'][0]['closest_event']
    fig4 = plot_event_impact(
        log_returns,
        event['date'],
        window_days=90,
        event_name=event['event_name']
    )
    fig4.savefig('figures/04_event_impact.png', dpi=300, bbox_inches='tight')
```

### Customization Examples

#### Custom Styling

```python
import matplotlib.pyplot as plt

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

# Create plot
fig = plot_price_with_changepoints(data, changepoints, events)

# Customize
ax = fig.axes[0]
ax.set_facecolor('#f0f0f0')
ax.set_xlabel('Date', fontsize=14, fontweight='bold')

# Save with custom settings
fig.savefig('custom_plot.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
```

#### Subplots with Multiple Plots

```python
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# Plot 1: Time series with change points
ax1 = plt.subplot(2, 2, 1)
fig1 = plot_price_with_changepoints(data, changepoints)
# Transfer to subplot manually or use tight_layout

# Plot 2: Tau distribution
ax2 = plt.subplot(2, 2, 2)
fig2 = plot_changepoint_distribution(trace, data)

# Plot 3: Parameter comparison
ax3 = plt.subplot(2, 2, 3)
fig3 = plot_parameter_comparison(trace)

# Plot 4: Event impact
ax4 = plt.subplot(2, 2, 4)
fig4 = plot_event_impact(data, event_date)

plt.tight_layout()
plt.savefig('combined_plots.png', dpi=300, bbox_inches='tight')
```

#### Interactive Plots (Plotly)

While this module uses matplotlib, you can convert to plotly for interactivity:

```python
import plotly.tools as tls

# Create matplotlib figure
fig_mpl = plot_price_with_changepoints(data, changepoints, events)

# Convert to plotly (basic conversion)
fig_plotly = tls.mpl_to_plotly(fig_mpl)
fig_plotly.show()
```

## Output Examples

### plot_price_with_changepoints()

![Price with Change Points](example_images/overview.png)

Features shown:
- Black line: Time series
- Red dashed line: Change point
- Red shaded region: 94% credible interval
- Colored vertical lines: Events (by type)
- Markers: Events (circles for near change points, triangles otherwise)

### plot_changepoint_distribution()

![Tau Posterior](example_images/tau_posterior.png)

Features shown:
- Blue histogram: Posterior samples
- Red dashed line: Mode (MAP)
- Green dashed line: Mean
- Red shaded region: 94% HDI
- Top x-axis: Corresponding dates

### plot_parameter_comparison()

![Parameter Comparison](example_images/parameters.png)

Features shown:
- Top left: μ violin plots (before vs after)
- Top right: μ KDE with HDI
- Bottom left: σ violin plots (before vs after)
- Bottom right: σ KDE with HDI

### plot_event_impact()

![Event Impact](example_images/event_impact.png)

Features shown:
- Blue line: Before event
- Red line: After event
- Red dashed line: Event date
- Blue/red shaded: Before/after regions
- Text box: Statistical comparison

## Design Considerations

### Color Scheme

- **Change points**: Red (high attention)
- **Events**: Type-based (Political=blue, Economic=green, etc.)
- **Before/After**: Blue/Red contrast
- **Credible intervals**: Semi-transparent matching colors

### Figure Sizes

Default sizes optimized for:
- Single plots: (12-14, 6-8) inches
- Multi-panel: Scale proportionally
- Publication quality: 300 DPI recommended

### Date Formatting

- Major ticks: Year level by default
- Format: 'YYYY-MM' for clarity
- Rotation: 45° for readability
- Adaptive based on date range

### Statistical Display

- Means: Horizontal dashed lines
- HDI: Shaded regions (20% alpha)
- Point estimates: Vertical lines with labels
- Stats box: Upper left, semi-transparent background

## Integration

This module integrates with:

- **src.models**: Uses InferenceData from BayesianChangePointModel
- **src.analysis**: Uses change point dictionaries from ChangePointAnalyzer
- **src.data**: Uses DataFrame format from EventDataLoader
- **matplotlib**: Core plotting library
- **seaborn**: Enhanced statistical plots

## Testing

Comprehensive test suite in `tests/test_plots.py`:
- 33 tests covering all functions
- Edge cases and error handling
- Figure saving verification
- Integration tests with full workflow

Run tests:
```bash
pytest tests/test_plots.py -v
```

## Dependencies

- matplotlib >= 3.5
- seaborn >= 0.11
- numpy >= 1.21
- pandas >= 1.3
- arviz >= 0.11
- scipy (for KDE in parameter comparison)

## Best Practices

1. **Always close figures** after saving to prevent memory leaks:
   ```python
   fig = plot_price_with_changepoints(data, changepoints)
   fig.savefig('plot.png')
   plt.close(fig)
   ```

2. **Use high DPI for publications**:
   ```python
   fig.savefig('plot.png', dpi=300, bbox_inches='tight')
   ```

3. **Customize after creation**:
   ```python
   fig = plot_price_with_changepoints(data, changepoints)
   ax = fig.axes[0]
   ax.set_ylim(-0.1, 0.1)
   fig.savefig('plot.png')
   ```

4. **Batch save all plots**:
   ```python
   from pathlib import Path
   
   figures_dir = Path('reports/figures')
   figures_dir.mkdir(parents=True, exist_ok=True)
   
   plots = [
       ('01_overview.png', plot_price_with_changepoints(data, cp)),
       ('02_tau.png', plot_changepoint_distribution(trace, data)),
       ('03_params.png', plot_parameter_comparison(trace)),
   ]
   
   for filename, fig in plots:
       fig.savefig(figures_dir / filename, dpi=300, bbox_inches='tight')
       plt.close(fig)
   ```

5. **Check figure before saving**:
   ```python
   fig = plot_price_with_changepoints(data, changepoints)
   plt.show()  # Display for inspection
   fig.savefig('plot.png')
   plt.close(fig)
   ```

## Future Enhancements

Potential additions:
- Plotly versions for interactivity
- Animation for MCMC sampling progress
- 3D plots for multi-parameter relationships
- Statistical test overlays (e.g., CUSUM)
- Regime-specific coloring in time series
- Automatic layout optimization for multiple change points
