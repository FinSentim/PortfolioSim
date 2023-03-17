from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div([
    html.Div(children=[
        html.H1("Professional Visualizer 3000", style={"textAlign": "center"}),
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
