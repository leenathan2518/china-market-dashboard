"""
Chart Utilities

Author: Vinci Lee

Purpose:
Create reusable Plotly charts.
"""

import plotly.express as px
def create_price_chart(df, title):
    """
    Create a line chart for stock or index prices.

    Parameters
    ----------
    df : DataFrame

    title : str

    Returns
    -------
    Plotly Figure
    """

    fig = px.line(
        df,
        x="date",
        y="close",
        title=title
    )

    return fig