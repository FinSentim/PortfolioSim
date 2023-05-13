from dash import html, dcc, callback, Input, Output
from . import ids

stocks = [
    "SBB",
    "NVIDIA",
    "APPLE",
    "AMD",
    "BBBY",
    "GME",
    "NOKIA",
    "ERICSSON",
    "AXFOOD",
    "ASTRA ZENECA",
    "VOLVO",
    "GOOGLE",
    "AMAZON",
    "MICROSOFT"
]


stock_selector_dropdown = html.Div([
        dcc.Store(id=ids.SELECTED_STOCKS, data=[]),
        dcc.Store(id=ids.SELECTED_STRATS, data={}),
        dcc.Dropdown(
            options=stocks,
            multi=True,
            optionHeight=50,
            placeholder="Select stock(s)",
            value=[],
            id=ids.STOCK_SELECT_DROPDOWN
        ),
    ],
    className="dash-bootstrap"
)


@callback(
    Output(ids.SELECTED_STOCKS, "data"),
    Input(ids.STOCK_SELECT_DROPDOWN, "value")
)
def update_selected_stocks(selected_stocks):
    return selected_stocks
