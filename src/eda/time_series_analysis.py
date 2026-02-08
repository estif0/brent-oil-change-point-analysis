"""
Exploratory Data Analysis (EDA) module for time series analysis.

This module provides classes and functions for analyzing time series data,
particularly focused on oil price analysis.
"""

from typing import Optional, Tuple
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.figure import Figure


class TimeSeriesAnalyzer:
    """
    A class for performing exploratory data analysis on time series data.

    This class provides methods for visualizing and analyzing time series data,
    calculating returns, rolling statistics, and volatility patterns.

    Attributes:
        data (pd.DataFrame): The time series data being analyzed.

    Example:
        >>> analyzer = TimeSeriesAnalyzer()
        >>> analyzer.data = price_data
        >>> fig = analyzer.plot_price_series()
        >>> returns = analyzer.calculate_log_returns()
    """

    def __init__(self, data: Optional[pd.DataFrame] = None):
        """
        Initialize the TimeSeriesAnalyzer.

        Args:
            data (pd.DataFrame, optional): Time series data with DatetimeIndex
                                          and numeric columns.
        """
        self.data = data

    def plot_price_series(
        self,
        data: Optional[pd.DataFrame] = None,
        column: str = "Price",
        title: str = "Brent Oil Price Over Time",
        figsize: Tuple[int, int] = (14, 6),
    ) -> Figure:
        """
        Visualize raw price series over time.

        Creates a line plot of the price series with customizable styling.

        Args:
            data (pd.DataFrame, optional): Data to plot. If None, uses self.data.
            column (str): Name of the column to plot. Default is 'Price'.
            title (str): Title for the plot.
            figsize (tuple): Figure size as (width, height).

        Returns:
            Figure: Matplotlib figure object.

        Raises:
            ValueError: If data is None and self.data is not set.
            KeyError: If specified column is not in the data.

        Example:
            >>> analyzer = TimeSeriesAnalyzer(price_data)
            >>> fig = analyzer.plot_price_series()
            >>> plt.show()
        """
        plot_data = data if data is not None else self.data

        if plot_data is None:
            raise ValueError("No data provided. Pass data or set self.data.")

        if column not in plot_data.columns:
            raise KeyError(
                f"Column '{column}' not found in data. Available: {plot_data.columns.tolist()}"
            )

        fig, ax = plt.subplots(figsize=figsize)

        ax.plot(plot_data.index, plot_data[column], linewidth=1, color="#2E86AB")
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Price (USD/barrel)", fontsize=12)
        ax.set_title(title, fontsize=14, fontweight="bold")
        ax.grid(True, alpha=0.3)

        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:.0f}"))

        plt.tight_layout()

        return fig

    def calculate_log_returns(
        self, data: Optional[pd.DataFrame] = None, column: str = "Price"
    ) -> pd.Series:
        """
        Calculate log returns from price data.

        Log returns are calculated as: ln(P_t / P_{t-1})
        where P_t is the price at time t.

        Args:
            data (pd.DataFrame, optional): Data containing prices. If None, uses self.data.
            column (str): Name of the price column. Default is 'Price'.

        Returns:
            pd.Series: Series of log returns with the same index as input data.

        Raises:
            ValueError: If data is None and self.data is not set.
            KeyError: If specified column is not in the data.

        Example:
            >>> analyzer = TimeSeriesAnalyzer(price_data)
            >>> log_returns = analyzer.calculate_log_returns()
            >>> print(f"Mean return: {log_returns.mean():.4f}")
        """
        calc_data = data if data is not None else self.data

        if calc_data is None:
            raise ValueError("No data provided. Pass data or set self.data.")

        if column not in calc_data.columns:
            raise KeyError(
                f"Column '{column}' not found in data. Available: {calc_data.columns.tolist()}"
            )

        # Calculate log returns
        log_returns = np.log(calc_data[column] / calc_data[column].shift(1))

        return log_returns

    def plot_log_returns(
        self,
        data: Optional[pd.DataFrame] = None,
        column: str = "Price",
        title: str = "Brent Oil Log Returns",
        figsize: Tuple[int, int] = (14, 8),
    ) -> Figure:
        """
        Visualize log returns over time.

        Creates a subplot with log returns time series and distribution histogram.

        Args:
            data (pd.DataFrame, optional): Data containing prices. If None, uses self.data.
            column (str): Name of the price column. Default is 'Price'.
            title (str): Title for the plot.
            figsize (tuple): Figure size as (width, height).

        Returns:
            Figure: Matplotlib figure object.

        Raises:
            ValueError: If data is None and self.data is not set.

        Example:
            >>> analyzer = TimeSeriesAnalyzer(price_data)
            >>> fig = analyzer.plot_log_returns()
            >>> plt.show()
        """
        plot_data = data if data is not None else self.data

        if plot_data is None:
            raise ValueError("No data provided. Pass data or set self.data.")

        # Calculate log returns
        log_returns = self.calculate_log_returns(plot_data, column)

        # Create subplots
        fig, axes = plt.subplots(2, 1, figsize=figsize)

        # Time series plot
        axes[0].plot(
            log_returns.index, log_returns, linewidth=0.8, color="#A23B72", alpha=0.8
        )
        axes[0].axhline(y=0, color="black", linestyle="--", linewidth=0.8, alpha=0.5)
        axes[0].set_xlabel("Date", fontsize=11)
        axes[0].set_ylabel("Log Returns", fontsize=11)
        axes[0].set_title(f"{title} - Time Series", fontsize=12, fontweight="bold")
        axes[0].grid(True, alpha=0.3)

        # Distribution plot
        log_returns_clean = log_returns.dropna()
        axes[1].hist(
            log_returns_clean, bins=100, color="#F18F01", alpha=0.7, edgecolor="black"
        )
        axes[1].axvline(
            log_returns_clean.mean(),
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Mean: {log_returns_clean.mean():.5f}",
        )
        axes[1].set_xlabel("Log Returns", fontsize=11)
        axes[1].set_ylabel("Frequency", fontsize=11)
        axes[1].set_title(f"{title} - Distribution", fontsize=12, fontweight="bold")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3, axis="y")

        plt.tight_layout()

        return fig

    def calculate_rolling_stats(
        self,
        data: Optional[pd.DataFrame] = None,
        column: str = "Price",
        window: int = 30,
    ) -> pd.DataFrame:
        """
        Calculate rolling mean and standard deviation.

        Computes rolling statistics over a specified window to identify
        trends and volatility patterns.

        Args:
            data (pd.DataFrame, optional): Data containing prices. If None, uses self.data.
            column (str): Name of the column to analyze. Default is 'Price'.
            window (int): Rolling window size in days. Default is 30.

        Returns:
            pd.DataFrame: DataFrame with columns 'rolling_mean' and 'rolling_std'.

        Raises:
            ValueError: If data is None and self.data is not set, or if window < 1.
            KeyError: If specified column is not in the data.

        Example:
            >>> analyzer = TimeSeriesAnalyzer(price_data)
            >>> rolling_stats = analyzer.calculate_rolling_stats(window=60)
            >>> print(rolling_stats.head())
        """
        calc_data = data if data is not None else self.data

        if calc_data is None:
            raise ValueError("No data provided. Pass data or set self.data.")

        if window < 1:
            raise ValueError("Window size must be at least 1")

        if column not in calc_data.columns:
            raise KeyError(
                f"Column '{column}' not found in data. Available: {calc_data.columns.tolist()}"
            )

        # Calculate rolling statistics
        rolling_stats = pd.DataFrame(index=calc_data.index)
        rolling_stats["rolling_mean"] = calc_data[column].rolling(window=window).mean()
        rolling_stats["rolling_std"] = calc_data[column].rolling(window=window).std()

        return rolling_stats

    def plot_volatility(
        self,
        data: Optional[pd.DataFrame] = None,
        column: str = "Price",
        window: int = 30,
        title: str = "Brent Oil Price Volatility Analysis",
        figsize: Tuple[int, int] = (14, 10),
    ) -> Figure:
        """
        Visualize price volatility patterns over time.

        Creates subplots showing:
        1. Price with rolling mean
        2. Rolling standard deviation (volatility)
        3. Log returns volatility

        Args:
            data (pd.DataFrame, optional): Data containing prices. If None, uses self.data.
            column (str): Name of the price column. Default is 'Price'.
            window (int): Rolling window size in days. Default is 30.
            title (str): Title for the plot.
            figsize (tuple): Figure size as (width, height).

        Returns:
            Figure: Matplotlib figure object.

        Raises:
            ValueError: If data is None and self.data is not set.

        Example:
            >>> analyzer = TimeSeriesAnalyzer(price_data)
            >>> fig = analyzer.plot_volatility(window=60)
            >>> plt.show()
        """
        plot_data = data if data is not None else self.data

        if plot_data is None:
            raise ValueError("No data provided. Pass data or set self.data.")

        # Calculate statistics
        rolling_stats = self.calculate_rolling_stats(plot_data, column, window)
        log_returns = self.calculate_log_returns(plot_data, column)

        # Calculate rolling volatility of returns
        returns_volatility = log_returns.rolling(window=window).std()

        # Create subplots
        fig, axes = plt.subplots(3, 1, figsize=figsize)

        # Plot 1: Price with rolling mean
        axes[0].plot(
            plot_data.index,
            plot_data[column],
            linewidth=1,
            alpha=0.7,
            label="Price",
            color="#2E86AB",
        )
        axes[0].plot(
            rolling_stats.index,
            rolling_stats["rolling_mean"],
            linewidth=2,
            label=f"{window}-day Rolling Mean",
            color="#F18F01",
        )
        axes[0].set_ylabel("Price (USD/barrel)", fontsize=11)
        axes[0].set_title(f"{title} - Price and Trend", fontsize=12, fontweight="bold")
        axes[0].legend(loc="upper left")
        axes[0].grid(True, alpha=0.3)
        axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:.0f}"))

        # Plot 2: Rolling standard deviation (price volatility)
        axes[1].plot(
            rolling_stats.index,
            rolling_stats["rolling_std"],
            linewidth=1.5,
            color="#A23B72",
            label=f"{window}-day Rolling Std Dev",
        )
        axes[1].fill_between(
            rolling_stats.index,
            rolling_stats["rolling_std"],
            alpha=0.3,
            color="#A23B72",
        )
        axes[1].set_ylabel("Standard Deviation", fontsize=11)
        axes[1].set_title(f"{title} - Price Volatility", fontsize=12, fontweight="bold")
        axes[1].legend(loc="upper left")
        axes[1].grid(True, alpha=0.3)

        # Plot 3: Returns volatility
        axes[2].plot(
            returns_volatility.index,
            returns_volatility,
            linewidth=1.5,
            color="#C73E1D",
            label=f"{window}-day Returns Volatility",
        )
        axes[2].fill_between(
            returns_volatility.index, returns_volatility, alpha=0.3, color="#C73E1D"
        )
        axes[2].set_xlabel("Date", fontsize=11)
        axes[2].set_ylabel("Volatility", fontsize=11)
        axes[2].set_title(
            f"{title} - Returns Volatility", fontsize=12, fontweight="bold"
        )
        axes[2].legend(loc="upper left")
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()

        return fig

    def get_summary_statistics(
        self, data: Optional[pd.DataFrame] = None, column: str = "Price"
    ) -> dict:
        """
        Get comprehensive summary statistics for the time series.

        Args:
            data (pd.DataFrame, optional): Data to analyze. If None, uses self.data.
            column (str): Name of the column to analyze. Default is 'Price'.

        Returns:
            dict: Dictionary containing summary statistics including:
                - Basic stats (mean, median, std, min, max)
                - Returns stats (mean return, volatility)
                - Percentiles

        Raises:
            ValueError: If data is None and self.data is not set.
        """
        calc_data = data if data is not None else self.data

        if calc_data is None:
            raise ValueError("No data provided. Pass data or set self.data.")

        if column not in calc_data.columns:
            raise KeyError(f"Column '{column}' not found in data.")

        prices = calc_data[column].dropna()
        log_returns = self.calculate_log_returns(calc_data, column).dropna()

        # Handle date range for empty data
        if len(calc_data) > 0 and not pd.isna(calc_data.index.min()):
            date_range = (
                str(calc_data.index.min().date()),
                str(calc_data.index.max().date()),
            )
        else:
            date_range = (None, None)

        return {
            "price_stats": {
                "mean": float(prices.mean()),
                "median": float(prices.median()),
                "std": float(prices.std()),
                "min": float(prices.min()),
                "max": float(prices.max()),
                "percentile_25": float(prices.quantile(0.25)),
                "percentile_75": float(prices.quantile(0.75)),
            },
            "returns_stats": {
                "mean_return": float(log_returns.mean()),
                "volatility": float(log_returns.std()),
                "skewness": float(log_returns.skew()),
                "kurtosis": float(log_returns.kurtosis()),
            },
            "data_info": {"count": int(len(prices)), "date_range": date_range},
        }
