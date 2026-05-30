"""
Financial Metrics Module

Author: Vinci Lee

Description
-----------
This module contains reusable financial metric functions.
These functions can be used across different dashboard pages.
"""

import numpy as np


def calculate_return(start_price, end_price):
    """
    Calculate holding period return in percentage.

    Parameters
    ----------
    start_price : float
        Price at the beginning of the selected period.

    end_price : float
        Price at the end of the selected period.

    Returns
    -------
    float
        Holding period return in percentage.
    """

    return (end_price / start_price - 1) * 100


def calculate_annualized_volatility(price_series):
    """
    Calculate annualized volatility based on daily returns.

    Parameters
    ----------
    price_series : pd.Series
        Daily closing prices.

    Returns
    -------
    float
        Annualized volatility in percentage.
    """

    daily_returns = price_series.pct_change().dropna()

    return daily_returns.std() * np.sqrt(252) * 100
