"""
Change Point Analysis Module

This module provides tools for analyzing detected change points, associating them
with events, and quantifying their impact on the time series.
"""

from .changepoint_analyzer import ChangePointAnalyzer

__all__ = ["ChangePointAnalyzer"]
