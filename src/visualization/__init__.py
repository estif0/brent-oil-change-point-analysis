"""
Visualization Module

This module provides plotting functions for Bayesian change point analysis results.

Functions:
    plot_price_with_changepoints: Overlay change points on price series
    plot_changepoint_distribution: Posterior distribution of τ (change point)
    plot_parameter_comparison: Compare before/after parameters
    plot_event_impact: Price behavior around event dates

All functions return matplotlib figures for customization and saving.
"""

from .plots import (
    plot_price_with_changepoints,
    plot_changepoint_distribution,
    plot_parameter_comparison,
    plot_event_impact,
)

__all__ = [
    "plot_price_with_changepoints",
    "plot_changepoint_distribution",
    "plot_parameter_comparison",
    "plot_event_impact",
]
