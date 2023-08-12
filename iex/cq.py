"""Worker connections.

note: there are two resources that are needed to use the worker processes.

1. redis server - this is the message broker that is used to communicate between the
worker and the main process. The redis server is referenced using environment variables
`REDIS_URL` and `LOCAL_REDIS`.  The `REDIS_URL` is used when the application is
deployed on web and the `LOCAL_REDIS` is used when debugging locally.

2. worker - this is the process that will be used to execute the tasks.  The worker
will be listening to the redis server for tasks to execute.

To run the worker process locally from the root directory, use the following command:
   celery -A iex.cq worker --pool=solo -l info

If wanting to look at monitoring celery, use the following command which will be
available at http://localhost:5555:
    celery -A iex.cq flower
"""

import yfinance as yf

from celery import Celery
from datetime import datetime

from iex.dashboard import layouts
from iex.portfolio import portfolio
from iex import constants

config_path = str(constants.ROOT_PATH / "iex" / "configs" / "portfolio_personal.ini")

celery_app = Celery(
    "tasks",
    broker=constants.REDIS_URL,
    backend=constants.REDIS_URL,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,
)


@celery_app.task
def sector_query(start="2023-01-01"):
    """Provide the sector historical stock prices.

    Parameters
    ----------
    start : date
       start date of series

    Returns
    -------
    cq_sector_close : json
       provides the list of prices for historical prices
    """
    sector_close = yf.download(
        layouts.list_sector, start=start, end=datetime(2100, 1, 1)
    )
    cq_sector_close = sector_close["Adj Close"].to_json()

    return cq_sector_close


@celery_app.task
def portfolio_query(config_path, broker="all", lookback=None):
    """Query for worker to generate portfolio.

    Parameters
    ----------
    config_path : str
       path to config file
    broker : str
        the brokers to include in analysis
    lookback : int (optional)
        amount of days to lookback

    Returns
    -------
    cq_portfolio_dict : dict
       provides a dict of portfolio objects
    """
    personal_portfolio = portfolio.Portfolio(config_path=config_path, portfolio=broker)

    # get transactions that have portfolio information as well
    transactions = personal_portfolio.transactions.head(10)

    # provide results in dictionary
    cq_portfolio_dict = {}
    cq_portfolio_dict["transactions"] = transactions.to_json()
    cq_portfolio_dict["performance"] = (
        personal_portfolio.get_performance(lookback=lookback).reset_index().to_json()
    )
    cq_portfolio_dict["view_return"] = personal_portfolio.get_view(
        view="return"
    ).to_json()
    cq_portfolio_dict["view_cost"] = personal_portfolio.get_view(
        view="cumulative_cost"
    ).to_json()
    cq_portfolio_dict["view_market_value"] = personal_portfolio.get_view(
        view="market_value"
    ).to_json()

    return cq_portfolio_dict


@celery_app.task
def manager_query(config_path, lookback=None):
    """Query for worker to generate manager.

    Parameters
    ----------
    config_path : str
       path to config file
    lookback : int (optional)
        amount of days to lookback

    Returns
    -------
    cq_pm : json
       provides the portfolio manager performance
    """
    # create portfolio objects
    pf = portfolio.Portfolio(config_path=config_path, portfolio="all")
    fidelity = portfolio.Portfolio(config_path=config_path, portfolio="fidelity")
    ib = portfolio.Portfolio(config_path=config_path, portfolio="ib")
    eiten = portfolio.Portfolio(config_path=config_path, portfolio="eiten")
    roth = portfolio.Portfolio(config_path=config_path, portfolio="roth")
    company = portfolio.Portfolio(config_path=config_path, portfolio="company")
    portfolios = [pf, fidelity, ib, eiten, roth, company]
    pm = portfolio.Manager(portfolios)
    cq_pm = pm.get_summary(lookback=lookback).to_json()

    return cq_pm
