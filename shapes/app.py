import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Shapes")
    ], style={
        'textAlign': "center",
        "padding-bottom": "30"}),
    html.Div([
        dcc.Dropdown(id="continent-selected",
                     options=[{'label': i, 'value': i} for i in df['continent'].unique()],
                     value="Asia",
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "50%"

                     }
                     )
    ], style={
        'textAlign': "center",
        "padding-bottom": "30"}),
    dcc.Graph(id="my-graph")

],className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("continent-selected", "value")]
)
def update_figure(selected):
    dff = df[df['continent'] == selected]

    trace = go.Scatter(
        x=dff["gdpPercap"],
        y=dff["lifeExp"],
        text=dff["country"],
        mode="markers",
        marker={
            'size': 15,
            'line': {'width': 0.5, 'color': 'white'},
            "color": "#ff751a"
        },
        name=selected
    )

    return {
        "data": [trace],
        "layout": go.Layout(
            xaxis={
                "title": 'Gdp Per cap',
                "range": [0, 50000],
                "tick0": 0,
                "dtick": 10000,
                "showline": True
            },
            yaxis={
                "title": "Life Expectancy",
                "showline": False
            },
            shapes=[
                {
                    'type': 'circle',
                    'xref': "x",
                    'yref': "y",
                    'x0': dff["gdpPercap"].quantile(q=0.2),
                    'y0': dff["lifeExp"].quantile(q=0.2),
                    'x1': dff["gdpPercap"].quantile(q=0.90),
                    'y1': dff["lifeExp"].quantile(q=0.90),
                    'opacity': 0.6,
                    'fillcolor': '#ffc299',
                    'line': {
                        'color': '#ffc299',
                    },
                }

            ]

        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
