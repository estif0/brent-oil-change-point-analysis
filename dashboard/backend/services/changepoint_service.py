"""
Change point service for handling detected change points data.

This module provides the ChangePointService class which handles loading,
filtering, and providing details about detected change points.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List
import sys

# Add project src to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))


class ChangePointService:
    """
    Service for managing change point data.

    This class provides methods to load and query detected change points
    from the Bayesian change point analysis.

    Attributes:
        changepoint_file (Path): Path to the change point summary CSV file.
        data (pd.DataFrame): Loaded change point data.
    """

    def __init__(self, changepoint_file: Path):
        """
        Initialize the ChangePointService.

        Args:
            changepoint_file (Path): Path to CSV file with change point summary.

        Raises:
            FileNotFoundError: If changepoint file does not exist.
        """
        self.changepoint_file = changepoint_file
        self.data = None
        self._load_data()

    def _load_data(self):
        """Load change point data from file."""
        if not self.changepoint_file.exists():
            # If file doesn't exist yet, initialize empty DataFrame
            self.data = pd.DataFrame(
                columns=[
                    "changepoint_id",
                    "date",
                    "mean_before",
                    "mean_after",
                    "std_before",
                    "std_after",
                    "price_change",
                    "percent_change",
                    "confidence",
                    "associated_event",
                ]
            )
            return

        try:
            self.data = pd.read_csv(self.changepoint_file)
            # Check if this is the expected format (processed changepoints)
            # vs model output format (posterior summaries)
            if (
                "date" not in self.data.columns
                and "changepoint_id" not in self.data.columns
            ):
                # File exists but doesn't have the expected structure
                # (likely raw model output, not processed results)
                self.data = pd.DataFrame(
                    columns=[
                        "changepoint_id",
                        "date",
                        "mean_before",
                        "mean_after",
                        "std_before",
                        "std_after",
                        "price_change",
                        "percent_change",
                        "confidence",
                        "associated_event",
                    ]
                )
                return

            # Ensure date column is datetime
            if "date" in self.data.columns:
                self.data["date"] = pd.to_datetime(self.data["date"])
        except Exception as e:
            # If there's any error loading, initialize empty DataFrame
            self.data = pd.DataFrame(
                columns=[
                    "changepoint_id",
                    "date",
                    "mean_before",
                    "mean_after",
                    "std_before",
                    "std_after",
                    "price_change",
                    "percent_change",
                    "confidence",
                    "associated_event",
                ]
            )

    def get_changepoints(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_confidence: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get list of detected change points with optional filtering.

        Args:
            start_date (str, optional): Filter change points from this date.
            end_date (str, optional): Filter change points until this date.
            min_confidence (float, optional): Minimum confidence threshold (0-1).

        Returns:
            List[Dict]: List of change point records.

        Example:
            >>> service = ChangePointService(Path('reports/changepoint_summary.csv'))
            >>> cps = service.get_changepoints(min_confidence=0.8)
            >>> len(cps)  # Number of high-confidence change points
            5
        """
        df = self.data.copy()

        # Apply filters
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        if min_confidence is not None:
            if "confidence" in df.columns:
                df = df[df["confidence"] >= min_confidence]

        # Convert to list of dictionaries
        result = []
        for _, row in df.iterrows():
            changepoint = {
                "id": int(row["changepoint_id"]) if "changepoint_id" in row else None,
                "date": (
                    row["date"].strftime("%Y-%m-%d") if pd.notna(row["date"]) else None
                ),
            }

            # Add all available columns dynamically
            for col in df.columns:
                if col not in ["changepoint_id", "date"]:
                    value = row[col]
                    if pd.notna(value):
                        if isinstance(value, (int, float)):
                            changepoint[col] = float(value)
                        else:
                            changepoint[col] = str(value)

            result.append(changepoint)

        return result

    def get_changepoint_details(self, changepoint_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a specific change point.

        Args:
            changepoint_id (int): ID of the change point.

        Returns:
            Dict or None: Change point details or None if not found.

        Example:
            >>> service = ChangePointService(Path('reports/changepoint_summary.csv'))
            >>> cp = service.get_changepoint_details(1)
            >>> cp['date']
            '2008-07-03'
        """
        if "changepoint_id" not in self.data.columns:
            return None

        cp_data = self.data[self.data["changepoint_id"] == changepoint_id]

        if len(cp_data) == 0:
            return None

        row = cp_data.iloc[0]
        result = {}

        for col in self.data.columns:
            value = row[col]
            if pd.notna(value):
                if col == "date":
                    result[col] = value.strftime("%Y-%m-%d")
                elif isinstance(value, (int, float)):
                    result[col] = float(value)
                else:
                    result[col] = str(value)

        return result

    def get_changepoint_count(self) -> int:
        """
        Get total number of detected change points.

        Returns:
            int: Count of change points.
        """
        return len(self.data)

    def get_changepoints_by_year(self) -> Dict[str, int]:
        """
        Get count of change points grouped by year.

        Returns:
            Dict: Dictionary mapping year to count of change points.

        Example:
            >>> service = ChangePointService(Path('reports/changepoint_summary.csv'))
            >>> by_year = service.get_changepoints_by_year()
            >>> by_year['2008']
            2
        """
        if len(self.data) == 0 or "date" not in self.data.columns:
            return {}

        df = self.data.copy()
        df["year"] = df["date"].dt.year
        year_counts = df["year"].value_counts().sort_index()

        return {str(year): int(count) for year, count in year_counts.items()}
