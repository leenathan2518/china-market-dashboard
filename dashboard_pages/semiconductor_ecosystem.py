"""
Semiconductor Ecosystem Page

Author: Vinci Lee

Description
-----------
This page renders the Semiconductor Ecosystem sector analysis by calling
the reusable sector page function.
"""

from utils.sector_page import render_sector_page


def show():
    """
    Render the Semiconductor Ecosystem page.
    """

    render_sector_page(
        category="SemiconductorEcosystem",
        title="Semiconductor Ecosystem",
        caption=(
            "This page tracks selected A-share companies that may benefit from "
            "semiconductor, AI computing, data center, PCB, and optical module demand."
        ),
        start_label="Ecosystem Start Date",
        end_label="Ecosystem End Date"
    )

