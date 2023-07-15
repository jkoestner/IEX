"""Personal dashboard."""

from dash import dash_table
from dash import dcc
from dash import html

from iex.dashboard import utils

# Creating the dash app
layout = html.Div(
    [
        html.Div(
            [
                utils.get_menu(),
                html.Button("Portfolio Manager", id="manager-initialize", n_clicks=0),
                dcc.Input(
                    id="lookback-input", placeholder="Enter Lookback...", type="number"
                ),
                html.Div(id="manager_refresh_text", children=""),
                # creating table for portfolio manager
                html.Label("Portfolio Manager Table"),
                dash_table.DataTable(
                    id="manager_table",
                    sort_action="native",
                    page_action="native",
                ),
                html.Button("Portfolio", id="personal-initialize", n_clicks=0),
                # dropdown
                dcc.Dropdown(
                    [
                        "Total",
                        "Ally_Individual",
                        "Company",
                        "Fidelity",
                        "IB",
                        "IB-eiten",
                        "Ally_Roth",
                    ],
                    "Total",
                    id="personal-dropdown",
                ),
                html.Div(id="personal_refresh_text", children=""),
                # graph
                dcc.Graph(
                    id="personal_graph",
                ),
                # range slider
                html.P(
                    [
                        html.Label("Time Period"),
                        dcc.RangeSlider(
                            id="personal_slider",
                            tooltip="always_visible",
                            min=0,
                            max=10,
                            value=[0, 10],
                            marks=0,
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
                html.Label("Performance Table"),
                dash_table.DataTable(
                    id="personal_perfomance_table",
                    sort_action="native",
                    page_action="native",
                ),
                html.P(),
                html.P(),
                # creating table for transactions
                html.Label("Transactions Table"),
                dash_table.DataTable(
                    id="personal_transaction_table",
                    sort_action="native",
                ),
                html.P(),
            ],
            className="row",
        ),
    ]
)