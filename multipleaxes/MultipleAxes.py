import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/nz_weather.csv")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = df.columns.values[1:]

app.layout = html.Div([
    html.Div([
        html.H1("NZ Weather")

    ], style={'textAlign': "center"}),

    html.Div([
        html.Div(
            dcc.Dropdown(
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Auckland'
            ), className="six columns"),
        html.Div(
            dcc.Dropdown(
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wellington'
            ), className="six columns")

    ], className="row"),
    dcc.Graph(id="my-graph")

], style={"padding-right": 100,
          'padding-left': 100})


@app.callback(
    Output('my-graph', 'figure'),
    [Input('yaxis-column1', 'value'),
     Input('yaxis-column2', 'value')])
def update_figure(selected_1, selected_2):
    trace1 = go.Scatter(
        x=df["DATE"],
        y=df[selected_1],
        name=selected_1,
        mode='lines',
        line={
            "dash": "dot"
        }
    )
    trace2 = go.Scatter(
        x=df["DATE"],
        y=df[selected_2],
        name=selected_2,
        yaxis="y2",
        xaxis='x',
        mode='lines',

    )
    return {

        "data": [trace1, trace2],
        "layout": go.Layout(
            title=f"Weather data for {selected_1} and {selected_2}",
            margin={"l": 100, "r": 100},
            xaxis={
                "title": "Date"
            },
            yaxis={'title': selected_1,

                   "range": [0, 300]
                   },
            yaxis2={'title': selected_2,
                    'overlaying': 'y',
                    'side': 'right',
                    "range": [0, 300],
                    "showgrid": False})

    }


if __name__ == '__main__':
    app.run_server(debug=True)
