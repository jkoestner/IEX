"""Stores constants."""

import os

from iex.util import utils

alpha_vantage_api = os.environ["ALPHAVANTAGE_API"]
iex_api_live = os.environ["IEX_API_LIVE"]
iex_api_sandbox = os.environ["IEX_API_SANDBOX"]
aws_tx_file = os.environ["AWS_TX_FILE"]
remote_path = utils.get_remote_path()
