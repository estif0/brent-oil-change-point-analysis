"""
Tests for the ChangePointAnalyzer class.

Tests cover:
    - Change point identification
    - Impact quantification
    - Event association
    - Impact statement generation
    - Batch analysis
    - Edge cases and error handling
"""

import pytest
import numpy as np
import pandas as pd
import arviz as az
from datetime import datetime, timedelta
import pymc as pm

from src.analysis.changepoint_analyzer import ChangePointAnalyzer


# Fixtures


@pytest.fixture
def analyzer():
    """Create a ChangePointAnalyzer instance."""
    return ChangePointAnalyzer()


@pytest.fixture
def sample_data():
    """Create sample time series data with datetime index."""
    dates = pd.date_range("2020-01-01", periods=100, freq="D")
    np.random.seed(42)
    values = np.concatenate([np.random.normal(0, 1, 50), np.random.normal(2, 1.5, 50)])
    return pd.Series(values, index=dates, name="value")


@pytest.fixture
def sample_data_no_datetime():
    """Create sample time series without datetime index."""
    np.random.seed(42)
    values = np.concatenate([np.random.normal(0, 1, 50), np.random.normal(2, 1.5, 50)])
    return pd.Series(values, name="value")


@pytest.fixture
def sample_trace(sample_data):
    """Create a sample MCMC trace with known change point."""
    np.random.seed(42)

    # Create synthetic trace data
    n_samples = 1000
    n_chains = 2

    # Keep tau as float to avoid inhomogeneous shape issues with ArViZ
    tau_samples = np.random.normal(50, 5, (n_chains, n_samples))
    tau_samples = np.clip(tau_samples, 10, 90).astype(np.float64)

    mu_1_samples = np.random.normal(0, 0.1, (n_chains, n_samples))
    mu_2_samples = np.random.normal(2, 0.1, (n_chains, n_samples))

    sigma_1_samples = np.abs(np.random.normal(1, 0.1, (n_chains, n_samples)))
    sigma_2_samples = np.abs(np.random.normal(1.5, 0.1, (n_chains, n_samples)))

    # Create InferenceData using xarray for better control
    import xarray as xr

    posterior_data = xr.Dataset(
        {
            "tau": (["chain", "draw"], tau_samples),
            "mu_1": (["chain", "draw"], mu_1_samples),
            "mu_2": (["chain", "draw"], mu_2_samples),
            "sigma_1": (["chain", "draw"], sigma_1_samples),
            "sigma_2": (["chain", "draw"], sigma_2_samples),
        },
        coords={"chain": np.arange(n_chains), "draw": np.arange(n_samples)},
    )

    trace = az.InferenceData(posterior=posterior_data)
    return trace


@pytest.fixture
def sample_events():
    """Create sample events DataFrame."""
    events = pd.DataFrame(
        {
            "date": pd.to_datetime(
                ["2020-02-15", "2020-02-25", "2020-03-10", "2020-05-01"]
            ),
            "event_name": ["Event A", "Event B", "Event C", "Event D"],
            "event_type": ["Political", "Economic", "Political", "Policy"],
            "expected_impact": ["Negative", "Negative", "Positive", "Neutral"],
        }
    )
    return events


# Test: Initialization


class TestInitialization:
    """Test ChangePointAnalyzer initialization."""

    def test_initialization(self, analyzer):
        """Test that analyzer initializes correctly."""
        assert analyzer is not None
        assert isinstance(analyzer, ChangePointAnalyzer)


# Test: identify_changepoints


class TestIdentifyChangepoints:
    """Test change point identification."""

    def test_identify_changepoints_basic(self, analyzer, sample_trace, sample_data):
        """Test basic change point identification."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)

        assert isinstance(changepoints, list)
        assert len(changepoints) == 1

        cp = changepoints[0]
        assert "index" in cp
        assert "date" in cp
        assert "credible_interval" in cp
        assert "ci_probability" in cp
        assert "posterior_std" in cp

    def test_identify_changepoints_index_in_range(
        self, analyzer, sample_trace, sample_data
    ):
        """Test that identified change point is in valid range."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        cp = changepoints[0]

        assert 0 <= cp["index"] < len(sample_data)

        ci_lower, ci_upper = cp["credible_interval"]
        assert 0 <= ci_lower <= ci_upper < len(sample_data)

    def test_identify_changepoints_mean_method(
        self, analyzer, sample_trace, sample_data
    ):
        """Test change point identification with mean method."""
        changepoints = analyzer.identify_changepoints(
            sample_trace, sample_data, method="mean"
        )
        cp = changepoints[0]

        assert cp["estimate_method"] == "mean"
        # Change point should be near 50 (true value)
        assert 40 <= cp["index"] <= 60

    def test_identify_changepoints_median_method(
        self, analyzer, sample_trace, sample_data
    ):
        """Test change point identification with median method."""
        changepoints = analyzer.identify_changepoints(
            sample_trace, sample_data, method="median"
        )
        cp = changepoints[0]

        assert cp["estimate_method"] == "median"
        assert 40 <= cp["index"] <= 60

    def test_identify_changepoints_mode_method(
        self, analyzer, sample_trace, sample_data
    ):
        """Test change point identification with mode method."""
        changepoints = analyzer.identify_changepoints(
            sample_trace, sample_data, method="mode"
        )
        cp = changepoints[0]

        assert cp["estimate_method"] == "mode"
        assert 40 <= cp["index"] <= 60

    def test_identify_changepoints_custom_confidence(
        self, analyzer, sample_trace, sample_data
    ):
        """Test change point identification with custom confidence."""
        changepoints = analyzer.identify_changepoints(
            sample_trace, sample_data, confidence=0.90
        )
        cp = changepoints[0]

        assert cp["ci_probability"] == 0.90

    def test_identify_changepoints_without_datetime_index(
        self, analyzer, sample_trace, sample_data_no_datetime
    ):
        """Test that change point without datetime index doesn't have date."""
        changepoints = analyzer.identify_changepoints(
            sample_trace, sample_data_no_datetime
        )
        cp = changepoints[0]

        assert "index" in cp
        assert "date" not in cp

    def test_identify_changepoints_invalid_method(
        self, analyzer, sample_trace, sample_data
    ):
        """Test that invalid method raises error."""
        with pytest.raises(ValueError, match="method must be"):
            analyzer.identify_changepoints(sample_trace, sample_data, method="invalid")

    def test_identify_changepoints_missing_posterior(self, analyzer, sample_data):
        """Test error when trace doesn't have posterior."""
        invalid_trace = az.from_dict({})

        with pytest.raises(ValueError, match="must contain posterior"):
            analyzer.identify_changepoints(invalid_trace, sample_data)

    def test_identify_changepoints_missing_tau(self, analyzer, sample_data):
        """Test error when trace doesn't have tau variable."""
        import xarray as xr

        posterior_data = xr.Dataset(
            {"mu_1": (["chain", "draw"], np.random.normal(0, 1, (2, 100)))},
            coords={"chain": np.arange(2), "draw": np.arange(100)},
        )
        invalid_trace = az.InferenceData(posterior=posterior_data)

        with pytest.raises(ValueError, match="must contain 'tau'"):
            analyzer.identify_changepoints(invalid_trace, sample_data)


# Test: quantify_impact


class TestQuantifyImpact:
    """Test impact quantification."""

    def test_quantify_impact_basic(self, analyzer, sample_trace, sample_data):
        """Test basic impact quantification."""
        impact = analyzer.quantify_impact(sample_trace, sample_data)

        # Check required keys
        assert "mu_before" in impact
        assert "mu_after" in impact
        assert "mean_change" in impact
        assert "mean_change_pct" in impact
        assert "direction" in impact
        assert "magnitude" in impact

    def test_quantify_impact_with_volatility(self, analyzer, sample_trace, sample_data):
        """Test impact quantification includes volatility."""
        impact = analyzer.quantify_impact(
            sample_trace, sample_data, include_volatility=True
        )

        assert "sigma_before" in impact
        assert "sigma_after" in impact
        assert "sigma_change" in impact
        assert "sigma_change_pct" in impact
        assert "volatility_direction" in impact

    def test_quantify_impact_without_volatility(
        self, analyzer, sample_trace, sample_data
    ):
        """Test impact quantification without volatility."""
        impact = analyzer.quantify_impact(
            sample_trace, sample_data, include_volatility=False
        )

        assert "sigma_before" not in impact
        assert "sigma_after" not in impact

    def test_quantify_impact_values(self, analyzer, sample_trace, sample_data):
        """Test that impact values are reasonable."""
        impact = analyzer.quantify_impact(sample_trace, sample_data)

        # Means should be near true values (0 and 2)
        assert -0.5 < impact["mu_before"] < 0.5
        assert 1.5 < impact["mu_after"] < 2.5

        # Change should be positive (increase)
        assert impact["mean_change"] > 0
        assert impact["direction"] in ["increase", "minimal"]

    def test_quantify_impact_credible_intervals(
        self, analyzer, sample_trace, sample_data
    ):
        """Test that credible intervals are included."""
        impact = analyzer.quantify_impact(sample_trace, sample_data)

        assert "mu_before_ci" in impact
        assert "mu_after_ci" in impact

        assert len(impact["mu_before_ci"]) == 2
        assert len(impact["mu_after_ci"]) == 2

        # CI should contain mean estimate
        assert (
            impact["mu_before_ci"][0]
            <= impact["mu_before"]
            <= impact["mu_before_ci"][1]
        )
        assert (
            impact["mu_after_ci"][0] <= impact["mu_after"] <= impact["mu_after_ci"][1]
        )

    def test_quantify_impact_direction_logic(self, analyzer, sample_trace, sample_data):
        """Test direction logic is correct."""
        impact = analyzer.quantify_impact(sample_trace, sample_data)

        if impact["mean_change"] > 0 and abs(impact["mean_change_pct"]) >= 5:
            assert impact["direction"] == "increase"
        elif impact["mean_change"] < 0 and abs(impact["mean_change_pct"]) >= 5:
            assert impact["direction"] == "decrease"
        else:
            assert impact["direction"] == "minimal"

    def test_quantify_impact_magnitude_logic(self, analyzer, sample_trace, sample_data):
        """Test that magnitude is assigned correctly."""
        impact = analyzer.quantify_impact(sample_trace, sample_data)

        assert impact["magnitude"] in [
            "negligible",
            "small",
            "moderate",
            "large",
            "very large",
        ]

        # Given our synthetic data (mean shift of 2, std ~1), expect moderate/large
        assert impact["magnitude"] in ["moderate", "large", "very large"]

    def test_quantify_impact_missing_posterior(self, analyzer, sample_data):
        """Test error when trace doesn't have posterior."""
        invalid_trace = az.from_dict({})

        with pytest.raises(ValueError, match="must contain posterior"):
            analyzer.quantify_impact(invalid_trace, sample_data)


# Test: associate_with_events


class TestAssociateWithEvents:
    """Test event association."""

    def test_associate_with_events_basic(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test basic event association."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        associations = analyzer.associate_with_events(
            changepoints, sample_events, window_days=30
        )

        assert isinstance(associations, list)
        assert len(associations) == 1

        assoc = associations[0]
        assert "changepoint_date" in assoc
        assert "associated_events" in assoc
        assert "closest_event" in assoc

    def test_associate_with_events_finds_nearby(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test that nearby events are found."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        associations = analyzer.associate_with_events(
            changepoints, sample_events, window_days=30
        )

        assoc = associations[0]

        # Change point around Feb 20, should find Event A (Feb 15) and B (Feb 25)
        assert assoc["num_events_in_window"] >= 1
        assert assoc["closest_event"] is not None

    def test_associate_with_events_closest(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test that closest event is identified."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        associations = analyzer.associate_with_events(
            changepoints, sample_events, window_days=30
        )

        assoc = associations[0]

        # Should find closest event
        assert assoc["closest_event"] is not None
        assert "event_name" in assoc["closest_event"]
        assert assoc["days_from_closest"] is not None

    def test_associate_with_events_window_size(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test that window size affects results."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)

        # Small window
        assoc_small = analyzer.associate_with_events(
            changepoints, sample_events, window_days=5
        )

        # Large window
        assoc_large = analyzer.associate_with_events(
            changepoints, sample_events, window_days=60
        )

        # Larger window should find more events
        assert (
            assoc_large[0]["num_events_in_window"]
            >= assoc_small[0]["num_events_in_window"]
        )

    def test_associate_with_events_no_matches(self, analyzer):
        """Test behavior when no events in window."""
        # Create change point far from events
        changepoints = [{"index": 99, "date": pd.to_datetime("2020-12-31")}]

        events = pd.DataFrame(
            {"date": pd.to_datetime(["2020-01-01"]), "event_name": ["Far Event"]}
        )

        associations = analyzer.associate_with_events(
            changepoints, events, window_days=30
        )

        assoc = associations[0]
        assert assoc["num_events_in_window"] == 0
        assert assoc["closest_event"] is None
        assert assoc["days_from_closest"] is None

    def test_associate_with_events_missing_date_column(
        self, analyzer, sample_trace, sample_data
    ):
        """Test error when events missing date column."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)

        invalid_events = pd.DataFrame({"event_name": ["Event A"]})

        with pytest.raises(ValueError, match="must have 'date' column"):
            analyzer.associate_with_events(changepoints, invalid_events)

    def test_associate_with_events_missing_changepoint_date(
        self, analyzer, sample_events
    ):
        """Test error when changepoints missing date."""
        changepoints = [{"index": 50}]  # No date field

        with pytest.raises(KeyError, match="must have 'date' field"):
            analyzer.associate_with_events(changepoints, sample_events)

    def test_associate_with_events_string_dates(
        self, analyzer, sample_trace, sample_data
    ):
        """Test that string dates in events are converted."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)

        events = pd.DataFrame(
            {"date": ["2020-02-20", "2020-03-01"], "event_name": ["Event A", "Event B"]}
        )

        # Should not raise error (dates converted internally)
        associations = analyzer.associate_with_events(changepoints, events)
        assert len(associations) == 1


# Test: generate_impact_statement


class TestGenerateImpactStatement:
    """Test impact statement generation."""

    def test_generate_impact_statement_basic(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test basic statement generation."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        impact = analyzer.quantify_impact(sample_trace, sample_data)

        statement = analyzer.generate_impact_statement(changepoints[0], impact)

        assert isinstance(statement, str)
        assert len(statement) > 0
        assert "Change Point" in statement or "CHANGE POINT" in statement

    def test_generate_impact_statement_with_association(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test statement with event association."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        impact = analyzer.quantify_impact(sample_trace, sample_data)
        associations = analyzer.associate_with_events(
            changepoints, sample_events, window_days=30
        )

        statement = analyzer.generate_impact_statement(
            changepoints[0], impact, associations[0]
        )

        assert "Associated Events" in statement or "ASSOCIATED EVENTS" in statement

    def test_generate_impact_statement_contains_key_info(
        self, analyzer, sample_trace, sample_data
    ):
        """Test that statement contains key information."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        impact = analyzer.quantify_impact(sample_trace, sample_data)

        statement = analyzer.generate_impact_statement(changepoints[0], impact)

        # Should contain date
        date_str = changepoints[0]["date"].strftime("%Y-%m-%d")
        assert date_str in statement

        # Should contain direction
        assert impact["direction"].upper() in statement

        # Should contain magnitude
        assert impact["magnitude"].upper() in statement

    def test_generate_impact_statement_with_volatility(
        self, analyzer, sample_trace, sample_data
    ):
        """Test statement includes volatility when provided."""
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        impact = analyzer.quantify_impact(
            sample_trace, sample_data, include_volatility=True
        )

        statement = analyzer.generate_impact_statement(changepoints[0], impact)

        assert "Volatility" in statement or "volatility" in statement


# Test: batch_analyze


class TestBatchAnalyze:
    """Test batch analysis."""

    def test_batch_analyze_without_events(self, analyzer, sample_trace, sample_data):
        """Test batch analysis without events."""
        results = analyzer.batch_analyze(sample_trace, sample_data)

        assert "changepoints" in results
        assert "impact" in results
        assert "associations" in results
        assert "statement" in results

        assert results["associations"] is None

    def test_batch_analyze_with_events(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test batch analysis with events."""
        results = analyzer.batch_analyze(sample_trace, sample_data, sample_events)

        assert "changepoints" in results
        assert "impact" in results
        assert "associations" in results
        assert "statement" in results

        assert results["associations"] is not None
        assert len(results["associations"]) > 0

    def test_batch_analyze_custom_window(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test batch analysis with custom window."""
        results = analyzer.batch_analyze(
            sample_trace, sample_data, sample_events, window_days=60
        )

        assert results["associations"] is not None

    def test_batch_analyze_returns_complete_results(
        self, analyzer, sample_trace, sample_data, sample_events
    ):
        """Test that batch analysis returns complete results."""
        results = analyzer.batch_analyze(sample_trace, sample_data, sample_events)

        # Check changepoints
        assert len(results["changepoints"]) == 1
        assert "index" in results["changepoints"][0]
        assert "date" in results["changepoints"][0]

        # Check impact
        assert "mu_before" in results["impact"]
        assert "mu_after" in results["impact"]
        assert "direction" in results["impact"]

        # Check associations
        assert len(results["associations"]) == 1
        assert "closest_event" in results["associations"][0]

        # Check statement
        assert isinstance(results["statement"], str)
        assert len(results["statement"]) > 100


# Integration tests


@pytest.mark.integration
class TestIntegration:
    """Integration tests with real workflow."""

    def test_full_workflow(self, analyzer, sample_trace, sample_data, sample_events):
        """Test complete analysis workflow."""
        # Identify change points
        changepoints = analyzer.identify_changepoints(sample_trace, sample_data)
        assert len(changepoints) == 1

        # Quantify impact
        impact = analyzer.quantify_impact(sample_trace, sample_data)
        assert impact["direction"] in ["increase", "decrease", "minimal"]

        # Associate with events
        associations = analyzer.associate_with_events(
            changepoints, sample_events, window_days=30
        )
        assert len(associations) == 1

        # Generate statement
        statement = analyzer.generate_impact_statement(
            changepoints[0], impact, associations[0]
        )
        assert len(statement) > 0

        print("\n" + statement)

    def test_batch_workflow(self, analyzer, sample_trace, sample_data, sample_events):
        """Test batch analysis workflow."""
        results = analyzer.batch_analyze(sample_trace, sample_data, sample_events)

        # Verify all components
        assert results["changepoints"] is not None
        assert results["impact"] is not None
        assert results["associations"] is not None
        assert results["statement"] is not None

        print("\n" + results["statement"])
