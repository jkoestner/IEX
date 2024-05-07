"""Personal dashboard."""

import dash
import plotly.graph_objs as go
from dash import Input, Output, State, callback, dcc, html

from folioflex.budget import budget
from folioflex.dashboard.utils import dashboard_helper
from folioflex.utils import custom_logger

logger = custom_logger.setup_logging(__name__)

dash.register_page(__name__, path="/", title="folioflex - Stocks", order=0)

#   _                            _
#  | |    __ _ _   _  ___  _   _| |_
#  | |   / _` | | | |/ _ \| | | | __|
#  | |__| (_| | |_| | (_) | |_| | |_
#  |_____\__,_|\__, |\___/ \__,_|\__|
#              |___/


def layout(login_status, login_alert):
    """Create layout for the personal dashboard."""
    return html.Div(
        [
            # adding variables needed that are used in callbacks.
            *dashboard_helper.get_defaults(),
            dcc.Store(id="login-status", data=login_status),
            html.Div(id="login-alert", children=login_alert, style={"display": "none"}),
            # ---------------------------------------------------------------
            html.Div(
                [
                    dashboard_helper.get_menu(),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.Label("Date (YYYY-MM)", style={"paddingRight": "10px"}),
                    dcc.Input(
                        id="budget-chart-input",
                        placeholder="Enter Date...",
                        type="string",
                        style={"marginRight": "10px"},
                    ),
                ],
                style={"display": "flex", "alignItems": "center"},
                className="row",
            ),
            html.Div(
                [
                    # budget chart
                    html.Button("Budget Chart", id="budget-chart-button", n_clicks=0),
                    dcc.Graph(
                        id="budget-chart",
                    ),
                    html.Div(id="budget-chart-labels", children=""),
                    # income chart
                    html.Button("Income Chart", id="income-chart-button", n_clicks=0),
                    dcc.Graph(
                        id="income-chart",
                    ),
                    # compare chart
                    html.Button(
                        "Compare Chart", id="budget-compare-button", n_clicks=0
                    ),
                    dcc.Graph(
                        id="compare-chart",
                    ),
                ],
                className="row",
            ),
        ]
    )


#    ____      _ _ _                _
#   / ___|__ _| | | |__   __ _  ___| | _____
#  | |   / _` | | | '_ \ / _` |/ __| |/ / __|
#  | |__| (_| | | | |_) | (_| | (__|   <\__ \
#   \____\__,_|_|_|_.__/ \__,_|\___|_|\_\___/


# budget expense chart
@callback(
    [
        Output("budget-chart", "figure"),
        Output("budget-chart-labels", "children"),
    ],
    [Input("budget-chart-button", "n_clicks")],
    [State("budget-chart-input", "value")],
)
def update_budgetchart(n_clicks, input_value):
    """Provide budget info chart."""
    if n_clicks == 0:
        budget_chart = go.Figure()
        budget_chart.add_annotation(
            text="No data available", x=0.5, y=0.5, showarrow=False, font_size=20
        )
        budget_chart.update_layout(xaxis={"visible": False}, yaxis={"visible": False})
        len_label = 0
        len_unlabel = 0
    else:
        bdgt = budget.Budget(config_path="budget_personal.ini", budget="personal")
        budget_df = bdgt.get_transactions()
        budget_df = bdgt.modify_transactions(budget_df)
        budget_view = bdgt.budget_view(
            budget_df, target_date=input_value, exclude_labels=["income"]
        )
        budget_chart = bdgt.display_budget_view(budget_view)
        len_label = len(budget_df[~budget_df["label"].isnull()])
        len_unlabel = len(budget_df[budget_df["label"].isnull()])

    return budget_chart, f"Labeled: {len_label} | Unlabeled: {len_unlabel}"


# income chart
@callback(
    Output("income-chart", "figure"),
    [Input("income-chart-button", "n_clicks")],
    [State("budget-chart-input", "value")],
)
def update_incomeview(n_clicks, input_value):
    """Provide income info chart."""
    if n_clicks == 0:
        income_chart = go.Figure()
        income_chart.add_annotation(
            text="No data available", x=0.5, y=0.5, showarrow=False, font_size=20
        )
        income_chart.update_layout(xaxis={"visible": False}, yaxis={"visible": False})
    else:
        bdgt = budget.Budget(config_path="budget_personal.ini", budget="personal")
        budget_df = bdgt.get_transactions()
        budget_df = bdgt.modify_transactions(budget_df)
        income_chart = bdgt.display_income_view(budget_df)

    return income_chart


# budget compare chart
@callback(
    Output("compare-chart", "figure"),
    [Input("budget-compare-button", "n_clicks")],
    [State("budget-chart-input", "value")],
)
def update_comparechart(n_clicks, input_value):
    """Provide budget compare info chart."""
    if n_clicks == 0:
        compare_chart = go.Figure()
        compare_chart.add_annotation(
            text="No data available", x=0.5, y=0.5, showarrow=False, font_size=20
        )
        compare_chart.update_layout(xaxis={"visible": False}, yaxis={"visible": False})
    else:
        bdgt = budget.Budget(config_path="budget_personal.ini", budget="personal")
        budget_df = bdgt.get_transactions()
        budget_df = bdgt.modify_transactions(budget_df)
        compare_chart = bdgt.display_compare_expenses_view(
            budget_df, target_date=input_value, avg_months=3
        )

    return compare_chart
