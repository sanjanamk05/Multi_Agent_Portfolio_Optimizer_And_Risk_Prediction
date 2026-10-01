# Multi-Agent Portfolio Optimizer

A Python-based portfolio optimization project that combines financial data processing, machine learning, and an interactive Streamlit dashboard. The system evaluates a small basket of technology stocks, computes technical indicators, estimates risk, and recommends allocations for a portfolio.

## Overview

This project is designed to help users explore how multiple AI agents can work together in a portfolio workflow:

- Data Agent: downloads and preprocesses market data
- Risk Agent: trains a predictive risk model using technical indicators
- Portfolio Agent: calculates portfolio allocations
- RL Agent: provides reinforcement-learning based experimentation for trading decisions
- Dashboard: visualizes strategy inputs and portfolio outputs in Streamlit

The current stock universe is:

- AAPL
- TSLA
- AMZN
- GOOGL

## Key Features

- Historical market data collection from Yahoo Finance
- Technical indicator generation including moving averages, RSI, MACD, ATR, and Bollinger Bands
- Risk estimation using Random Forest regression
- Allocation logic and CSV export of portfolio recommendations
- Streamlit dashboard for interactive portfolio analysis
- Saved outputs for processed datasets, reports, and model artifacts

## Tech Stack

- Python 3.10+
- pandas, NumPy, scikit-learn
- yfinance
- matplotlib, seaborn, plotly
- stable-baselines3 and gymnasium
- Streamlit

See [requirements.txt](requirements.txt) for the complete dependency list.

## Project Structure

```text
majorproj/
├── agents/
│   ├── data_agent.py
│   ├── portfolio_agent.py
│   ├── risk_agent.py
│   └── rl_agent.py
├── config/
│   └── config.py
├── data/
│   ├── processed/
│   └── raw/
├── datasets/
│   ├── csv_exports/
│   └── saved_datasets/
├── demo_results/
├── docs/
│   └── class_diagram.md
├── models/
│   └── trained_models/
├── reports/
├── dashboard.py
├── test.py
├── requirements.txt
├── README.md
└── utils/
```

## Installation

1. Open a terminal in the project root.
2. Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

On macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Data Pipeline

The data preprocessing pipeline is implemented in [data/data_loader.py](data/data_loader.py). It performs the following steps:

1. Downloads historical stock market data from Yahoo Finance
2. Saves raw CSV files in [data/raw](data/raw)
3. Cleans and normalizes the data
4. Computes technical indicators
5. Saves processed data to [data/processed](data/processed)

To run the pipeline manually:

```bash
python data/data_loader.py
```

## Running the App

Launch the dashboard with:

```bash
streamlit run dashboard.py
```

This starts the interactive portfolio dashboard with sidebar controls for:

- investment amount
- risk tolerance
- rebalance frequency
- minimum and maximum stock allocation
- technical analysis toggle

## Running Agent Workflows

You can also execute the individual agents directly:

```bash
python agents/portfolio_agent.py
python agents/risk_agent.py
```

These scripts generate model artifacts and portfolio outputs that are saved in the configured folders.

## Configuration

Most project settings are defined in [config/config.py](config/config.py). This includes:

- selected stock list
- investment amount
- data date range
- risk model parameters
- portfolio optimization thresholds
- file paths for datasets and reports

Edit this file if you want to change:

- the stock universe
- the time window for your analysis
- the default risk profile
- model hyperparameters

## Outputs

The project creates a set of generated artifacts:

- Raw data: [data/raw](data/raw)
- Processed datasets: [data/processed](data/processed)
- Portfolio exports: [datasets/csv_exports](datasets/csv_exports)
- Trained models: [models/trained_models](models/trained_models)
- Reports: [reports](reports)
- Demo results and visualizations: [demo_results](demo_results)

## Quick Validation

A quick environment check can be run with:

```bash
python test.py
```

This verifies that the main scientific and ML libraries are available before you begin analysis or dashboard work.

## Notes

- The project is intended for research, experimentation, and learning rather than live trading execution.
- Financial data access depends on the Yahoo Finance service and may be affected by provider availability or rate limits.
- Some agent functionality may require generated CSV files before running downstream analysis.

## Recommended Workflow

1. Install dependencies
2. Run [data/data_loader.py](data/data_loader.py) to fetch and preprocess market data
3. Run the risk and portfolio agents
4. Launch the dashboard with Streamlit
5. Review generated reports and exported allocations

## Related Documentation

- [docs/class_diagram.md](docs/class_diagram.md) contains a class-level system overview
- [reports](reports) stores generated analysis summaries

## License

This project is provided for educational and research purposes. Please confirm repository-specific licensing requirements before commercial use.
