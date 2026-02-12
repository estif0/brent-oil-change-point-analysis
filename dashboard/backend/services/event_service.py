"""
Event service for handling geopolitical and economic events data.

This module provides the EventService class which handles loading,
filtering, and providing impact analysis for events.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List
import sys

# Add project src to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data.event_loader import EventDataLoader


class EventService:
    """
    Service for managing event data.

    This class provides methods to load and query geopolitical and economic
    events that may impact oil prices.

    Attributes:
        event_file (Path): Path to the events CSV file.
        data (pd.DataFrame): Loaded event data.
        loader (EventDataLoader): Event data loader instance.
    """

    def __init__(self, event_file: Path):
        """
        Initialize the EventService.

        Args:
            event_file (Path): Path to CSV file containing events data.

        Raises:
            FileNotFoundError: If event file does not exist.
        """
        self.event_file = event_file
        self.loader = EventDataLoader()
        self.data = None
        self._load_data()

    def _load_data(self):
        """Load event data from file using EventDataLoader."""
        self.data = self.loader.load_events(self.event_file)
        if self.data is None:
            raise ValueError("Failed to load event data")

    def get_events(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of events with optional filtering.

        Args:
            start_date (str, optional): Filter events from this date.
            end_date (str, optional): Filter events until this date.
            event_type (str, optional): Filter by event type
                (geopolitical, opec_decision, economic_shock, sanction).

        Returns:
            List[Dict]: List of event records.

        Example:
            >>> service = EventService(Path('data/events.csv'))
            >>> events = service.get_events(event_type='opec_decision')
            >>> len(events)
            5
        """
        df = self.data.copy()

        # Apply filters
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        if event_type:
            df = self.loader.filter_by_type(event_type)

        # Convert to list of dictionaries
        result = []
        for idx, row in df.iterrows():
            event = {
                "id": int(idx),
                "date": row["date"].strftime("%Y-%m-%d"),
                "event_name": str(row["event_name"]),
                "event_type": str(row["event_type"]),
            }

            # Add optional fields if available
            if "description" in row and pd.notna(row["description"]):
                event["description"] = str(row["description"])
            if "expected_impact" in row and pd.notna(row["expected_impact"]):
                event["expected_impact"] = str(row["expected_impact"])

            result.append(event)

        return result

    def get_event_details(self, event_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific event.

        Args:
            event_id (int): Index/ID of the event.

        Returns:
            Dict or None: Event details or None if not found.

        Example:
            >>> service = EventService(Path('data/events.csv'))
            >>> event = service.get_event_details(0)
            >>> event['event_name']
            'Gulf War'
        """
        if event_id >= len(self.data) or event_id < 0:
            return None

        row = self.data.iloc[event_id]
        event = {
            "id": event_id,
            "date": row["date"].strftime("%Y-%m-%d"),
            "event_name": str(row["event_name"]),
            "event_type": str(row["event_type"]),
        }

        # Add optional fields
        if "description" in row and pd.notna(row["description"]):
            event["description"] = str(row["description"])
        if "expected_impact" in row and pd.notna(row["expected_impact"]):
            event["expected_impact"] = str(row["expected_impact"])

        return event

    def get_event_impact(
        self, event_id: int, price_data: pd.DataFrame, window_days: int = 30
    ) -> Dict[str, Any]:
        """
        Calculate price impact around a specific event.

        Args:
            event_id (int): Index/ID of the event.
            price_data (pd.DataFrame): DataFrame with 'Date' and 'Price' columns.
            window_days (int): Number of days before/after event to analyze.

        Returns:
            Dict: Impact analysis including before/after prices and change.

        Example:
            >>> service = EventService(Path('data/events.csv'))
            >>> impact = service.get_event_impact(0, price_df, window_days=30)
            >>> impact['price_change_pct']
            15.3
        """
        if event_id >= len(self.data) or event_id < 0:
            return {"error": "Event not found"}

        event = self.data.iloc[event_id]
        event_date = event["date"]

        # Calculate date windows
        start_window = event_date - pd.Timedelta(days=window_days)
        end_window = event_date + pd.Timedelta(days=window_days)

        # Filter price data
        before_data = price_data[
            (price_data["Date"] >= start_window) & (price_data["Date"] < event_date)
        ]
        after_data = price_data[
            (price_data["Date"] > event_date) & (price_data["Date"] <= end_window)
        ]

        if len(before_data) == 0 or len(after_data) == 0:
            return {
                "error": "Insufficient data around event date",
                "event_date": event_date.strftime("%Y-%m-%d"),
            }

        # Calculate statistics
        mean_before = float(before_data["Price"].mean())
        mean_after = float(after_data["Price"].mean())
        price_change = mean_after - mean_before
        price_change_pct = (price_change / mean_before) * 100

        return {
            "event_id": event_id,
            "event_name": str(event["event_name"]),
            "event_date": event_date.strftime("%Y-%m-%d"),
            "window_days": window_days,
            "mean_price_before": mean_before,
            "mean_price_after": mean_after,
            "price_change": price_change,
            "price_change_pct": price_change_pct,
            "volatility_before": float(before_data["Price"].std()),
            "volatility_after": float(after_data["Price"].std()),
        }

    def get_event_types(self) -> List[str]:
        """
        Get list of unique event types in the dataset.

        Returns:
            List[str]: List of event type strings.
        """
        return list(self.data["event_type"].unique())

    def get_events_by_type(self) -> Dict[str, int]:
        """
        Get count of events grouped by type.

        Returns:
            Dict: Dictionary mapping event type to count.

        Example:
            >>> service = EventService(Path('data/events.csv'))
            >>> by_type = service.get_events_by_type()
            >>> by_type['geopolitical']
            7
        """
        type_counts = self.data["event_type"].value_counts()
        return {
            str(event_type): int(count) for event_type, count in type_counts.items()
        }
