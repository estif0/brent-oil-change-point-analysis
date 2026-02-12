# Understanding Oil Market Dynamics Through Bayesian Change Point Analysis
## A Data-Driven Investigation of Brent Oil Price Structural Breaks

**Author**: Estifanose Sahilu  
**Client**: Birhan Energies  
**Date**: February 12, 2026  
**Analysis Period**: May 1987 - September 2022

---

## Executive Summary

In this analysis, I employed Bayesian change point detection to investigate how major geopolitical events, OPEC decisions, and economic shocks create structural breaks in Brent oil prices. Working with 35 years of daily price data and 17 carefully researched historical events, I identified a critical change point on **July 14, 2008**, coinciding with the peak oil prices before the global financial crisis. The analysis revealed that while the mean daily return shifted negligibly (-0.0004), **market volatility increased by 21.4%**, signaling a fundamental shift from the pre-crisis stability to post-crisis uncertainty. This research provides actionable insights for investors managing risk, policymakers ensuring energy security, and energy companies planning operations in increasingly volatile markets.

---

## Business Context and Objectives

As a data scientist working with Birhan Energies—a consultancy specializing in energy sector insights—my objective was to answer a critical question facing our clients: **How do major global events translate into quantifiable changes in oil market behavior?** 

Three key stakeholder groups depend on this analysis:

**Investors** need to understand market regime changes to optimize portfolio allocation and hedge against oil price volatility. **Policymakers** require evidence-based insights to develop strategies for economic stability and energy security, particularly in oil-dependent economies. **Energy Companies** must plan operations, manage costs, and optimize supply chains in response to price dynamics driven by events beyond their control.

Rather than simply documenting price fluctuations, I sought to identify *when* the market fundamentally changed its behavior and *why*, providing stakeholders with predictive insights rather than retrospective explanations.

---

## Methodology: A Three-Phase Approach

### Phase 1: Foundation and Event Research

I began by establishing a rigorous analytical workflow and compiling a comprehensive event dataset. Through extensive research of historical records, OPEC archives, and economic databases, I identified **17 major events** spanning 1990-2022, including the Iraq invasion of Kuwait (1990), Asian Financial Crisis (1997), multiple OPEC production decisions, the 2008 financial crisis, Arab Spring (2010), and Russia's invasion of Ukraine (2022). Each event was categorized by type (geopolitical, OPEC decision, economic shock, sanction) and expected impact direction.

My exploratory data analysis revealed that while raw Brent prices showed strong upward trends and non-stationarity, **log returns exhibited mean-reverting behavior suitable for change point modeling**. Stationarity testing using Augmented Dickey-Fuller and KPSS tests confirmed that log returns were stationary (ADF statistic: -60.43, p < 0.01), validating our modeling approach. Volatility analysis demonstrated clear clustering effects—periods of high volatility begetting more volatility—particularly around major crises.

### Phase 2: Bayesian Change Point Modeling

I implemented a Bayesian change point model using PyMC, which offers significant advantages over classical methods: it quantifies uncertainty through posterior distributions, naturally incorporates prior knowledge, and provides credible intervals rather than point estimates.

**Model Specification:**
```
For observations y₁, y₂, ..., yₙ (log returns):
  τ ~ DiscreteUniform(1, n)                    # Change point location
  μ₁, μ₂ ~ Normal(0, 1)                        # Mean before/after
  σ₁, σ₂ ~ HalfNormal(1)                       # Volatility before/after
  y ~ Normal(μ₁, σ₁) if t < τ, else Normal(μ₂, σ₂)
```

I ran MCMC sampling with 2,000 iterations across 4 chains, achieving excellent convergence (all R̂ = 1.0) and effective sample sizes exceeding 1,000 for all parameters. Trace plots showed stable mixing with no divergences, validating the reliability of our posterior estimates.

### Phase 3: Interactive Dashboard

To democratize access to these insights, I developed a full-stack dashboard with a Flask backend serving RESTful APIs and a React+TypeScript frontend featuring interactive Recharts visualizations. The dashboard allows stakeholders to explore the entire price history, zoom into specific periods, filter by event types, and examine the change point distribution—all with responsive design for desktop and mobile access.

---

## Key Findings

### The 2008 Structural Break

My analysis identified a **single dominant change point on July 14, 2008** (94% credible interval: May 8 - September 8, 2008), occurring just **3 days after oil prices peaked** at $147/barrel on July 11, 2008. This timing is not coincidental—it captures the precise moment when market dynamics shifted from speculation-driven growth to crisis-driven collapse.

**Quantified Impact:**
- **Mean Return**: Shifted from +0.0344% daily to -0.0045% daily (113% decrease)
- **Volatility**: Increased from 2.24% to 2.72% daily standard deviation (+21.4%)
- **Market Regime**: Transition from stable growth with moderate volatility to uncertain, high-volatility environment

![Change Point Analysis](../figures/07_price_with_changepoints.png)
*Figure 1: Detected change point (red line) aligning with the 2008 oil price peak and financial crisis onset.*

### Event Association and Market Response

By analyzing all 17 historical events relative to the detected change point, I found the **2008-2009 period uniquely dense with market-transforming events**: the oil price peak (July 11), Lehman Brothers collapse (September 15), and the subsequent demand destruction. No other period in our 35-year dataset exhibited such concentrated, high-impact disruption sufficient to create a lasting structural break.

Earlier events (Gulf War, Asian Financial Crisis, Iraq War) and later events (Arab Spring, OPEC production cuts, COVID-19 pandemic) caused temporary price spikes or drops but did not fundamentally alter the volatility regime of the market. This finding suggests that **the scale and simultaneity of shocks matter more than individual events** in creating lasting structural changes.

---

## Strategic Recommendations

### For Investors: Embrace Volatility-Aware Strategies

The 21.4% increase in volatility post-2008 is not a temporary anomaly—it represents the new normal. I recommend:

1. **Increase portfolio hedging** through options and volatility derivatives, particularly during geopolitically sensitive periods
2. **Shift from buy-and-hold to tactical allocation** in energy sectors, rebalancing more frequently in response to event-driven volatility
3. **Implement regime-switching models** that adjust risk parameters based on detected market states

### For Policymakers: Prepare for Persistent Uncertainty

Oil price volatility directly impacts inflation, trade balances, and fiscal stability. My recommendations:

1. **Expand strategic petroleum reserves** during low-volatility periods as insurance against future shocks
2. **Diversify energy sources** to reduce dependence on oil, mitigating exposure to external price shocks
3. **Develop early warning systems** combining change point detection with geopolitical monitoring to anticipate market disruptions

### For Energy Companies: Build Operational Resilience

The post-2008 high-volatility regime requires operational adaptability:

1. **Implement flexible supply contracts** with price adjustment clauses to manage input cost volatility
2. **Optimize inventory management** to balance carrying costs against price volatility risks
3. **Invest in scenario planning** using Bayesian methods to quantify uncertainty in cash flow projections

---

## Limitations and Future Directions

### Acknowledging Constraints

**Correlation ≠ Causation**: While my change point temporally aligns with the 2008 crisis, statistical association does not prove causal mechanisms. Oil price movements result from complex interactions of supply, demand, speculation, and regulatory factors.

**Single Change Point Model**: I deliberately chose a simple model for interpretability, but reality likely includes multiple smaller structural breaks. Events like the 2014 OPEC production decision and COVID-19 pandemic arguably created additional regime changes not captured here.

**Data Limitations**: Daily granularity misses intraday volatility, and the dataset ends in September 2022, omitting subsequent events like the 2022-2023 energy crisis escalation.

### Promising Extensions

Future work should address these limitations through:

1. **Multiple Change Point Models**: Implement algorithms detecting 3-5 structural breaks to capture additional regime transitions
2. **Multivariate Analysis**: Incorporate GDP growth, exchange rates, and inventory levels using Vector Autoregression (VAR) to understand dynamic causal relationships
3. **Advanced Architectures**: Deploy Markov-Switching models to allow parameters to evolve continuously rather than at discrete change points
4. **Real-Time Implementation**: Develop online Bayesian updating methods to detect emerging change points as new data arrives

---

## Conclusion

This analysis demonstrates that Bayesian change point detection provides a principled, uncertainty-aware framework for identifying structural breaks in oil markets. By quantifying that the 2008 financial crisis increased market volatility by 21.4% with lasting effects, I have provided stakeholders with actionable insights for risk management, policy development, and operational planning.

The interactive dashboard I developed ensures these insights remain accessible and actionable. Rather than a static report, stakeholders can explore the data dynamically, test hypotheses, and integrate findings into their decision-making workflows.

As global events continue to shape energy markets—from climate policy transitions to geopolitical realignments—the methods I've developed here provide a replicable framework for ongoing market intelligence. The question is no longer whether events affect oil prices, but *when* they create fundamental regime changes and *how* stakeholders can position themselves accordingly.

---

**Dashboard Access**: [View Interactive Dashboard](http://localhost:5173)  
**Repository**: Available upon request with full reproducible code, tests, and documentation  
**Contact**: estifanose.sahilu@example.com
