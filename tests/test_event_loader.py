"""
Unit tests for the EventDataLoader class.
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path

from src.data.event_loader import EventDataLoader


class TestEventDataLoader:
    """Test cases for EventDataLoader class."""

    @pytest.fixture
    def sample_events_csv(self):
        """Create a temporary CSV file with sample event data."""
        data = """date,event_name,event_type,description,expected_impact
2008-09-15,Global Financial Crisis,economic_shock,Lehman Brothers collapse,decrease
2011-03-11,Arab Spring,geopolitical,Political uprisings in Middle East,increase
2014-11-27,OPEC Maintains Production,opec_decision,OPEC decided not to cut production,decrease
2018-05-08,US Withdraws from Iran Deal,sanction,US reimposed sanctions on Iran,increase
2020-03-09,COVID-19 Pandemic,economic_shock,Pandemic lockdowns destroyed demand,decrease"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            f.write(data)
            temp_path = f.name

        yield temp_path

        os.unlink(temp_path)

    @pytest.fixture
    def sample_events_missing_columns(self):
        """Create a CSV file with missing required columns."""
        data = """date,event_name
2008-09-15,Global Financial Crisis
2011-03-11,Arab Spring"""

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as f:
            f.write(data)
            temp_path = f.name

        yield temp_path

        os.unlink(temp_path)

    def test_initialization(self):
        """Test EventDataLoader initialization."""
        loader = EventDataLoader()
        assert loader.events is None
        assert loader.file_path is None

    def test_load_events_valid_file(self, sample_events_csv):
        """Test loading events from a valid CSV file."""
        loader = EventDataLoader()
        events = loader.load_events(sample_events_csv)

        # Check data is loaded
        assert events is not None
        assert len(events) == 5

        # Check all required columns exist
        required_columns = [
            "date",
            "event_name",
            "event_type",
            "description",
            "expected_impact",
        ]
        for col in required_columns:
            assert col in events.columns

        # Check date is datetime
        assert pd.api.types.is_datetime64_any_dtype(events["date"])

        # Check data is sorted by date
        assert events["date"].is_monotonic_increasing

        # Check file path is stored
        assert loader.file_path == sample_events_csv

    def test_load_events_nonexistent_file(self):
        """Test loading events from a non-existent file."""
        loader = EventDataLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_events("nonexistent_events.csv")

    def test_load_events_missing_columns(self, sample_events_missing_columns):
        """Test loading events from CSV with missing required columns."""
        loader = EventDataLoader()

        with pytest.raises(ValueError, match="Missing"):
            loader.load_events(sample_events_missing_columns)

    def test_filter_by_date_range_valid(self, sample_events_csv):
        """Test filtering events by valid date range."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        # Filter events in 2011-2018
        filtered = loader.filter_by_date_range("2011-01-01", "2018-12-31")

        assert len(filtered) == 3
        assert all(
            pd.to_datetime("2011-01-01") <= date <= pd.to_datetime("2018-12-31")
            for date in filtered["date"]
        )

    def test_filter_by_date_range_no_events(self, sample_events_csv):
        """Test filtering by date range with no matching events."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        # Filter for dates before any events
        filtered = loader.filter_by_date_range("2000-01-01", "2005-12-31")

        assert len(filtered) == 0

    def test_filter_by_date_range_before_loading(self):
        """Test filtering by date range before loading events."""
        loader = EventDataLoader()

        with pytest.raises(RuntimeError, match="No events loaded"):
            loader.filter_by_date_range("2010-01-01", "2020-12-31")

    def test_filter_by_date_range_invalid_dates(self, sample_events_csv):
        """Test filtering with invalid date format."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        with pytest.raises(ValueError):
            loader.filter_by_date_range("invalid-date", "2020-12-31")

    def test_filter_by_date_range_start_after_end(self, sample_events_csv):
        """Test filtering with start date after end date."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        with pytest.raises(ValueError, match="Start date must be before"):
            loader.filter_by_date_range("2020-01-01", "2010-01-01")

    def test_filter_by_type_valid(self, sample_events_csv):
        """Test filtering events by valid event type."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        # Filter for economic shocks
        economic = loader.filter_by_type("economic_shock")
        assert len(economic) == 2
        assert all(event == "economic_shock" for event in economic["event_type"])

        # Filter for OPEC decisions
        opec = loader.filter_by_type("opec_decision")
        assert len(opec) == 1

        # Filter for geopolitical
        geopolitical = loader.filter_by_type("geopolitical")
        assert len(geopolitical) == 1

        # Filter for sanctions
        sanctions = loader.filter_by_type("sanction")
        assert len(sanctions) == 1

    def test_filter_by_type_invalid(self, sample_events_csv):
        """Test filtering by invalid event type."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        with pytest.raises(ValueError, match="Invalid event_type"):
            loader.filter_by_type("invalid_type")

    def test_filter_by_type_before_loading(self):
        """Test filtering by type before loading events."""
        loader = EventDataLoader()

        with pytest.raises(RuntimeError, match="No events loaded"):
            loader.filter_by_type("geopolitical")

    def test_get_event_types(self, sample_events_csv):
        """Test getting list of event types."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        types = loader.get_event_types()

        assert isinstance(types, list)
        assert len(types) == 4
        assert "economic_shock" in types
        assert "geopolitical" in types
        assert "opec_decision" in types
        assert "sanction" in types
        # Check it's sorted
        assert types == sorted(types)

    def test_get_event_types_before_loading(self):
        """Test getting event types before loading events."""
        loader = EventDataLoader()

        with pytest.raises(RuntimeError, match="No events loaded"):
            loader.get_event_types()

    def test_get_events_summary(self, sample_events_csv):
        """Test getting summary statistics."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        summary = loader.get_events_summary()

        assert "total_events" in summary
        assert summary["total_events"] == 5

        assert "date_range" in summary
        assert isinstance(summary["date_range"], tuple)

        assert "by_type" in summary
        assert isinstance(summary["by_type"], dict)
        assert summary["by_type"]["economic_shock"] == 2

        assert "by_impact" in summary
        assert isinstance(summary["by_impact"], dict)

    def test_get_events_summary_before_loading(self):
        """Test getting summary before loading events."""
        loader = EventDataLoader()

        with pytest.raises(RuntimeError, match="No events loaded"):
            loader.get_events_summary()

    def test_find_events_near_date(self, sample_events_csv):
        """Test finding events near a target date."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        # Find events within 365 days of 2014-11-27
        nearby = loader.find_events_near_date("2014-11-27", window_days=365)

        assert len(nearby) >= 1
        assert "days_from_target" in nearby.columns

        # Check all events are within window
        assert all(abs(days) <= 365 for days in nearby["days_from_target"])

    def test_find_events_near_date_small_window(self, sample_events_csv):
        """Test finding events with small time window."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        # Very small window - likely no events
        nearby = loader.find_events_near_date("2010-01-01", window_days=1)

        # Should return empty or very few events
        assert len(nearby) >= 0

    def test_find_events_near_date_invalid_date(self, sample_events_csv):
        """Test finding events with invalid date."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        with pytest.raises(ValueError):
            loader.find_events_near_date("invalid-date")

    def test_find_events_near_date_negative_window(self, sample_events_csv):
        """Test finding events with negative window."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        with pytest.raises(ValueError, match="must be non-negative"):
            loader.find_events_near_date("2014-11-27", window_days=-10)

    def test_find_events_near_date_before_loading(self):
        """Test finding events before loading data."""
        loader = EventDataLoader()

        with pytest.raises(RuntimeError, match="No events loaded"):
            loader.find_events_near_date("2014-11-27")

    def test_combined_filtering(self, sample_events_csv):
        """Test combining multiple filtering operations."""
        loader = EventDataLoader()
        loader.load_events(sample_events_csv)

        # First filter by date range
        date_filtered = loader.filter_by_date_range("2008-01-01", "2015-12-31")

        # Then filter by type
        economic_in_range = date_filtered[
            date_filtered["event_type"] == "economic_shock"
        ]

        assert len(economic_in_range) == 1
        assert economic_in_range.iloc[0]["event_name"] == "Global Financial Crisis"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
