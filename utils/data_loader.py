"""
Data Loading Module

Author: Vinci Lee

Description
-----------
This module contains reusable functions for loading financial data.

Data sources:
1. BaoStock
   - Used for historical index data.
2. AKShare Sina interface
   - Used for real-time A-share market snapshot.

Keeping data loading functions in this file helps avoid duplicated code
across different dashboard pages.
"""

import baostock as bs
import pandas as pd
import akshare as ak
import streamlit as st


@st.cache_data
def get_index_data(code, start_date, end_date):
    """
    Download historical index data from BaoStock.

    Parameters
    ----------
    code : str
        Index code.
        Examples:
        sh.000001 = Shanghai Composite
        sz.399001 = Shenzhen Component
        sh.000300 = CSI 300
        sz.399006 = ChiNext Index

    start_date : str
        Start date in YYYY-MM-DD format.

    end_date : str
        End date in YYYY-MM-DD format.

    Returns
    -------
    pd.DataFrame
        Historical OHLCV data, including:
        date, code, open, high, low, close, volume, amount.
    """

    # Login to BaoStock server before requesting data
    bs.login()

    # Request daily historical data from BaoStock
    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,volume,amount",
        start_date=start_date,
        end_date=end_date,
        frequency="d"
    )

    # Convert BaoStock query result into a list of rows
    data = []
    while rs.next():
        data.append(rs.get_row_data())

    # Convert raw list data into a pandas DataFrame
    df = pd.DataFrame(data, columns=rs.fields)

    # Logout from BaoStock after data download
    bs.logout()

    # Convert columns into correct data types
    df["date"] = pd.to_datetime(df["date"])
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])
    df["amount"] = pd.to_numeric(df["amount"])

    return df


@st.cache_data(ttl=300)
def get_realtime_data():
    """
    Get real-time A-share market data from AKShare Sina interface.

    Notes
    -----
    The data is cached for 300 seconds to avoid sending too many requests.
    This is important because free public data interfaces may temporarily
    block frequent requests.

    Returns
    -------
    pd.DataFrame
        Real-time A-share market snapshot.
    """

    # Request real-time A-share data from Sina Finance via AKShare
    df = ak.stock_zh_a_spot()

    return df


def load_sector_stocks():
    """
    Load custom sector stock classification from local CSV file.

    File path
    ---------
    data/sector_stocks.csv

    Returns
    -------
    pd.DataFrame
        Custom stock classification table with:
        category, stock_code, stock_name.
    """

    # Read custom sector mapping file
    df = pd.read_csv("data/sector_stocks.csv")

    return df

@st.cache_data
def get_stock_data(stock_code, start_date, end_date):
    """
    Download historical daily stock data from BaoStock.

    Parameters
    ----------
    stock_code : str
        Six-digit A-share stock code.
        Example:
        600036 = 招商银行

    start_date : str
        Start date in YYYY-MM-DD format.

    end_date : str
        End date in YYYY-MM-DD format.

    Returns
    -------
    pd.DataFrame
        Historical stock OHLCV data.
    """

    # BaoStock requires exchange prefix:
    # Shanghai stocks usually start with 6
    # Shenzhen stocks usually start with 0 or 3
    if stock_code.startswith("6"):
        bs_code = f"sh.{stock_code}"
    else:
        bs_code = f"sz.{stock_code}"

    # Login to BaoStock server
    bs.login()

    # Request historical daily stock data
    rs = bs.query_history_k_data_plus(
        bs_code,
        "date,code,open,high,low,close,volume,amount",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="2"
    )

    data = []
    while rs.next():
        data.append(rs.get_row_data())

    df = pd.DataFrame(data, columns=rs.fields)

    # Logout after data request
    bs.logout()

    # --------------------------------------------------
    # Data Validation
    # --------------------------------------------------

    # Return empty DataFrame when no data is available
    if df.empty:
        return pd.DataFrame()

    # Return empty DataFrame when required columns are missing
    if "date" not in df.columns:
        return pd.DataFrame()

    # Convert data types
    df["date"] = pd.to_datetime(df["date"])
    df["open"] = pd.to_numeric(df["open"])
    df["high"] = pd.to_numeric(df["high"])
    df["low"] = pd.to_numeric(df["low"])
    df["close"] = pd.to_numeric(df["close"])
    df["volume"] = pd.to_numeric(df["volume"])
    df["amount"] = pd.to_numeric(df["amount"])

    return df

@st.cache_data(ttl=300)
def get_individual_fund_flow():
    """
    Get individual stock fund flow data from AKShare.

    Data source
    -----------
    AKShare fund flow interface.

    Notes
    -----
    The data is cached for 300 seconds to reduce request frequency.

    Returns
    -------
    pd.DataFrame
        Fund flow data for individual A-share stocks.
    """

    # Request individual stock fund flow data
    df = ak.stock_fund_flow_individual()

    return df

# --------------------------------------------------
# Smart Money Data
# --------------------------------------------------

@st.cache_data(ttl=300)
def get_individual_fund_flow():
    """
    Get individual stock fund flow data from AKShare.

    Data source
    -----------
    AKShare fund flow interface.

    Notes
    -----
    The data is cached for 300 seconds to reduce request frequency.

    Returns
    -------
    pd.DataFrame
        Fund flow data for individual A-share stocks.
    """

    # Request individual stock fund flow data
    df = ak.stock_fund_flow_individual()

    return df

