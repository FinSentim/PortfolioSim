import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, ALL, State, ctx
from . import ids
from dash.exceptions import PreventUpdate
import requests

button = html.Div([
        dbc.Button(
            "Simulate",
            id=ids.SIMULATE_BUTTON,
            n_clicks=0,
        ),
    ],
    className="d-grid gap-2",
)


@callback(
    Output("graph", "children"),
    Output(ids.ERROR_SIMULATE_BUTTON, "children"),
    Input(ids.SIMULATE_BUTTON, "n_clicks"),
    State(ids.SELECTED_STOCKS, "data"),
    State(ids.SELECTED_STRATS, "data"),
    State(ids.SELECTED_DATE, "data"),
    prevent_initial_call=True
)
def on_button_click(clicks, selected_stocks, selected_strats, selected_date):
    if clicks is None:
        raise PreventUpdate
    errs = []
    if not selected_stocks:
        errs.append("stock(s)")
    if not selected_strats or None in selected_strats.values() or [] in selected_strats.values():
        errs.append("strategies")
    if not selected_date:
        errs.append("dates")
    if errs:
        err_msg = f"Select {', '.join(errs)}"
        return None, html.Div([html.P(err_msg)])
    return fetch_data(), None


def fetch_data():
    x_values = [1, 2, 3, 4, 5]
    y_values = [x**2 for x in x_values]
    graph = dcc.Graph(
                id='example-graph',
                figure={
                    'data': [{'x': x_values, 'y': y_values, 'type': 'line'}],
                    'layout': {'title': 'Graph of y = x^2'}
                }
            )
    return graph
