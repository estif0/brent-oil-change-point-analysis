"""
Data loading module for Brent oil price data.

This module provides classes for loading and validating Brent oil price data
from CSV files.
"""

from typing import Tuple
import pandas as pd
import numpy as np
from pathlib import Path


class BrentDataLoader:
    """
    A class for loading and validating Brent oil price data.

    This class handles loading Brent oil price data from CSV files,
    validates the data for missing values and date continuity,
    and provides utility methods for date range extraction.

    Attributes:
        data (pd.DataFrame): The loaded price data with Date and Price columns.
        file_path (str): Path to the data file.

    Example:
        >>> loader = BrentDataLoader()
        >>> data = loader.load_data('data/raw/BrentOilPrices.csv')
        >>> loader.validate_data()
        >>> start_date, end_date = loader.get_date_range()
    """

    def __init__(self):
        """Initialize the BrentDataLoader."""
        self.data: pd.DataFrame = None
        self.file_path: str = None

    def load_data(self, file_path: str) -> pd.DataFrame:
        """
        Load Brent oil price data from a CSV file.

        The CSV file should have columns: 'Date' and 'Price'.
        Dates are parsed from various formats and set as the index.

        Args:
            file_path (str): Path to the CSV file containing Brent oil prices.

        Returns:
            pd.DataFrame: DataFrame with DatetimeIndex and 'Price' column.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            ValueError: If the CSV does not contain required columns.

        Example:
            >>> loader = BrentDataLoader()
            >>> data = loader.load_data('data/raw/BrentOilPrices.csv')
            >>> print(data.head())
        """
        # Check if file exists
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        # Load the CSV file
        try:
            self.data = pd.read_csv(file_path)
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {e}")

        # Validate required columns exist
        if "Date" not in self.data.columns or "Price" not in self.data.columns:
            raise ValueError(
                f"CSV must contain 'Date' and 'Price' columns. Found: {self.data.columns.tolist()}"
            )

        # Parse dates and set as index
        try:
            self.data["Date"] = pd.to_datetime(self.data["Date"], format="%d-%b-%y")
        except:
            # Try alternative formats if the first one fails
            self.data["Date"] = pd.to_datetime(self.data["Date"])

        self.data.set_index("Date", inplace=True)
        self.data.sort_index(inplace=True)

        # Convert Price to numeric, handling any non-numeric values
        self.data["Price"] = pd.to_numeric(self.data["Price"], errors="coerce")

        self.file_path = file_path

        return self.data

    def validate_data(self) -> dict:
        """
        Validate the loaded data for missing values and date continuity.

        Checks for:
        - Missing values in the Price column
        - Duplicate dates
        - Data completeness

        Returns:
            dict: Validation results containing:
                - missing_count (int): Number of missing price values
                - duplicate_dates (int): Number of duplicate dates
                - total_records (int): Total number of records
                - is_valid (bool): Whether the data passes basic validation
                - warnings (list): List of warning messages

        Raises:
            RuntimeError: If no data has been loaded yet.

        Example:
            >>> loader = BrentDataLoader()
            >>> loader.load_data('data/raw/BrentOilPrices.csv')
            >>> results = loader.validate_data()
            >>> if not results['is_valid']:
            ...     print(results['warnings'])
        """
        if self.data is None:
            raise RuntimeError("No data loaded. Call load_data() first.")

        validation_results = {
            "missing_count": 0,
            "duplicate_dates": 0,
            "total_records": len(self.data),
            "is_valid": True,
            "warnings": [],
        }

        # Check for missing values
        missing_count = self.data["Price"].isna().sum()
        validation_results["missing_count"] = int(missing_count)

        if missing_count > 0:
            validation_results["warnings"].append(
                f"Found {missing_count} missing price values ({missing_count/len(self.data)*100:.2f}%)"
            )

        # Check for duplicate dates
        duplicate_count = self.data.index.duplicated().sum()
        validation_results["duplicate_dates"] = int(duplicate_count)

        if duplicate_count > 0:
            validation_results["is_valid"] = False
            validation_results["warnings"].append(
                f"Found {duplicate_count} duplicate dates"
            )

        # Check for negative prices
        if (self.data["Price"] < 0).any():
            validation_results["is_valid"] = False
            validation_results["warnings"].append("Found negative price values")

        return validation_results

    def get_date_range(self) -> Tuple[pd.Timestamp, pd.Timestamp]:
        """
        Get the minimum and maximum dates in the dataset.

        Returns:
            Tuple[pd.Timestamp, pd.Timestamp]: A tuple of (start_date, end_date).

        Raises:
            RuntimeError: If no data has been loaded yet.

        Example:
            >>> loader = BrentDataLoader()
            >>> loader.load_data('data/raw/BrentOilPrices.csv')
            >>> start, end = loader.get_date_range()
            >>> print(f"Data spans from {start.date()} to {end.date()}")
        """
        if self.data is None:
            raise RuntimeError("No data loaded. Call load_data() first.")

        return self.data.index.min(), self.data.index.max()

    def get_summary_statistics(self) -> dict:
        """
        Get summary statistics for the price data.

        Returns:
            dict: Dictionary containing summary statistics:
                - mean, median, std, min, max, count

        Raises:
            RuntimeError: If no data has been loaded yet.
        """
        if self.data is None:
            raise RuntimeError("No data loaded. Call load_data() first.")

        price_series = self.data["Price"].dropna()

        return {
            "count": int(len(price_series)),
            "mean": float(price_series.mean()),
            "median": float(price_series.median()),
            "std": float(price_series.std()),
            "min": float(price_series.min()),
            "max": float(price_series.max()),
            "date_range": (
                str(self.data.index.min().date()),
                str(self.data.index.max().date()),
            ),
        }
