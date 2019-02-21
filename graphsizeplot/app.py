import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df1 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Aids%20Data.csv")
df = df1.groupby(['Indicator', 'Time Period']).mean().reset_index()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("AIDS")

    ], style={'textAlign': "center"}),

    html.Div(
        dcc.Dropdown(
            id="selected-type",
            options=[{
                "label": i, "value": i
            } for i in df.Indicator.unique()],
            value='AIDS-related deaths',

        ), style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "60%"
        }

    ),
    html.Div([
        dcc.Graph(id="my-graph")])

], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-type', 'value')])
def update_figure(selected):
    dff = df[df['Indicator'] == selected]
    traces = go.Scatter(
        x=dff['Time Period'],
        y=dff['Data Value'],
        mode='lines+markers',
        marker={"size": 6}
    )

    return {

        "data": [traces],
        "layout": go.Layout(
            title=f"Changing graph-size",
            xaxis={
                "title": "Time period"
            },
            yaxis={
                "title": selected,
            },

            autosize=False,
            height=700,
            margin=go.layout.Margin(
                l=100,
                r=100,
                b=100,
                t=100,
                pad=4
            ),
            paper_bgcolor='#b3ccff',
            plot_bgcolor='#e6eeff'
        )
    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
