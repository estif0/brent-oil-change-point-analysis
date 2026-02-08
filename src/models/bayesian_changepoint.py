"""
Bayesian Change Point Model

This module implements a Bayesian change point detection model for time series analysis.
The model identifies a single point in time where the statistical properties of the series
change significantly, using Markov Chain Monte Carlo (MCMC) sampling via PyMC.

Key Concepts:
    - Change Point (τ): The time index where the series behavior changes
    - Before Parameters (μ₁, σ₁): Mean and standard deviation before τ
    - After Parameters (μ₂, σ₂): Mean and standard deviation after τ
    - Prior Distributions: Our beliefs about parameters before seeing data
    - Posterior Distributions: Updated beliefs after observing data

Example:
    >>> import pandas as pd
    >>> from src.models.bayesian_changepoint import BayesianChangePointModel
    >>> 
    >>> # Load log returns data
    >>> data = pd.Series([...])  # Your time series data
    >>> 
    >>> # Create and fit model
    >>> model = BayesianChangePointModel(data)
    >>> model.build_model()
    >>> trace = model.fit(samples=2000, tune=1000, chains=2)
    >>> 
    >>> # Analyze results
    >>> summary = model.get_summary()
    >>> print(summary)
"""

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
from typing import Optional, Dict, Any
import warnings


class BayesianChangePointModel:
    """
    Bayesian change point detection model for time series.
    
    This model assumes a single change point where the mean and/or standard deviation
    of the time series changes. It uses Bayesian inference to estimate:
    - The location of the change point (τ)
    - Statistical properties before the change point (μ₁, σ₁)
    - Statistical properties after the change point (μ₂, σ₂)
    
    The model uses weakly informative priors and MCMC sampling to obtain posterior
    distributions for all parameters.
    
    Attributes:
        data (pd.Series): Time series data to analyze
        n_observations (int): Number of data points
        model (pm.Model): PyMC model object
        trace (az.InferenceData): MCMC sampling results
        
    Mathematical Formulation:
        τ ~ DiscreteUniform(0, n-1)           # Change point location
        μ₁ ~ Normal(data_mean, data_std * 2)  # Mean before τ
        μ₂ ~ Normal(data_mean, data_std * 2)  # Mean after τ
        σ₁ ~ HalfNormal(data_std * 2)         # Std dev before τ
        σ₂ ~ HalfNormal(data_std * 2)         # Std dev after τ
        
        For t < τ:  y_t ~ Normal(μ₁, σ₁)
        For t ≥ τ:  y_t ~ Normal(μ₂, σ₂)
    """
    
    def __init__(self, data: pd.Series, name: str = "changepoint"):
        """
        Initialize the Bayesian change point model.
        
        Args:
            data: Time series data (typically log returns or differenced series).
                  Should be a pandas Series with datetime index.
            name: Name for the model (used in PyMC model naming)
            
        Raises:
            ValueError: If data is empty or contains NaN values
            TypeError: If data is not a pandas Series
            
        Example:
            >>> import pandas as pd
            >>> data = pd.Series([1, 2, 3, 10, 11, 12], 
            ...                  index=pd.date_range('2020-01-01', periods=6))
            >>> model = BayesianChangePointModel(data)
        """
        if not isinstance(data, pd.Series):
            raise TypeError("Data must be a pandas Series")
        
        if len(data) == 0:
            raise ValueError("Data cannot be empty")
        
        if data.isna().any():
            raise ValueError("Data contains NaN values. Please clean data first.")
        
        self.data = data
        self.data_values = data.values
        self.n_observations = len(data)
        self.name = name
        self.model = None
        self.trace = None
        
        # Calculate data statistics for priors
        self.data_mean = np.mean(self.data_values)
        self.data_std = np.std(self.data_values)
        
    def build_model(self, 
                    prior_std_scale: float = 2.0,
                    min_segment_length: int = 30) -> pm.Model:
        """
        Construct the PyMC Bayesian change point model.
        
        This method builds the probabilistic model structure including:
        - Prior distributions for all parameters
        - Likelihood function using pm.math.switch for regime switching
        - Constraints on change point location to ensure meaningful segments
        
        Args:
            prior_std_scale: Scale factor for prior standard deviations.
                           Larger values = more diffuse priors. Default: 2.0
            min_segment_length: Minimum number of observations in each segment.
                              This prevents change points too close to boundaries.
                              Default: 30
                              
        Returns:
            The constructed PyMC model object
            
        Raises:
            ValueError: If min_segment_length is too large for the data
            
        Note:
            After calling this method, you must call fit() to perform inference.
            
        Example:
            >>> model = BayesianChangePointModel(data)
            >>> model.build_model(prior_std_scale=2.0)
            >>> # Model is ready for fitting
        """
        if min_segment_length * 2 >= self.n_observations:
            raise ValueError(
                f"min_segment_length ({min_segment_length}) is too large. "
                f"Data has {self.n_observations} observations. "
                f"Need at least {min_segment_length * 2} observations."
            )
        
        with pm.Model() as self.model:
            # ============================================================
            # PRIOR DISTRIBUTIONS
            # ============================================================
            
            # Change point location (τ)
            # Uniform discrete prior over valid change point locations
            # We exclude the first and last min_segment_length points to ensure
            # both segments have enough data
            tau = pm.DiscreteUniform(
                'tau',
                lower=min_segment_length,
                upper=self.n_observations - min_segment_length - 1
            )
            
            # Mean before change point (μ₁)
            # Centered around observed data mean with wide standard deviation
            mu_1 = pm.Normal(
                'mu_1',
                mu=self.data_mean,
                sigma=self.data_std * prior_std_scale
            )
            
            # Mean after change point (μ₂)
            mu_2 = pm.Normal(
                'mu_2',
                mu=self.data_mean,
                sigma=self.data_std * prior_std_scale
            )
            
            # Standard deviation before change point (σ₁)
            # Half-normal prior (only positive values)
            sigma_1 = pm.HalfNormal(
                'sigma_1',
                sigma=self.data_std * prior_std_scale
            )
            
            # Standard deviation after change point (σ₂)
            sigma_2 = pm.HalfNormal(
                'sigma_2',
                sigma=self.data_std * prior_std_scale
            )
            
            # ============================================================
            # REGIME-SWITCHING LIKELIHOOD
            # ============================================================
            
            # Create index array for switching
            # This determines which regime each observation belongs to
            idx = np.arange(self.n_observations)
            
            # Use pm.math.switch to select parameters based on regime
            # If idx < tau: use (mu_1, sigma_1), else use (mu_2, sigma_2)
            mu = pm.math.switch(tau >= idx, mu_1, mu_2)
            sigma = pm.math.switch(tau >= idx, sigma_1, sigma_2)
            
            # Likelihood: observations follow Normal distribution
            # with regime-specific parameters
            observation = pm.Normal(
                'obs',
                mu=mu,
                sigma=sigma,
                observed=self.data_values
            )
        
        return self.model
    
    def fit(self, 
            samples: int = 2000,
            tune: int = 1000,
            chains: int = 2,
            target_accept: float = 0.95,
            random_seed: Optional[int] = None,
            **kwargs) -> az.InferenceData:
        """
        Fit the model using MCMC sampling.
        
        This method performs Markov Chain Monte Carlo sampling to obtain posterior
        distributions for all model parameters. It uses the NUTS sampler (No-U-Turn
        Sampler), which is efficient for continuous parameters, combined with
        step methods appropriate for the discrete change point parameter.
        
        Args:
            samples: Number of samples to draw from the posterior (per chain).
                    More samples = better approximation but longer runtime.
                    Default: 2000
            tune: Number of tuning/warmup samples (per chain). These are discarded.
                 Tuning helps the sampler adapt to the posterior geometry.
                 Default: 1000
            chains: Number of independent MCMC chains to run.
                   Multiple chains help diagnose convergence.
                   Default: 2
            target_accept: Target acceptance probability for NUTS sampler.
                          Higher values = more accurate but slower.
                          Default: 0.95
            random_seed: Random seed for reproducibility. Default: None
            **kwargs: Additional arguments passed to pm.sample()
            
        Returns:
            InferenceData object containing:
                - Posterior samples for all parameters
                - Sampling diagnostics
                - Model information
                
        Raises:
            RuntimeError: If model hasn't been built yet
            
        Note:
            This can take several minutes depending on data size and number of samples.
            Progress bars will show sampling progress for each chain.
            
        Example:
            >>> model = BayesianChangePointModel(data)
            >>> model.build_model()
            >>> trace = model.fit(samples=2000, tune=1000, chains=2)
            >>> # Check convergence
            >>> print(trace.posterior['tau'].mean())
        """
        if self.model is None:
            raise RuntimeError(
                "Model must be built before fitting. Call build_model() first."
            )
        
        with self.model:
            # Sample from posterior using MCMC
            # PyMC automatically selects appropriate step methods
            self.trace = pm.sample(
                draws=samples,
                tune=tune,
                chains=chains,
                target_accept=target_accept,
                random_seed=random_seed,
                return_inferencedata=True,
                **kwargs
            )
        
        return self.trace
    
    def get_trace(self) -> az.InferenceData:
        """
        Get the MCMC trace (posterior samples).
        
        Returns:
            InferenceData object containing posterior samples and diagnostics
            
        Raises:
            RuntimeError: If model hasn't been fitted yet
            
        Example:
            >>> trace = model.get_trace()
            >>> # Access posterior samples
            >>> tau_samples = trace.posterior['tau'].values
        """
        if self.trace is None:
            raise RuntimeError(
                "Model must be fitted before accessing trace. Call fit() first."
            )
        return self.trace
    
    def get_summary(self, 
                    var_names: Optional[list] = None,
                    hdi_prob: float = 0.94) -> pd.DataFrame:
        """
        Get summary statistics for posterior distributions.
        
        This provides a comprehensive summary including:
        - Mean, standard deviation
        - Highest Density Interval (HDI)
        - Effective sample size (ESS)
        - R-hat convergence diagnostic
        
        Args:
            var_names: List of variable names to summarize.
                      If None, summarizes all variables.
                      Default: None
            hdi_prob: Probability mass for Highest Density Interval.
                     Default: 0.94 (94% HDI)
                     
        Returns:
            DataFrame with summary statistics for each parameter
            
        Raises:
            RuntimeError: If model hasn't been fitted yet
            
        Example:
            >>> summary = model.get_summary()
            >>> print(summary)
            >>> # Check specific parameter
            >>> tau_mean = summary.loc['tau', 'mean']
        """
        if self.trace is None:
            raise RuntimeError(
                "Model must be fitted before getting summary. Call fit() first."
            )
        
        return az.summary(
            self.trace,
            var_names=var_names,
            hdi_prob=hdi_prob
        )
    
    def get_changepoint_estimate(self, 
                                 method: str = 'mean') -> Dict[str, Any]:
        """
        Get the estimated change point location and associated date.
        
        Args:
            method: Method for point estimate. Options:
                   - 'mean': Posterior mean
                   - 'median': Posterior median
                   - 'mode': Most probable value (MAP)
                   Default: 'mean'
                   
        Returns:
            Dictionary containing:
                - 'index': Integer index of change point
                - 'date': Datetime of change point (if data has datetime index)
                - 'method': Method used for estimation
                
        Raises:
            RuntimeError: If model hasn't been fitted yet
            ValueError: If method is not recognized
            
        Example:
            >>> cp = model.get_changepoint_estimate(method='mean')
            >>> print(f"Change point at: {cp['date']}, index: {cp['index']}")
        """
        if self.trace is None:
            raise RuntimeError(
                "Model must be fitted before estimating change point. Call fit() first."
            )
        
        tau_samples = self.trace.posterior['tau'].values.flatten()
        
        if method == 'mean':
            tau_estimate = int(np.round(np.mean(tau_samples)))
        elif method == 'median':
            tau_estimate = int(np.round(np.median(tau_samples)))
        elif method == 'mode':
            # Most frequent value in posterior samples
            tau_estimate = int(np.bincount(tau_samples.astype(int)).argmax())
        else:
            raise ValueError(
                f"Method '{method}' not recognized. "
                f"Choose from: 'mean', 'median', 'mode'"
            )
        
        result = {
            'index': tau_estimate,
            'method': method
        }
        
        # Add date if data has datetime index
        if isinstance(self.data.index, pd.DatetimeIndex):
            result['date'] = self.data.index[tau_estimate]
        
        return result
    
    def get_parameter_estimates(self) -> Dict[str, Dict[str, float]]:
        """
        Get point estimates and credible intervals for all parameters.
        
        Returns:
            Nested dictionary with structure:
                {
                    'tau': {'mean': ..., 'hdi_lower': ..., 'hdi_upper': ...},
                    'mu_1': {...},
                    'mu_2': {...},
                    'sigma_1': {...},
                    'sigma_2': {...}
                }
                
        Raises:
            RuntimeError: If model hasn't been fitted yet
            
        Example:
            >>> params = model.get_parameter_estimates()
            >>> print(f"Mean before: {params['mu_1']['mean']:.4f}")
            >>> print(f"Mean after: {params['mu_2']['mean']:.4f}")
        """
        if self.trace is None:
            raise RuntimeError(
                "Model must be fitted before getting parameters. Call fit() first."
            )
        
        summary = self.get_summary()
        
        result = {}
        for var in ['tau', 'mu_1', 'mu_2', 'sigma_1', 'sigma_2']:
            result[var] = {
                'mean': summary.loc[var, 'mean'],
                'std': summary.loc[var, 'sd'],
                'hdi_lower': summary.loc[var, 'hdi_3%'],
                'hdi_upper': summary.loc[var, 'hdi_97%']
            }
        
        return result
    
    def __repr__(self) -> str:
        """String representation of the model."""
        status = "not fitted"
        if self.trace is not None:
            n_samples = len(self.trace.posterior.chain) * len(self.trace.posterior.draw)
            status = f"fitted with {n_samples} samples"
        
        return (
            f"BayesianChangePointModel("
            f"n_observations={self.n_observations}, "
            f"status='{status}')"
        )
