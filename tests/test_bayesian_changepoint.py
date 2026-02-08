"""
Tests for Bayesian Change Point Model

This module tests the BayesianChangePointModel class to ensure:
- Proper model construction
- Correct handling of synthetic data with known change points
- Parameter estimation accuracy
- Error handling for invalid inputs
"""

import pytest
import numpy as np
import pandas as pd
import pymc as pm
from src.models.bayesian_changepoint import BayesianChangePointModel


class TestBayesianChangePointModelInit:
    """Test model initialization and validation."""

    def test_init_with_valid_series(self):
        """Test initialization with valid pandas Series."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)

        assert model.n_observations == 100
        assert model.data_values.shape == (100,)
        assert model.model is None
        assert model.trace is None

    def test_init_with_datetime_index(self):
        """Test initialization with datetime index."""
        dates = pd.date_range("2020-01-01", periods=100)
        data = pd.Series(np.random.randn(100), index=dates)
        model = BayesianChangePointModel(data)

        assert isinstance(model.data.index, pd.DatetimeIndex)
        assert model.n_observations == 100

    def test_init_calculates_statistics(self):
        """Test that initialization calculates data statistics."""
        data = pd.Series([1, 2, 3, 4, 5])
        model = BayesianChangePointModel(data)

        assert np.isclose(model.data_mean, 3.0)
        assert model.data_std > 0

    def test_init_with_empty_data_raises_error(self):
        """Test that empty data raises ValueError."""
        with pytest.raises(ValueError, match="Data cannot be empty"):
            BayesianChangePointModel(pd.Series([]))

    def test_init_with_nan_raises_error(self):
        """Test that data with NaN values raises ValueError."""
        data = pd.Series([1, 2, np.nan, 4, 5])
        with pytest.raises(ValueError, match="contains NaN values"):
            BayesianChangePointModel(data)

    def test_init_with_non_series_raises_error(self):
        """Test that non-Series data raises TypeError."""
        with pytest.raises(TypeError, match="must be a pandas Series"):
            BayesianChangePointModel([1, 2, 3, 4, 5])

    def test_repr_before_fitting(self):
        """Test string representation before fitting."""
        data = pd.Series(np.random.randn(50))
        model = BayesianChangePointModel(data)
        repr_str = repr(model)

        assert "n_observations=50" in repr_str
        assert "not fitted" in repr_str


class TestBayesianChangePointModelBuild:
    """Test model building."""

    def test_build_model_creates_pymc_model(self):
        """Test that build_model creates a PyMC model object."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)
        pymc_model = model.build_model()

        assert isinstance(pymc_model, pm.Model)
        assert model.model is not None

    def test_build_model_creates_required_variables(self):
        """Test that all required variables are created."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)
        model.build_model()

        required_vars = ["tau", "mu_1", "mu_2", "sigma_1", "sigma_2", "obs"]
        for var_name in required_vars:
            assert var_name in model.model.named_vars

    def test_build_model_with_custom_min_segment(self):
        """Test building model with custom minimum segment length."""
        data = pd.Series(np.random.randn(200))
        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=50)

        assert model.model is not None

    def test_build_model_min_segment_too_large_raises_error(self):
        """Test that too large min_segment_length raises error."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)

        with pytest.raises(ValueError, match="min_segment_length"):
            model.build_model(min_segment_length=60)

    def test_build_model_with_custom_prior_scale(self):
        """Test building model with custom prior scale."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)
        model.build_model(prior_std_scale=3.0)

        assert model.model is not None


class TestBayesianChangePointModelFit:
    """Test model fitting."""

    def test_fit_without_build_raises_error(self):
        """Test that fitting without building raises error."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)

        with pytest.raises(RuntimeError, match="must be built"):
            model.fit(samples=100)

    @pytest.mark.slow
    def test_fit_creates_trace(self):
        """Test that fitting creates a trace object."""
        # Create simple synthetic data with clear change point
        np.random.seed(42)
        data_before = np.random.normal(0, 1, 50)
        data_after = np.random.normal(5, 1, 50)
        data = pd.Series(np.concatenate([data_before, data_after]))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=10)
        trace = model.fit(samples=500, tune=200, chains=1, random_seed=42)

        assert trace is not None
        assert model.trace is not None
        assert "tau" in trace.posterior

    @pytest.mark.slow
    def test_fit_returns_inference_data(self):
        """Test that fit returns proper InferenceData object."""
        np.random.seed(42)
        data = pd.Series(np.random.randn(80))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=10)
        trace = model.fit(samples=500, tune=200, chains=1, random_seed=42)

        # Check that trace contains expected groups
        assert hasattr(trace, "posterior")
        assert hasattr(trace, "sample_stats")


class TestBayesianChangePointModelGetters:
    """Test getter methods."""

    def test_get_trace_without_fit_raises_error(self):
        """Test that get_trace without fitting raises error."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)

        with pytest.raises(RuntimeError, match="must be fitted"):
            model.get_trace()

    def test_get_summary_without_fit_raises_error(self):
        """Test that get_summary without fitting raises error."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)

        with pytest.raises(RuntimeError, match="must be fitted"):
            model.get_summary()

    def test_get_changepoint_estimate_without_fit_raises_error(self):
        """Test that get_changepoint_estimate without fitting raises error."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)

        with pytest.raises(RuntimeError, match="must be fitted"):
            model.get_changepoint_estimate()

    def test_get_parameter_estimates_without_fit_raises_error(self):
        """Test that get_parameter_estimates without fitting raises error."""
        data = pd.Series(np.random.randn(100))
        model = BayesianChangePointModel(data)

        with pytest.raises(RuntimeError, match="must be fitted"):
            model.get_parameter_estimates()


class TestBayesianChangePointModelWithSyntheticData:
    """Test model with synthetic data where true change point is known."""

    @pytest.mark.slow
    def test_detects_mean_shift(self):
        """Test that model detects a clear mean shift."""
        np.random.seed(42)

        # Create data with clear mean shift at t=60
        data_before = np.random.normal(0, 1, 60)
        data_after = np.random.normal(5, 1, 60)
        data = pd.Series(np.concatenate([data_before, data_after]))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=20)
        model.fit(samples=1000, tune=500, chains=2, random_seed=42)

        cp = model.get_changepoint_estimate(method="mean")

        # Change point should be detected around index 60
        # Allow some tolerance due to stochastic nature
        assert abs(cp["index"] - 60) < 15, f"Expected ~60, got {cp['index']}"

    @pytest.mark.slow
    def test_estimates_before_after_parameters(self):
        """Test that model correctly estimates before/after parameters."""
        np.random.seed(42)

        # Create data with known parameters
        true_mu1, true_mu2 = 0.0, 3.0
        true_sigma1, true_sigma2 = 1.0, 1.5

        data_before = np.random.normal(true_mu1, true_sigma1, 60)
        data_after = np.random.normal(true_mu2, true_sigma2, 60)
        data = pd.Series(np.concatenate([data_before, data_after]))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=20)
        model.fit(samples=1000, tune=500, chains=2, random_seed=42)

        params = model.get_parameter_estimates()

        # Check that estimates are reasonably close to true values
        # (allowing for sampling variability)
        assert abs(params["mu_1"]["mean"] - true_mu1) < 0.5
        assert abs(params["mu_2"]["mean"] - true_mu2) < 0.5

    @pytest.mark.slow
    def test_changepoint_with_datetime_index(self):
        """Test change point detection with datetime index."""
        np.random.seed(42)

        dates = pd.date_range("2020-01-01", periods=100)
        data_before = np.random.normal(0, 1, 50)
        data_after = np.random.normal(3, 1, 50)
        data = pd.Series(np.concatenate([data_before, data_after]), index=dates)

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=15)
        model.fit(samples=1000, tune=500, chains=1, random_seed=42)

        cp = model.get_changepoint_estimate()

        # Should return both index and date
        assert "index" in cp
        assert "date" in cp
        assert isinstance(cp["date"], pd.Timestamp)

    @pytest.mark.slow
    def test_summary_includes_all_parameters(self):
        """Test that summary includes all model parameters."""
        np.random.seed(42)
        data = pd.Series(np.random.randn(80))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=10)
        model.fit(samples=500, tune=200, chains=1, random_seed=42)

        summary = model.get_summary()

        required_params = ["tau", "mu_1", "mu_2", "sigma_1", "sigma_2"]
        for param in required_params:
            assert param in summary.index

        # Check that summary has expected columns
        assert "mean" in summary.columns
        assert "sd" in summary.columns
        assert "hdi_3%" in summary.columns
        assert "hdi_97%" in summary.columns

    @pytest.mark.slow
    def test_different_estimation_methods(self):
        """Test different methods for change point estimation."""
        np.random.seed(42)
        data = pd.Series(np.random.randn(80))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=10)
        model.fit(samples=500, tune=200, chains=1, random_seed=42)

        cp_mean = model.get_changepoint_estimate(method="mean")
        cp_median = model.get_changepoint_estimate(method="median")
        cp_mode = model.get_changepoint_estimate(method="mode")

        # All should return valid indices
        assert 0 <= cp_mean["index"] < 80
        assert 0 <= cp_median["index"] < 80
        assert 0 <= cp_mode["index"] < 80

        # Method should be recorded
        assert cp_mean["method"] == "mean"
        assert cp_median["method"] == "median"
        assert cp_mode["method"] == "mode"

    def test_invalid_estimation_method_raises_error(self):
        """Test that invalid estimation method raises error."""
        np.random.seed(42)
        data = pd.Series(np.random.randn(80))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=10)
        model.fit(samples=100, tune=50, chains=1, random_seed=42)

        with pytest.raises(ValueError, match="not recognized"):
            model.get_changepoint_estimate(method="invalid")


class TestBayesianChangePointModelRepr:
    """Test string representation."""

    @pytest.mark.slow
    def test_repr_after_fitting(self):
        """Test string representation after fitting."""
        np.random.seed(42)
        data = pd.Series(np.random.randn(60))

        model = BayesianChangePointModel(data)
        model.build_model(min_segment_length=10)
        model.fit(samples=500, tune=200, chains=2, random_seed=42)

        repr_str = repr(model)

        assert "n_observations=60" in repr_str
        assert "fitted with" in repr_str
        assert "samples" in repr_str
