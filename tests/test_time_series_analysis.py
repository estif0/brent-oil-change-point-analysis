"""
Unit tests for the TimeSeriesAnalyzer class.
"""

import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from src.eda.time_series_analysis import TimeSeriesAnalyzer


class TestTimeSeriesAnalyzer:
    """Test cases for TimeSeriesAnalyzer class."""

    @pytest.fixture
    def sample_price_data(self):
        """Create sample price data for testing."""
        dates = pd.date_range(start="2020-01-01", end="2020-12-31", freq="D")
        prices = 50 + np.cumsum(np.random.randn(len(dates)) * 2)  # Random walk

        df = pd.DataFrame({"Price": prices}, index=dates)
        return df

    @pytest.fixture
    def sample_price_data_with_nulls(self):
        """Create sample price data with null values."""
        dates = pd.date_range(start="2020-01-01", end="2020-12-31", freq="D")
        prices = 50 + np.cumsum(np.random.randn(len(dates)) * 2)
        prices[100:105] = np.nan  # Add some nulls

        df = pd.DataFrame({"Price": prices}, index=dates)
        return df

    def test_initialization_without_data(self):
        """Test TimeSeriesAnalyzer initialization without data."""
        analyzer = TimeSeriesAnalyzer()
        assert analyzer.data is None

    def test_initialization_with_data(self, sample_price_data):
        """Test TimeSeriesAnalyzer initialization with data."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)
        assert analyzer.data is not None
        assert len(analyzer.data) == len(sample_price_data)

    def test_plot_price_series_with_data(self, sample_price_data):
        """Test plotting price series with valid data."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)
        fig = analyzer.plot_price_series()

        assert isinstance(fig, Figure)
        assert len(fig.axes) == 1

        plt.close(fig)

    def test_plot_price_series_with_passed_data(self, sample_price_data):
        """Test plotting price series with data passed directly."""
        analyzer = TimeSeriesAnalyzer()
        fig = analyzer.plot_price_series(data=sample_price_data)

        assert isinstance(fig, Figure)
        plt.close(fig)

    def test_plot_price_series_without_data(self):
        """Test plotting price series without data raises error."""
        analyzer = TimeSeriesAnalyzer()

        with pytest.raises(ValueError, match="No data provided"):
            analyzer.plot_price_series()

    def test_plot_price_series_invalid_column(self, sample_price_data):
        """Test plotting price series with invalid column name."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)

        with pytest.raises(KeyError, match="not found in data"):
            analyzer.plot_price_series(column="InvalidColumn")

    def test_calculate_log_returns_valid(self, sample_price_data):
        """Test calculating log returns with valid data."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)
        log_returns = analyzer.calculate_log_returns()

        assert isinstance(log_returns, pd.Series)
        assert len(log_returns) == len(sample_price_data)
        # First value should be NaN
        assert pd.isna(log_returns.iloc[0])
        # Remaining values should be numeric
        assert not log_returns.iloc[1:].isna().all()

    def test_calculate_log_returns_mathematical_correctness(self):
        """Test log returns calculation is mathematically correct."""
        # Create simple test data
        dates = pd.date_range(start="2020-01-01", periods=5, freq="D")
        prices = pd.Series([100, 110, 105, 115, 120], index=dates)
        df = pd.DataFrame({"Price": prices})

        analyzer = TimeSeriesAnalyzer(df)
        log_returns = analyzer.calculate_log_returns()

        # Manually calculate expected log returns
        expected = np.log(110 / 100)

        assert abs(log_returns.iloc[1] - expected) < 1e-10

    def test_calculate_log_returns_without_data(self):
        """Test calculating log returns without data raises error."""
        analyzer = TimeSeriesAnalyzer()

        with pytest.raises(ValueError, match="No data provided"):
            analyzer.calculate_log_returns()

    def test_calculate_log_returns_invalid_column(self, sample_price_data):
        """Test calculating log returns with invalid column."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)

        with pytest.raises(KeyError, match="not found in data"):
            analyzer.calculate_log_returns(column="InvalidColumn")

    def test_plot_log_returns_valid(self, sample_price_data):
        """Test plotting log returns with valid data."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)
        fig = analyzer.plot_log_returns()

        assert isinstance(fig, Figure)
        assert len(fig.axes) == 2  # Time series and distribution

        plt.close(fig)

    def test_plot_log_returns_without_data(self):
        """Test plotting log returns without data raises error."""
        analyzer = TimeSeriesAnalyzer()

        with pytest.raises(ValueError, match="No data provided"):
            analyzer.plot_log_returns()

    def test_calculate_rolling_stats_valid(self, sample_price_data):
        """Test calculating rolling statistics with valid data."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)
        rolling_stats = analyzer.calculate_rolling_stats(window=30)

        assert isinstance(rolling_stats, pd.DataFrame)
        assert "rolling_mean" in rolling_stats.columns
        assert "rolling_std" in rolling_stats.columns
        assert len(rolling_stats) == len(sample_price_data)

        # First window-1 values should be NaN
        assert rolling_stats["rolling_mean"].iloc[:29].isna().all()
        # Values after window should be numeric
        assert not rolling_stats["rolling_mean"].iloc[29:].isna().all()

    def test_calculate_rolling_stats_different_windows(self, sample_price_data):
        """Test rolling statistics with different window sizes."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)

        for window in [7, 14, 30, 60]:
            rolling_stats = analyzer.calculate_rolling_stats(window=window)
            # Check first window-1 values are NaN
            assert rolling_stats["rolling_mean"].iloc[window - 1 :].notna().any()

    def test_calculate_rolling_stats_invalid_window(self, sample_price_data):
        """Test calculating rolling statistics with invalid window size."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)

        with pytest.raises(ValueError, match="Window size must be at least 1"):
            analyzer.calculate_rolling_stats(window=0)

        with pytest.raises(ValueError, match="Window size must be at least 1"):
            analyzer.calculate_rolling_stats(window=-5)

    def test_calculate_rolling_stats_without_data(self):
        """Test calculating rolling statistics without data raises error."""
        analyzer = TimeSeriesAnalyzer()

        with pytest.raises(ValueError, match="No data provided"):
            analyzer.calculate_rolling_stats()

    def test_calculate_rolling_stats_invalid_column(self, sample_price_data):
        """Test calculating rolling statistics with invalid column."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)

        with pytest.raises(KeyError, match="not found in data"):
            analyzer.calculate_rolling_stats(column="InvalidColumn")

    def test_plot_volatility_valid(self, sample_price_data):
        """Test plotting volatility analysis with valid data."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)
        fig = analyzer.plot_volatility(window=30)

        assert isinstance(fig, Figure)
        assert len(fig.axes) == 3  # Price, volatility, returns volatility

        plt.close(fig)

    def test_plot_volatility_different_windows(self, sample_price_data):
        """Test plotting volatility with different window sizes."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)

        for window in [7, 14, 30]:
            fig = analyzer.plot_volatility(window=window)
            assert isinstance(fig, Figure)
            plt.close(fig)

    def test_plot_volatility_without_data(self):
        """Test plotting volatility without data raises error."""
        analyzer = TimeSeriesAnalyzer()

        with pytest.raises(ValueError, match="No data provided"):
            analyzer.plot_volatility()

    def test_get_summary_statistics_valid(self, sample_price_data):
        """Test getting summary statistics with valid data."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)
        stats = analyzer.get_summary_statistics()

        assert "price_stats" in stats
        assert "returns_stats" in stats
        assert "data_info" in stats

        # Check price stats
        assert "mean" in stats["price_stats"]
        assert "median" in stats["price_stats"]
        assert "std" in stats["price_stats"]
        assert "min" in stats["price_stats"]
        assert "max" in stats["price_stats"]

        # Check returns stats
        assert "mean_return" in stats["returns_stats"]
        assert "volatility" in stats["returns_stats"]
        assert "skewness" in stats["returns_stats"]
        assert "kurtosis" in stats["returns_stats"]

        # Check data info
        assert "count" in stats["data_info"]
        assert "date_range" in stats["data_info"]

    def test_get_summary_statistics_without_data(self):
        """Test getting summary statistics without data raises error."""
        analyzer = TimeSeriesAnalyzer()

        with pytest.raises(ValueError, match="No data provided"):
            analyzer.get_summary_statistics()

    def test_get_summary_statistics_with_nulls(self, sample_price_data_with_nulls):
        """Test summary statistics with null values."""
        analyzer = TimeSeriesAnalyzer(sample_price_data_with_nulls)
        stats = analyzer.get_summary_statistics()

        # Should handle nulls gracefully
        assert stats is not None
        assert stats["data_info"]["count"] > 0

    def test_custom_column_name(self):
        """Test analyzer with custom column name."""
        dates = pd.date_range(start="2020-01-01", periods=100, freq="D")
        df = pd.DataFrame({"CustomPrice": np.random.randn(100) + 50}, index=dates)

        analyzer = TimeSeriesAnalyzer(df)

        # Should work with custom column name
        fig = analyzer.plot_price_series(column="CustomPrice")
        assert isinstance(fig, Figure)
        plt.close(fig)

        log_returns = analyzer.calculate_log_returns(column="CustomPrice")
        assert isinstance(log_returns, pd.Series)

    def test_data_persistence(self, sample_price_data):
        """Test that data persists across method calls."""
        analyzer = TimeSeriesAnalyzer(sample_price_data)

        # Call multiple methods
        fig1 = analyzer.plot_price_series()
        log_returns = analyzer.calculate_log_returns()
        rolling_stats = analyzer.calculate_rolling_stats()
        stats = analyzer.get_summary_statistics()

        # Data should still be accessible
        assert analyzer.data is not None
        assert len(analyzer.data) == len(sample_price_data)

        plt.close(fig1)

    def test_empty_dataframe(self):
        """Test analyzer with empty dataframe."""
        df = pd.DataFrame({"Price": []})
        analyzer = TimeSeriesAnalyzer(df)

        # Should handle gracefully or raise appropriate error
        # This will depend on implementation details
        # For now, we just check it doesn't crash unexpectedly
        try:
            stats = analyzer.get_summary_statistics()
        except (ValueError, ZeroDivisionError):
            # These are acceptable errors for empty data
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
