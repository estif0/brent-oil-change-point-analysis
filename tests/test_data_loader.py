"""
Unit tests for the BrentDataLoader class.
"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os

from src.data.loader import BrentDataLoader


class TestBrentDataLoader:
    """Test cases for BrentDataLoader class."""

    @pytest.fixture
    def sample_csv_file(self):
        """Create a temporary CSV file with sample data for testing."""
        data = """Date,Price
20-May-87,18.63
21-May-87,18.45
22-May-87,18.55
25-May-87,18.6
26-May-87,18.63"""

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            f.write(data)
            temp_path = f.name

        yield temp_path

        # Cleanup
        os.unlink(temp_path)

    @pytest.fixture
    def sample_csv_with_missing(self):
        """Create a temporary CSV file with missing values."""
        data = """Date,Price
20-May-87,18.63
21-May-87,
22-May-87,18.55
25-May-87,18.6"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            f.write(data)
            temp_path = f.name

        yield temp_path

        os.unlink(temp_path)

    @pytest.fixture
    def sample_csv_invalid_columns(self):
        """Create a temporary CSV file with invalid column names."""
        data = """InvalidDate,InvalidPrice
20-May-87,18.63
21-May-87,18.45"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            f.write(data)
            temp_path = f.name

        yield temp_path

        os.unlink(temp_path)

    def test_initialization(self):
        """Test BrentDataLoader initialization."""
        loader = BrentDataLoader()
        assert loader.data is None
        assert loader.file_path is None

    def test_load_data_valid_file(self, sample_csv_file):
        """Test loading data from a valid CSV file."""
        loader = BrentDataLoader()
        data = loader.load_data(sample_csv_file)

        # Check data is loaded
        assert data is not None
        assert len(data) == 5

        # Check columns
        assert "Price" in data.columns

        # Check index is DatetimeIndex
        assert isinstance(data.index, pd.DatetimeIndex)

        # Check data is sorted by date
        assert data.index.is_monotonic_increasing

        # Check file path is stored
        assert loader.file_path == sample_csv_file

    def test_load_data_nonexistent_file(self):
        """Test loading data from a non-existent file."""
        loader = BrentDataLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_data("nonexistent_file.csv")

    def test_load_data_invalid_columns(self, sample_csv_invalid_columns):
        """Test loading data from CSV with invalid columns."""
        loader = BrentDataLoader()

        with pytest.raises(
            ValueError, match="CSV must contain 'Date' and 'Price' columns"
        ):
            loader.load_data(sample_csv_invalid_columns)

    def test_validate_data_valid(self, sample_csv_file):
        """Test validation of valid data."""
        loader = BrentDataLoader()
        loader.load_data(sample_csv_file)

        results = loader.validate_data()

        assert results["is_valid"] is True
        assert results["missing_count"] == 0
        assert results["duplicate_dates"] == 0
        assert results["total_records"] == 5
        assert len(results["warnings"]) == 0

    def test_validate_data_with_missing_values(self, sample_csv_with_missing):
        """Test validation of data with missing values."""
        loader = BrentDataLoader()
        loader.load_data(sample_csv_with_missing)

        results = loader.validate_data()

        assert results["missing_count"] == 1
        assert any("missing" in warning.lower() for warning in results["warnings"])

    def test_validate_data_before_loading(self):
        """Test validation before data is loaded."""
        loader = BrentDataLoader()

        with pytest.raises(RuntimeError, match="No data loaded"):
            loader.validate_data()

    def test_get_date_range(self, sample_csv_file):
        """Test getting date range from loaded data."""
        loader = BrentDataLoader()
        loader.load_data(sample_csv_file)

        start_date, end_date = loader.get_date_range()

        assert isinstance(start_date, pd.Timestamp)
        assert isinstance(end_date, pd.Timestamp)
        assert start_date < end_date

        # Check specific dates
        assert start_date.date() == pd.Timestamp("1987-05-20").date()
        assert end_date.date() == pd.Timestamp("1987-05-26").date()

    def test_get_date_range_before_loading(self):
        """Test getting date range before data is loaded."""
        loader = BrentDataLoader()

        with pytest.raises(RuntimeError, match="No data loaded"):
            loader.get_date_range()

    def test_get_summary_statistics(self, sample_csv_file):
        """Test getting summary statistics."""
        loader = BrentDataLoader()
        loader.load_data(sample_csv_file)

        stats = loader.get_summary_statistics()

        assert "count" in stats
        assert "mean" in stats
        assert "median" in stats
        assert "std" in stats
        assert "min" in stats
        assert "max" in stats
        assert "date_range" in stats

        assert stats["count"] == 5
        assert stats["min"] == 18.45
        assert stats["max"] == 18.63

    def test_get_summary_statistics_before_loading(self):
        """Test getting summary statistics before data is loaded."""
        loader = BrentDataLoader()

        with pytest.raises(RuntimeError, match="No data loaded"):
            loader.get_summary_statistics()

    def test_price_numeric_conversion(self, sample_csv_file):
        """Test that prices are properly converted to numeric."""
        loader = BrentDataLoader()
        data = loader.load_data(sample_csv_file)

        # Check all prices are numeric
        assert pd.api.types.is_numeric_dtype(data["Price"])

    def test_data_sorting(self):
        """Test that data is sorted by date after loading."""
        # Create unsorted data
        data = """Date,Price
25-May-87,18.6
20-May-87,18.63
22-May-87,18.55"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            f.write(data)
            temp_path = f.name

        try:
            loader = BrentDataLoader()
            loaded_data = loader.load_data(temp_path)

            # Check data is sorted
            assert loaded_data.index.is_monotonic_increasing
        finally:
            os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
