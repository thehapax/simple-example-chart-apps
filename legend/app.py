import re

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/iris.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Iris Species Comparison"),
    ], style={
        'textAlign': "center"}),
    html.Div([
        html.Div([
            html.Span("x-Axis : ", className="six columns",
                      style={'textAlign': "right", "text-decoration": "underline"}),
            dcc.RadioItems(id="xaxis",
                           options=[
                               {'label': 'Sepal Length', 'value': 'SepalLength'},
                               {'label': 'Sepal Width', 'value': 'SepalWidth'},
                           ],
                           value='SepalLength',
                           labelStyle={"display": "inline", "padding": 10}
                           )], className="six columns"),

        html.Div([
            html.Span("y-Axis : ", className="six columns",
                      style={'textAlign': "right", "text-decoration": "underline"}),
            dcc.RadioItems(id="yaxis",
                           options=[
                               {'label': 'Petal Length', 'value': 'PetalLength'},
                               {'label': 'Petal Width', 'value': 'PetalWidth'}, ],
                           value='PetalLength',
                           labelStyle={"display": "inline", "padding": 10}

                           )], className="six columns")

    ], className="row"),
    html.Div([
        dcc.Graph(id="my-graph"),
    ], className="row"),
    html.Div([
        html.Div([
            html.Div([
                html.Span("Legend Visible", className="six columns",
                          style={'textAlign': "right", "text-decoration": "underline"}),
                daq.BooleanSwitch(id="legend",
                                  on=True,
                                  label="Hide _________ Show",
                                  labelPosition="bottom",
                                  color="#137d1c",
                                  className="six columns"
                                  ),
            ], className="six columns"),

            html.Div([
                html.Span("Legend Orientation", className="six columns",
                          style={'textAlign': "right", "text-decoration": "underline"}),
                daq.ToggleSwitch(id="position",
                                 value=True,
                                 label="Horizontal_________Vertical",
                                 labelPosition="bottom",
                                 className="six columns"
                                 )
            ], className="six columns")
        ])
    ], className="row", style={"padding": 10, "border": ".5px solid black"}),

    html.Div([
        html.Span("Legend Position:Input X and Y values", className="row",
                  style={'textAlign': "center", "padding": 20, "margin": 5, "text-decoration": "underline"}),
        dcc.Input(id="x-value", type="number", value=1),
        dcc.Input(id="y-value", type="number", value=1),
        html.Button('Submit', id="button")
    ], className="row",
        style={"margin-left": "auto", "margin-right": "auto", "display": "block", "width": "60%", "padding": 20}),

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("xaxis", "value"),
     dash.dependencies.Input("yaxis", "value"),
     dash.dependencies.Input("legend", "on"),
     dash.dependencies.Input("position", "value"),
     dash.dependencies.Input("button", "n_clicks")],
    [dash.dependencies.State("x-value", "value"),
     dash.dependencies.State("y-value", "value")]
)
def update_graph(x_axis, y_axis, legend, position, n_clicks, xvalue, yvalue):
    trace = []
    for name in df.Name.unique():
        dff = df[df["Name"] == name]
        trace.append(go.Scatter(
            x=dff[x_axis],
            y=dff[y_axis],
            name=name,
            mode="markers",
            marker={
                'size': 10,
            },
        ))

    return {
        "data": trace,
        "layout": go.Layout(
            title=f"Iris data",
            xaxis={
                "title": f"{re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', x_axis)} (cm)"
            },
            yaxis={
                "title": f"{re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', y_axis)} (cm)"
            },
            colorway=["#E20048", "#CEF600", "#FFCB00"],
            legend={"x": xvalue,
                    "y": yvalue,
                    "orientation": f'{"v" if position == True else "h"}'},
            showlegend=legend
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
