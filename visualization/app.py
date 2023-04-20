from dash import Dash
import dash_bootstrap_components as dbc
from visualization.components import layout

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = layout.create_layout()

if __name__ == "__main__":
    app.run_server(debug=True)
