from dash import html
import dash_bootstrap_components as dbc
from . import ids
from visualization.components import (
    stock_select,
    strategy,
    date_select,
    simulate_button
)


def create_layout() -> html.Div:
    return html.Div([
            dbc.Row(dbc.Col(html.H1("FinSentim Visualization"), width=8),
                    justify="start",
                    align="center",
                    className="py-3", style={"padding": "2em"}),
            dbc.Col(html.Div([
                dbc.Row(dbc.Col(stock_select.stock_selector_dropdown)),
                dbc.Row([strategy.radio_items],
                        style={"margin": "10px auto"}),
                dbc.Row(html.Div([date_select.date_selector],
                        style={"margin": "9px 9px 9px"})),
                dbc.Row(
                    dbc.Col(html.Div([
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
                        style={"margin": "10px auto"})
                        )),
                dbc.Row([simulate_button.button]),
                dbc.Row(html.Div(id=ids.ERROR_SIMULATE_BUTTON, style={"color": "red", "font-size": "1.5em"}))
            ], style={"position": "relative", "left": "30px", "text-align": "center"}),
                style={"min-width": "300px", "max-width": "400px"}, width=3),
            html.Br(),
            dbc.Row(html.Div(id="graph"))
    ])
