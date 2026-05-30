"""
Reusable Sector Page Module

Author: Vinci Lee

Description
-----------
This module contains a reusable function for rendering sector analysis pages.

It avoids duplicated code across:
1. Cash Flow Assets
2. Core Semiconductor
3. Semiconductor Ecosystem
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from utils.data_loader import load_sector_stocks, get_stock_data
from utils.metrics import calculate_return, calculate_annualized_volatility


def render_sector_page(category, title, caption, start_label, end_label):
    """
    Render a reusable sector analysis page.

    Parameters
    ----------
    category : str
        Category name used in data/sector_stocks.csv.
        Example: CashFlowAssets

    title : str
        Page title displayed on the dashboard.

    caption : str
        Short page description.

    start_label : str
        Label for the start date selector.

    end_label : str
        Label for the end date selector.

    Returns
    -------
    None
    """

    # --------------------------------------------------
    # Page Header
    # --------------------------------------------------

    st.title(title)
    st.caption(caption)

    # --------------------------------------------------
    # Sidebar Controls
    # --------------------------------------------------

    st.sidebar.header(f"{title} Controls")

    # Default date range:
    # Recent 120 calendar days.
    # This avoids missing data for newly listed stocks.
    today = datetime.today()
    default_start = today - timedelta(days=120)

    start_date = st.sidebar.date_input(
        start_label,
        default_start
    )

    end_date = st.sidebar.date_input(
        end_label,
        today
    )

    # --------------------------------------------------
    # Load Stock Classification
    # --------------------------------------------------

    sector_df = load_sector_stocks()

    selected_stocks = sector_df[
        sector_df["category"] == category
    ]

    st.subheader("Selected Stocks")
    st.dataframe(selected_stocks, width="stretch")

    # --------------------------------------------------
    # Download Stock Data and Calculate Metrics
    # --------------------------------------------------

    result_list = []
    price_data_list = []

    for _, row in selected_stocks.iterrows():
        stock_code = str(row["stock_code"]).zfill(6)
        stock_name = row["stock_name"]

        # Download historical stock data
        df_stock = get_stock_data(
            stock_code,
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )

        # Skip stocks with unavailable data
        if df_stock.empty:
            continue

        start_price = df_stock["close"].iloc[0]
        end_price = df_stock["close"].iloc[-1]

        period_return = calculate_return(start_price, end_price)
        volatility = calculate_annualized_volatility(df_stock["close"])

        result_list.append({
            "stock_code": stock_code,
            "stock_name": stock_name,
            "period_return": period_return,
            "annualized_volatility": volatility,
            "trading_days": len(df_stock)
        })

        # Normalize price to 100 for comparison
        df_stock["normalized_close"] = (
            df_stock["close"] / df_stock["close"].iloc[0] * 100
        )
        df_stock["stock_name"] = stock_name

        price_data_list.append(df_stock)

    result_df = pd.DataFrame(result_list)

    if result_df.empty:
        st.warning("No data available for the selected period.")
        return

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric("Number of Stocks", len(result_df))
    col2.metric("Average Return", f"{result_df['period_return'].mean():.2f}%")
    col3.metric(
        "Average Volatility",
        f"{result_df['annualized_volatility'].mean():.2f}%"
    )

    # --------------------------------------------------
    # Performance Ranking
    # --------------------------------------------------

    st.subheader("Performance Ranking")

    result_df = result_df.sort_values(
        by="period_return",
        ascending=False
    )

    st.dataframe(result_df, width="stretch")

    fig_bar = px.bar(
        result_df,
        x="stock_name",
        y="period_return",
        title="Period Return by Stock"
    )

    st.plotly_chart(fig_bar, width="stretch")

    # --------------------------------------------------
    # Normalized Price Comparison
    # --------------------------------------------------

    st.subheader("Normalized Price Comparison")

    combined_price_df = pd.concat(price_data_list, ignore_index=True)

    fig_line = px.line(
        combined_price_df,
        x="date",
        y="normalized_close",
        color="stock_name",
        title="Normalized Price Performance"
    )

    st.plotly_chart(fig_line, width="stretch")

