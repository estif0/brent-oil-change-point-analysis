"""
Statistical tests module for time series analysis.

This module provides statistical tests for analyzing time series properties,
particularly stationarity testing.
"""

from typing import Dict, Tuple, Optional
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss


class StationarityTester:
    """
    A class for testing stationarity of time series data.

    This class provides methods for performing various stationarity tests
    including Augmented Dickey-Fuller (ADF) and KPSS tests, along with
    interpretation of results.

    Stationarity is a key property for many time series models. A stationary
    time series has constant mean, variance, and autocorrelation over time.

    Example:
        >>> tester = StationarityTester()
        >>> adf_results = tester.adf_test(price_series)
        >>> kpss_results = tester.kpss_test(price_series)
        >>> interpretation = tester.interpret_results(
        ...     adf_results['test_statistic'],
        ...     adf_results['p_value'],
        ...     test_type='adf'
        ... )
    """

    def __init__(self):
        """Initialize the StationarityTester."""
        pass

    def adf_test(
        self,
        series: pd.Series,
        regression: str = "c",
        autolag: str = "AIC",
        maxlag: Optional[int] = None,
    ) -> Dict:
        """
        Perform Augmented Dickey-Fuller (ADF) test for stationarity.

        The ADF test tests the null hypothesis that a unit root is present
        in the time series (i.e., the series is non-stationary).

        - Null hypothesis (H0): The series has a unit root (non-stationary)
        - Alternative hypothesis (H1): The series is stationary

        A small p-value (< 0.05) suggests rejecting the null hypothesis,
        indicating the series is stationary.

        Args:
            series (pd.Series): Time series data to test.
            regression (str): Constant and trend order to include in regression.
                            'c' : constant only (default)
                            'ct' : constant and trend
                            'ctt' : constant, linear and quadratic trend
                            'n' : no constant, no trend
            autolag (str): Method to use for automatic lag selection.
                          'AIC' : Akaike Information Criterion (default)
                          'BIC' : Bayesian Information Criterion
                          't-stat' : Based on t-statistic
            maxlag (int, optional): Maximum lag to consider.

        Returns:
            dict: Dictionary containing:
                - test_statistic: The test statistic
                - p_value: MacKinnon's approximate p-value
                - used_lag: Number of lags used
                - n_obs: Number of observations
                - critical_values: Critical values for 1%, 5%, and 10%
                - is_stationary: Boolean indicating if series is stationary (p < 0.05)

        Raises:
            ValueError: If series is empty or contains only NaN values.

        Example:
            >>> tester = StationarityTester()
            >>> results = tester.adf_test(price_series)
            >>> if results['is_stationary']:
            ...     print(f"Series is stationary (p-value: {results['p_value']:.4f})")
            ... else:
            ...     print(f"Series is non-stationary (p-value: {results['p_value']:.4f})")
        """
        # Clean the series
        clean_series = series.dropna()

        if len(clean_series) == 0:
            raise ValueError("Series is empty or contains only NaN values")

        # Perform ADF test
        adf_result = adfuller(
            clean_series, regression=regression, autolag=autolag, maxlag=maxlag
        )

        # Extract results
        test_statistic = float(adf_result[0])
        p_value = float(adf_result[1])
        used_lag = int(adf_result[2])
        n_obs = int(adf_result[3])
        critical_values = {key: float(value) for key, value in adf_result[4].items()}

        return {
            "test_statistic": test_statistic,
            "p_value": p_value,
            "used_lag": used_lag,
            "n_obs": n_obs,
            "critical_values": critical_values,
            "is_stationary": p_value < 0.05,
        }

    def kpss_test(
        self, series: pd.Series, regression: str = "c", nlags: str = "auto"
    ) -> Dict:
        """
        Perform Kwiatkowski-Phillips-Schmidt-Shin (KPSS) test for stationarity.

        The KPSS test tests the null hypothesis that the series is stationary
        around a deterministic trend.

        - Null hypothesis (H0): The series is stationary
        - Alternative hypothesis (H1): The series has a unit root (non-stationary)

        Note: This is opposite to the ADF test!

        A small p-value (< 0.05) suggests rejecting the null hypothesis,
        indicating the series is non-stationary.

        Args:
            series (pd.Series): Time series data to test.
            regression (str): Trend component specification.
                            'c' : constant only (default)
                            'ct' : constant and trend
            nlags (str or int): Lags to use. If 'auto', uses int(12*(n/100)^(1/4))

        Returns:
            dict: Dictionary containing:
                - test_statistic: The test statistic
                - p_value: MacKinnon's approximate p-value
                - used_lag: Number of lags used
                - critical_values: Critical values for 10%, 5%, 2.5%, and 1%
                - is_stationary: Boolean indicating if series is stationary (p > 0.05)

        Raises:
            ValueError: If series is empty or contains only NaN values.

        Example:
            >>> tester = StationarityTester()
            >>> results = tester.kpss_test(price_series)
            >>> if results['is_stationary']:
            ...     print(f"Series is stationary (p-value: {results['p_value']:.4f})")
            ... else:
            ...     print(f"Series is non-stationary (p-value: {results['p_value']:.4f})")
        """
        # Clean the series
        clean_series = series.dropna()

        if len(clean_series) == 0:
            raise ValueError("Series is empty or contains only NaN values")

        # Perform KPSS test
        kpss_result = kpss(clean_series, regression=regression, nlags=nlags)

        # Extract results
        test_statistic = float(kpss_result[0])
        p_value = float(kpss_result[1])
        used_lag = int(kpss_result[2])
        critical_values = {key: float(value) for key, value in kpss_result[3].items()}

        return {
            "test_statistic": test_statistic,
            "p_value": p_value,
            "used_lag": used_lag,
            "critical_values": critical_values,
            "is_stationary": p_value > 0.05,  # Note: opposite to ADF
        }

    def interpret_results(
        self,
        test_statistic: float,
        p_value: float,
        test_type: str = "adf",
        significance_level: float = 0.05,
    ) -> str:
        """
        Provide human-readable interpretation of stationarity test results.

        Args:
            test_statistic (float): The test statistic value.
            p_value (float): The p-value from the test.
            test_type (str): Type of test ('adf' or 'kpss'). Default is 'adf'.
            significance_level (float): Significance level for hypothesis test.
                                       Default is 0.05 (5%).

        Returns:
            str: Human-readable interpretation of the test results.

        Raises:
            ValueError: If test_type is not 'adf' or 'kpss'.

        Example:
            >>> tester = StationarityTester()
            >>> adf_results = tester.adf_test(series)
            >>> interpretation = tester.interpret_results(
            ...     adf_results['test_statistic'],
            ...     adf_results['p_value'],
            ...     test_type='adf'
            ... )
            >>> print(interpretation)
        """
        test_type = test_type.lower()

        if test_type not in ["adf", "kpss"]:
            raise ValueError("test_type must be either 'adf' or 'kpss'")

        interpretation = []

        # Add test information
        if test_type == "adf":
            interpretation.append("Augmented Dickey-Fuller (ADF) Test Results:")
            interpretation.append("=" * 50)
            interpretation.append(f"Test Statistic: {test_statistic:.6f}")
            interpretation.append(f"P-value: {p_value:.6f}")
            interpretation.append("")
            interpretation.append(
                "Null Hypothesis (H0): Series has a unit root (non-stationary)"
            )
            interpretation.append("Alternative Hypothesis (H1): Series is stationary")
            interpretation.append("")

            if p_value < significance_level:
                interpretation.append(
                    f"✓ CONCLUSION: Reject null hypothesis at {significance_level*100}% significance level"
                )
                interpretation.append("  → The series appears to be STATIONARY")
                interpretation.append(
                    f"  → Evidence: p-value ({p_value:.6f}) < {significance_level}"
                )
            else:
                interpretation.append(
                    f"✗ CONCLUSION: Fail to reject null hypothesis at {significance_level*100}% significance level"
                )
                interpretation.append("  → The series appears to be NON-STATIONARY")
                interpretation.append(
                    f"  → Evidence: p-value ({p_value:.6f}) >= {significance_level}"
                )
                interpretation.append("")
                interpretation.append(
                    "  Recommendation: Consider differencing or transformation"
                )

        else:  # kpss
            interpretation.append(
                "Kwiatkowski-Phillips-Schmidt-Shin (KPSS) Test Results:"
            )
            interpretation.append("=" * 50)
            interpretation.append(f"Test Statistic: {test_statistic:.6f}")
            interpretation.append(f"P-value: {p_value:.6f}")
            interpretation.append("")
            interpretation.append("Null Hypothesis (H0): Series is stationary")
            interpretation.append(
                "Alternative Hypothesis (H1): Series has a unit root (non-stationary)"
            )
            interpretation.append("")

            if p_value < significance_level:
                interpretation.append(
                    f"✗ CONCLUSION: Reject null hypothesis at {significance_level*100}% significance level"
                )
                interpretation.append("  → The series appears to be NON-STATIONARY")
                interpretation.append(
                    f"  → Evidence: p-value ({p_value:.6f}) < {significance_level}"
                )
                interpretation.append("")
                interpretation.append(
                    "  Recommendation: Consider differencing or transformation"
                )
            else:
                interpretation.append(
                    f"✓ CONCLUSION: Fail to reject null hypothesis at {significance_level*100}% significance level"
                )
                interpretation.append("  → The series appears to be STATIONARY")
                interpretation.append(
                    f"  → Evidence: p-value ({p_value:.6f}) >= {significance_level}"
                )

        return "\n".join(interpretation)

    def comprehensive_stationarity_test(
        self, series: pd.Series, series_name: str = "Series"
    ) -> Dict:
        """
        Perform both ADF and KPSS tests and provide comprehensive analysis.

        This method runs both tests and helps identify the stationarity
        of the series by comparing results from both tests.

        Args:
            series (pd.Series): Time series data to test.
            series_name (str): Name of the series for reporting. Default is "Series".

        Returns:
            dict: Dictionary containing:
                - adf_results: Results from ADF test
                - kpss_results: Results from KPSS test
                - conclusion: Overall conclusion about stationarity
                - recommendation: Recommendations for data transformation

        Example:
            >>> tester = StationarityTester()
            >>> results = tester.comprehensive_stationarity_test(
            ...     price_series,
            ...     series_name="Brent Oil Prices"
            ... )
            >>> print(results['conclusion'])
        """
        # Perform both tests
        adf_results = self.adf_test(series)
        kpss_results = self.kpss_test(series)

        # Determine conclusion based on both tests
        adf_stationary = adf_results["is_stationary"]
        kpss_stationary = kpss_results["is_stationary"]

        if adf_stationary and kpss_stationary:
            conclusion = f"{series_name} is STATIONARY (both ADF and KPSS agree)"
            recommendation = (
                "No transformation needed. Series is suitable for modeling."
            )
        elif not adf_stationary and not kpss_stationary:
            conclusion = f"{series_name} is NON-STATIONARY (both ADF and KPSS agree)"
            recommendation = "Apply differencing or other transformations (e.g., log returns) to achieve stationarity."
        elif adf_stationary and not kpss_stationary:
            conclusion = f"{series_name} has MIXED results (ADF: stationary, KPSS: non-stationary)"
            recommendation = "Series may be trend-stationary. Consider detrending or use caution in interpretation."
        else:  # not adf_stationary and kpss_stationary
            conclusion = f"{series_name} has MIXED results (ADF: non-stationary, KPSS: stationary)"
            recommendation = (
                "Unusual case. Review data quality and consider additional tests."
            )

        return {
            "adf_results": adf_results,
            "kpss_results": kpss_results,
            "adf_interpretation": self.interpret_results(
                adf_results["test_statistic"], adf_results["p_value"], test_type="adf"
            ),
            "kpss_interpretation": self.interpret_results(
                kpss_results["test_statistic"],
                kpss_results["p_value"],
                test_type="kpss",
            ),
            "conclusion": conclusion,
            "recommendation": recommendation,
        }
