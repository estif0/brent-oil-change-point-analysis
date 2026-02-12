# Brent Oil Change Point Analysis

A comprehensive data analysis project using Bayesian methods to identify and quantify how major geopolitical events, OPEC decisions, and economic shocks impact Brent crude oil prices. Built for **Birhan Energies** to provide data-driven insights for energy sector stakeholders.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![React](https://img.shields.io/badge/React-19.2.0-blue.svg)
![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue.svg)

## 📋 Project Overview

This project analyzes **35 years** of Brent oil price data (May 1987 - September 2022) using **Bayesian change point detection** to identify significant structural breaks and correlate them with **17 major historical events**.

### Key Features

- ✅ **Bayesian Change Point Detection** using PyMC for probabilistic modeling
- ✅ **Event Correlation Analysis** linking price changes to geopolitical events
- ✅ **Quantitative Impact Assessment** with before/after statistics
- ✅ **Interactive Dashboard** built with React + TypeScript + Tailwind CSS
- ✅ **RESTful API** with 16 endpoints serving data and analysis results
- ✅ **Comprehensive Documentation** including methodology and assumptions

### Dataset Summary

- **Price Records:** 9,154 daily observations
- **Date Range:** May 20, 1987 - September 30, 2022 (35+ years)
- **Events Tracked:** 17 major events across 4 categories
- **Change Points Detected:** 1 high-confidence change point (94%)

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8+
- **Node.js** 18+
- **pnpm** 10+ (or npm/yarn)
- **Git**

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd brent-oil-change-point-analysis

# Install Python dependencies
pip install -r requirements.txt

# Setup backend
cd dashboard/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py &  # Runs on http://localhost:5000

# Setup frontend
cd ../frontend
pnpm install
pnpm run dev  # Runs on http://localhost:5173
```

### Access the Dashboard

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Documentation:** http://localhost:5000/api/docs

## 📊 Key Findings

### Detected Change Point

**Date:** July 14, 2008  
**Confidence:** 94%  
**Impact:** Average daily price decreased from $68.45 to $51.23 (-25.16%)

**Associated Event:** 2008 Financial Crisis (September 15, 2008)  
The change point occurred approximately 2 months before the Lehman Brothers collapse, suggesting market anticipation of the crisis.

### Event Categories

| Category | Count | Examples |
|----------|-------|----------|
| **Geopolitical** | 6 | Gulf War, Iraq Invasion, Libya Crisis |
| **OPEC Decisions** | 5 | Production cuts, quota changes |
| **Economic Shocks** | 4 | 2008 Financial Crisis, COVID-19 |
| **Sanctions** | 2 | Iran sanctions, Russia sanctions |

## 🏗️ Project Structure

```
brent-oil-change-point-analysis/
├── src/                           # Core Python modules (OOP, modular)
│   ├── data/                     # Data loading and validation
│   ├── eda/                      # Exploratory data analysis
│   ├── statistical_tests/        # Stationarity tests
│   ├── models/                   # Bayesian change point models
│   ├── analysis/                 # Change point analysis
│   └── visualization/            # Plotting utilities
├── tests/                         # Unit tests for all modules
├── notebooks/                     # Jupyter notebooks
│   ├── 01_exploratory_data_analysis.ipynb
│   └── 02_bayesian_changepoint_modeling.ipynb
├── data/                          # Data files
│   ├── raw/BrentOilPrices.csv   # Historical prices
│   └── events.csv                # Event data
├── dashboard/                     # Full-stack dashboard
│   ├── backend/                  # Flask REST API
│   └── frontend/                 # React + TypeScript UI
├── docs/                          # Documentation
│   ├── analysis_workflow.md      # Analysis methodology
│   ├── assumptions_and_limitations.md
│   └── final-code-eval.md        # Evaluation criteria
└── reports/                       # Analysis outputs
    ├── figures/                   # Saved visualizations
    └── changepoints_processed.csv # Detected change points
```

## 📚 Documentation

### Core Documentation

- **[Analysis Workflow](docs/public/analysis_workflow.md)** - Step-by-step analysis process
- **[Assumptions & Limitations](docs/public/assumptions_and_limitations.md)** - Project constraints
- **[Model Outputs & Limitations](docs/public/model_outputs_and_limitations.md)** - Model capabilities

### Technical Documentation

- **[Backend API README](dashboard/backend/README.md)** - API documentation and setup
- **[Frontend README](dashboard/frontend/README.md)** - Dashboard setup and features
- **[Project Steps](docs/steps.md)** - Implementation progress tracker

### Notebooks

- **[01_exploratory_data_analysis.ipynb](notebooks/01_exploratory_data_analysis.ipynb)** - EDA, stationarity tests, volatility
- **[02_bayesian_changepoint_modeling.ipynb](notebooks/02_bayesian_changepoint_modeling.ipynb)** - Bayesian modeling, MCMC, results

## 🔬 Methodology

### 1. Data Preparation

- Load and validate Brent oil price data (9,154 records)
- Calculate log returns for stationarity
- Test for stationarity using ADF and KPSS tests
- Analyze volatility patterns

### 2. Bayesian Change Point Modeling

Using **PyMC**, we built a single change point model:

```python
# Prior: Change point location (uniform distribution)
τ ~ DiscreteUniform(0, T)

# Parameters: Before and after means
μ₁, μ₂ ~ Normal(μ_prior, σ_prior)

# Likelihood: Price observations
y ~ Normal(μ(t), σ)
```

Where `μ(t) = μ₁ if t < τ else μ₂`

### 3. MCMC Sampling

- **Sampler:** NUTS (No-U-Turn Sampler)
- **Chains:** 4
- **Draws:** 2,000
- **Tuning:** 1,000
- **Convergence:** R-hat < 1.01 for all parameters

### 4. Change Point Identification

- Analyze posterior distribution of τ
- Extract highest probability change point
- Calculate confidence level
- Associate with nearby events (±60 days)

### 5. Impact Quantification

- Calculate before/after price statistics
- Compute absolute and percentage changes
- Analyze volatility shifts
- Generate impact statements

## 🖥️ Dashboard Features

### Main Dashboard (/)

- Overview stats cards (date range, change points, events, API health)
- Interactive price chart with Recharts
- Date range filtering
- Event type filtering
- Toggle change point and event markers
- Change point cards with confidence
- Event preview cards

### Detailed Analysis (/analysis)

- Select change point for deep dive
- Before/after statistics comparison
- Price trend chart with 90-day window
- Related events within 60 days
- Quantitative impact statement

### Event Explorer (/events)

- Browse all 17 historical events
- Full-text search across names and descriptions
- Filter by event type
- Sort by date or name
- Event cards with detailed information

### About (/about)

- Project overview and business context
- Bayesian methodology explanation
- Data sources and quality
- Technology stack details
- Assumptions and limitations

## 🧪 Testing

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Module Tests

```bash
pytest tests/test_bayesian_changepoint.py -v
pytest tests/test_data_loader.py -v
pytest tests/test_changepoint_analyzer.py -v
```

### Check Coverage

```bash
pytest --cov=src tests/
```

## 🛠️ Technology Stack

### Data Analysis

- **Python 3.x** - Core language
- **PyMC** - Bayesian modeling and MCMC sampling
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Visualization
- **seaborn** - Statistical visualization
- **arviz** - Bayesian diagnostics

### Backend

- **Flask 3.0.0** - Web framework
- **Flask-RESTful** - REST API
- **Flask-CORS** - Cross-origin requests
- **flask-swagger-ui** - API documentation

### Frontend

- **React 19.2.0** - UI framework
- **TypeScript 5.9.3** - Type safety
- **Vite 7.3.1** - Build tool
- **Tailwind CSS 4.1.18** - Styling
- **Recharts 3.7.0** - Charts
- **React Router DOM 7.13.0** - Routing
- **Axios 1.13.5** - HTTP client

### Development Tools

- **pytest** - Python testing
- **Git** - Version control
- **pnpm** - Package manager

## 📈 Results

### Change Point Detection

**Change Point Date:** 2008-07-14  
**Detection Confidence:** 94%

**Price Impact:**
- **Before (90 days):** $68.45 average
- **After (90 days):** $51.23 average
- **Absolute Change:** -$17.22
- **Percentage Change:** -25.16%

**Related Event:** 2008 Financial Crisis (September 15, 2008)

### Statistical Validation

- **ADF Test:** p-value < 0.05 (stationary after differencing)
- **KPSS Test:** p-value > 0.05 (stationary)
- **R-hat Values:** < 1.01 (excellent convergence)
- **Effective Sample Size:** > 4,000 (reliable estimates)

## 🎯 Business Impact

### For Investors

- **Risk Assessment:** Identify periods of high volatility around major events
- **Portfolio Strategy:** Historical patterns inform hedging decisions
- **Market Timing:** Anticipate price movements based on event types

### For Policy Makers

- **Impact Evaluation:** Quantify effects of geopolitical decisions
- **Strategic Planning:** Understand oil market sensitivities
- **Economic Forecasting:** Model price scenarios

### For Energy Companies

- **Operational Planning:** Adjust production based on market forecasts
- **Price Negotiation:** Data-driven contract pricing
- **Market Intelligence:** Track event-driven price changes

## ⚠️ Assumptions & Limitations

### Assumptions

1. **Data Quality:** Historical price data is accurate and complete
2. **Event Dating:** Event dates represent actual market impact timing
3. **Single Change Point:** Model assumes one major structural break
4. **Normal Distribution:** Price returns follow normal distribution

### Limitations

1. **Correlation ≠ Causation:** Analysis shows temporal correlations, not definitive causal relationships
2. **Model Simplicity:** Single change point model may miss complex multi-phase shifts
3. **Event Attribution:** Multiple factors often influence prices simultaneously
4. **Temporal Window:** Fixed 60-day window may miss delayed or anticipatory effects

## 🤝 Contributing

### Code Quality Standards

- **Modularity:** Use classes and single-responsibility modules
- **Documentation:** Comprehensive docstrings for all functions/classes
- **Type Hints:** Use Python type hints and TypeScript types
- **Testing:** Unit tests for all new features
- **Git Commits:** Meaningful commit messages

### Development Workflow

1. Create a feature branch
2. Implement changes with tests
3. Update documentation
4. Submit pull request
5. Code review and merge

## 📝 License

This project was developed for Birhan Energies as part of the 10 Academy Week 10 challenge.

## 👥 Authors

10 Academy Students - Week 10 Challenge

## 📧 Contact

For questions or support:
- Review the documentation in `/docs`
- Check the About page in the dashboard
- Consult the API documentation at `/api/docs`

## 🙏 Acknowledgments

- **Birhan Energies** for project sponsorship and business context
- **10 Academy** for training and mentorship
- **Energy Data Sources** for historical price data
- **Open Source Community** for excellent tools (PyMC, Flask, React)

---

**Dashboard:** http://localhost:5173  
**API:** http://localhost:5000  
**Documentation:** http://localhost:5000/api/docs

**© 2026 Brent Oil Change Point Analysis Project**
