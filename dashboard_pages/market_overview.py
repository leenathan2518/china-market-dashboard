"""
Market Overview Page

Author: Vinci Lee

Description
-----------
This page provides a high-level overview of China's A-share market.

Main features:
1. Historical index performance
2. Key market performance indicators
3. Real-time A-share market snapshot

Data sources:
1. BaoStock for historical index data
2. AKShare Sina interface for real-time A-share data
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import get_index_data, get_realtime_data
from datetime import datetime, timedelta


def show():
    """
    Render the Market Overview page.

    This function is called by main.py when the user selects
    'Market Overview' from the sidebar navigation.
    """

    # --------------------------------------------------
    # Page Header
    # --------------------------------------------------

    st.title("China A-Share Market Dashboard")
    st.caption(
        "Historical index data from BaoStock; "
        "real-time stock data from AKShare Sina interface."
    )

    # --------------------------------------------------
    # Index Selection
    # --------------------------------------------------

    # Major Chinese stock market indices used in this dashboard
    index_map = {
        "Shanghai Composite": "sh.000001",
        "Shenzhen Component": "sz.399001",
        "CSI 300": "sh.000300",
        "ChiNext Index": "sz.399006",
    }

    st.sidebar.header("Market Overview Controls")

    # User selects which index to display
    selected_index = st.sidebar.selectbox(
        "Select Index",
        list(index_map.keys())
    )

    # Default date range:
    # Recent 120 calendar days
    # This avoids problems for newly listed stocks

    today = datetime.today()

    default_start = today - timedelta(days=120)

    start_date = st.sidebar.date_input(
        "Start Date",
        default_start
    )

    end_date = st.sidebar.date_input(
        "End Date",
        today
    )

    # --------------------------------------------------
    # Historical Index Data
    # --------------------------------------------------

    # Download selected index data from BaoStock
    df_index = get_index_data(
        index_map[selected_index],
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )

    # Latest closing price in the selected period
    latest_close = df_index["close"].iloc[-1]

    # First closing price in the selected period
    first_close = df_index["close"].iloc[0]

    # Calculate percentage return over the selected period
    period_return = (latest_close / first_close - 1) * 100

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("Latest Close", f"{latest_close:,.2f}")
    col2.metric("Period Return", f"{period_return:.2f}%")
    col3.metric("Trading Days", len(df_index))

    # --------------------------------------------------
    # Index Trend Chart
    # --------------------------------------------------

    # Create a line chart for the selected index closing price
    fig = px.line(
        df_index,
        x="date",
        y="close",
        title=f"{selected_index} Closing Price"
    )

    st.plotly_chart(fig, width="stretch")

    # --------------------------------------------------
    # Real-time Market Snapshot
    # --------------------------------------------------

    st.subheader("Real-time A-share Market Snapshot")

    # Load real-time A-share data from AKShare Sina interface
    df_realtime = get_realtime_data()

    # Display only the first 20 rows for the first version
    st.dataframe(df_realtime.head(20), width="stretch")

