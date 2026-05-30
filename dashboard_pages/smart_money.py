"""
Smart Money Tracker Page

Author: Vinci Lee

Description
-----------
This page tracks individual stock fund flow in China's A-share market.

Main features:
1. Top capital inflow stocks
2. Top capital outflow stocks
3. Top turnover stocks

Data source:
AKShare fund flow interface.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import get_individual_fund_flow


def convert_money_to_number(value):
    """
    Convert Chinese fund flow text into numeric value.

    Examples
    --------
    1.39亿 -> 139000000
    1150.70万 -> 11507000
    0.00 -> 0

    Parameters
    ----------
    value : str
        Money value text from AKShare.

    Returns
    -------
    float
        Numeric money value in RMB.
    """

    value = str(value).replace(",", "").strip()

    if value.endswith("亿"):
        return float(value.replace("亿", "")) * 100000000

    if value.endswith("万"):
        return float(value.replace("万", "")) * 10000

    try:
        return float(value)
    except ValueError:
        return 0.0


def show():
    """
    Render the Smart Money Tracker page.
    """

    st.title("Smart Money Tracker")
    st.caption(
        "This page tracks capital inflow and outflow among individual A-share stocks."
    )

    # --------------------------------------------------
    # Load Fund Flow Data
    # --------------------------------------------------

    df = get_individual_fund_flow()

    if df.empty:
        st.warning("No fund flow data available.")
        return

    # --------------------------------------------------
    # Data Cleaning
    # --------------------------------------------------

    # Convert fund flow text values into numeric RMB values
    df["net_inflow_value"] = df["净额"].apply(convert_money_to_number)
    df["turnover_value"] = df["成交额"].apply(convert_money_to_number)

    # Convert percentage text into numeric values
    df["change_pct"] = (
        df["涨跌幅"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .astype(float)
    )

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    total_net_inflow = df["net_inflow_value"].sum()
    average_change = df["change_pct"].mean()
    total_turnover = df["turnover_value"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Net Inflow", f"{total_net_inflow / 100000000:.2f} 亿")
    col2.metric("Average Change", f"{average_change:.2f}%")
    col3.metric("Total Turnover", f"{total_turnover / 100000000:.2f} 亿")

    # --------------------------------------------------
    # Capital Inflow Ranking
    # --------------------------------------------------

    st.subheader("Top 20 Capital Inflow Stocks")

    top_inflow = df.sort_values(
        by="net_inflow_value",
        ascending=False
    ).head(20)

    st.dataframe(top_inflow, width="stretch")

    fig_inflow = px.bar(
        top_inflow,
        x="股票简称",
        y="net_inflow_value",
        title="Top 20 Capital Inflow Stocks"
    )

    st.plotly_chart(fig_inflow, width="stretch")

    # --------------------------------------------------
    # Capital Outflow Ranking
    # --------------------------------------------------

    st.subheader("Top 20 Capital Outflow Stocks")

    top_outflow = df.sort_values(
        by="net_inflow_value",
        ascending=True
    ).head(20)

    st.dataframe(top_outflow, width="stretch")

    fig_outflow = px.bar(
        top_outflow,
        x="股票简称",
        y="net_inflow_value",
        title="Top 20 Capital Outflow Stocks"
    )

    st.plotly_chart(fig_outflow, width="stretch")

    # --------------------------------------------------
    # Turnover Ranking
    # --------------------------------------------------

    st.subheader("Top 20 Turnover Stocks")

    top_turnover = df.sort_values(
        by="turnover_value",
        ascending=False
    ).head(20)

    st.dataframe(top_turnover, width="stretch")

    fig_turnover = px.bar(
        top_turnover,
        x="股票简称",
        y="turnover_value",
        title="Top 20 Turnover Stocks"
    )

    st.plotly_chart(fig_turnover, width="stretch")

