"""
Cash Flow Assets Page

Author: Vinci Lee

Description
-----------
This page renders the Cash Flow Assets sector analysis by calling
the reusable sector page function.
"""

from utils.sector_page import render_sector_page


def show():
    """
    Render the Cash Flow Assets page.
    """

    render_sector_page(
        category="CashFlowAssets",
        title="Cash Flow Assets",
        caption=(
            "This page tracks selected A-share companies with relatively stable "
            "cash flow, including banks, insurers, utilities, and energy companies."
        ),
        start_label="Cash Flow Start Date",
        end_label="Cash Flow End Date"
    )

