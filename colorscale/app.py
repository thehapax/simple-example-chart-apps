import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/nz_weather.csv')
df["Dunedin"] = pd.to_numeric(df["Dunedin"], errors='coerce')
df["Hamilton"] = pd.to_numeric(df["Hamilton"], errors='coerce')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Weather Records")

    ], style={
        'textAlign': "center"
    }),
    html.Div(
        dcc.Dropdown(
            id="selected-city",
            options=[{
                "label": i, "value": i
            } for i in df.columns.values[1:]],
            value="Auckland",

        ), style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "70%"

        }

    ),
    dcc.Graph(id="my-graph")

])


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-city', 'value')])
def update_figure(selected):
    trace = (go.Scatter(
        x=df["DATE"],
        y=df[selected],
        name=selected,
        mode='markers',
        marker={'size': 8,
                'cmax': 250,
                'cmin': 0,
                'color': df[selected].values.tolist(),
                'colorscale': 'Hot'},

        line=dict(
            # color=('rgb(22, 96, 167)'),
            width=4,
        )

    )
    )

    return {
        "data": [trace],

        "layout": go.Layout(
            title=f"Weather for {selected}",
            xaxis={
                "title": "Dates"

            },
            yaxis={
                "title": "Value",
                "range": [0, 350]
            }
        )

    }


server = app.server


if __name__ == '__main__':
    app.run_server(debug=True)
