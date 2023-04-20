
from dash import html, dcc, callback, Input, Output
from . import ids
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go

graph = html.Div([
    dcc.Store(id=ids.SIMULATION_DATA),
    dcc.Graph(id="graph")
    ], id="graph-container"
    )


@callback(
        Output("graph-container", "style"),
        Input(ids.SIMULATION_DATA, "data"),
)
def update_visibility(data):
    if data is None:
        return {"display": "none"}
    return {"display": "block"}


@callback(
        Output("graph", "figure"),
        Input(ids.SIMULATION_DATA, "data"),
        prevent_initial_call=True
)
def update_graph(data):
    if data is None:
        raise PreventUpdate
    df = get_data_df(data)
    fig = go.Figure(layout=go.Layout(width=1000,
                                     height=600,
                                     plot_bgcolor="rgba(0,0,0,0)",
                                     paper_bgcolor="rgba(0,0,0,0)",
                                     font=dict(color="white")
                                     )
                    )
    for column in df.columns:
        stock, strategy = column
        fig.add_trace(go.Scatter(x=df.index, y=df[column], name=f"{stock}: {strategy}"))
    return fig


def get_data_df(data):
    df = pd.read_json(data)
    df_pivot = df.pivot(index="date", columns=["stock", "strategy"], values="return")
    return df_pivot
