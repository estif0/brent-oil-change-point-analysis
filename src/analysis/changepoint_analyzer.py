"""
Change Point Analyzer

This module provides the ChangePointAnalyzer class for analyzing detected change points,
associating them with historical events, and quantifying their impact on time series.

Key Features:
    - Identify change point locations with confidence intervals
    - Quantify impact (before/after statistics)
    - Associate change points with known events
    - Generate quantitative impact statements

Example:
    >>> from src.analysis import ChangePointAnalyzer
    >>> from src.models import BayesianChangePointModel
    >>> from src.data import EventDataLoader
    >>>
    >>> # After fitting model
    >>> analyzer = ChangePointAnalyzer()
    >>> changepoints = analyzer.identify_changepoints(trace, data, confidence=0.94)
    >>> impact = analyzer.quantify_impact(trace, data)
    >>> associations = analyzer.associate_with_events(changepoints, events, window_days=30)
"""

import numpy as np
import pandas as pd
import arviz as az
from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import timedelta


class ChangePointAnalyzer:
    """
    Analyzer for extracting insights from Bayesian change point models.

    This class provides methods to:
    1. Identify change point locations with credible intervals
    2. Quantify the magnitude and direction of changes
    3. Associate detected change points with known historical events
    4. Generate human-readable impact statements

    The analyzer works with posterior samples from MCMC to provide
    robust, uncertainty-aware analysis of change points.

    Example:
        >>> analyzer = ChangePointAnalyzer()
        >>> # Identify change points
        >>> changepoints = analyzer.identify_changepoints(trace, data)
        >>> print(f"Change point at: {changepoints[0]['date']}")
        >>>
        >>> # Quantify impact
        >>> impact = analyzer.quantify_impact(trace, data)
        >>> print(f"Mean shifted from {impact['mu_before']:.4f} to {impact['mu_after']:.4f}")
    """

    def __init__(self):
        """
        Initialize the ChangePointAnalyzer.

        The analyzer is stateless and can be reused for multiple analyses.
        """
        pass

    def identify_changepoints(
        self,
        trace: az.InferenceData,
        data: pd.Series,
        confidence: float = 0.94,
        method: str = "mean",
    ) -> List[Dict[str, Any]]:
        """
        Identify change point locations from MCMC trace.

        Extracts the change point estimate with credible interval from
        the posterior distribution. Returns detailed information including
        index, date (if available), and uncertainty bounds.

        Args:
            trace: ArViZ InferenceData from MCMC sampling
            data: Original time series data with datetime index
            confidence: Probability for credible interval (default: 0.94)
            method: Point estimate method - 'mean', 'median', or 'mode'
                   (default: 'mean')

        Returns:
            List of dictionaries, each containing:
                - 'index': Integer index of change point
                - 'date': Datetime of change point (if data has datetime index)
                - 'estimate_method': Method used for point estimate
                - 'credible_interval': Tuple of (lower, upper) bounds
                - 'ci_probability': Confidence level used
                - 'posterior_std': Posterior standard deviation

        Raises:
            ValueError: If method is not recognized or trace invalid

        Example:
            >>> changepoints = analyzer.identify_changepoints(
            ...     trace, data, confidence=0.94, method='mean'
            ... )
            >>> cp = changepoints[0]
            >>> print(f"Change at {cp['date']} (index {cp['index']})")
            >>> print(f"94% CI: [{cp['credible_interval'][0]}, {cp['credible_interval'][1]}]")
        """
        if not hasattr(trace, "posterior"):
            raise ValueError("trace must contain posterior samples")

        if "tau" not in trace.posterior:
            raise ValueError("trace must contain 'tau' variable (change point)")

        # Extract tau samples
        tau_samples = trace.posterior["tau"].values.flatten()

        # Calculate point estimate
        if method == "mean":
            tau_estimate = int(np.round(np.mean(tau_samples)))
        elif method == "median":
            tau_estimate = int(np.round(np.median(tau_samples)))
        elif method == "mode":
            tau_estimate = int(np.bincount(tau_samples.astype(int)).argmax())
        else:
            raise ValueError(
                f"method must be 'mean', 'median', or 'mode', got '{method}'"
            )

        # Calculate credible interval using HDI
        hdi_data = az.hdi(trace, hdi_prob=confidence, var_names=["tau"])
        ci_lower = int(np.floor(hdi_data["tau"].values[0]))
        ci_upper = int(np.ceil(hdi_data["tau"].values[1]))

        # Calculate posterior standard deviation
        tau_std = np.std(tau_samples)

        # Build result dictionary
        changepoint = {
            "index": tau_estimate,
            "estimate_method": method,
            "credible_interval": (ci_lower, ci_upper),
            "ci_probability": confidence,
            "posterior_std": float(tau_std),
            "posterior_samples": len(tau_samples),
        }

        # Add date if data has datetime index
        if isinstance(data.index, pd.DatetimeIndex):
            changepoint["date"] = data.index[tau_estimate]
            changepoint["ci_dates"] = (data.index[ci_lower], data.index[ci_upper])

        return [changepoint]  # Return list for consistency (future multi-changepoint)

    def quantify_impact(
        self, trace: az.InferenceData, data: pd.Series, include_volatility: bool = True
    ) -> Dict[str, Any]:
        """
        Quantify the impact of the change point on series statistics.

        Calculates before/after statistics including mean, standard deviation,
        and the magnitude/direction of change. Provides both point estimates
        and credible intervals for all quantities.

        Args:
            trace: ArViZ InferenceData from MCMC sampling
            data: Original time series data
            include_volatility: Whether to include volatility (sigma) analysis
                              (default: True)

        Returns:
            Dictionary containing:
                - 'mu_before': Mean before change point (point estimate)
                - 'mu_after': Mean after change point (point estimate)
                - 'mu_before_ci': Credible interval for before mean
                - 'mu_after_ci': Credible interval for after mean
                - 'mean_change': Absolute change in mean (after - before)
                - 'mean_change_pct': Percentage change in mean
                - 'sigma_before': Std dev before (if include_volatility=True)
                - 'sigma_after': Std dev after (if include_volatility=True)
                - 'sigma_change': Absolute change in std dev
                - 'sigma_change_pct': Percentage change in std dev
                - 'direction': 'increase', 'decrease', or 'minimal'
                - 'magnitude': Qualitative description of change size

        Example:
            >>> impact = analyzer.quantify_impact(trace, data)
            >>> print(f"Mean changed from {impact['mu_before']:.4f} to {impact['mu_after']:.4f}")
            >>> print(f"Direction: {impact['direction']}")
            >>> print(f"Magnitude: {impact['magnitude']}")
        """
        if not hasattr(trace, "posterior"):
            raise ValueError("trace must contain posterior samples")

        # Extract parameter samples
        mu_1_samples = trace.posterior["mu_1"].values.flatten()
        mu_2_samples = trace.posterior["mu_2"].values.flatten()

        # Calculate mean estimates and CIs
        mu_before = float(np.mean(mu_1_samples))
        mu_after = float(np.mean(mu_2_samples))

        mu_before_ci = az.hdi(trace, var_names=["mu_1"])["mu_1"].values
        mu_after_ci = az.hdi(trace, var_names=["mu_2"])["mu_2"].values

        # Calculate change in mean
        mean_change = mu_after - mu_before
        mean_change_pct = (
            (mean_change / abs(mu_before) * 100) if mu_before != 0 else np.inf
        )

        # Determine direction
        if abs(mean_change_pct) < 5:
            direction = "minimal"
        elif mean_change > 0:
            direction = "increase"
        else:
            direction = "decrease"

        # Determine magnitude (based on standard deviations)
        std_data = np.std(data.values)
        magnitude_in_std = abs(mean_change) / std_data if std_data > 0 else 0

        if magnitude_in_std < 0.2:
            magnitude = "negligible"
        elif magnitude_in_std < 0.5:
            magnitude = "small"
        elif magnitude_in_std < 1.0:
            magnitude = "moderate"
        elif magnitude_in_std < 2.0:
            magnitude = "large"
        else:
            magnitude = "very large"

        result = {
            "mu_before": mu_before,
            "mu_after": mu_after,
            "mu_before_ci": tuple(mu_before_ci),
            "mu_after_ci": tuple(mu_after_ci),
            "mean_change": mean_change,
            "mean_change_pct": mean_change_pct,
            "direction": direction,
            "magnitude": magnitude,
            "magnitude_in_std": magnitude_in_std,
        }

        # Add volatility analysis if requested
        if include_volatility:
            sigma_1_samples = trace.posterior["sigma_1"].values.flatten()
            sigma_2_samples = trace.posterior["sigma_2"].values.flatten()

            sigma_before = float(np.mean(sigma_1_samples))
            sigma_after = float(np.mean(sigma_2_samples))

            sigma_before_ci = az.hdi(trace, var_names=["sigma_1"])["sigma_1"].values
            sigma_after_ci = az.hdi(trace, var_names=["sigma_2"])["sigma_2"].values

            sigma_change = sigma_after - sigma_before
            sigma_change_pct = (
                (sigma_change / sigma_before * 100) if sigma_before != 0 else np.inf
            )

            volatility_direction = "increase" if sigma_change > 0 else "decrease"

            result.update(
                {
                    "sigma_before": sigma_before,
                    "sigma_after": sigma_after,
                    "sigma_before_ci": tuple(sigma_before_ci),
                    "sigma_after_ci": tuple(sigma_after_ci),
                    "sigma_change": sigma_change,
                    "sigma_change_pct": sigma_change_pct,
                    "volatility_direction": volatility_direction,
                }
            )

        return result

    def associate_with_events(
        self,
        changepoints: List[Dict[str, Any]],
        events: pd.DataFrame,
        window_days: int = 30,
        date_column: str = "date",
    ) -> List[Dict[str, Any]]:
        """
        Associate detected change points with known historical events.

        Searches for events within a time window of each change point and
        returns matches with distance metrics. This helps interpret whether
        a detected change point corresponds to a known event.

        Args:
            changepoints: List of change point dictionaries from identify_changepoints()
            events: DataFrame with historical events (must have date column)
            window_days: Search window in days (±window_days from change point)
                        (default: 30)
            date_column: Name of date column in events DataFrame
                        (default: 'date')

        Returns:
            List of dictionaries, each containing:
                - 'changepoint_date': Date of change point
                - 'changepoint_index': Index of change point
                - 'associated_events': List of matching events with distances
                - 'closest_event': The nearest event (if any found)
                - 'days_from_closest': Days between change point and closest event

        Raises:
            ValueError: If events DataFrame doesn't have required columns
            KeyError: If changepoints don't contain 'date' field

        Example:
            >>> associations = analyzer.associate_with_events(
            ...     changepoints, events, window_days=30
            ... )
            >>> for assoc in associations:
            ...     if assoc['closest_event'] is not None:
            ...         print(f"Change at {assoc['changepoint_date']} "
            ...               f"linked to {assoc['closest_event']['event_name']}")
        """
        if date_column not in events.columns:
            raise ValueError(f"events DataFrame must have '{date_column}' column")

        # Ensure date column is datetime
        if not pd.api.types.is_datetime64_any_dtype(events[date_column]):
            events = events.copy()
            events[date_column] = pd.to_datetime(events[date_column])

        associations = []

        for cp in changepoints:
            if "date" not in cp:
                raise KeyError(
                    "Changepoints must have 'date' field. "
                    "Ensure data has datetime index when calling identify_changepoints()"
                )

            cp_date = pd.to_datetime(cp["date"])

            # Define search window
            window_start = cp_date - timedelta(days=window_days)
            window_end = cp_date + timedelta(days=window_days)

            # Find events within window
            mask = (events[date_column] >= window_start) & (
                events[date_column] <= window_end
            )
            nearby_events = events[mask].copy()

            # Calculate distances
            if len(nearby_events) > 0:
                nearby_events["days_from_changepoint"] = (
                    nearby_events[date_column] - cp_date
                ).dt.days
                nearby_events["abs_days_from_changepoint"] = nearby_events[
                    "days_from_changepoint"
                ].abs()

                # Sort by proximity
                nearby_events = nearby_events.sort_values("abs_days_from_changepoint")

                # Convert to list of dicts
                associated_events = nearby_events.to_dict("records")

                # Get closest event
                closest_event = associated_events[0]
                days_from_closest = int(closest_event["days_from_changepoint"])
            else:
                associated_events = []
                closest_event = None
                days_from_closest = None

            associations.append(
                {
                    "changepoint_date": cp_date,
                    "changepoint_index": cp["index"],
                    "associated_events": associated_events,
                    "closest_event": closest_event,
                    "days_from_closest": days_from_closest,
                    "num_events_in_window": len(associated_events),
                }
            )

        return associations

    def generate_impact_statement(
        self,
        changepoint: Dict[str, Any],
        impact: Dict[str, Any],
        association: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a human-readable statement describing the change point impact.

        Creates a comprehensive, quantitative statement summarizing:
        - When the change occurred
        - What changed (mean, volatility)
        - How much it changed (magnitude, direction)
        - Potential cause (if event association provided)

        Args:
            changepoint: Change point info from identify_changepoints()
            impact: Impact quantification from quantify_impact()
            association: Optional event association from associate_with_events()

        Returns:
            Formatted string describing the change point and its impact

        Example:
            >>> changepoints = analyzer.identify_changepoints(trace, data)
            >>> impact = analyzer.quantify_impact(trace, data)
            >>> associations = analyzer.associate_with_events(changepoints, events)
            >>>
            >>> statement = analyzer.generate_impact_statement(
            ...     changepoints[0], impact, associations[0]
            ... )
            >>> print(statement)
        """
        lines = []

        # Header
        lines.append("=" * 70)
        lines.append("CHANGE POINT ANALYSIS SUMMARY")
        lines.append("=" * 70)

        # Change point location
        if "date" in changepoint:
            date_str = changepoint["date"].strftime("%Y-%m-%d")
            lines.append(f"\n📍 Change Point Detected: {date_str}")
            lines.append(f"   Index: {changepoint['index']}")

            if "ci_dates" in changepoint:
                ci_lower = changepoint["ci_dates"][0].strftime("%Y-%m-%d")
                ci_upper = changepoint["ci_dates"][1].strftime("%Y-%m-%d")
                ci_prob = int(changepoint["ci_probability"] * 100)
                lines.append(
                    f"   {ci_prob}% Credible Interval: [{ci_lower}, {ci_upper}]"
                )
        else:
            lines.append(f"\n📍 Change Point Detected at Index: {changepoint['index']}")

        # Impact on mean
        lines.append(f"\n📊 Impact on Mean:")
        lines.append(f"   Before: {impact['mu_before']:.6f}")
        lines.append(f"   After:  {impact['mu_after']:.6f}")
        lines.append(
            f"   Change: {impact['mean_change']:+.6f} ({impact['mean_change_pct']:+.2f}%)"
        )
        lines.append(f"   Direction: {impact['direction'].upper()}")
        lines.append(f"   Magnitude: {impact['magnitude'].upper()}")

        # Impact on volatility (if available)
        if "sigma_before" in impact:
            lines.append(f"\n📈 Impact on Volatility:")
            lines.append(f"   Before: {impact['sigma_before']:.6f}")
            lines.append(f"   After:  {impact['sigma_after']:.6f}")
            lines.append(
                f"   Change: {impact['sigma_change']:+.6f} ({impact['sigma_change_pct']:+.2f}%)"
            )
            lines.append(f"   Volatility: {impact['volatility_direction'].upper()}")

        # Event association (if provided)
        if association is not None:
            lines.append(f"\n🌍 Associated Events:")
            if association["closest_event"] is not None:
                event = association["closest_event"]
                lines.append(f"   Event: {event['event_name']}")
                lines.append(
                    f"   Event Date: {pd.to_datetime(event['date']).strftime('%Y-%m-%d')}"
                )
                lines.append(f"   Distance: {association['days_from_closest']} days")

                if "event_type" in event:
                    lines.append(f"   Type: {event['event_type']}")
                if "expected_impact" in event:
                    lines.append(f"   Expected Impact: {event['expected_impact']}")

                if association["num_events_in_window"] > 1:
                    lines.append(
                        f"   ({association['num_events_in_window']} events within window)"
                    )
            else:
                lines.append(f"   No events found within ±{30} day window")

        # Interpretation
        lines.append(f"\n💡 Interpretation:")

        # Interpret direction and magnitude
        if impact["direction"] == "increase":
            if impact["magnitude"] in ["large", "very large"]:
                lines.append(f"   Strong positive shift detected in the time series.")
            else:
                lines.append(f"   Moderate positive shift detected in the time series.")
        elif impact["direction"] == "decrease":
            if impact["magnitude"] in ["large", "very large"]:
                lines.append(f"   Strong negative shift detected in the time series.")
            else:
                lines.append(f"   Moderate negative shift detected in the time series.")
        else:
            lines.append(f"   Minimal change in central tendency detected.")

        # Volatility interpretation
        if "volatility_direction" in impact:
            if impact["volatility_direction"] == "increase":
                lines.append(
                    f"   Volatility increased, indicating higher market uncertainty."
                )
            else:
                lines.append(
                    f"   Volatility decreased, indicating more stable conditions."
                )

        # Event causality note
        if association and association["closest_event"]:
            days = abs(association["days_from_closest"])
            if days <= 7:
                lines.append(
                    f"   Timing closely aligns with major event (within {days} days)."
                )
            elif days <= 30:
                lines.append(
                    f"   Potential association with event ({days} days difference)."
                )

        lines.append("\n" + "=" * 70)

        return "\n".join(lines)

    def batch_analyze(
        self,
        trace: az.InferenceData,
        data: pd.Series,
        events: Optional[pd.DataFrame] = None,
        window_days: int = 30,
    ) -> Dict[str, Any]:
        """
        Perform complete analysis pipeline in one call.

        Convenience method that runs all analysis steps:
        1. Identify change points
        2. Quantify impact
        3. Associate with events (if provided)
        4. Generate impact statement

        Args:
            trace: ArViZ InferenceData from MCMC sampling
            data: Original time series data
            events: Optional DataFrame with historical events
            window_days: Search window for event association (default: 30)

        Returns:
            Dictionary containing:
                - 'changepoints': List of identified change points
                - 'impact': Impact quantification
                - 'associations': Event associations (if events provided)
                - 'statement': Human-readable impact statement

        Example:
            >>> results = analyzer.batch_analyze(trace, data, events)
            >>> print(results['statement'])
            >>> print(f"Change at {results['changepoints'][0]['date']}")
        """
        # Step 1: Identify change points
        changepoints = self.identify_changepoints(trace, data)

        # Step 2: Quantify impact
        impact = self.quantify_impact(trace, data)

        # Step 3: Associate with events (if provided)
        associations = None
        if events is not None:
            associations = self.associate_with_events(
                changepoints, events, window_days=window_days
            )

        # Step 4: Generate statement
        association_for_statement = associations[0] if associations else None
        statement = self.generate_impact_statement(
            changepoints[0], impact, association_for_statement
        )

        return {
            "changepoints": changepoints,
            "impact": impact,
            "associations": associations,
            "statement": statement,
        }
