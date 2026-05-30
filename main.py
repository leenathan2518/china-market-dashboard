"""
China Market Dashboard

Author: Vinci Lee

Description
-----------
Main application entry point.

This file is responsible for:
1. Streamlit page configuration
2. Sidebar navigation
3. Page routing

Business logic, data loading, and chart generation should be placed
in dedicated files under the dashboard_pages/ and utils/ directories.

Current modules:
1. Market Overview
2. Cash Flow Assets
3. Core Semiconductor
4. Semiconductor Ecosystem
5. Smart Money Tracker

Future development:
1. Capital Flow Analysis
2. Sector Rotation
3. Risk Metrics
4. Factor Analysis
5. Forecasting Models
"""

import streamlit as st

# Import dashboard dashboard_pages
from dashboard_pages import market_overview
from dashboard_pages import cashflow_assets
from dashboard_pages import core_semiconductor
from dashboard_pages import semiconductor_ecosystem
from dashboard_pages import smart_money
from dashboard_pages import sector_rotation


# --------------------------------------------------
# Application Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="China Market Dashboard",
    layout="wide"
)


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

st.sidebar.title("Navigation")

# Select which dashboard page to display
page = st.sidebar.radio(
    "Select Page",
    [
        "Market Overview",
        "Cash Flow Assets",
        "Core Semiconductor",
        "Semiconductor Ecosystem",
        "Smart Money Tracker",
        "Sector Rotation",

    ]
)


# --------------------------------------------------
# Page Routing
# --------------------------------------------------

# Render selected page
if page == "Market Overview":
    market_overview.show()

# Placeholder dashboard_pages for future development
elif page == "Cash Flow Assets":
    cashflow_assets.show()

elif page == "Core Semiconductor":
    core_semiconductor.show()

elif page == "Semiconductor Ecosystem":
    semiconductor_ecosystem.show()

elif page == "Smart Money Tracker":
    smart_money.show()

elif page == "Sector Rotation":
    sector_rotation.show()






