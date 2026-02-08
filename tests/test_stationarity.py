"""
Unit tests for the StationarityTester class.
"""

import pytest
import pandas as pd
import numpy as np

from src.statistical_tests.stationarity import StationarityTester


class TestStationarityTester:
    """Test cases for StationarityTester class."""

    @pytest.fixture
    def stationary_series(self):
        """Create a stationary time series (white noise)."""
        np.random.seed(42)
        return pd.Series(np.random.randn(1000))

    @pytest.fixture
    def non_stationary_series(self):
        """Create a non-stationary time series (random walk)."""
        np.random.seed(42)
        return pd.Series(np.cumsum(np.random.randn(1000)))

    @pytest.fixture
    def trend_series(self):
        """Create a series with a trend."""
        np.random.seed(42)
        t = np.arange(1000)
        return pd.Series(0.5 * t + np.random.randn(1000) * 10)

    @pytest.fixture
    def series_with_nulls(self):
        """Create a series with null values."""
        np.random.seed(42)
        series = pd.Series(np.random.randn(100))
        series.iloc[10:15] = np.nan
        return series

    def test_initialization(self):
        """Test StationarityTester initialization."""
        tester = StationarityTester()
        assert tester is not None

    def test_adf_test_stationary_series(self, stationary_series):
        """Test ADF test on stationary series."""
        tester = StationarityTester()
        results = tester.adf_test(stationary_series)

        # Check all required fields are present
        assert "test_statistic" in results
        assert "p_value" in results
        assert "used_lag" in results
        assert "n_obs" in results
        assert "critical_values" in results
        assert "is_stationary" in results

        # Check data types
        assert isinstance(results["test_statistic"], float)
        assert isinstance(results["p_value"], float)
        assert isinstance(results["used_lag"], int)
        assert isinstance(results["n_obs"], int)
        assert isinstance(results["critical_values"], dict)
        assert isinstance(results["is_stationary"], bool)

        # Stationary series should have low p-value
        assert results["is_stationary"] is True
        assert results["p_value"] < 0.05

    def test_adf_test_non_stationary_series(self, non_stationary_series):
        """Test ADF test on non-stationary series."""
        tester = StationarityTester()
        results = tester.adf_test(non_stationary_series)

        # Non-stationary series should have high p-value
        assert results["is_stationary"] is False
        assert results["p_value"] >= 0.05

    def test_adf_test_empty_series(self):
        """Test ADF test with empty series."""
        tester = StationarityTester()
        empty_series = pd.Series([])

        with pytest.raises(ValueError, match="empty or contains only NaN"):
            tester.adf_test(empty_series)

    def test_adf_test_all_nan_series(self):
        """Test ADF test with series containing only NaN."""
        tester = StationarityTester()
        nan_series = pd.Series([np.nan, np.nan, np.nan])

        with pytest.raises(ValueError, match="empty or contains only NaN"):
            tester.adf_test(nan_series)

    def test_adf_test_with_nulls(self, series_with_nulls):
        """Test ADF test with series containing some NaN values."""
        tester = StationarityTester()
        results = tester.adf_test(series_with_nulls)

        # Should handle NaN values by dropping them
        assert results is not None
        assert "p_value" in results

    def test_adf_test_different_regressions(self, stationary_series):
        """Test ADF test with different regression parameters."""
        tester = StationarityTester()

        for regression in ["c", "ct", "ctt", "n"]:
            results = tester.adf_test(stationary_series, regression=regression)
            assert results is not None
            assert "p_value" in results

    def test_adf_test_different_autolags(self, stationary_series):
        """Test ADF test with different autolag methods."""
        tester = StationarityTester()

        for autolag in ["AIC", "BIC", "t-stat"]:
            results = tester.adf_test(stationary_series, autolag=autolag)
            assert results is not None
            assert "p_value" in results

    def test_kpss_test_stationary_series(self, stationary_series):
        """Test KPSS test on stationary series."""
        tester = StationarityTester()
        results = tester.kpss_test(stationary_series)

        # Check all required fields are present
        assert "test_statistic" in results
        assert "p_value" in results
        assert "used_lag" in results
        assert "critical_values" in results
        assert "is_stationary" in results

        # Check data types
        assert isinstance(results["test_statistic"], float)
        assert isinstance(results["p_value"], float)
        assert isinstance(results["used_lag"], int)
        assert isinstance(results["critical_values"], dict)
        assert isinstance(results["is_stationary"], bool)

        # Stationary series should have high p-value in KPSS
        assert results["is_stationary"] is True
        assert results["p_value"] > 0.05

    def test_kpss_test_non_stationary_series(self, non_stationary_series):
        """Test KPSS test on non-stationary series."""
        tester = StationarityTester()
        results = tester.kpss_test(non_stationary_series)

        # Non-stationary series should have low p-value in KPSS
        assert results["is_stationary"] is False
        assert results["p_value"] <= 0.05

    def test_kpss_test_empty_series(self):
        """Test KPSS test with empty series."""
        tester = StationarityTester()
        empty_series = pd.Series([])

        with pytest.raises(ValueError, match="empty or contains only NaN"):
            tester.kpss_test(empty_series)

    def test_kpss_test_all_nan_series(self):
        """Test KPSS test with series containing only NaN."""
        tester = StationarityTester()
        nan_series = pd.Series([np.nan, np.nan, np.nan])

        with pytest.raises(ValueError, match="empty or contains only NaN"):
            tester.kpss_test(nan_series)

    def test_kpss_test_with_nulls(self, series_with_nulls):
        """Test KPSS test with series containing some NaN values."""
        tester = StationarityTester()
        results = tester.kpss_test(series_with_nulls)

        # Should handle NaN values by dropping them
        assert results is not None
        assert "p_value" in results

    def test_kpss_test_different_regressions(self, stationary_series):
        """Test KPSS test with different regression parameters."""
        tester = StationarityTester()

        for regression in ["c", "ct"]:
            results = tester.kpss_test(stationary_series, regression=regression)
            assert results is not None
            assert "p_value" in results

    def test_interpret_results_adf_stationary(self):
        """Test interpretation of ADF results for stationary series."""
        tester = StationarityTester()
        interpretation = tester.interpret_results(
            test_statistic=-5.0, p_value=0.001, test_type="adf"
        )

        assert isinstance(interpretation, str)
        assert "ADF" in interpretation
        assert "STATIONARY" in interpretation
        assert "Reject" in interpretation

    def test_interpret_results_adf_non_stationary(self):
        """Test interpretation of ADF results for non-stationary series."""
        tester = StationarityTester()
        interpretation = tester.interpret_results(
            test_statistic=-1.0, p_value=0.75, test_type="adf"
        )

        assert isinstance(interpretation, str)
        assert "ADF" in interpretation
        assert "NON-STATIONARY" in interpretation
        assert "Fail to reject" in interpretation

    def test_interpret_results_kpss_stationary(self):
        """Test interpretation of KPSS results for stationary series."""
        tester = StationarityTester()
        interpretation = tester.interpret_results(
            test_statistic=0.2, p_value=0.10, test_type="kpss"
        )

        assert isinstance(interpretation, str)
        assert "KPSS" in interpretation
        assert "STATIONARY" in interpretation
        assert "Fail to reject" in interpretation

    def test_interpret_results_kpss_non_stationary(self):
        """Test interpretation of KPSS results for non-stationary series."""
        tester = StationarityTester()
        interpretation = tester.interpret_results(
            test_statistic=2.0, p_value=0.01, test_type="kpss"
        )

        assert isinstance(interpretation, str)
        assert "KPSS" in interpretation
        assert "NON-STATIONARY" in interpretation
        assert "Reject" in interpretation

    def test_interpret_results_invalid_test_type(self):
        """Test interpretation with invalid test type."""
        tester = StationarityTester()

        with pytest.raises(ValueError, match="must be either 'adf' or 'kpss'"):
            tester.interpret_results(
                test_statistic=-5.0, p_value=0.001, test_type="invalid"
            )

    def test_interpret_results_custom_significance(self):
        """Test interpretation with custom significance level."""
        tester = StationarityTester()

        # p-value = 0.03 should pass at 0.05 but fail at 0.01
        interpretation_5 = tester.interpret_results(
            test_statistic=-3.0, p_value=0.03, test_type="adf", significance_level=0.05
        )

        interpretation_1 = tester.interpret_results(
            test_statistic=-3.0, p_value=0.03, test_type="adf", significance_level=0.01
        )

        assert "STATIONARY" in interpretation_5
        assert "NON-STATIONARY" in interpretation_1

    def test_comprehensive_test_stationary(self, stationary_series):
        """Test comprehensive stationarity test on stationary series."""
        tester = StationarityTester()
        results = tester.comprehensive_stationarity_test(
            stationary_series, series_name="Test Series"
        )

        # Check all required fields
        assert "adf_results" in results
        assert "kpss_results" in results
        assert "adf_interpretation" in results
        assert "kpss_interpretation" in results
        assert "conclusion" in results
        assert "recommendation" in results

        # Check that both tests agree on stationarity
        assert "STATIONARY" in results["conclusion"]
        assert "Test Series" in results["conclusion"]

    def test_comprehensive_test_non_stationary(self, non_stationary_series):
        """Test comprehensive stationarity test on non-stationary series."""
        tester = StationarityTester()
        results = tester.comprehensive_stationarity_test(
            non_stationary_series, series_name="Random Walk"
        )

        # Check that both tests agree on non-stationarity
        assert "NON-STATIONARY" in results["conclusion"]
        assert "Random Walk" in results["conclusion"]
        assert "differencing" in results["recommendation"].lower()

    def test_comprehensive_test_custom_name(self, stationary_series):
        """Test comprehensive test with custom series name."""
        tester = StationarityTester()
        results = tester.comprehensive_stationarity_test(
            stationary_series, series_name="Custom Name"
        )

        assert "Custom Name" in results["conclusion"]

    def test_critical_values_format(self, stationary_series):
        """Test that critical values are properly formatted."""
        tester = StationarityTester()

        # ADF test
        adf_results = tester.adf_test(stationary_series)
        assert "1%" in adf_results["critical_values"]
        assert "5%" in adf_results["critical_values"]
        assert "10%" in adf_results["critical_values"]

        # KPSS test
        kpss_results = tester.kpss_test(stationary_series)
        assert "10%" in kpss_results["critical_values"]
        assert "5%" in kpss_results["critical_values"]
        assert "2.5%" in kpss_results["critical_values"]
        assert "1%" in kpss_results["critical_values"]

    def test_series_length_impact(self):
        """Test how series length impacts test results."""
        tester = StationarityTester()

        # Short series
        np.random.seed(42)
        short_series = pd.Series(np.random.randn(50))
        short_results = tester.adf_test(short_series)

        # Long series
        long_series = pd.Series(np.random.randn(1000))
        long_results = tester.adf_test(long_series)

        # Both should detect stationarity, but with different lags/observations
        assert short_results["n_obs"] < long_results["n_obs"]

    def test_differenced_series(self, non_stationary_series):
        """Test that differencing makes non-stationary series stationary."""
        tester = StationarityTester()

        # Original series should be non-stationary
        original_results = tester.adf_test(non_stationary_series)
        assert original_results["is_stationary"] is False

        # Differenced series should be stationary
        differenced_series = non_stationary_series.diff().dropna()
        differenced_results = tester.adf_test(differenced_series)
        assert differenced_results["is_stationary"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
