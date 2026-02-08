# Change Point Detection: Expected Outputs and Limitations

**Version:** 1.0  
**Last Updated:** February 8, 2026  
**Audience:** Non-Technical Stakeholders

---

## Purpose

This document explains what to expect from our Bayesian change point detection analysis and its limitations. It's written for business stakeholders without requiring statistical or technical expertise.

---

## What This Analysis Does

Our change point detection model examines historical Brent oil prices to identify moments when the market fundamentally changed behavior. Think of it as detecting "before and after" moments in the oil market - like how the 2008 financial crisis marked a clear shift in market dynamics.

---

## Expected Outputs

When the analysis completes, you'll receive the following information:

### 1. Change Point Date(s)

**What you get:**
- **Most Likely Date**: The specific date when the market shift occurred (e.g., "July 14, 2008")
- **Confidence Range**: A date range showing our uncertainty (e.g., "May 8 - September 8, 2008")
- **Uncertainty Level**: How confident we are, measured in days (e.g., "±25 days")

**How to interpret:**
- The "most likely date" is our best estimate of when the shift happened
- The "confidence range" tells you the window in which we're 94% confident the true change occurred
- Smaller uncertainty = more precise detection

**Example Output:**
```
Change Point Detected: July 14, 2008
94% Confidence Interval: May 8, 2008 - September 8, 2008
Uncertainty: ±25 days
```

---

### 2. Parameter Shifts (Market Behavior Changes)

**What you get:**
- **Before Period Statistics**: Average return and volatility before the change
- **After Period Statistics**: Average return and volatility after the change
- **Magnitude of Change**: How much things shifted (percentage or absolute change)
- **Direction**: Whether returns went up or down, volatility increased or decreased

**How to interpret:**
- **Average Return Shift**: Did prices tend to rise or fall faster after the change?
- **Volatility Change**: Did the market become more or less predictable?
  - Higher volatility = more uncertainty and larger price swings
  - Lower volatility = more stable, predictable prices

**Example Output:**
```
Mean Return:
  Before:  0.034% per day
  After:  -0.008% per day
  Change:  -0.042% (-308% shift)
  
Volatility:
  Before:  2.0% per day
  After:   2.8% per day  
  Change:  +0.8% (+40% increase)
  
Interpretation: Market shifted from slight growth to slight decline,
                and became 40% more volatile (less predictable).
```

---

### 3. Event Association

**What you get:**
- **Nearby Historical Events**: Major events that occurred near the detected change point
- **Event Details**: Name, date, type (geopolitical, economic, OPEC decision)
- **Distance from Change Point**: How many days before/after the event the change occurred
- **Expected vs. Actual Impact**: Whether the market shift aligns with what we'd expect

**How to interpret:**
- If a major event is within ±30 days of the change point, there's likely a connection
- Multiple events near a change point suggest complex, interconnected causes
- The "expected impact" shows whether the market reacted as anticipated

**Example Output:**
```
Closest Event: Oil Price Peak
Event Date: July 11, 2008
Distance: -3 days (change point occurred 3 days after event)
Event Type: Economic Shock
Expected Impact: Price increase followed by correction

Interpretation: The change point occurred immediately after oil reached 
                its historical peak ($147/barrel), marking the start of 
                the 2008 financial crisis period.
```

---

### 4. Visual Outputs

**What you get:**
- **Time Series Plot**: Price history with change point marked
- **Distribution Plots**: Statistical visualizations of uncertainty
- **Before/After Comparison**: Visual comparison of market behavior in both periods
- **Event Timeline**: Change points plotted alongside major historical events

**How to interpret:**
- Red vertical lines = detected change points
- Shaded regions = confidence intervals
- Blue vs. orange regions = before and after the change
- Triangles on timeline = major historical events

---

### 5. Impact Statement

**What you get:**
A plain-language summary of the findings, structured as:
- What changed and when
- How big the change was
- What might have caused it
- What it means for stakeholders

**Example:**
```
On July 14, 2008, we detected a significant regime shift in Brent oil 
prices. The market transitioned from a growth phase (0.03% daily returns) 
to a declining phase (-0.01% daily returns), with volatility increasing 
by 21%. This change occurred just 3 days after oil reached its historical 
peak of $147/barrel and coincides with the onset of the 2008 financial 
crisis. The increased volatility suggests heightened market uncertainty 
during this period.
```

---

## Key Limitations

### 1. **Historical Analysis Only**

**What this means:**
- The model analyzes past data to detect changes that already happened
- It cannot predict when future change points will occur
- Past patterns don't guarantee future behavior

**Practical implication:**
Use these insights to understand market history and what drove past changes, but not to forecast exact future shift dates.

---

### 2. **Single Change Point Focus**

**What this means:**
- The current model identifies ONE major change point in the data
- Reality likely has multiple smaller shifts
- We're highlighting the most significant regime change

**Practical implication:**
The detected change point represents the dominant shift. Other smaller changes may exist but aren't captured. For multi-change point analysis, request the enhanced model.

---

### 3. **Correlation vs. Causation**

**What this means:**
- We can show that events happened near change points
- We cannot prove the events caused the changes
- Multiple factors often work together

**Practical implication:**
Event associations suggest likely drivers of market shifts but aren't definitive proof. Use domain expertise to evaluate plausibility.

---

### 4. **Normal Distribution Assumption**

**What this means:**
- The model assumes returns follow a bell curve (normal distribution)
- Real markets have "fat tails" (more extreme events than expected)
- Very rare, extreme events might not be captured perfectly

**Practical implication:**
The model works well for typical market behavior but may underestimate the probability of extreme crashes or spikes.

---

### 5. **Data Quality Dependent**

**What this means:**
- Results are only as good as the input data
- Missing data, errors, or gaps reduce accuracy
- We rely on historical price data being accurate and complete

**Practical implication:**
Before interpreting results, verify data quality. Check the validation report for any data issues.

---

### 6. **Uncertainty Exists**

**What this means:**
- All change point dates have uncertainty ranges
- Parameter estimates have confidence intervals
- "Most likely" doesn't mean "guaranteed"

**Practical implication:**
Always consider the confidence intervals. A change point with ±5 days uncertainty is much more reliable than one with ±60 days.

---

### 7. **Aggregate Market View**

**What this means:**
- We analyze Brent crude oil prices as a whole
- Individual refinery, transport, or regional price differences aren't captured
- Market-wide shifts may not affect all participants equally

**Practical implication:**
Results apply to the Brent crude benchmark. Local market conditions may differ. Use these insights as a starting point for deeper regional analysis.

---

## Best Practices for Using These Results

### ✓ Do:
- **Consider the confidence intervals** - Not just point estimates
- **Review event associations** - But apply domain knowledge
- **Use visualizations** - Pictures tell the story better than numbers
- **Combine with qualitative analysis** - Statistical findings + expert judgment
- **Check data quality first** - Garbage in = garbage out

### ✗ Don't:
- **Treat dates as exact** - Always account for uncertainty
- **Assume causation** - Events near change points suggest but don't prove causality
- **Ignore limitations** - Every model has weaknesses
- **Use alone for decisions** - Combine with other analyses and expertise
- **Extrapolate to future** - Historical change points don't predict new ones

---

## Questions to Ask When Reviewing Results

1. **How certain are we?** 
   - Check the confidence interval width
   - Smaller = better

2. **Does this make business sense?**
   - Do the detected dates align with known market events?
   - Does the direction of change (up/down, more/less volatile) match expectations?

3. **How big was the impact?**
   - Is the volatility change meaningful (>10%)?
   - Is the return shift practically significant?

4. **What events are nearby?**
   - Are they plausible drivers?
   - Do we see multiple events or a single clear trigger?

5. **What's missing?**
   - Are there known events that weren't detected?
   - Could data quality issues explain unexpected results?

---

## Getting Help

**If results seem unexpected:**
1. Review the data validation report
2. Check for missing data or outliers
3. Consider running sensitivity analysis with different parameters
4. Consult with the analytics team

**For questions about:**
- **Methodology**: See `docs/analysis_workflow.md`
- **Technical details**: See `docs/assumptions_and_limitations.md`
- **Data sources**: See `data/README.md`

---

## Example Use Cases

### Investment Strategy
**Question:** "When did market conditions fundamentally change?"  
**Output Used:** Change point dates + volatility shifts  
**Action:** Adjust portfolio risk models for different market regimes

### Policy Analysis
**Question:** "What impact did the sanctions have on oil markets?"  
**Output Used:** Event associations + parameter shifts  
**Action:** Quantify policy effectiveness and market response

### Risk Management
**Question:** "How has market volatility evolved over time?"  
**Output Used:** Before/after volatility comparison  
**Action:** Update hedging strategies and VaR models

### Market Research
**Question:** "What drives oil price regime changes?"  
**Output Used:** Change points + associated events + impact statements  
**Action:** Build qualitative narratives backed by quantitative evidence

---

## Revision History

| Version | Date        | Changes                   |
| ------- | ----------- | ------------------------- |
| 1.0     | Feb 8, 2026 | Initial document creation |

---

**For technical documentation, see:**
- `docs/assumptions_and_limitations.md` - Technical assumptions
- `docs/analysis_workflow.md` - Complete methodology
- `docs/project-overview.md` - Project context and goals
