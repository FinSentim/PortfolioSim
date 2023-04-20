import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, State
from . import ids
from dash.exceptions import PreventUpdate
import random
import pandas as pd

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
    Output(ids.SIMULATION_DATA, "data"),
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
    return fetch_data(selected_stocks, selected_strats, selected_date), None


def fetch_data(stocks, strategies, dates):
    # Request should happen here, mock data for now.
    data = []
    date_list = pd.date_range(start=dates["start_date"], end=dates["end_date"])
    for stock, strats in strategies.items():
        if isinstance(strats, list):
            for strat in strats:
                for d in date_list:
                    data.append((stock, strat, d, random.random()))
        else:
            for d in date_list:
                data.append((stock, strats, d, random.random()))

    df = pd.DataFrame(data, columns=['stock', 'strategy', 'date', 'return'])
    return df.to_json()
    # print(df_pivot.loc[:, ('Stock 3', slice(None))])
    # return graph
