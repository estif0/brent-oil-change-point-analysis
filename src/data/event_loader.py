"""
Event data loading module for Brent oil price analysis.

This module provides classes for loading and filtering event data that
may have impacted oil prices.
"""

from typing import List, Optional
import pandas as pd
from pathlib import Path


class EventDataLoader:
    """
    A class for loading and filtering event data related to oil price changes.

    This class handles loading event data from CSV files and provides
    filtering capabilities by date range and event type.

    Attributes:
        events (pd.DataFrame): The loaded event data.
        file_path (str): Path to the events data file.

    Example:
        >>> loader = EventDataLoader()
        >>> events = loader.load_events('data/events.csv')
        >>> opec_events = loader.filter_by_type('opec_decision')
        >>> recent_events = loader.filter_by_date_range('2010-01-01', '2020-12-31')
    """

    def __init__(self):
        """Initialize the EventDataLoader."""
        self.events: pd.DataFrame = None
        self.file_path: str = None

    def load_events(self, file_path: str) -> pd.DataFrame:
        """
        Load event data from a CSV file.

        The CSV file should have columns: 'date', 'event_name', 'event_type',
        'description', and 'expected_impact'.

        Args:
            file_path (str): Path to the CSV file containing event data.

        Returns:
            pd.DataFrame: DataFrame with event data and DatetimeIndex.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the CSV does not contain required columns.

        Example:
            >>> loader = EventDataLoader()
            >>> events = loader.load_events('data/events.csv')
            >>> print(f"Loaded {len(events)} events")
        """
        # Check if file exists
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Events file not found: {file_path}")

        # Load the CSV file
        try:
            self.events = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

        # Validate required columns exist
        required_columns = [
            "date",
            "event_name",
            "event_type",
            "description",
            "expected_impact",
        ]
        missing_columns = [
            col for col in required_columns if col not in self.events.columns
        ]

        if missing_columns:
            raise ValueError(
                f"CSV must contain columns: {required_columns}. "
                f"Missing: {missing_columns}"
            )

        # Parse dates
        try:
            self.events["date"] = pd.to_datetime(self.events["date"])
        except Exception as e:
            raise ValueError(f"Error parsing dates: {e}")

        # Sort by date
        self.events.sort_values("date", inplace=True)
        self.events.reset_index(drop=True, inplace=True)

        self.file_path = file_path

        return self.events

    def filter_by_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Filter events by date range.

        Args:
            start_date (str): Start date in format 'YYYY-MM-DD'.
            end_date (str): End date in format 'YYYY-MM-DD'.

        Returns:
            pd.DataFrame: Filtered DataFrame containing events within the date range.

        Raises:
            RuntimeError: If no events have been loaded yet.
            ValueError: If date format is invalid.

        Example:
            >>> loader = EventDataLoader()
            >>> loader.load_events('data/events.csv')
            >>> events_2008 = loader.filter_by_date_range('2008-01-01', '2008-12-31')
            >>> print(f"Found {len(events_2008)} events in 2008")
        """
        if self.events is None:
            raise RuntimeError("No events loaded. Call load_events() first.")

        try:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
        except Exception as e:
            raise ValueError(f"Invalid date format: {e}")

        if start > end:
            raise ValueError("Start date must be before or equal to end date")

        mask = (self.events["date"] >= start) & (self.events["date"] <= end)
        filtered = self.events[mask].copy()

        return filtered

    def filter_by_type(self, event_type: str) -> pd.DataFrame:
        """
        Filter events by event type.

        Valid event types: 'geopolitical', 'opec_decision', 'economic_shock', 'sanction'

        Args:
            event_type (str): The type of events to filter for.

        Returns:
            pd.DataFrame: Filtered DataFrame containing events of the specified type.

        Raises:
            RuntimeError: If no events have been loaded yet.
            ValueError: If event_type is invalid.

        Example:
            >>> loader = EventDataLoader()
            >>> loader.load_events('data/events.csv')
            >>> opec_events = loader.filter_by_type('opec_decision')
            >>> print(f"Found {len(opec_events)} OPEC decisions")
        """
        if self.events is None:
            raise RuntimeError("No events loaded. Call load_events() first.")

        valid_types = ["geopolitical", "opec_decision", "economic_shock", "sanction"]

        if event_type not in valid_types:
            raise ValueError(
                f"Invalid event_type: '{event_type}'. " f"Valid types: {valid_types}"
            )

        filtered = self.events[self.events["event_type"] == event_type].copy()

        return filtered

    def get_event_types(self) -> List[str]:
        """
        Get list of unique event types in the loaded data.

        Returns:
            List[str]: Sorted list of unique event types.

        Raises:
            RuntimeError: If no events have been loaded yet.

        Example:
            >>> loader = EventDataLoader()
            >>> loader.load_events('data/events.csv')
            >>> types = loader.get_event_types()
            >>> print(f"Event types: {', '.join(types)}")
        """
        if self.events is None:
            raise RuntimeError("No events loaded. Call load_events() first.")

        return sorted(self.events["event_type"].unique().tolist())

    def get_events_summary(self) -> dict:
        """
        Get summary statistics about the loaded events.

        Returns:
            dict: Dictionary containing:
                - total_events: Total number of events
                - date_range: Tuple of (earliest_date, latest_date)
                - by_type: Count of events by type
                - by_impact: Count of events by expected impact

        Raises:
            RuntimeError: If no events have been loaded yet.
        """
        if self.events is None:
            raise RuntimeError("No events loaded. Call load_events() first.")

        return {
            "total_events": len(self.events),
            "date_range": (
                str(self.events["date"].min().date()),
                str(self.events["date"].max().date()),
            ),
            "by_type": self.events["event_type"].value_counts().to_dict(),
            "by_impact": self.events["expected_impact"].value_counts().to_dict(),
        }

    def find_events_near_date(
        self, target_date: str, window_days: int = 30
    ) -> pd.DataFrame:
        """
        Find events within a specified time window around a target date.

        Args:
            target_date (str): Target date in format 'YYYY-MM-DD'.
            window_days (int): Number of days before and after target date to search.
                             Default is 30 days.

        Returns:
            pd.DataFrame: Events within the time window, sorted by date.

        Raises:
            RuntimeError: If no events have been loaded yet.
            ValueError: If date format is invalid.

        Example:
            >>> loader = EventDataLoader()
            >>> loader.load_events('data/events.csv')
            >>> # Find events around the 2008 financial crisis
            >>> nearby = loader.find_events_near_date('2008-09-15', window_days=60)
        """
        if self.events is None:
            raise RuntimeError("No events loaded. Call load_events() first.")

        try:
            target = pd.to_datetime(target_date)
        except Exception as e:
            raise ValueError(f"Invalid date format: {e}")

        if window_days < 0:
            raise ValueError("window_days must be non-negative")

        start = target - pd.Timedelta(days=window_days)
        end = target + pd.Timedelta(days=window_days)

        mask = (self.events["date"] >= start) & (self.events["date"] <= end)
        filtered = self.events[mask].copy()

        # Add days_from_target column
        filtered["days_from_target"] = (filtered["date"] - target).dt.days

        return filtered
