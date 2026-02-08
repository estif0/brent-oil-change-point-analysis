"""
Tests for Model Diagnostics Module

This module tests the ModelDiagnostics class to ensure:
- Proper initialization and validation
- Convergence checking functionality
- Plotting functions work correctly
- Summary statistics are accurate
- HDI calculations are correct
"""

import pytest
import numpy as np
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt
from src.models import BayesianChangePointModel
from src.models.diagnostics import ModelDiagnostics


@pytest.fixture
def sample_trace():
    """Create a sample trace for testing."""
    np.random.seed(42)

    # Create simple synthetic data with clear change point
    data_before = np.random.normal(0, 1, 60)
    data_after = np.random.normal(3, 1, 60)
    data = pd.Series(np.concatenate([data_before, data_after]))

    # Fit model
    model = BayesianChangePointModel(data)
    model.build_model(min_segment_length=15)
    trace = model.fit(samples=500, tune=200, chains=2, random_seed=42)

    return trace


class TestModelDiagnosticsInit:
    """Test diagnostics initialization."""

    def test_init_with_valid_trace(self, sample_trace):
        """Test initialization with valid trace."""
        diagnostics = ModelDiagnostics(sample_trace)

        assert diagnostics.trace is not None
        assert len(diagnostics._var_names) > 0
        assert "tau" in diagnostics._var_names

    def test_init_with_invalid_type_raises_error(self):
        """Test that non-InferenceData raises TypeError."""
        with pytest.raises(TypeError, match="must be an ArViZ InferenceData"):
            ModelDiagnostics("not a trace")

    def test_init_extracts_variable_names(self, sample_trace):
        """Test that variable names are extracted correctly."""
        diagnostics = ModelDiagnostics(sample_trace)

        expected_vars = ["tau", "mu_1", "mu_2", "sigma_1", "sigma_2"]
        for var in expected_vars:
            assert var in diagnostics._var_names

    def test_repr(self, sample_trace):
        """Test string representation."""
        diagnostics = ModelDiagnostics(sample_trace)
        repr_str = repr(diagnostics)

        assert "ModelDiagnostics" in repr_str
        assert "variables=" in repr_str
        assert "chains=" in repr_str
        assert "draws=" in repr_str


class TestModelDiagnosticsConvergence:
    """Test convergence checking."""

    def test_check_convergence_returns_boolean(self, sample_trace):
        """Test that check_convergence returns a boolean."""
        diagnostics = ModelDiagnostics(sample_trace)
        result = diagnostics.check_convergence()

        assert isinstance(result, bool)

    def test_check_convergence_with_custom_thresholds(self, sample_trace):
        """Test convergence check with custom thresholds."""
        diagnostics = ModelDiagnostics(sample_trace)

        # More lenient thresholds
        result = diagnostics.check_convergence(
            rhat_threshold=1.1, ess_bulk_threshold=50, ess_tail_threshold=50
        )

        assert isinstance(result, bool)

    def test_check_convergence_specific_variables(self, sample_trace):
        """Test convergence check for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        result = diagnostics.check_convergence(var_names=["tau", "mu_1"])

        assert isinstance(result, bool)

    def test_get_rhat(self, sample_trace):
        """Test getting R-hat values."""
        diagnostics = ModelDiagnostics(sample_trace)
        rhat = diagnostics.get_rhat()

        assert isinstance(rhat, pd.Series)
        assert len(rhat) > 0
        assert "tau" in rhat.index
        # R-hat should be close to 1.0 for converged chains
        assert all(rhat < 1.2)  # Lenient threshold for tests

    def test_get_rhat_specific_variables(self, sample_trace):
        """Test getting R-hat for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        rhat = diagnostics.get_rhat(var_names=["tau", "mu_1"])

        assert len(rhat) == 2
        assert "tau" in rhat.index
        assert "mu_1" in rhat.index

    def test_get_effective_n(self, sample_trace):
        """Test getting effective sample sizes."""
        diagnostics = ModelDiagnostics(sample_trace)
        ess = diagnostics.get_effective_n()

        assert isinstance(ess, pd.DataFrame)
        assert "ess_bulk" in ess.columns
        assert "ess_tail" in ess.columns
        assert len(ess) > 0
        # ESS should be positive
        assert all(ess["ess_bulk"] > 0)
        assert all(ess["ess_tail"] > 0)

    def test_get_effective_n_specific_variables(self, sample_trace):
        """Test ESS for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        ess = diagnostics.get_effective_n(var_names=["tau"])

        assert len(ess) == 1
        assert "tau" in ess.index


class TestModelDiagnosticsSummary:
    """Test summary statistics."""

    def test_summary_stats_returns_dataframe(self, sample_trace):
        """Test that summary_stats returns DataFrame."""
        diagnostics = ModelDiagnostics(sample_trace)
        summary = diagnostics.summary_stats()

        assert isinstance(summary, pd.DataFrame)
        assert len(summary) > 0

    def test_summary_stats_has_required_columns(self, sample_trace):
        """Test that summary has all required columns."""
        diagnostics = ModelDiagnostics(sample_trace)
        summary = diagnostics.summary_stats()

        required_cols = [
            "mean",
            "sd",
            "hdi_3%",
            "hdi_97%",
            "ess_bulk",
            "ess_tail",
            "r_hat",
        ]
        for col in required_cols:
            assert col in summary.columns

    def test_summary_stats_with_custom_hdi(self, sample_trace):
        """Test summary with custom HDI probability."""
        diagnostics = ModelDiagnostics(sample_trace)
        summary = diagnostics.summary_stats(hdi_prob=0.90)

        # Should have 90% HDI columns
        assert "hdi_5%" in summary.columns
        assert "hdi_95%" in summary.columns

    def test_summary_stats_specific_variables(self, sample_trace):
        """Test summary for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        summary = diagnostics.summary_stats(var_names=["tau", "mu_1"])

        assert len(summary) == 2
        assert "tau" in summary.index
        assert "mu_1" in summary.index


class TestModelDiagnosticsHDI:
    """Test HDI calculations."""

    def test_get_hdi_returns_dict(self, sample_trace):
        """Test that get_hdi returns dictionary."""
        diagnostics = ModelDiagnostics(sample_trace)
        hdi = diagnostics.get_hdi("tau")

        assert isinstance(hdi, dict)
        assert "lower" in hdi
        assert "upper" in hdi
        assert "width" in hdi
        assert "probability" in hdi

    def test_get_hdi_bounds_are_ordered(self, sample_trace):
        """Test that HDI lower < upper."""
        diagnostics = ModelDiagnostics(sample_trace)
        hdi = diagnostics.get_hdi("tau")

        assert hdi["lower"] < hdi["upper"]

    def test_get_hdi_width_is_correct(self, sample_trace):
        """Test that HDI width is correctly calculated."""
        diagnostics = ModelDiagnostics(sample_trace)
        hdi = diagnostics.get_hdi("tau")

        expected_width = hdi["upper"] - hdi["lower"]
        assert np.isclose(hdi["width"], expected_width)

    def test_get_hdi_with_custom_probability(self, sample_trace):
        """Test HDI with custom probability."""
        diagnostics = ModelDiagnostics(sample_trace)

        hdi_90 = diagnostics.get_hdi("mu_1", hdi_prob=0.90)  # Use continuous variable
        hdi_94 = diagnostics.get_hdi("mu_1", hdi_prob=0.94)

        # 90% HDI should be narrower than or equal to 94% HDI
        # (equal is possible for discrete variables)
        assert hdi_90["width"] <= hdi_94["width"]
        assert hdi_90["probability"] == 0.90
        assert hdi_94["probability"] == 0.94

    def test_get_hdi_invalid_variable_raises_error(self, sample_trace):
        """Test that invalid variable name raises error."""
        diagnostics = ModelDiagnostics(sample_trace)

        with pytest.raises(ValueError, match="not found in trace"):
            diagnostics.get_hdi("nonexistent_var")


class TestModelDiagnosticsPlots:
    """Test plotting functions."""

    def test_plot_trace_returns_figure(self, sample_trace):
        """Test that plot_trace returns matplotlib Figure."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_trace()

        assert isinstance(fig, plt.Figure) or fig is not None
        plt.close("all")

    def test_plot_trace_specific_variables(self, sample_trace):
        """Test trace plot for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_trace(var_names=["tau", "mu_1"])

        assert fig is not None
        plt.close("all")

    def test_plot_trace_with_custom_figsize(self, sample_trace):
        """Test trace plot with custom figure size."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_trace(figsize=(12, 8))

        assert fig is not None
        plt.close("all")

    def test_plot_posterior_returns_figure(self, sample_trace):
        """Test that plot_posterior returns figure."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_posterior()

        assert fig is not None
        plt.close("all")

    def test_plot_posterior_specific_variables(self, sample_trace):
        """Test posterior plot for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_posterior(var_names=["tau"])

        assert fig is not None
        plt.close("all")

    def test_plot_posterior_with_custom_hdi(self, sample_trace):
        """Test posterior plot with custom HDI."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_posterior(hdi_prob=0.90)

        assert fig is not None
        plt.close("all")

    def test_plot_forest_returns_figure(self, sample_trace):
        """Test that plot_forest returns figure."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_forest()

        assert fig is not None
        plt.close("all")

    def test_plot_forest_specific_variables(self, sample_trace):
        """Test forest plot for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_forest(var_names=["mu_1", "mu_2"])

        assert fig is not None
        plt.close("all")

    def test_plot_forest_combined(self, sample_trace):
        """Test forest plot with combined chains."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_forest(combined=True)

        assert fig is not None
        plt.close("all")

    def test_plot_autocorr_returns_figure(self, sample_trace):
        """Test that plot_autocorr returns figure."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_autocorr()

        assert fig is not None
        plt.close("all")

    def test_plot_autocorr_specific_variables(self, sample_trace):
        """Test autocorr plot for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_autocorr(var_names=["tau"])

        assert fig is not None
        plt.close("all")

    def test_plot_autocorr_custom_max_lag(self, sample_trace):
        """Test autocorr plot with custom max lag."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_autocorr(max_lag=50)

        assert fig is not None
        plt.close("all")

    def test_plot_rank_returns_figure(self, sample_trace):
        """Test that plot_rank returns figure."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_rank()

        assert fig is not None
        plt.close("all")

    def test_plot_rank_specific_variables(self, sample_trace):
        """Test rank plot for specific variables."""
        diagnostics = ModelDiagnostics(sample_trace)
        fig = diagnostics.plot_rank(var_names=["tau"])

        assert fig is not None
        plt.close("all")


class TestModelDiagnosticsIntegration:
    """Integration tests for typical workflows."""

    def test_full_diagnostic_workflow(self, sample_trace):
        """Test a complete diagnostic workflow."""
        diagnostics = ModelDiagnostics(sample_trace)

        # 1. Check convergence
        converged = diagnostics.check_convergence()
        assert isinstance(converged, bool)

        # 2. Get summary
        summary = diagnostics.summary_stats()
        assert len(summary) > 0

        # 3. Get HDI for tau
        hdi = diagnostics.get_hdi("tau")
        assert "lower" in hdi

        # 4. Check R-hat
        rhat = diagnostics.get_rhat()
        assert len(rhat) > 0

        # 5. Check ESS
        ess = diagnostics.get_effective_n()
        assert len(ess) > 0

        # All steps should complete without errors
        assert True

    def test_diagnostic_plots_workflow(self, sample_trace):
        """Test creating all diagnostic plots."""
        diagnostics = ModelDiagnostics(sample_trace)

        # Create all plots
        trace_fig = diagnostics.plot_trace(var_names=["tau"])
        posterior_fig = diagnostics.plot_posterior(var_names=["mu_1", "mu_2"])
        forest_fig = diagnostics.plot_forest()

        # All should succeed
        assert trace_fig is not None
        assert posterior_fig is not None
        assert forest_fig is not None

        plt.close("all")
