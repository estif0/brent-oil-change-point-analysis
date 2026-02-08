# Brent Oil Change Point Analysis

A Bayesian statistical analysis framework for detecting and analyzing structural breaks in Brent crude oil prices, identifying how major geopolitical events, OPEC decisions, and economic shocks impact global oil markets.

**Analysis Period**: May 1987 - September 2022  
**Methodology**: Bayesian Change Point Detection with MCMC Sampling

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Data Sources](#data-sources)
- [Documentation](#documentation)
- [Testing](#testing)
- [Dashboard](#dashboard)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project provides data-driven insights into historical Brent oil price changes to guide:
- **Investment strategies** for energy sector stakeholders
- **Policy development** for government agencies
- **Operational planning** for energy companies

Using Bayesian change point detection, we identify structural breaks in oil prices and quantify their relationship with major world events including wars, financial crises, OPEC decisions, and economic shocks.

### Business Objectives

- Analyze how political and economic events affect Brent oil prices
- Quantify the magnitude and direction of price changes at structural breaks
- Associate change points with specific historical events
- Provide probabilistic uncertainty estimates using Bayesian inference
- Deliver insights through an interactive web dashboard

---

## ✨ Key Features

### Analysis Capabilities
- **Bayesian Change Point Detection**: Probabilistic identification of structural breaks
- **Event Association**: Links detected change points to geopolitical events, OPEC decisions, and economic shocks
- **Impact Quantification**: Measures price shifts with credible intervals
- **Stationarity Testing**: ADF and KPSS tests for time series properties
- **Volatility Analysis**: Rolling statistics and variance assessment
- **MCMC Diagnostics**: Comprehensive convergence checks (R-hat, ESS, trace plots)

### Engineering Features
- **Modular OOP Design**: Clean, maintainable, and extensible codebase
- **Comprehensive Testing**: 219+ unit tests with pytest
- **Type Safety**: Full type hints for better IDE support and error detection
- **Production Ready**: Error handling, logging, and validation throughout
- **Documentation**: Extensive docstrings and user guides

---

## 📁 Project Structure

```
brent-oil-change-point-analysis/
├── src/                          # Core Python modules (OOP, documented, tested)
│   ├── data/                     # Data loading and validation
│   │   ├── loader.py            # BrentDataLoader class
│   │   └── event_loader.py      # EventDataLoader class
│   ├── eda/                      # Exploratory data analysis
│   │   └── time_series_analysis.py  # TimeSeriesAnalyzer class
│   ├── statistical_tests/        # Statistical testing
│   │   └── stationarity.py      # StationarityTester class
│   ├── models/                   # Bayesian models
│   │   ├── bayesian_changepoint.py  # BayesianChangePointModel class
│   │   └── diagnostics.py       # ModelDiagnostics class
│   ├── analysis/                 # Change point analysis
│   │   └── changepoint_analyzer.py  # ChangePointAnalyzer class
│   └── visualization/            # Plotting utilities
│       └── plots.py             # Visualization functions
│
├── tests/                        # Unit tests (mirrors src/ structure)
│   ├── test_data_loader.py
│   ├── test_event_loader.py
│   ├── test_time_series_analysis.py
│   ├── test_stationarity.py
│   ├── test_bayesian_changepoint.py
│   ├── test_diagnostics.py
│   ├── test_changepoint_analyzer.py
│   └── test_plots.py
│
├── notebooks/                    # Jupyter notebooks for analysis
│   ├── 01_exploratory_data_analysis.ipynb
│   └── 02_bayesian_changepoint_modeling.ipynb
│
├── data/                         # Data files (gitignored)
│   ├── raw/
│   │   └── BrentOilPrices.csv   # Historical Brent oil prices
│   ├── events.csv               # Curated event dataset (17 events)
│   └── processed/               # Processed data outputs
│
├── docs/                         # Documentation
│   ├── project-overview.md      # High-level project description
│   ├── steps.md                 # Task tracking and milestones
│   ├── analysis_workflow.md     # Detailed analysis workflow
│   ├── assumptions_and_limitations.md  # Critical assumptions
│   ├── communication_channels.md  # Stakeholder communication guide
│   ├── interim-code-eval.md     # Interim evaluation criteria
│   └── final-code-eval.md       # Final evaluation criteria
│
├── reports/                      # Analysis outputs
│   ├── figures/                 # Saved visualizations
│   ├── interim/                 # Interim submission materials
│   └── final/                   # Final submission materials
│
├── dashboard/                    # Web dashboard (Task 3)
│   ├── backend/                 # Flask API
│   └── frontend/                # React + TypeScript app
│
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
└── README.md                    # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.9+ (recommended: 3.10 or 3.11)
- pip or conda package manager
- Git

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd brent-oil-change-point-analysis
```

### Step 2: Create Virtual Environment

**Using venv:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Using conda:**
```bash
conda create -n brent-analysis python=3.10
conda activate brent-analysis
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
# Run tests to ensure everything is working
pytest tests/ -v

# Should see: 219 passed
```

---

## ⚡ Quick Start

### 1. Load and Explore Data

```python
from src.data import BrentDataLoader, EventDataLoader

# Load Brent oil price data
loader = BrentDataLoader()
data = loader.load_data('data/raw/BrentOilPrices.csv')
print(f"Loaded {len(data)} price observations")

# Validate data
validation = loader.validate_data()
if validation['is_valid']:
    print("✓ Data validation passed")
    
# Load events
event_loader = EventDataLoader()
events = event_loader.load_events('data/events.csv')
print(f"Loaded {len(events)} historical events")
```

### 2. Perform EDA and Stationarity Tests

```python
from src.eda import TimeSeriesAnalyzer
from src.statistical_tests import StationarityTester

# Time series analysis
analyzer = TimeSeriesAnalyzer(data)
log_returns = analyzer.calculate_log_returns()

# Test stationarity
tester = StationarityTester()
adf_result = tester.adf_test(log_returns)
kpss_result = tester.kpss_test(log_returns)
interpretation = tester.interpret_results(adf_result, kpss_result)
print(interpretation)
```

### 3. Build and Fit Bayesian Change Point Model

```python
from src.models import BayesianChangePointModel

# Create model
model = BayesianChangePointModel(log_returns, name="brent_changepoint")
model.build_model(min_segment_length=30, prior_std_scale=2.0)

# Fit using MCMC
trace = model.fit(samples=2000, tune=1000, chains=2, random_seed=42)

# Get change point estimate
changepoint = model.get_changepoint_estimate(method='mean')
print(f"Change point detected on: {changepoint['date']}")
print(f"Credible interval: {changepoint['hdi_lower']} to {changepoint['hdi_upper']}")
```

### 4. Analyze Change Points and Associate with Events

```python
from src.analysis import ChangePointAnalyzer

# Create analyzer
cp_analyzer = ChangePointAnalyzer()

# Perform batch analysis
results = cp_analyzer.batch_analyze(
    model=model,
    trace=trace,
    data=data,
    events=events,
    window_days=30
)

# Generate impact statement
for cp in results['changepoints']:
    statement = cp_analyzer.generate_impact_statement(
        changepoint=cp,
        impact=cp['impact'],
        association=cp['event_association']
    )
    print(statement)
```

### 5. Run Jupyter Notebooks

The project includes two comprehensive notebooks:

```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
jupyter notebook notebooks/02_bayesian_changepoint_modeling.ipynb
```

---

## 📊 Usage

### Running the Full Analysis Pipeline

For a complete analysis workflow, see [docs/analysis_workflow.md](docs/analysis_workflow.md).

**Key Steps:**
1. **Data Loading**: Load price and event data
2. **EDA**: Explore trends, calculate returns, analyze volatility
3. **Statistical Testing**: Test stationarity, identify properties
4. **Bayesian Modeling**: Build and fit change point model
5. **Analysis**: Identify change points, quantify impact, associate with events
6. **Reporting**: Generate visualizations and impact statements

### Command Line Usage

Run tests:
```bash
pytest tests/                          # Run all tests
pytest tests/test_data_loader.py -v   # Run specific test file
pytest tests/ --cov=src                # With coverage report
```

### Using Individual Modules

Each module in `src/` can be used independently. See README files in each module directory:
- [src/data/README.md](src/data/README.md)
- [src/eda/README.md](src/eda/README.md)
- [src/models/README.md](src/models/README.md)
- [src/analysis/README.md](src/analysis/README.md)

---

## 📈 Data Sources

### Brent Oil Prices
- **File**: `data/raw/BrentOilPrices.csv`
- **Period**: May 20, 1987 - September 30, 2022
- **Frequency**: Daily
- **Source**: U.S. Energy Information Administration (EIA)
- **Format**: CSV with columns: Date, Price

### Event Data
- **File**: `data/events.csv`
- **Events**: 17 major geopolitical events, OPEC decisions, and economic shocks
- **Period**: 1990-2022
- **Format**: CSV with columns: date, event_name, event_type, description, expected_impact

**Event Types:**
- `geopolitical`: Wars, conflicts, political instability
- `opec_decision`: Production quotas, policy changes
- `economic_shock`: Financial crises, disasters
- `sanction`: Trade restrictions, embargoes

**Sample Events:**
- Iraq Invasion of Kuwait (1990)
- Asian Financial Crisis (1997)
- 9/11 Attacks (2001)
- Global Financial Crisis (2008)
- Arab Spring (2010)
- COVID-19 Pandemic (2020)
- Russia Invades Ukraine (2022)

---

## 📚 Documentation

### Core Documentation
- **[Project Overview](docs/project-overview.md)**: Business objectives and scope
- **[Analysis Workflow](docs/analysis_workflow.md)**: Detailed step-by-step analysis guide (481 lines)
- **[Assumptions & Limitations](docs/assumptions_and_limitations.md)**: Critical assumptions and methodological constraints (412 lines)
- **[Communication Channels](docs/communication_channels.md)**: Guide for presenting results to stakeholders
- **[Steps](docs/steps.md)**: Task tracking and project milestones

### Evaluation Criteria
- **[Interim Code Evaluation](docs/interim-code-eval.md)**: Criteria for interim submission
- **[Final Code Evaluation](docs/final-code-eval.md)**: Criteria for final submission

### Technical Documentation
- All classes and functions have comprehensive docstrings
- Type hints throughout codebase
- Module-level README files in `src/` subdirectories

---

## 🧪 Testing

The project has **219+ unit tests** with comprehensive coverage.

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Categories
```bash
pytest tests/test_data_loader.py          # Data loading tests
pytest tests/test_bayesian_changepoint.py # Bayesian model tests
pytest tests/test_changepoint_analyzer.py # Analysis tests
```

### Coverage Report
```bash
pytest tests/ --cov=src --cov-report=html
# Open htmlcov/index.html to view coverage
```

### Test Structure
Tests mirror the `src/` structure and cover:
- ✓ Valid input scenarios
- ✓ Edge cases (empty data, missing values, etc.)
- ✓ Error handling and validation
- ✓ Integration workflows

---

## 🎨 Dashboard

An interactive web dashboard for exploring change points and events (Task 3).

### Architecture
- **Backend**: Flask + Flask-CORS + Flask-RESTful
- **Frontend**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Charts**: Recharts

### Running the Dashboard

**Backend:**
```bash
cd dashboard/backend
pip install -r requirements.txt
python app.py
# API runs on http://localhost:5000
```

**Frontend:**
```bash
cd dashboard/frontend
npm install
npm run dev
# App runs on http://localhost:5173
```

**Features:**
- Interactive price charts with change points
- Event timeline and filtering
- Impact quantification display
- Responsive design (desktop, tablet, mobile)

---

## 🤝 Contributing

### Code Quality Standards

1. **Modularity**: Use OOP with clear class responsibilities
2. **Documentation**: Comprehensive docstrings for all classes and methods
3. **Testing**: Write tests for all new functionality
4. **Type Hints**: Use type annotations for function signatures
5. **Error Handling**: Graceful handling with informative error messages
6. **Style**: Follow PEP 8 guidelines

### Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes with clear, focused commits
3. Add tests for new functionality
4. Ensure all tests pass: `pytest tests/`
5. Update documentation as needed
6. Submit a pull request

---

## 🙏 Acknowledgments

- **Client**: Birhan Energies
- **Data Source**: U.S. Energy Information Administration (EIA)
- **Methodology**: Bayesian change point detection using PyMC
- **Evaluation Framework**: 10 Academy curriculum guidelines

---

## 📄 License

This project is developed as part of an academic/consulting engagement for Birhan Energies.

---

## 📧 Contact

For questions or support:
- Check [docs/](docs/) for detailed documentation
- Review [assumptions_and_limitations.md](docs/assumptions_and_limitations.md) for methodology constraints
- See [communication_channels.md](docs/communication_channels.md) for stakeholder communication guidelines

---

**Last Updated**: February 8, 2026  
**Version**: 1.0  
**Status**: Interim Submission Complete
