# Assumptions and Limitations

**Project**: Brent Oil Price Change Point Analysis  
**Client**: Birhan Energies  
**Date**: February 2026

---

## Overview

This document outlines the key assumptions made in the Brent oil price change point analysis and acknowledges the limitations of our approach. Understanding these constraints is crucial for proper interpretation and application of the results.

---

## Data Assumptions

### 1. Data Quality and Completeness

**Assumptions:**
- Historical Brent oil price data is accurate and reliable
- Prices reflect true market conditions at the time of recording
- Data collection methodology remained consistent over time
- Missing values are randomly distributed (if any)

**Limitations:**
- Early data (1980s-1990s) may have less precision or fewer data points
- Price data may not capture all intraday volatility
- We rely on publicly available data which may have reporting delays
- Data from different sources may use different conventions (spot vs. futures)

**Mitigation:**
- Use reputable data sources (e.g., EIA, Bloomberg)
- Document and handle missing values transparently
- Validate data against multiple sources where possible

---

### 2. Event Data

**Assumptions:**
- Selected events represent major oil market drivers
- Event dates are accurate and well-documented
- Events have discrete start dates (not gradual processes)
- Event categorization (geopolitical, OPEC, economic, sanction) is meaningful

**Limitations:**
- Event selection involves subjective judgment
- Some events may have been omitted
- Event impacts may overlap or interact
- Exact timing of event impact on prices is uncertain
- Events may have anticipatory effects (price changes before official date)

**Mitigation:**
- Use consensus historical sources for event dates
- Include events identified by domain experts
- Consider ±30 day window around events for association
- Document event selection criteria

---

## Model Assumptions

### 3. Bayesian Change Point Model

**Assumptions:**
- Price changes follow a normal distribution
- Change points represent discrete structural breaks
- Parameters (mean, variance) are constant within regimes
- Single change point is sufficient (for simple model)
- Prior distributions are non-informative or weakly informative

**Limitations:**
- Real markets may have gradual transitions, not discrete breaks
- Multiple simultaneous factors may affect prices
- Model assumes independence of observations (may violate due to autocorrelation)
- Normal distribution may not capture extreme events (fat tails)
- Single change point model oversimplifies complex dynamics

**Mitigation:**
- Test multiple model specifications
- Check residuals for model fit
- Use robust priors informed by domain knowledge
- Consider multiple change point models for complex patterns
- Validate results against known historical events

---

### 4. Stationarity

**Assumptions:**
- Log returns are approximately stationary
- ADF and KPSS tests adequately assess stationarity
- Non-stationarity can be addressed through differencing or log transformation

**Limitations:**
- Oil prices may exhibit non-stationary behavior even after transformation
- Tests have limited power with finite samples
- Stationarity may hold in some periods but not others (local non-stationarity)
- Structural breaks can affect stationarity tests

**Mitigation:**
- Use both ADF and KPSS tests (compare results)
- Test on multiple time windows
- Visually inspect time series for obvious non-stationarity
- Consider regime-switching models if needed

---

## Analytical Assumptions

### 5. Causality vs. Correlation

**Critical Limitation:**
- **This analysis identifies correlations, not causal relationships**
- A change point coinciding with an event does not prove the event caused the price change
- Multiple factors may contribute to price movements
- Reverse causality is possible (price changes triggering events)
- Confounding variables may exist

**Implications:**
- Cannot definitively attribute price changes to specific events
- Other unmeasured factors may be the true drivers
- Events may be symptoms rather than causes
- Timing coincidence may be spurious

**Best Practices:**
- Use careful language ("associated with" not "caused by")
- Consider alternative explanations
- Triangulate with domain knowledge and other evidence
- Acknowledge uncertainty in interpretations
- State conclusions as provisional, not definitive

---

### 6. Event Attribution

**Assumptions:**
- Events within ±30 days of change point are potentially related
- Closer events are more likely to be related
- Event type provides information about likely impact direction

**Limitations:**
- Window size (30 days) is arbitrary
- Multiple events may occur in same window
- Events may have delayed or anticipatory effects
- Some change points may not correspond to known events
- Event databases may be incomplete

**Mitigation:**
- Test sensitivity to different window sizes
- Report all events in window, not just closest
- Consider event magnitude and market attention
- Acknowledge when no clear event association exists

---

## Scope Limitations

### 7. Temporal Scope

**Limitations:**
- Analysis covers May 1987 - September 2022
- Patterns identified may not apply to other periods
- Market structure has evolved over time
- Recent market dynamics may differ from historical patterns

**Implications:**
- Findings may not generalize to future periods
- Early period (1980s) may behave differently from recent period (2010s+)
- Structural changes in oil markets (shale revolution, renewables) affect dynamics

---

### 8. Geographic and Market Scope

**Assumptions:**
- Brent crude is representative of global oil prices
- Events affecting Brent also affect global oil markets

**Limitations:**
- Brent is one of several oil benchmarks (WTI, Dubai, etc.)
- Regional price differentials exist
- Analysis doesn't capture local supply/demand dynamics
- Transportation costs, refining capacity, and storage affect local prices

**Implications:**
- Results most applicable to Brent-linked contracts
- May not fully represent US or Asian markets
- Regional events may not impact Brent prices

---

## Methodological Limitations

### 9. Model Complexity

**Trade-offs:**
- Simple models are interpretable but may miss complexity
- Complex models capture nuances but risk overfitting
- Bayesian models require subjective prior specification

**Limitations:**
- Current single change point model is deliberately simple
- Real price dynamics are highly complex
- Model may not capture:
  - Seasonality
  - Long-term trends
  - Volatility clustering (GARCH effects)
  - Asymmetric responses to shocks
  - Multiple regime changes

**Future Work:**
- Multiple change point models
- Time-varying volatility models
- Machine learning ensemble approaches
- Factor models incorporating supply/demand

---

### 10. Computational Constraints

**Limitations:**
- MCMC sampling is computationally intensive
- Long chains needed for convergence
- Multiple chains needed for validation
- Model selection requires multiple runs

**Implications:**
- Some model specifications may be impractical
- Trade-off between model complexity and computation time
- Real-time analysis may not be feasible with current approach

---

## Interpretation Limitations

### 11. Uncertainty Quantification

**Strengths:**
- Bayesian approach provides posterior distributions
- Credible intervals quantify uncertainty

**Limitations:**
- Uncertainty only reflects model and sampling uncertainty
- Doesn't account for model misspecification
- Doesn't capture uncertainty in event selection or data quality
- Assumes model structure is correct

**Best Practices:**
- Report credible intervals, not just point estimates
- Acknowledge additional sources of uncertainty
- Use sensitivity analyses to test robustness

---

### 12. Predictive Limitations

**Critical Limitations:**
- This is a **retrospective analysis**, not a predictive model
- Identified patterns may not persist in the future
- Cannot predict future change points with high accuracy
- Markets are forward-looking; historical patterns may break down

**Implications:**
- Results inform understanding of past events
- Can identify correlates of past price changes
- Should not be used for price forecasting without additional modeling
- Real-time change point detection is a different problem

---

## External Factors Not Considered

### 13. Omitted Variables

**Factors not explicitly modeled:**
- Supply side: OPEC production, non-OPEC supply, shale production
- Demand side: Economic growth, industrial activity, transportation demand
- Market factors: Inventory levels, speculation, futures markets
- Currency effects: USD strength, exchange rates
- Technological changes: Fracking, renewable energy, EVs
- Policy factors: Environmental regulations, subsidies, carbon pricing
- Weather and seasonality: Heating/cooling demand, hurricanes

**Implications:**
- Price changes may be driven by factors not in event database
- Model may attribute changes to events when other factors are responsible
- Comprehensive oil price modeling requires multivariate approach

---

## Assumptions About Oil Markets

### 14. Market Efficiency

**Assumptions:**
- Prices reflect available information
- Markets respond to events reasonably quickly
- Price discovery is effective

**Limitations:**
- Markets may overreact or underreact to events
- Information asymmetry exists
- Speculation and herding behavior occur
- Market structure has changed over time (algorithmic trading)

---

### 15. Supply and Demand

**Implicit Assumptions:**
- Events affect price primarily through supply/demand channels
- Supply disruptions have immediate price effects
- Demand shocks affect prices systematically

**Limitations:**
- Oil markets have complex supply chains
- Inventory buffers smooth supply shocks
- Demand is price-inelastic in short run
- Substitution effects take time to manifest

---

## Recommendations for Users

### How to Interpret Results

✅ **Appropriate Uses:**
- Understanding historical price movements
- Identifying periods of structural change
- Exploring event-price relationships
- Generating hypotheses for further research
- Educational purposes and market analysis

❌ **Inappropriate Uses:**
- Price forecasting or prediction
- Trading signals or investment advice
- Definitive causal claims
- Policy decisions without additional analysis
- Ignoring stated limitations

---

### Communicating Findings

**Recommended Language:**
- "Associated with" not "caused by"
- "Suggests" or "indicates" not "proves"
- "Approximately" when giving point estimates
- Include uncertainty ranges
- Acknowledge alternative explanations

**Example:**
> "Our analysis identifies a change point on September 15, 2008, associated with the Lehman Brothers collapse. Prices shifted from approximately $96 to $76 USD/barrel (credible interval: $70-$82), representing a roughly 21% decline. While this timing strongly suggests a relationship with the financial crisis, other factors including demand destruction and inventory levels also contributed to the price movement."

---

## Model Validation and Robustness

### Checks Performed:
1. Convergence diagnostics (R-hat, ESS)
2. Posterior predictive checks
3. Sensitivity to prior specifications
4. Comparison with alternative models
5. Visual inspection of results
6. Domain expert review

### Checks Recommended:
1. Out-of-sample validation (if extended)
2. Cross-validation across time periods
3. Comparison with other change point methods
4. Sensitivity to event window size
5. Robustness to data preprocessing choices

---

## Future Improvements

To address these limitations, future work should consider:

1. **Multiple Change Points**: Extension to detect multiple regime changes
2. **Hierarchical Models**: Account for event types hierarchically
3. **External Regressors**: Include supply/demand variables explicitly
4. **Non-Parametric Approaches**: Relax distributional assumptions
5. **Online Detection**: Real-time change point monitoring
6. **Causal Inference**: Use structural models or natural experiments
7. **Machine Learning**: Complement with ML approaches for pattern recognition
8. **Longer Data**: Extend to more recent data as available
9. **Cross-Market Analysis**: Compare Brent with WTI, Dubai benchmarks
10. **Sentiment Analysis**: Incorporate news sentiment data

---

## Conclusion

This analysis provides valuable insights into historical Brent oil price changes and their association with major events. However, users must understand and acknowledge the assumptions and limitations outlined in this document. 

**Key Takeaways:**
- Results show correlations, not definitive causation
- Model is deliberately simplified for interpretability
- Multiple factors beyond modeled events affect prices
- Findings are retrospective and may not predict future patterns
- Proper interpretation requires domain knowledge and caution

When used appropriately with these limitations in mind, the analysis offers a rigorous, probabilistic framework for understanding how major world events have historically corresponded with structural changes in oil prices.

---

**Document Version**: 1.0  
**Last Updated**: February 8, 2026  
**Review Recommended**: Before each major presentation or publication
