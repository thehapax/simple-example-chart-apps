import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df1 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Aids%20Data.csv")
df2 = df1[df1["Unit"] != "Percent"]
df = df2.groupby(['Indicator', 'Time Period']).mean().reset_index()

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Animation Plot")

    ], style={'textAlign': "center"}),
    html.Div([
        dcc.Graph(id="my-graph"),
        dcc.Interval(
            id='interval-component',
            interval=800,  # in milliseconds
            n_intervals=0
        ),
    ])

], className="container")


@app.callback(
    [Output('my-graph', 'figure'),
     Output('interval-component', 'disabled')],
    [Input('interval-component', 'n_intervals')],
)
def update_figure(interval):
    dff = df[df['Indicator'] == "AIDS-related deaths"]
    disable = False
    trace = [go.Scatter(
        x=dff['Time Period'],
        y=dff['Data Value'],
        mode='lines',
        name="No of Deaths",
        marker={"color": "#4daf4a"}
    )]

    figure = {
        "data": trace,
        "layout": go.Layout(
            title="AIDS Related Deaths",
            height=600,
            showlegend=False,
            xaxis={
                "title": "Date"
            },
            yaxis={
                "title": "AIDS Related Deaths (Number) ",
                "range": [50, 500000],
            },

            hovermode="closest",
        ),
    }
    trace.append(go.Scatter(
        x=[dff['Time Period'][interval]],
        y=[dff['Data Value'][interval]],
        mode='markers',
        name="Animation trace",
        marker={"size": 25, "color": "#e41a1c", "symbol": "star-triangle-up"}
    ))
    if interval >= 25:
        disable = True

    return figure, disable


server = app.server # the Flask app

if __name__ == '__main__':
    app.run_server(debug=True)
