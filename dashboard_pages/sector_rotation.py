"""
Sector Rotation Page

Author: Vinci Lee

Description
-----------
This page compares the performance and risk of different custom sectors.

Sectors include:
1. Cash Flow Assets
2. Core Semiconductor
3. Semiconductor Ecosystem

Main features:
1. Sector return ranking
2. Sector volatility ranking
3. Risk-return scatter plot
"""

from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_sector_stocks, get_stock_data
from utils.metrics import calculate_return, calculate_annualized_volatility


def show():
    """
    Render the Sector Rotation page.
    """

    st.title("Sector Rotation Dashboard")
    st.caption(
        "This page compares return and risk across custom A-share sector groups."
    )

    # --------------------------------------------------
    # Sidebar Controls
    # --------------------------------------------------

    st.sidebar.header("Sector Rotation Controls")

    # Default date range:
    # Recent 120 calendar days
    today = datetime.today()
    default_start = today - timedelta(days=120)

    start_date = st.sidebar.date_input(
        "Sector Rotation Start Date",
        default_start
    )

    end_date = st.sidebar.date_input(
        "Sector Rotation End Date",
        today
    )

    # --------------------------------------------------
    # Load Sector Mapping
    # --------------------------------------------------

    sector_df = load_sector_stocks()

    categories = sector_df["category"].unique()

    sector_result_list = []

    # --------------------------------------------------
    # Calculate Sector-level Metrics
    # --------------------------------------------------

    for category in categories:
        selected_stocks = sector_df[sector_df["category"] == category]

        stock_return_list = []
        stock_volatility_list = []

        for _, row in selected_stocks.iterrows():
            stock_code = str(row["stock_code"]).zfill(6)

            # Download stock historical data
            df_stock = get_stock_data(
                stock_code,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

            # Skip invalid or unavailable data
            if df_stock.empty:
                continue

            start_price = df_stock["close"].iloc[0]
            end_price = df_stock["close"].iloc[-1]

            stock_return = calculate_return(start_price, end_price)
            stock_volatility = calculate_annualized_volatility(df_stock["close"])

            stock_return_list.append(stock_return)
            stock_volatility_list.append(stock_volatility)

        # Skip sector if no valid stocks are available
        if len(stock_return_list) == 0:
            continue

        sector_result_list.append({
            "category": category,
            "average_return": sum(stock_return_list) / len(stock_return_list),
            "average_volatility": sum(stock_volatility_list) / len(stock_volatility_list),
            "number_of_stocks": len(stock_return_list)
        })

    sector_result_df = pd.DataFrame(sector_result_list)

    if sector_result_df.empty:
        st.warning("No sector data available for the selected period.")
        return

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    best_sector = sector_result_df.sort_values(
        by="average_return",
        ascending=False
    ).iloc[0]

    most_volatile_sector = sector_result_df.sort_values(
        by="average_volatility",
        ascending=False
    ).iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric("Number of Sectors", len(sector_result_df))
    col2.metric("Best Performing Sector", best_sector["category"])
    col3.metric("Most Volatile Sector", most_volatile_sector["category"])

    # --------------------------------------------------
    # Sector Return Ranking
    # --------------------------------------------------

    st.subheader("Sector Return Ranking")

    return_ranking = sector_result_df.sort_values(
        by="average_return",
        ascending=False
    )

    st.dataframe(return_ranking, width="stretch")

    fig_return = px.bar(
        return_ranking,
        x="category",
        y="average_return",
        title="Average Return by Sector"
    )

    st.plotly_chart(fig_return, width="stretch")

    # --------------------------------------------------
    # Sector Volatility Ranking
    # --------------------------------------------------

    st.subheader("Sector Volatility Ranking")

    volatility_ranking = sector_result_df.sort_values(
        by="average_volatility",
        ascending=False
    )

    fig_volatility = px.bar(
        volatility_ranking,
        x="category",
        y="average_volatility",
        title="Average Annualized Volatility by Sector"
    )

    st.plotly_chart(fig_volatility, width="stretch")

    # --------------------------------------------------
    # Risk-return Scatter Plot
    # --------------------------------------------------

    st.subheader("Risk-return Comparison")

    fig_scatter = px.scatter(
        sector_result_df,
        x="average_volatility",
        y="average_return",
        size="number_of_stocks",
        text="category",
        title="Sector Risk-return Profile"
    )

    fig_scatter.update_traces(textposition="top center")

    st.plotly_chart(fig_scatter, width="stretch")

