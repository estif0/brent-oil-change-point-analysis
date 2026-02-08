# Data Module

This module handles data loading and validation for the Brent oil price analysis project.

## Quick Start

For simple data loading, use the convenience function:

```python
from src.data import load_brent_data

# Load Brent oil prices with automatic date parsing
data = load_brent_data('data/raw/BrentOilPrices.csv')
print(f"Loaded {len(data)} observations")
print(f"Date range: {data.index.min()} to {data.index.max()}")
```

For advanced features (validation, statistics), use the full classes documented below.

---

## Files

### `loader.py`
Contains the `BrentDataLoader` class and `load_brent_data()` convenience function for loading Brent oil price data from CSV files.

#### Convenience Function: `load_brent_data(file_path)`

**Purpose:** Simple, one-line data loading with automatic date parsing.

**Parameters:**
- `file_path` (str): Path to the Brent oil prices CSV file

**Returns:**
- `pd.DataFrame`: DataFrame with DatetimeIndex and 'Price' column

**Example:**
```python
from src.data import load_brent_data

# Quick loading
data = load_brent_data('data/raw/BrentOilPrices.csv')
prices = data['Price']
```

#### Class: `BrentDataLoader`

**Purpose:** Full-featured data loading with validation and statistics.

**Key Features:**
- Load CSV files with date parsing
- Validate data for missing values and duplicates
- Get date ranges and summary statistics
- Comprehensive error handling

**Usage Example:**
```python
from src.data import BrentDataLoader

# Load and validate data
loader = BrentDataLoader()
data = loader.load_data('data/raw/BrentOilPrices.csv')
validation = loader.validate_data()

if validation['is_valid']:
    start, end = loader.get_date_range()
    stats = loader.get_summary_statistics()
    print(f"Data spans from {start.date()} to {end.date()}")
    print(f"Average price: ${stats['mean']:.2f}")
else:
    print("Data validation failed:", validation['warnings'])
```

### `event_loader.py`
Contains the `EventDataLoader` class for loading and filtering event data that may have impacted oil prices.

**Key Features:**
- Load event data from CSV files
- Filter events by date range
- Filter events by type (geopolitical, opec_decision, economic_shock, sanction)
- Find events near a specific date with configurable time window
- Get summary statistics about events

**Usage Example:**
```python
from src.data import EventDataLoader

# Load and filter events
loader = EventDataLoader()
events = loader.load_events('data/events.csv')

# Get summary
summary = loader.get_events_summary()
print(f"Total events: {summary['total_events']}")
print(f"Event types: {summary['by_type']}")

# Filter by type
opec_events = loader.filter_by_type('opec_decision')
print(f"OPEC decisions: {len(opec_events)}")

# Filter by date range
crisis_events = loader.filter_by_date_range('2008-01-01', '2009-12-31')

# Find events near a change point
nearby = loader.find_events_near_date('2008-09-15', window_days=30)
```

## Testing

Run tests with:
```bash
pytest tests/test_data_loader.py -v
```

All modules in this directory have corresponding test files in the `tests/` directory.
