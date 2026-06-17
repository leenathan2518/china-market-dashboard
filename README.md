# China A-Share Market Dashboard

An interactive Streamlit dashboard for monitoring China's A-share market across major indices, selected sector groups, individual stock performance, capital-flow signals, and sector rotation.

This project was built as a lightweight market analytics platform for combining Chinese financial data sources with Python-based dashboarding. It focuses on market structure, sector comparison, and fund-flow observation rather than single-company valuation.

## Project Overview

The dashboard provides a multi-page interface for analysing China's A-share market from several perspectives:

- Broad market index performance
- Real-time A-share market snapshot
- Custom sector analysis for cash-flow assets and semiconductor-related companies
- Individual stock return and volatility comparison
- Smart-money / capital-flow tracking
- Sector rotation and risk-return comparison

The project is designed for portfolio demonstration, market research practice, and financial data workflow development using public data interfaces.

## Key Features

### 1. Market Overview

- Tracks major Chinese stock indices, including:
  - Shanghai Composite
  - Shenzhen Component
  - CSI 300
  - ChiNext Index
- Allows users to select a custom date range.
- Displays key indicators such as latest close, period return, and number of trading days.
- Provides a real-time A-share market snapshot using AKShare's Sina Finance interface.

### 2. Cash Flow Assets

- Analyses selected A-share companies with relatively stable cash-flow characteristics.
- Covers sectors such as banking, insurance, utilities, energy, telecom, and large state-owned assets.
- Compares selected stocks by period return, annualized volatility, and normalized price performance.

### 3. Core Semiconductor

- Tracks selected core semiconductor companies in China's A-share market.
- Covers companies related to chip manufacturing, semiconductor equipment, chip design, EDA software, and AI chips.
- Provides return ranking and normalized price comparison across selected semiconductor names.

### 4. Semiconductor Ecosystem

- Extends the semiconductor analysis to related upstream and downstream companies.
- Includes companies linked to AI computing, data centers, PCB, optical modules, and computing infrastructure.
- Helps compare direct semiconductor exposure with broader semiconductor ecosystem exposure.

### 5. Smart Money Tracker

- Uses AKShare fund-flow data to track capital inflow and outflow among individual A-share stocks.
- Displays:
  - Top capital inflow stocks
  - Top capital outflow stocks
  - Top turnover stocks
- Converts Chinese money units such as `亿` and `万` into numerical RMB values for analysis.

### 6. Sector Rotation

- Compares custom sector groups using return and risk indicators.
- Calculates:
  - Average sector return
  - Average annualized volatility
  - Number of valid stocks in each sector
- Visualizes sector performance ranking, volatility ranking, and risk-return profiles.

## Data Sources

- **BaoStock**
  - Historical index data
  - Historical A-share stock OHLCV data
- **AKShare**
  - Real-time A-share market snapshot
  - Individual stock fund-flow data
- **Local CSV files**
  - Custom sector classification table for selected A-share companies

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Plotly
- BaoStock
- AKShare
- DuckDB
- scikit-learn
- statsmodels
- openpyxl

## Project Structure

```text
china-market-dashboard/
├── main.py                         # Streamlit entry point and page router
├── requirements.txt                # Python dependencies
├── data/
│   └── sector_stocks.csv           # Custom sector-stock classification
├── dashboard_pages/
│   ├── market_overview.py          # Market overview and real-time snapshot
│   ├── cashflow_assets.py          # Cash-flow asset sector page
│   ├── core_semiconductor.py       # Core semiconductor page
│   ├── semiconductor_ecosystem.py  # Semiconductor ecosystem page
│   ├── smart_money.py              # Fund-flow tracker
│   └── sector_rotation.py          # Sector rotation comparison
└── utils/
    ├── data_loader.py              # BaoStock / AKShare data loading functions
    ├── metrics.py                  # Return and volatility calculations
    └── sector_page.py              # Reusable sector analysis page template
```

## Methodology

The dashboard uses a modular structure:

1. `main.py` defines the Streamlit layout, sidebar navigation, and page routing.
2. Each page under `dashboard_pages/` focuses on one analytical module.
3. Reusable data loading functions are stored in `utils/data_loader.py`.
4. Reusable financial calculations are stored in `utils/metrics.py`.
5. Sector pages share a common reusable rendering function from `utils/sector_page.py` to reduce duplicated code.

For historical price analysis, the dashboard calculates holding-period return and annualized volatility based on daily closing prices. For sector rotation, these indicators are aggregated across custom-defined sector groups.

## Installation

Clone the repository:

```bash
git clone https://github.com/leenathan2518/china-market-dashboard.git
cd china-market-dashboard
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS / Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run main.py
```

## Notes

- The dashboard relies on free public financial data interfaces, so data availability may vary depending on market hours, interface stability, and request frequency.
- Streamlit caching is used for selected real-time and fund-flow data to reduce repeated requests.
- This project is for market analytics and portfolio demonstration only. It is not financial advice.

## Future Improvements

- Add more sector groups and broader industry classification.
- Add technical indicators such as moving averages, RSI, and drawdown.
- Add historical capital-flow tracking and fund-flow time series.
- Add exportable analytical reports.
- Add database storage for repeated market snapshots.
- Improve error handling when public data interfaces are unavailable.
- Deploy the dashboard to Streamlit Cloud with stable demo data.

## Author

Vinci Lee
