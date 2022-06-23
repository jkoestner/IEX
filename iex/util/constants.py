"""Stores constants."""

import os

from iex.util import utils, portfolio

alpha_vantage_api = os.environ["ALPHAVANTAGE_API"]
iex_api_live = os.environ["IEX_API_LIVE"]
iex_api_sandbox = os.environ["IEX_API_SANDBOX"]
aws_tx_file = os.environ["AWS_TX_FILE"]
remote_path = utils.get_remote_path()

# tracker vars
tracker_tx_file = remote_path + r"transactions.xlsx"
tracker_portfolio = portfolio.portfolio(
    tracker_tx_file, filter_type=["Cash", "Dividend"], funds=["BLKRK"]
)

# personal vars
personal_tx_file = aws_tx_file
personal_portfolio = portfolio.portfolio(
    personal_tx_file,
    filter_type=["Cash", "Dividend"],
    funds=["BLKEQIX", "TRPILCG", "TRPSV", "LIPIX", "BLKRVIX", "BLKRGIX", "HLIEIX"],
    other_fields=["Broker", "Account"],
)
