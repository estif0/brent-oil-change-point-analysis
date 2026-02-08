"""
Model Diagnostics for Bayesian Change Point Models

This module provides diagnostic tools for assessing MCMC convergence and
posterior distributions from Bayesian change point models.

Key Features:
    - Convergence diagnostics (R-hat, ESS)
    - Trace plots for visual inspection
    - Posterior distribution plots
    - Highest Density Intervals (HDI)
    - Summary statistics

Example:
    >>> from src.models.diagnostics import ModelDiagnostics
    >>>
    >>> # After fitting a model
    >>> diagnostics = ModelDiagnostics(trace)
    >>>
    >>> # Check convergence
    >>> is_converged = diagnostics.check_convergence()
    >>> print(f"Model converged: {is_converged}")
    >>>
    >>> # Plot trace
    >>> fig = diagnostics.plot_trace(['tau', 'mu_1', 'mu_2'])
    >>> fig.savefig('trace_plot.png')
"""

import numpy as np
import pandas as pd
import arviz as az
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Dict, Any, Union, Tuple
import warnings


class ModelDiagnostics:
    """
    Diagnostic tools for Bayesian MCMC models.

    This class provides comprehensive diagnostics for assessing the quality
    of MCMC sampling results, including:
    - Convergence checks (R-hat, effective sample size)
    - Trace plots for visual inspection
    - Posterior distribution visualizations
    - Summary statistics
    - Highest Density Intervals (HDI)

    The diagnostics help ensure that:
    1. Chains have converged to the target distribution
    2. Enough independent samples were collected
    3. Posterior estimates are reliable

    Attributes:
        trace: ArViZ InferenceData object from MCMC sampling

    Example:
        >>> diagnostics = ModelDiagnostics(trace)
        >>> # Check if sampling converged
        >>> if diagnostics.check_convergence():
        >>>     print("Sampling converged successfully!")
        >>> else:
        >>>     print("WARNING: Convergence issues detected")
    """

    def __init__(self, trace: az.InferenceData):
        """
        Initialize diagnostics with MCMC trace.

        Args:
            trace: ArViZ InferenceData object containing posterior samples

        Raises:
            TypeError: If trace is not an InferenceData object
            ValueError: If trace doesn't contain posterior samples

        Example:
            >>> from src.models import BayesianChangePointModel
            >>> model = BayesianChangePointModel(data)
            >>> model.build_model()
            >>> trace = model.fit()
            >>> diagnostics = ModelDiagnostics(trace)
        """
        if not isinstance(trace, az.InferenceData):
            raise TypeError(
                "trace must be an ArViZ InferenceData object. "
                f"Got {type(trace)} instead."
            )

        if not hasattr(trace, "posterior"):
            raise ValueError(
                "trace must contain posterior samples. "
                "Ensure the model was fitted successfully."
            )

        self.trace = trace
        self._var_names = list(trace.posterior.data_vars.keys())

    def check_convergence(
        self,
        var_names: Optional[List[str]] = None,
        rhat_threshold: float = 1.01,
        ess_bulk_threshold: int = 100,
        ess_tail_threshold: int = 100,
    ) -> bool:
        """
        Check if MCMC chains have converged.

        This method checks multiple convergence diagnostics:
        1. R-hat (Gelman-Rubin statistic): Measures between-chain variance
           - Values close to 1.0 indicate convergence
           - Threshold: < 1.01 (recommended)
        2. ESS Bulk: Effective sample size for bulk of distribution
           - Should be > 100 (preferably > 400)
        3. ESS Tail: Effective sample size for distribution tails
           - Should be > 100 (preferably > 400)

        Args:
            var_names: Variables to check. If None, checks all variables.
            rhat_threshold: Maximum acceptable R-hat value (default: 1.01)
            ess_bulk_threshold: Minimum ESS bulk (default: 100)
            ess_tail_threshold: Minimum ESS tail (default: 100)

        Returns:
            True if all diagnostics pass, False otherwise

        Note:
            Prints detailed warnings for any convergence issues found.

        Example:
            >>> diagnostics = ModelDiagnostics(trace)
            >>> if not diagnostics.check_convergence():
            >>>     print("Consider running more samples or increasing tune period")
        """
        if var_names is None:
            var_names = self._var_names

        summary = az.summary(self.trace, var_names=var_names)

        converged = True
        issues = []

        # Check R-hat values
        if "r_hat" in summary.columns:
            bad_rhat = summary[summary["r_hat"] > rhat_threshold]
            if not bad_rhat.empty:
                converged = False
                for var in bad_rhat.index:
                    rhat_val = bad_rhat.loc[var, "r_hat"]
                    issues.append(
                        f"R-hat for '{var}' = {rhat_val:.4f} (threshold: {rhat_threshold})"
                    )

        # Check ESS bulk
        if "ess_bulk" in summary.columns:
            bad_ess_bulk = summary[summary["ess_bulk"] < ess_bulk_threshold]
            if not bad_ess_bulk.empty:
                converged = False
                for var in bad_ess_bulk.index:
                    ess_val = bad_ess_bulk.loc[var, "ess_bulk"]
                    issues.append(
                        f"ESS bulk for '{var}' = {ess_val:.0f} (threshold: {ess_bulk_threshold})"
                    )

        # Check ESS tail
        if "ess_tail" in summary.columns:
            bad_ess_tail = summary[summary["ess_tail"] < ess_tail_threshold]
            if not bad_ess_tail.empty:
                converged = False
                for var in bad_ess_tail.index:
                    ess_val = bad_ess_tail.loc[var, "ess_tail"]
                    issues.append(
                        f"ESS tail for '{var}' = {ess_val:.0f} (threshold: {ess_tail_threshold})"
                    )

        # Report issues
        if not converged:
            warnings.warn(
                f"Convergence issues detected:\n"
                + "\n".join(f"  - {issue}" for issue in issues),
                UserWarning,
            )

        return converged

    def plot_trace(
        self,
        var_names: Optional[List[str]] = None,
        figsize: Optional[Tuple[int, int]] = None,
        compact: bool = True,
    ) -> plt.Figure:
        """
        Create trace plots for MCMC chains.

        Trace plots show:
        - Left panel: Parameter value over sampling iterations (all chains)
        - Right panel: Distribution of sampled values (KDE)

        Good trace plots show:
        - Random scatter around a stable mean (no trends)
        - Good mixing between chains
        - Symmetric, unimodal distributions

        Args:
            var_names: Variables to plot. If None, plots all.
            figsize: Figure size (width, height). Auto-calculated if None.
            compact: If True, uses compact layout (default: True)

        Returns:
            matplotlib Figure object

        Example:
            >>> fig = diagnostics.plot_trace(['tau', 'mu_1', 'mu_2'])
            >>> fig.savefig('trace_plot.png', dpi=300, bbox_inches='tight')
            >>> plt.show()
        """
        if var_names is None:
            var_names = self._var_names

        fig = az.plot_trace(
            self.trace, var_names=var_names, figsize=figsize, compact=compact
        )

        # Enhance the figure
        if hasattr(fig, "suptitle"):
            fig.suptitle("MCMC Trace Plots", fontsize=14, y=1.00)

        plt.tight_layout()
        return fig if isinstance(fig, plt.Figure) else plt.gcf()

    def plot_posterior(
        self,
        var_names: Optional[List[str]] = None,
        hdi_prob: float = 0.94,
        point_estimate: str = "mean",
        figsize: Optional[Tuple[int, int]] = None,
    ) -> plt.Figure:
        """
        Plot posterior distributions with HDI and point estimates.

        Shows the posterior distribution for each parameter with:
        - Density curve (KDE)
        - Point estimate (mean, median, or mode)
        - Highest Density Interval (credible interval)

        Args:
            var_names: Variables to plot. If None, plots all.
            hdi_prob: Probability for HDI (default: 0.94 = 94% interval)
            point_estimate: Type of point estimate ('mean', 'median', 'mode')
            figsize: Figure size (width, height). Auto-calculated if None.

        Returns:
            matplotlib Figure object

        Example:
            >>> fig = diagnostics.plot_posterior(['tau', 'mu_1', 'mu_2'])
            >>> fig.savefig('posterior_plot.png', dpi=300, bbox_inches='tight')
        """
        if var_names is None:
            var_names = self._var_names

        axes = az.plot_posterior(
            self.trace,
            var_names=var_names,
            hdi_prob=hdi_prob,
            point_estimate=point_estimate,
            figsize=figsize,
        )

        fig = plt.gcf()
        fig.suptitle(
            f"Posterior Distributions ({int(hdi_prob*100)}% HDI)", fontsize=14, y=1.00
        )

        plt.tight_layout()
        return fig

    def plot_forest(
        self,
        var_names: Optional[List[str]] = None,
        hdi_prob: float = 0.94,
        combined: bool = False,
        figsize: Optional[Tuple[int, int]] = None,
    ) -> plt.Figure:
        """
        Create forest plot showing HDI for parameters.

        Forest plots are useful for:
        - Comparing parameter estimates across chains
        - Visualizing uncertainty (HDI width)
        - Identifying convergence issues (separated chains)

        Args:
            var_names: Variables to plot. If None, plots all.
            hdi_prob: Probability for HDI (default: 0.94)
            combined: If True, show combined chains only (default: False)
            figsize: Figure size. Auto-calculated if None.

        Returns:
            matplotlib Figure object

        Example:
            >>> fig = diagnostics.plot_forest(['mu_1', 'mu_2', 'sigma_1', 'sigma_2'])
            >>> plt.show()
        """
        if var_names is None:
            var_names = self._var_names

        axes = az.plot_forest(
            self.trace,
            var_names=var_names,
            hdi_prob=hdi_prob,
            combined=combined,
            figsize=figsize,
        )

        fig = plt.gcf()
        fig.suptitle(
            f"Forest Plot - Parameter Estimates with {int(hdi_prob*100)}% HDI",
            fontsize=14,
        )

        plt.tight_layout()
        return fig

    def summary_stats(
        self, var_names: Optional[List[str]] = None, hdi_prob: float = 0.94
    ) -> pd.DataFrame:
        """
        Get comprehensive summary statistics for parameters.

        Returns a DataFrame with:
        - mean: Posterior mean
        - sd: Posterior standard deviation
        - hdi_X%: Highest Density Interval bounds
        - mcse_mean: Monte Carlo Standard Error for mean
        - mcse_sd: Monte Carlo Standard Error for sd
        - ess_bulk: Effective sample size (bulk)
        - ess_tail: Effective sample size (tail)
        - r_hat: Gelman-Rubin convergence statistic

        Args:
            var_names: Variables to summarize. If None, all variables.
            hdi_prob: Probability for HDI (default: 0.94)

        Returns:
            pandas DataFrame with summary statistics

        Example:
            >>> summary = diagnostics.summary_stats()
            >>> print(summary)
            >>> # Export to CSV
            >>> summary.to_csv('mcmc_summary.csv')
        """
        if var_names is None:
            var_names = self._var_names

        return az.summary(self.trace, var_names=var_names, hdi_prob=hdi_prob)

    def get_hdi(self, var_name: str, hdi_prob: float = 0.94) -> Dict[str, float]:
        """
        Get Highest Density Interval for a specific variable.

        The HDI is a Bayesian credible interval that contains the most
        probable values. Unlike quantile-based intervals, HDI is more
        intuitive for skewed distributions.

        Args:
            var_name: Name of the variable
            hdi_prob: Probability mass in interval (default: 0.94)

        Returns:
            Dictionary with 'lower', 'upper', and 'width' keys

        Raises:
            ValueError: If var_name is not in trace

        Example:
            >>> hdi = diagnostics.get_hdi('tau', hdi_prob=0.94)
            >>> print(f"94% HDI for tau: [{hdi['lower']:.1f}, {hdi['upper']:.1f}]")
            >>> print(f"HDI width: {hdi['width']:.1f}")
        """
        if var_name not in self._var_names:
            raise ValueError(
                f"Variable '{var_name}' not found in trace. "
                f"Available variables: {', '.join(self._var_names)}"
            )

        # Get HDI from ArViZ
        hdi_data = az.hdi(self.trace, hdi_prob=hdi_prob, var_names=[var_name])

        # Extract values
        lower = float(hdi_data[var_name].values[0])
        upper = float(hdi_data[var_name].values[1])

        return {
            "lower": lower,
            "upper": upper,
            "width": upper - lower,
            "probability": hdi_prob,
        }

    def plot_autocorr(
        self,
        var_names: Optional[List[str]] = None,
        max_lag: int = 100,
        figsize: Optional[Tuple[int, int]] = None,
    ) -> plt.Figure:
        """
        Plot autocorrelation for MCMC chains.

        Autocorrelation plots show correlation between samples at different
        lags. Good mixing shows rapid decay to zero.

        High autocorrelation indicates:
        - Poor mixing (need more samples)
        - Possible convergence issues
        - Lower effective sample size

        Args:
            var_names: Variables to plot. If None, plots all.
            max_lag: Maximum lag to display (default: 100)
            figsize: Figure size. Auto-calculated if None.

        Returns:
            matplotlib Figure object

        Example:
            >>> fig = diagnostics.plot_autocorr(['tau'])
            >>> plt.show()
        """
        if var_names is None:
            var_names = self._var_names

        axes = az.plot_autocorr(
            self.trace, var_names=var_names, max_lag=max_lag, figsize=figsize
        )

        fig = plt.gcf()
        fig.suptitle("Autocorrelation Plots", fontsize=14)

        plt.tight_layout()
        return fig

    def plot_rank(
        self,
        var_names: Optional[List[str]] = None,
        figsize: Optional[Tuple[int, int]] = None,
    ) -> plt.Figure:
        """
        Create rank plots for convergence diagnostics.

        Rank plots show the distribution of ranks of samples across chains.
        Uniform distribution indicates good mixing and convergence.

        This is a more sensitive diagnostic than traditional trace plots.

        Args:
            var_names: Variables to plot. If None, plots all.
            figsize: Figure size. Auto-calculated if None.

        Returns:
            matplotlib Figure object

        Example:
            >>> fig = diagnostics.plot_rank(['tau', 'mu_1', 'mu_2'])
            >>> plt.show()
        """
        if var_names is None:
            var_names = self._var_names

        axes = az.plot_rank(self.trace, var_names=var_names, figsize=figsize)

        fig = plt.gcf()
        fig.suptitle("Rank Plots - Convergence Diagnostic", fontsize=14)

        plt.tight_layout()
        return fig

    def get_effective_n(self, var_names: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Get effective sample sizes for all parameters.

        Effective Sample Size (ESS) accounts for autocorrelation in MCMC
        samples. It represents the number of independent samples that would
        give the same statistical precision.

        Args:
            var_names: Variables to analyze. If None, all variables.

        Returns:
            DataFrame with ESS bulk and tail for each variable

        Example:
            >>> ess = diagnostics.get_effective_n()
            >>> print(ess)
            >>> # Check if ESS is sufficient
            >>> if (ess['ess_bulk'] > 400).all():
            >>>     print("Sufficient effective samples!")
        """
        if var_names is None:
            var_names = self._var_names

        summary = self.summary_stats(var_names=var_names)

        return summary[["ess_bulk", "ess_tail"]]

    def get_rhat(self, var_names: Optional[List[str]] = None) -> pd.Series:
        """
        Get R-hat (Gelman-Rubin) statistics for all parameters.

        R-hat measures convergence by comparing variance within and between
        chains. Values close to 1.0 indicate convergence.

        Interpretation:
        - R-hat < 1.01: Excellent convergence
        - 1.01 ≤ R-hat < 1.05: Acceptable
        - R-hat ≥ 1.05: Poor convergence (need more samples)

        Args:
            var_names: Variables to analyze. If None, all variables.

        Returns:
            pandas Series with R-hat values

        Example:
            >>> rhat = diagnostics.get_rhat()
            >>> print(rhat)
            >>> # Check convergence
            >>> if (rhat < 1.01).all():
            >>>     print("All chains converged!")
        """
        if var_names is None:
            var_names = self._var_names

        summary = self.summary_stats(var_names=var_names)

        return summary["r_hat"]

    def __repr__(self) -> str:
        """String representation of diagnostics object."""
        n_vars = len(self._var_names)
        n_chains = len(self.trace.posterior.chain)
        n_draws = len(self.trace.posterior.draw)

        return (
            f"ModelDiagnostics("
            f"variables={n_vars}, "
            f"chains={n_chains}, "
            f"draws={n_draws})"
        )
