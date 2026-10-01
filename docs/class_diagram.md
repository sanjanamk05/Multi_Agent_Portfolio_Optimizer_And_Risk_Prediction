# Multi-Agent Portfolio Optimizer: Class Diagram

## Class and Module Structure

```mermaid
classDiagram
    class Configuration {
        <<module>>
        +STOCKS
        +INVESTMENT_AMOUNT
        +data and indicator settings
        +risk and allocation settings
        +file paths
    }

    class DataLoader {
        +stocks
        +start_date
        +end_date
        +interval
        +raw_data
        +processed_data
        +download_data()
        +save_raw_data()
        +clean_data()
        +normalize_data()
        +compute_technical_indicators()
        +save_processed_data()
        +get_data(stock)
        +get_all_data()
    }

    class DataAgent {
        +stocks
        +data
        +analysis_results
        +load_processed_data()
        +analyze_moving_averages(stock)
        +analyze_rsi(stock)
        +analyze_macd(stock)
        +calculate_price_change(stock)
        +determine_overall_trend(stock)
        +analyze_all_stocks()
        +generate_report()
        +get_analysis(stock)
        +get_all_analysis()
    }

    class RiskAgent {
        +stocks
        +data
        +models
        +risk_scores
        +load_processed_data()
        +prepare_features_and_target(stock)
        +train_risk_model(stock)
        +save_models()
        +predict_risk(stock)
        +categorize_risk(risk_score)
        +analyze_all_stocks()
        +generate_risk_report()
        +get_risk_score(stock)
        +get_all_risk_scores()
    }

    class PortfolioAgent {
        +stocks
        +investment_amount
        +data
        +returns_data
        +portfolio_allocation
        +portfolio_performance
        +load_processed_data()
        +optimize_equal_weight()
        +optimize_portfolio()
        +save_portfolio_allocation()
    }

    class RLAgent {
        +stocks
        +data
        +q_table
        +load_processed_data()
        +calculate_stock_scores()
        +optimize_allocation(scores)
        +save_allocation(allocation)
        +run_full_pipeline()
    }

    class Dashboard {
        <<Streamlit module, not a class>>
        +load_csv(filename)
        +load_market_data(stock)
        +overview page
        +market analysis page
        +risk assessment page
        +portfolio allocation page
        +agent comparison page
    }

    class ProcessedCSV {
        <<shared input artifact>>
        +one CSV per stock
        +prices and technical indicators
    }

    class RawCSV {
        <<output artifact>>
        +one CSV per stock
        +downloaded historical prices
    }

    class RiskModelFiles {
        <<output artifact>>
        +one serialized model per stock
    }

    class AllocationCSVs {
        <<output artifact>>
        +Portfolio_Allocation.csv
        +RL_Portfolio_Allocation.csv
    }

    class TextReports {
        <<output artifact>>
        +Market_Analysis_Report.txt
        +Risk_Analysis_Report.txt
    }

    Configuration ..> DataLoader : parameters and paths
    Configuration ..> DataAgent : stock list and paths
    Configuration ..> RiskAgent : stock list, model and risk settings
    Configuration ..> PortfolioAgent : stock list, amount and paths
    Configuration ..> RLAgent : stock list, amount and paths
    Configuration ..> Dashboard : stock list, amount and paths

    DataLoader ..> RawCSV : writes
    DataLoader ..> ProcessedCSV : writes
    DataAgent ..> ProcessedCSV : reads
    RiskAgent ..> ProcessedCSV : reads
    PortfolioAgent ..> ProcessedCSV : reads
    RLAgent ..> ProcessedCSV : reads
    Dashboard ..> ProcessedCSV : reads

    RiskAgent ..> RiskModelFiles : writes
    RiskAgent ..> TextReports : writes risk report
    DataAgent ..> TextReports : writes market report
    PortfolioAgent ..> AllocationCSVs : writes standard allocation
    RLAgent ..> AllocationCSVs : writes score-based allocation
    Dashboard ..> AllocationCSVs : reads
```

## Runtime Design

- `DataLoader` is the data-preparation stage. It downloads historical prices, cleans and normalizes the data, computes indicators, and persists per-stock CSV files.
- The four agents are independent consumers of the processed CSV files. There is no shared agent base class, service layer, or central orchestrator; each agent loads the files itself and can be run as a script.
- `DataAgent` calculates technical-analysis signals and can write a market report. `RiskAgent` trains a random-forest regressor per stock, predicts risk, and writes serialized models and a risk report. `PortfolioAgent` creates an equal-weight allocation. `RLAgent` uses calculated stock scores to create a proportional allocation.
- `Dashboard` is a top-level Streamlit script with helper functions and page branches, not an object-oriented view/controller. It reads processed and exported CSV files directly.
- `Configuration` is a module of constants rather than an instantiated configuration object. Components import the settings and paths they need.

## Important Implementation Notes

- `PortfolioAgent` is defined twice in `agents/portfolio_agent.py`. The later class binding replaces the earlier one; the two definitions are currently duplicates. The diagram treats them as one effective class.
- Despite its docstring and configuration values, `PortfolioAgent.optimize_portfolio()` currently performs equal weighting. `MIN_ALLOCATION`, `MAX_ALLOCATION`, `RISK_FREE_RATE`, and the portfolio performance/returns fields are not used by that implementation.
- `RLAgent` is described as Q-learning based, but `q_table` is not used for learning. The current flow calculates indicator-based scores and normalizes those scores into allocations.
- The dashboard's risk table uses hard-coded sample values, and its allocation controls calculate a display-only custom allocation. The page controls are not connected to the agent pipelines.
- `test.py` checks dependency imports and basic workspace setup; it does not define automated tests for these classes.
