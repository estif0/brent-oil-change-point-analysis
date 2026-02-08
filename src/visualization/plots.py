"""
Plotting Functions for Change Point Analysis

This module provides visualization functions for Bayesian change point detection results.
All functions return matplotlib Figure objects for flexibility.

Functions:
    - plot_price_with_changepoints: Overlay change points and events on price series
    - plot_changepoint_distribution: Posterior distribution of τ
    - plot_parameter_comparison: Before/after parameter distributions
    - plot_event_impact: Price behavior around event dates
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import arviz as az
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import timedelta
import seaborn as sns


def plot_price_with_changepoints(
    data: pd.Series,
    changepoints: Optional[List[Dict[str, Any]]] = None,
    events: Optional[pd.DataFrame] = None,
    figsize: Tuple[int, int] = (14, 6),
    title: Optional[str] = None,
    show_ci: bool = True,
    event_window: int = 30,
) -> plt.Figure:
    """
    Plot time series with detected change points and historical events.

    Creates a comprehensive visualization showing:
    - Original price/returns time series
    - Detected change points with credible intervals
    - Historical events (if provided)
    - Visual indicators for regime changes

    Args:
        data: Time series data with datetime index
        changepoints: List of change point dictionaries from ChangePointAnalyzer
        events: Optional DataFrame with historical events
        figsize: Figure size (width, height) in inches
        title: Optional custom title
        show_ci: Whether to show credible intervals for change points
        event_window: Window for highlighting events near change points (days)

    Returns:
        matplotlib.figure.Figure object

    Example:
        >>> from src.visualization import plot_price_with_changepoints
        >>> fig = plot_price_with_changepoints(
        ...     data=log_returns,
        ...     changepoints=changepoints,
        ...     events=events
        ... )
        >>> fig.savefig('changepoints.png', dpi=300, bbox_inches='tight')
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Plot the main time series
    ax.plot(data.index, data.values, "k-", alpha=0.6, linewidth=1, label="Time Series")

    # Add change points if provided
    if changepoints is not None:
        for i, cp in enumerate(changepoints):
            # Main change point line
            cp_date = cp["date"]
            ax.axvline(
                cp_date,
                color="red",
                linestyle="--",
                linewidth=2,
                label="Change Point" if i == 0 else "",
                zorder=5,
            )

            # Add credible interval if requested and available
            if show_ci and "ci_dates" in cp:
                ci_lower, ci_upper = cp["ci_dates"]
                ax.axvspan(
                    ci_lower,
                    ci_upper,
                    alpha=0.2,
                    color="red",
                    label=f"{int(cp['ci_probability']*100)}% CI" if i == 0 else "",
                )

            # Add annotation for change point
            y_pos = data.max() * 0.9
            ax.annotate(
                f"CP {i+1}",
                xy=(cp_date, y_pos),
                xytext=(10, 10),
                textcoords="offset points",
                fontsize=10,
                bbox=dict(boxstyle="round,pad=0.5", facecolor="red", alpha=0.7),
                arrowprops=dict(arrowstyle="->", color="red", lw=1.5),
            )

    # Add events if provided
    if events is not None and not events.empty:
        # Ensure date column is datetime
        if "date" in events.columns:
            events = events.copy()
            events["date"] = pd.to_datetime(events["date"])

            # Filter events within data range
            events = events[
                (events["date"] >= data.index.min())
                & (events["date"] <= data.index.max())
            ]

            # Color map for event types
            event_colors = {
                "Political": "blue",
                "Economic": "green",
                "Policy": "purple",
                "War": "darkred",
                "Crisis": "orange",
            }

            for idx, event in events.iterrows():
                event_date = event["date"]
                event_type = event.get("event_type", "Other")
                color = event_colors.get(event_type, "gray")

                # Check if event is near a change point
                near_cp = False
                if changepoints is not None:
                    for cp in changepoints:
                        days_diff = abs((event_date - cp["date"]).days)
                        if days_diff <= event_window:
                            near_cp = True
                            break

                # Use different marker for events near change points
                marker = "o" if near_cp else "^"
                markersize = 10 if near_cp else 6

                ax.axvline(
                    event_date, color=color, linestyle=":", alpha=0.4, linewidth=1
                )
                ax.scatter(
                    event_date,
                    data.min() * 0.9,
                    marker=marker,
                    s=markersize**2,
                    color=color,
                    zorder=4,
                    edgecolors="black",
                    linewidth=0.5,
                )

            # Add legend for event types
            legend_elements = [
                plt.Line2D(
                    [0],
                    [0],
                    marker="^",
                    color="w",
                    markerfacecolor=color,
                    markersize=8,
                    label=event_type,
                    markeredgecolor="black",
                    markeredgewidth=0.5,
                )
                for event_type, color in event_colors.items()
                if event_type in events["event_type"].values
            ]

            # Add change point legend elements
            if changepoints is not None:
                legend_elements.insert(
                    0,
                    plt.Line2D(
                        [0],
                        [0],
                        color="red",
                        linestyle="--",
                        linewidth=2,
                        label="Change Point",
                    ),
                )

    # Formatting
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)

    if title:
        ax.set_title(title, fontsize=14, fontweight="bold")
    else:
        ax.set_title(
            "Time Series with Change Points and Events", fontsize=14, fontweight="bold"
        )

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    ax.xaxis.set_major_locator(mdates.YearLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="best", fontsize=9)

    plt.tight_layout()
    return fig


def plot_changepoint_distribution(
    trace: az.InferenceData,
    data: pd.Series,
    bins: int = 50,
    figsize: Tuple[int, int] = (10, 6),
    show_map: bool = True,
    show_mean: bool = True,
    show_hdi: bool = True,
    hdi_prob: float = 0.94,
) -> plt.Figure:
    """
    Plot posterior distribution of the change point (τ).

    Visualizes the uncertainty in change point location with:
    - Histogram of posterior samples
    - Point estimates (MAP, mean)
    - Credible interval (HDI)

    Args:
        trace: ArViZ InferenceData with posterior samples
        data: Original time series (for x-axis labeling)
        bins: Number of histogram bins
        figsize: Figure size (width, height) in inches
        show_map: Show maximum a posteriori (mode) estimate
        show_mean: Show mean estimate
        show_hdi: Show highest density interval
        hdi_prob: Probability for HDI (default: 0.94)

    Returns:
        matplotlib.figure.Figure object

    Example:
        >>> fig = plot_changepoint_distribution(trace, data)
        >>> fig.savefig('tau_posterior.png', dpi=300, bbox_inches='tight')
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Extract tau samples
    tau_samples = trace.posterior["tau"].values.flatten()

    # Create histogram
    counts, bin_edges, patches = ax.hist(
        tau_samples,
        bins=bins,
        density=True,
        alpha=0.7,
        color="skyblue",
        edgecolor="black",
        linewidth=0.5,
    )

    # Calculate point estimates
    tau_mean = np.mean(tau_samples)
    tau_mode = np.bincount(tau_samples.astype(int)).argmax()

    # Show MAP (mode)
    if show_map:
        ax.axvline(
            tau_mode,
            color="red",
            linestyle="--",
            linewidth=2,
            label=f"Mode (MAP): {int(tau_mode)}",
        )

    # Show mean
    if show_mean:
        ax.axvline(
            tau_mean,
            color="green",
            linestyle="--",
            linewidth=2,
            label=f"Mean: {tau_mean:.1f}",
        )

    # Show HDI
    if show_hdi:
        hdi = az.hdi(trace, hdi_prob=hdi_prob, var_names=["tau"])
        hdi_lower = int(np.floor(hdi["tau"].values[0]))
        hdi_upper = int(np.ceil(hdi["tau"].values[1]))

        ax.axvspan(
            hdi_lower,
            hdi_upper,
            alpha=0.2,
            color="red",
            label=f"{int(hdi_prob*100)}% HDI: [{hdi_lower}, {hdi_upper}]",
        )

    # Convert x-axis to dates if data has datetime index
    if isinstance(data.index, pd.DatetimeIndex) and len(data) > max(tau_samples):
        # Create custom tick locations and labels
        n_ticks = 6
        tick_indices = np.linspace(
            tau_samples.min(), tau_samples.max(), n_ticks, dtype=int
        )
        tick_dates = [data.index[int(idx)].strftime("%Y-%m-%d") for idx in tick_indices]

        ax2 = ax.twiny()
        ax2.set_xlim(ax.get_xlim())
        ax2.set_xticks(tick_indices)
        ax2.set_xticklabels(tick_dates, rotation=45, ha="left")
        ax2.set_xlabel("Date", fontsize=11)

    # Formatting
    ax.set_xlabel("Index (τ)", fontsize=12)
    ax.set_ylabel("Probability Density", fontsize=12)
    ax.set_title(
        "Posterior Distribution of Change Point (τ)", fontsize=14, fontweight="bold"
    )
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3, linestyle="--", axis="y")

    plt.tight_layout()
    return fig


def plot_parameter_comparison(
    trace: az.InferenceData,
    figsize: Tuple[int, int] = (12, 8),
    hdi_prob: float = 0.94,
    include_sigma: bool = True,
) -> plt.Figure:
    """
    Compare before and after parameter distributions.

    Creates violin/box plots showing:
    - μ₁ vs μ₂ (mean before vs after)
    - σ₁ vs σ₂ (volatility before vs after)
    - Credible intervals

    Args:
        trace: ArViZ InferenceData with posterior samples
        figsize: Figure size (width, height) in inches
        hdi_prob: Probability for credible intervals
        include_sigma: Whether to include volatility parameters

    Returns:
        matplotlib.figure.Figure object

    Example:
        >>> fig = plot_parameter_comparison(trace)
        >>> fig.savefig('parameter_comparison.png', dpi=300, bbox_inches='tight')
    """
    # Extract samples
    mu_1 = trace.posterior["mu_1"].values.flatten()
    mu_2 = trace.posterior["mu_2"].values.flatten()

    if include_sigma:
        sigma_1 = trace.posterior["sigma_1"].values.flatten()
        sigma_2 = trace.posterior["sigma_2"].values.flatten()
        n_rows = 2
    else:
        n_rows = 1

    fig, axes = plt.subplots(n_rows, 2, figsize=figsize)
    if n_rows == 1:
        axes = axes.reshape(1, -1)

    # Plot μ parameters
    # Left: Violin plots
    ax = axes[0, 0]
    parts = ax.violinplot(
        [mu_1, mu_2], positions=[1, 2], showmeans=True, showmedians=True, widths=0.6
    )

    # Color the violins
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(["steelblue", "coral"][i])
        pc.set_alpha(0.6)

    ax.set_xticks([1, 2])
    ax.set_xticklabels(["μ₁ (Before)", "μ₂ (After)"])
    ax.set_ylabel("Value", fontsize=11)
    ax.set_title("Mean Parameters Distribution", fontsize=12, fontweight="bold")
    ax.grid(True, alpha=0.3, axis="y")

    # Right: Posterior distributions with HDI
    ax = axes[0, 1]

    # Plot KDE for both parameters
    from scipy.stats import gaussian_kde

    kde_mu1 = gaussian_kde(mu_1)
    kde_mu2 = gaussian_kde(mu_2)

    x_min = min(mu_1.min(), mu_2.min())
    x_max = max(mu_1.max(), mu_2.max())
    x_range = np.linspace(x_min, x_max, 200)

    ax.plot(
        x_range, kde_mu1(x_range), label="μ₁ (Before)", color="steelblue", linewidth=2
    )
    ax.plot(x_range, kde_mu2(x_range), label="μ₂ (After)", color="coral", linewidth=2)

    # Add HDI regions
    hdi_mu1 = az.hdi(trace, hdi_prob=hdi_prob, var_names=["mu_1"])["mu_1"].values
    hdi_mu2 = az.hdi(trace, hdi_prob=hdi_prob, var_names=["mu_2"])["mu_2"].values

    ax.axvspan(hdi_mu1[0], hdi_mu1[1], alpha=0.2, color="steelblue")
    ax.axvspan(hdi_mu2[0], hdi_mu2[1], alpha=0.2, color="coral")

    ax.set_xlabel("Value", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.set_title(
        f"Mean Parameters with {int(hdi_prob*100)}% HDI", fontsize=12, fontweight="bold"
    )
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)

    # Plot σ parameters if requested
    if include_sigma:
        # Left: Violin plots
        ax = axes[1, 0]
        parts = ax.violinplot(
            [sigma_1, sigma_2],
            positions=[1, 2],
            showmeans=True,
            showmedians=True,
            widths=0.6,
        )

        for i, pc in enumerate(parts["bodies"]):
            pc.set_facecolor(["steelblue", "coral"][i])
            pc.set_alpha(0.6)

        ax.set_xticks([1, 2])
        ax.set_xticklabels(["σ₁ (Before)", "σ₂ (After)"])
        ax.set_ylabel("Value", fontsize=11)
        ax.set_title(
            "Volatility Parameters Distribution", fontsize=12, fontweight="bold"
        )
        ax.grid(True, alpha=0.3, axis="y")

        # Right: Posterior distributions with HDI
        ax = axes[1, 1]

        kde_sigma1 = gaussian_kde(sigma_1)
        kde_sigma2 = gaussian_kde(sigma_2)

        x_min = min(sigma_1.min(), sigma_2.min())
        x_max = max(sigma_1.max(), sigma_2.max())
        x_range = np.linspace(x_min, x_max, 200)

        ax.plot(
            x_range,
            kde_sigma1(x_range),
            label="σ₁ (Before)",
            color="steelblue",
            linewidth=2,
        )
        ax.plot(
            x_range, kde_sigma2(x_range), label="σ₂ (After)", color="coral", linewidth=2
        )

        # Add HDI regions
        hdi_sigma1 = az.hdi(trace, hdi_prob=hdi_prob, var_names=["sigma_1"])[
            "sigma_1"
        ].values
        hdi_sigma2 = az.hdi(trace, hdi_prob=hdi_prob, var_names=["sigma_2"])[
            "sigma_2"
        ].values

        ax.axvspan(hdi_sigma1[0], hdi_sigma1[1], alpha=0.2, color="steelblue")
        ax.axvspan(hdi_sigma2[0], hdi_sigma2[1], alpha=0.2, color="coral")

        ax.set_xlabel("Value", fontsize=11)
        ax.set_ylabel("Density", fontsize=11)
        ax.set_title(
            f"Volatility Parameters with {int(hdi_prob*100)}% HDI",
            fontsize=12,
            fontweight="bold",
        )
        ax.legend(loc="best", fontsize=10)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_event_impact(
    data: pd.Series,
    event_date: pd.Timestamp,
    window_days: int = 60,
    figsize: Tuple[int, int] = (12, 6),
    event_name: Optional[str] = None,
    show_stats: bool = True,
) -> plt.Figure:
    """
    Plot price behavior around a specific event.

    Creates visualization showing:
    - Time series before and after event
    - Event marker
    - Statistical comparison (mean, volatility)
    - Percentage changes

    Args:
        data: Time series data with datetime index
        event_date: Date of the event
        window_days: Days to show before and after event
        figsize: Figure size (width, height) in inches
        event_name: Optional name of the event for title
        show_stats: Whether to display before/after statistics

    Returns:
        matplotlib.figure.Figure object

    Example:
        >>> event_date = pd.Timestamp('2008-09-15')  # Lehman Brothers
        >>> fig = plot_event_impact(
        ...     data=log_returns,
        ...     event_date=event_date,
        ...     window_days=90,
        ...     event_name='Lehman Brothers Collapse'
        ... )
        >>> fig.savefig('event_impact.png', dpi=300, bbox_inches='tight')
    """
    fig, ax = plt.subplots(figsize=figsize)

    # Convert event_date to pandas Timestamp if needed
    event_date = pd.to_datetime(event_date)

    # Define window
    start_date = event_date - timedelta(days=window_days)
    end_date = event_date + timedelta(days=window_days)

    # Filter data
    mask = (data.index >= start_date) & (data.index <= end_date)
    windowed_data = data[mask]

    if len(windowed_data) == 0:
        raise ValueError(f"No data found between {start_date} and {end_date}")

    # Split before and after
    before_mask = windowed_data.index < event_date
    after_mask = windowed_data.index >= event_date

    before_data = windowed_data[before_mask]
    after_data = windowed_data[after_mask]

    # Plot before and after with different colors
    ax.plot(
        before_data.index,
        before_data.values,
        "b-",
        alpha=0.7,
        linewidth=1.5,
        label="Before Event",
    )
    ax.plot(
        after_data.index,
        after_data.values,
        "r-",
        alpha=0.7,
        linewidth=1.5,
        label="After Event",
    )

    # Add event line
    ax.axvline(
        event_date,
        color="darkred",
        linestyle="--",
        linewidth=2.5,
        label="Event",
        zorder=5,
    )

    # Add shaded regions for before/after
    ax.axvspan(start_date, event_date, alpha=0.1, color="blue")
    ax.axvspan(event_date, end_date, alpha=0.1, color="red")

    # Calculate and display statistics if requested
    if show_stats and len(before_data) > 0 and len(after_data) > 0:
        mean_before = before_data.mean()
        mean_after = after_data.mean()
        std_before = before_data.std()
        std_after = after_data.std()

        # Add horizontal lines for means
        ax.axhline(
            mean_before,
            color="blue",
            linestyle=":",
            alpha=0.5,
            linewidth=1,
            xmin=0,
            xmax=0.45,
        )
        ax.axhline(
            mean_after,
            color="red",
            linestyle=":",
            alpha=0.5,
            linewidth=1,
            xmin=0.55,
            xmax=1,
        )

        # Create stats text box
        mean_change = mean_after - mean_before
        mean_change_pct = (
            (mean_change / abs(mean_before) * 100) if mean_before != 0 else np.inf
        )
        std_change_pct = (
            ((std_after - std_before) / std_before * 100) if std_before != 0 else np.inf
        )

        stats_text = (
            f"Before:\n"
            f"  Mean: {mean_before:.6f}\n"
            f"  Std: {std_before:.6f}\n"
            f"After:\n"
            f"  Mean: {mean_after:.6f}\n"
            f"  Std: {std_after:.6f}\n"
            f"Change:\n"
            f"  Mean: {mean_change:+.6f} ({mean_change_pct:+.1f}%)\n"
            f"  Volatility: {std_change_pct:+.1f}%"
        )

        ax.text(
            0.02,
            0.98,
            stats_text,
            transform=ax.transAxes,
            fontsize=9,
            verticalalignment="top",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8),
        )

    # Formatting
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Value", fontsize=12)

    if event_name:
        title = f'Impact of {event_name}\n({event_date.strftime("%Y-%m-%d")})'
    else:
        title = f'Event Impact Analysis\n({event_date.strftime("%Y-%m-%d")})'

    ax.set_title(title, fontsize=14, fontweight="bold")

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

    ax.grid(True, alpha=0.3, linestyle="--")
    ax.legend(loc="best", fontsize=10)

    plt.tight_layout()
    return fig
