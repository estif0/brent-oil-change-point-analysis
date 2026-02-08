"""
Tests for the visualization plotting functions.

Tests cover:
    - plot_price_with_changepoints
    - plot_changepoint_distribution
    - plot_parameter_comparison
    - plot_event_impact
    - Plot elements verification
    - Edge cases and error handling
"""

import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import arviz as az
from datetime import datetime, timedelta

from src.visualization.plots import (
    plot_price_with_changepoints,
    plot_changepoint_distribution,
    plot_parameter_comparison,
    plot_event_impact,
)


# Fixtures


@pytest.fixture
def sample_data():
    """Create sample time series data with datetime index."""
    dates = pd.date_range("2020-01-01", periods=200, freq="D")
    np.random.seed(42)
    values = np.concatenate(
        [np.random.normal(0, 1, 100), np.random.normal(2, 1.5, 100)]
    )
    return pd.Series(values, index=dates, name="value")


@pytest.fixture
def sample_changepoints(sample_data):
    """Create sample change point dictionaries."""
    changepoints = [
        {
            "index": 100,
            "date": sample_data.index[100],
            "estimate_method": "mean",
            "credible_interval": (95, 105),
            "ci_probability": 0.94,
            "posterior_std": 3.2,
            "ci_dates": (sample_data.index[95], sample_data.index[105]),
        }
    ]
    return changepoints


@pytest.fixture
def sample_events():
    """Create sample events DataFrame."""
    events = pd.DataFrame(
        {
            "date": pd.to_datetime(
                [
                    "2020-03-15",
                    "2020-04-10",
                    "2020-05-20",
                ]
            ),
            "event_name": ["Event A", "Event B", "Event C"],
            "event_type": ["Political", "Economic", "Policy"],
            "expected_impact": ["Negative", "Positive", "Neutral"],
        }
    )
    return events


@pytest.fixture
def sample_trace():
    """Create sample MCMC trace."""
    np.random.seed(42)

    n_samples = 1000
    n_chains = 2

    import xarray as xr

    # Generate samples centered around index 100
    tau_samples = np.random.normal(100, 5, (n_chains, n_samples))
    tau_samples = np.clip(tau_samples, 50, 150).astype(np.float64)

    mu_1_samples = np.random.normal(0, 0.1, (n_chains, n_samples))
    mu_2_samples = np.random.normal(2, 0.1, (n_chains, n_samples))

    sigma_1_samples = np.abs(np.random.normal(1, 0.1, (n_chains, n_samples)))
    sigma_2_samples = np.abs(np.random.normal(1.5, 0.1, (n_chains, n_samples)))

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


# Test: plot_price_with_changepoints


class TestPlotPriceWithChangepoints:
    """Test plot_price_with_changepoints function."""

    def test_returns_figure(self, sample_data):
        """Test that function returns a Figure object."""
        fig = plot_price_with_changepoints(sample_data)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_with_changepoints(self, sample_data, sample_changepoints):
        """Test plotting with change points."""
        fig = plot_price_with_changepoints(sample_data, sample_changepoints)

        assert isinstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Check that vertical lines were added (change points)
        vlines = [
            child
            for child in ax.get_children()
            if hasattr(child, "get_linestyle") and child.get_linestyle() == "--"
        ]
        assert len(vlines) > 0

        plt.close(fig)

    def test_with_events(self, sample_data, sample_events):
        """Test plotting with events."""
        fig = plot_price_with_changepoints(sample_data, events=sample_events)

        assert isinstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Should have multiple vertical lines (events)
        vlines = [
            child for child in ax.get_children() if hasattr(child, "get_linestyle")
        ]
        assert len(vlines) > 0

        plt.close(fig)

    def test_with_both_changepoints_and_events(
        self, sample_data, sample_changepoints, sample_events
    ):
        """Test plotting with both change points and events."""
        fig = plot_price_with_changepoints(
            sample_data, sample_changepoints, sample_events
        )

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_title(self, sample_data):
        """Test custom title."""
        custom_title = "My Custom Title"
        fig = plot_price_with_changepoints(sample_data, title=custom_title)

        ax = fig.axes[0]
        assert custom_title in ax.get_title()

        plt.close(fig)

    def test_without_ci(self, sample_data, sample_changepoints):
        """Test without credible intervals."""
        fig = plot_price_with_changepoints(
            sample_data, sample_changepoints, show_ci=False
        )

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_figsize(self, sample_data):
        """Test custom figure size."""
        figsize = (16, 8)
        fig = plot_price_with_changepoints(sample_data, figsize=figsize)

        # Figure size is in inches, allow small tolerance
        assert abs(fig.get_figwidth() - figsize[0]) < 0.1
        assert abs(fig.get_figheight() - figsize[1]) < 0.1

        plt.close(fig)

    def test_empty_events(self, sample_data):
        """Test with empty events DataFrame."""
        empty_events = pd.DataFrame(columns=["date", "event_name", "event_type"])
        fig = plot_price_with_changepoints(sample_data, events=empty_events)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


# Test: plot_changepoint_distribution


class TestPlotChangepointDistribution:
    """Test plot_changepoint_distribution function."""

    def test_returns_figure(self, sample_trace, sample_data):
        """Test that function returns a Figure object."""
        fig = plot_changepoint_distribution(sample_trace, sample_data)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_with_all_estimates(self, sample_trace, sample_data):
        """Test with all point estimates shown."""
        fig = plot_changepoint_distribution(
            sample_trace, sample_data, show_map=True, show_mean=True, show_hdi=True
        )

        assert isinstance(fig, plt.Figure)
        ax = fig.axes[0]

        # Should have multiple vertical lines (estimates)
        vlines = [
            child
            for child in ax.get_children()
            if hasattr(child, "get_linestyle") and child.get_linestyle() == "--"
        ]
        assert len(vlines) >= 2  # At least MAP and mean

        plt.close(fig)

    def test_without_map(self, sample_trace, sample_data):
        """Test without MAP estimate."""
        fig = plot_changepoint_distribution(sample_trace, sample_data, show_map=False)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_without_hdi(self, sample_trace, sample_data):
        """Test without HDI."""
        fig = plot_changepoint_distribution(sample_trace, sample_data, show_hdi=False)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_bins(self, sample_trace, sample_data):
        """Test with custom number of bins."""
        fig = plot_changepoint_distribution(sample_trace, sample_data, bins=30)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_hdi_prob(self, sample_trace, sample_data):
        """Test with custom HDI probability."""
        fig = plot_changepoint_distribution(sample_trace, sample_data, hdi_prob=0.90)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_figsize(self, sample_trace, sample_data):
        """Test custom figure size."""
        figsize = (12, 8)
        fig = plot_changepoint_distribution(sample_trace, sample_data, figsize=figsize)

        assert abs(fig.get_figwidth() - figsize[0]) < 0.1
        assert abs(fig.get_figheight() - figsize[1]) < 0.1

        plt.close(fig)


# Test: plot_parameter_comparison


class TestPlotParameterComparison:
    """Test plot_parameter_comparison function."""

    def test_returns_figure(self, sample_trace):
        """Test that function returns a Figure object."""
        fig = plot_parameter_comparison(sample_trace)
        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_with_sigma(self, sample_trace):
        """Test with volatility parameters."""
        fig = plot_parameter_comparison(sample_trace, include_sigma=True)

        assert isinstance(fig, plt.Figure)
        # Should have 4 subplots (2x2)
        assert len(fig.axes) == 4

        plt.close(fig)

    def test_without_sigma(self, sample_trace):
        """Test without volatility parameters."""
        fig = plot_parameter_comparison(sample_trace, include_sigma=False)

        assert isinstance(fig, plt.Figure)
        # Should have 2 subplots (1x2)
        assert len(fig.axes) == 2

        plt.close(fig)

    def test_custom_hdi_prob(self, sample_trace):
        """Test with custom HDI probability."""
        fig = plot_parameter_comparison(sample_trace, hdi_prob=0.90)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_figsize(self, sample_trace):
        """Test custom figure size."""
        figsize = (14, 10)
        fig = plot_parameter_comparison(sample_trace, figsize=figsize)

        assert abs(fig.get_figwidth() - figsize[0]) < 0.1
        assert abs(fig.get_figheight() - figsize[1]) < 0.1

        plt.close(fig)

    def test_violin_plots_created(self, sample_trace):
        """Test that violin plots are created."""
        fig = plot_parameter_comparison(sample_trace)

        # Check that violin plot elements exist
        ax = fig.axes[0]
        collections = [
            child for child in ax.get_children() if hasattr(child, "get_paths")
        ]
        assert len(collections) > 0

        plt.close(fig)


# Test: plot_event_impact


class TestPlotEventImpact:
    """Test plot_event_impact function."""

    def test_returns_figure(self, sample_data):
        """Test that function returns a Figure object."""
        event_date = sample_data.index[100]
        fig = plot_event_impact(sample_data, event_date)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_with_event_name(self, sample_data):
        """Test with event name."""
        event_date = sample_data.index[100]
        event_name = "Test Event"

        fig = plot_event_impact(sample_data, event_date, event_name=event_name)

        ax = fig.axes[0]
        assert event_name in ax.get_title()

        plt.close(fig)

    def test_with_stats(self, sample_data):
        """Test with statistics displayed."""
        event_date = sample_data.index[100]
        fig = plot_event_impact(sample_data, event_date, show_stats=True)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_without_stats(self, sample_data):
        """Test without statistics."""
        event_date = sample_data.index[100]
        fig = plot_event_impact(sample_data, event_date, show_stats=False)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_window(self, sample_data):
        """Test with custom window size."""
        event_date = sample_data.index[100]
        fig = plot_event_impact(sample_data, event_date, window_days=30)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_custom_figsize(self, sample_data):
        """Test custom figure size."""
        event_date = sample_data.index[100]
        figsize = (14, 8)

        fig = plot_event_impact(sample_data, event_date, figsize=figsize)

        assert abs(fig.get_figwidth() - figsize[0]) < 0.1
        assert abs(fig.get_figheight() - figsize[1]) < 0.1

        plt.close(fig)

    def test_event_at_start(self, sample_data):
        """Test with event at start of series."""
        event_date = sample_data.index[10]
        fig = plot_event_impact(sample_data, event_date, window_days=20)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_event_at_end(self, sample_data):
        """Test with event near end of series."""
        event_date = sample_data.index[-10]
        fig = plot_event_impact(sample_data, event_date, window_days=20)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_invalid_event_date(self, sample_data):
        """Test with event date outside data range."""
        event_date = pd.Timestamp("2019-01-01")  # Before data starts

        with pytest.raises(ValueError, match="No data found"):
            plot_event_impact(sample_data, event_date, window_days=10)

    def test_before_after_split(self, sample_data):
        """Test that data is properly split before/after event."""
        event_date = sample_data.index[100]
        fig = plot_event_impact(sample_data, event_date, window_days=50)

        ax = fig.axes[0]
        # Should have 2 main line plots (before and after)
        lines = ax.get_lines()
        assert len(lines) >= 2

        plt.close(fig)


# Integration tests


@pytest.mark.integration
class TestIntegration:
    """Integration tests with real workflow."""

    def test_full_visualization_workflow(
        self, sample_data, sample_trace, sample_changepoints, sample_events
    ):
        """Test complete visualization workflow."""
        # Plot 1: Price with change points
        fig1 = plot_price_with_changepoints(
            sample_data, sample_changepoints, sample_events
        )
        assert isinstance(fig1, plt.Figure)
        plt.close(fig1)

        # Plot 2: Change point distribution
        fig2 = plot_changepoint_distribution(sample_trace, sample_data)
        assert isinstance(fig2, plt.Figure)
        plt.close(fig2)

        # Plot 3: Parameter comparison
        fig3 = plot_parameter_comparison(sample_trace)
        assert isinstance(fig3, plt.Figure)
        plt.close(fig3)

        # Plot 4: Event impact
        event_date = sample_events.iloc[0]["date"]
        fig4 = plot_event_impact(sample_data, event_date, window_days=30)
        assert isinstance(fig4, plt.Figure)
        plt.close(fig4)

    def test_save_all_plots(
        self, tmp_path, sample_data, sample_trace, sample_changepoints, sample_events
    ):
        """Test saving all plot types to files."""
        # Plot 1
        fig1 = plot_price_with_changepoints(sample_data, sample_changepoints)
        fig1.savefig(tmp_path / "plot1.png", dpi=100, bbox_inches="tight")
        plt.close(fig1)
        assert (tmp_path / "plot1.png").exists()

        # Plot 2
        fig2 = plot_changepoint_distribution(sample_trace, sample_data)
        fig2.savefig(tmp_path / "plot2.png", dpi=100, bbox_inches="tight")
        plt.close(fig2)
        assert (tmp_path / "plot2.png").exists()

        # Plot 3
        fig3 = plot_parameter_comparison(sample_trace)
        fig3.savefig(tmp_path / "plot3.png", dpi=100, bbox_inches="tight")
        plt.close(fig3)
        assert (tmp_path / "plot3.png").exists()

        # Plot 4
        event_date = sample_data.index[100]
        fig4 = plot_event_impact(sample_data, event_date)
        fig4.savefig(tmp_path / "plot4.png", dpi=100, bbox_inches="tight")
        plt.close(fig4)
        assert (tmp_path / "plot4.png").exists()


# Cleanup


@pytest.fixture(autouse=True)
def cleanup_plots():
    """Automatically close all plots after each test."""
    yield
    plt.close("all")
