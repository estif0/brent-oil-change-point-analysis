# Data Module

This module handles data loading and validation for the Brent oil price analysis project.

## Files

### `loader.py`
Contains the `BrentDataLoader` class for loading and validating Brent oil price data from CSV files.

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

### `event_loader.py` (To be implemented)
Will contain the `EventDataLoader` class for loading and filtering event data.

## Testing

Run tests with:
```bash
pytest tests/test_data_loader.py -v
```

All modules in this directory have corresponding test files in the `tests/` directory.
