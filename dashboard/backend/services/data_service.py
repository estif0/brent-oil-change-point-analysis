"""
Data service for handling historical Brent oil price data.

This module provides the DataService class which handles loading,
filtering, and computing statistics for historical price data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List
import sys

# Add project src to path
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from src.data.loader import BrentDataLoader


class DataService:
    """
    Service for managing historical Brent oil price data.

    This class provides methods to load, filter, and compute statistics
    on historical Brent oil prices for the dashboard API.

    Attributes:
        data_file (Path): Path to the Brent oil prices CSV file.
        data (pd.DataFrame): Loaded price data.
        loader (BrentDataLoader): Data loader instance.
    """

    def __init__(self, data_file: Path):
        """
        Initialize the DataService.

        Args:
            data_file (Path): Path to the CSV file containing Brent oil prices.

        Raises:
            FileNotFoundError: If data file does not exist.
        """
        self.data_file = data_file
        self.loader = BrentDataLoader()
        self.data = None
        self._load_data()

    def _load_data(self):
        """Load data from file using BrentDataLoader."""
        self.data = self.loader.load_data(self.data_file)
        if self.data is None:
            raise ValueError("Failed to load data")
        # Reset index to make Date a column instead of index
        self.data = self.data.reset_index()

    def get_historical_prices(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get historical price data within specified date range.

        Args:
            start_date (str, optional): Start date in 'YYYY-MM-DD' format.
                                       If None, returns from earliest date.
            end_date (str, optional): End date in 'YYYY-MM-DD' format.
                                     If None, returns up to latest date.

        Returns:
            List[Dict]: List of price records with 'date' and 'price' keys.

        Example:
            >>> service = DataService(Path('data/BrentOilPrices.csv'))
            >>> prices = service.get_historical_prices('2020-01-01', '2020-12-31')
            >>> len(prices)  # Number of records in 2020
            253
        """
        df = self.data.copy()

        # Filter by date range
        if start_date:
            df = df[df["Date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["Date"] <= pd.to_datetime(end_date)]

        # Convert to list of dictionaries
        result = []
        for _, row in df.iterrows():
            result.append(
                {"date": row["Date"].strftime("%Y-%m-%d"), "price": float(row["Price"])}
            )

        return result

    def get_price_statistics(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate summary statistics for prices in specified date range.

        Args:
            start_date (str, optional): Start date in 'YYYY-MM-DD' format.
            end_date (str, optional): End date in 'YYYY-MM-DD' format.

        Returns:
            Dict: Dictionary containing statistical measures:
                - mean: Average price
                - median: Median price
                - std: Standard deviation
                - min: Minimum price
                - max: Maximum price
                - count: Number of data points
                - start_date: Actual start date of the range
                - end_date: Actual end date of the range

        Example:
            >>> service = DataService(Path('data/BrentOilPrices.csv'))
            >>> stats = service.get_price_statistics('2020-01-01', '2020-12-31')
            >>> stats['mean']  # Average price in 2020
            43.21
        """
        df = self.data.copy()

        # Filter by date range
        if start_date:
            df = df[df["Date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["Date"] <= pd.to_datetime(end_date)]

        if len(df) == 0:
            return {
                "error": "No data available for the specified date range",
                "count": 0,
            }

        prices = df["Price"]

        return {
            "mean": float(prices.mean()),
            "median": float(prices.median()),
            "std": float(prices.std()),
            "min": float(prices.min()),
            "max": float(prices.max()),
            "count": int(len(prices)),
            "start_date": df["Date"].min().strftime("%Y-%m-%d"),
            "end_date": df["Date"].max().strftime("%Y-%m-%d"),
            "percentile_25": float(prices.quantile(0.25)),
            "percentile_75": float(prices.quantile(0.75)),
        }

    def get_date_range(self) -> Dict[str, str]:
        """
        Get the full date range available in the dataset.

        Returns:
            Dict: Dictionary with 'min_date' and 'max_date' keys.

        Example:
            >>> service = DataService(Path('data/BrentOilPrices.csv'))
            >>> date_range = service.get_date_range()
            >>> date_range['min_date']
            '1987-05-20'
        """
        return {
            "min_date": self.data["Date"].min().strftime("%Y-%m-%d"),
            "max_date": self.data["Date"].max().strftime("%Y-%m-%d"),
        }

    def get_data_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded dataset.

        Returns:
            Dict: Dataset information including record count and date range.
        """
        return {
            "total_records": len(self.data),
            "date_range": self.get_date_range(),
            "columns": list(self.data.columns),
            "missing_values": int(self.data.isnull().sum().sum()),
        }
