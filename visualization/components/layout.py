from dash import Dash, html
import dash_bootstrap_components as dbc
from . import ids
from visualization.components import (
    stock_select,
    strategy,
)


def create_layout(app: Dash) -> html.Div:
    return html.Div([
            dbc.Row(dbc.Col(stock_select.stock_selector_dropdown, width=6)),
            dbc.Row([
                dbc.Col(strategy.radio_items, width=3),
                dbc.Col(
                    html.Div([
                        html.Div(
                            strategy.single_dropdown,
                            className="dash-bootstrap",
                            id=ids.SINGLE_STRAT_CARD,
                            style={"display": "block"}),
                        html.Div(
                            children=[],
                            id=ids.MULTI_STRAT_CARD,
                            style={"display": "none"}),
                        ],
                        id=ids.STRAT_CARD,
                        className="dash-bootstrap",
                        ), width=3),
            ]),
            html.Br(),
            dbc.Row(html.Div(id='output')),
    ])
