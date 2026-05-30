"""
Test AKShare Capital Flow Interface

Author: Vinci Lee
"""

from utils.data_loader import get_individual_fund_flow

df = get_individual_fund_flow()

print(df.head())
