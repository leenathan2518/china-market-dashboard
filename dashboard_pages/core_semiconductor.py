"""
Core Semiconductor Page

Author: Vinci Lee

Description
-----------
This page renders the Core Semiconductor sector analysis by calling
the reusable sector page function.
"""

from utils.sector_page import render_sector_page


def show():
    """
    Render the Core Semiconductor page.
    """

    render_sector_page(
        category="CoreSemiconductor",
        title="Core Semiconductor",
        caption=(
            "This page tracks selected A-share companies directly related to "
            "chip design, semiconductor manufacturing, semiconductor equipment, "
            "EDA software, and AI chips."
        ),
        start_label="Core Semiconductor Start Date",
        end_label="Core Semiconductor End Date"
    )