"""Tracker dashboard."""

from dash import dash_table
from dash import dcc
from dash import html

from iex.util import constants, utils

tracker_portfolio = constants.tracker_portfolio

portfolio_view = tracker_portfolio.portfolio_view
performance = tracker_portfolio.get_performance().reset_index()
transactions = tracker_portfolio.transactions

min, max, value, marks = utils.get_slider_values(portfolio_view.index)

# Creating the dash app
layout = html.Div(
    [
        html.Div(
            [
                utils.get_menu(),
                # graph
                dcc.Graph(
                    id="Tracker-Graph",
                ),
                # range slider
                html.P(
                    [
                        html.Label("Time Period"),
                        dcc.RangeSlider(
                            id="track_slider",
                            tooltip="always_visible",
                            min=min,
                            max=max,
                            value=value,
                            marks=marks,
                        ),
                    ],
                    style={
                        "width": "80%",
                        "fontSize": "20px",
                        "padding-left": "100px",
                        "display": "inline-block",
                    },
                ),
                html.P(),
                html.P(),
                # creating table for performance
                html.Label("Performance"),
                dash_table.DataTable(
                    id="perfomance-table",
                    sort_action="native",
                    columns=[{"name": i, "id": i} for i in performance.columns],
                    data=performance.to_dict("records"),
                ),
                html.P(),
                html.P(),
                # creating table for transactions
                html.Label("Transactions"),
                dash_table.DataTable(
                    id="transaction-table",
                    sort_action="native",
                    columns=[{"name": i, "id": i} for i in transactions.columns],
                    data=transactions.to_dict("records"),
                ),
                html.P(),
            ],
            className="row",
        ),
    ]
)