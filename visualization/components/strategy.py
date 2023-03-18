import dash_bootstrap_components as dbc
from dash import html, dcc, callback, Input, Output, ALL, State, ctx
from dash.exceptions import PreventUpdate
from . import ids


strategies = [f"Strategy {i}" for i in range(1, 50)]


radio_items = html.Div(
    dbc.RadioItems(
        options=[
            {"label": "Use same strategy", "value": "same"},
            {"label": "Use different strategies", "value": "different"},
        ],
        value="same",
        inline=True,
        id=ids.STRAT_RADIO_ITEM,
    )
)


single_dropdown = html.Div(
    dcc.Dropdown(
        options=strategies,
        optionHeight=50,
        placeholder="Select strategy",
        persistence=True,
        id=ids.SINGLE_STRAT_DROPDOWN
    )
)


def create_multi_dropdown(stock_id, strategies) -> html.Div:
    return dcc.Dropdown(
            options=strategies,
            optionHeight=50,
            multi=True,
            placeholder=f"Select strategies for {stock_id}",
            value=[],
            persistence=True,
            id={"type": f"{ids.MULTI_STRAT_DROPDOWN}", "index": f"{stock_id}"},
            className="dash-bootstrap",
        )


@callback(
    Output(ids.STRAT_CARD, "children"),
    Input(ids.STRAT_RADIO_ITEM, "value"),
    Input(ids.SELECTED_STOCKS, "data"),
)
def show_hide_strategy_card(strategy, stocks):
    if strategy == "same":
        return [
            html.Div(
                single_dropdown,
                style={'display': 'block'},
                id=ids.SINGLE_STRAT_CARD,
                ),
            html.Div(
                [],
                style={"display": "none"},
                id=ids.MULTI_STRAT_CARD,
            )
            ]
    elif strategy == "different":
        return [
            html.Div(
                single_dropdown,
                style={'display': 'none'},
                id=ids.SINGLE_STRAT_CARD,
                className="dash-bootstrap",
                ),
            html.Div(
                [create_multi_dropdown(stock, strategies) for stock in stocks],
                style={'display': 'block'},
                id=ids.MULTI_STRAT_CARD,
                className="dash-bootstrap",
            )
            ]


@callback(
    Output("output", "children"),
    Input(ids.SELECTED_STRATS, "data")
)
def show_queries(strategies) -> html.Div:
    if not strategies:
        raise PreventUpdate
    return [html.Div(f"{k}: {v}") for k, v in strategies.items()]


@callback(
        Output(ids.SELECTED_STRATS, "data"),
        State(ids.STRAT_RADIO_ITEM, "value"),
        Input(ids.SINGLE_STRAT_DROPDOWN, "value"),
        Input({"type": f"{ids.MULTI_STRAT_DROPDOWN}", "index": ALL}, "value"),
        State(ids.SELECTED_STOCKS, "data"),
        State(ids.SELECTED_STRATS, "data"),
    )
def update_strats(radio, single_strat, multiple_strats, stocks, strats):
    trigger_id = ctx.triggered_id
    if trigger_id == ids.SINGLE_STRAT_DROPDOWN and radio == "same":
        return {stock: single_strat for stock in stocks}
    elif trigger_id == ids.SINGLE_STRAT_DROPDOWN and radio == "different":
        # single-strat-dropdwon can fire if selected stocks fire, circular cb
        return {stock: multiple_strats[i] for i, stock in enumerate(stocks)}
    elif trigger_id is not None:
        return {stock: multiple_strats[i] for i, stock in enumerate(stocks)}
    else:
        raise PreventUpdate
