import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/iris.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Iris Flower"),
    ], style={
        'textAlign': "center"}),
    html.Div([
        html.Div([
            html.Span("X-Axis", className="six columns", style={'textAlign': "right", "text-decoration": "underline"}),
            dcc.RadioItems(id="xaxis",
                           options=[
                               {'label': 'Sepal Length', 'value': 'SepalLength'},
                               {'label': 'Sepal Width', 'value': 'SepalWidth'},
                           ],
                           value='SepalLength',
                           labelStyle={"display": "inline", "padding": 10}
                           )], className="six columns"),

        html.Div([
            html.Span("Y-Axis", className="six columns", style={'textAlign': "right", "text-decoration": "underline"}),
            dcc.RadioItems(id="yaxis",
                           options=[
                               {'label': 'Petal Length', 'value': 'PetalLength'},
                               {'label': 'Petal Width', 'value': 'PetallWidth'}, ],
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
                dcc.RadioItems(id="legend",
                               options=[
                                   {'label': 'Show', 'value': 1},
                                   {'label': 'Hide', 'value': 0},
                               ],
                               value=1,
                               labelStyle={"display": "inline", "padding": 5},
                               className="six columns"
                               ),
            ], className="six columns"),

            html.Div([
                html.Span("Legend Orientation", className="six columns",
                          style={'textAlign': "right", "text-decoration": "underline"}),
                dcc.RadioItems(id="position",
                               options=[
                                   {'label': 'Horizontal', 'value': 'h'},
                                   {'label': 'vertical', 'value': 'v'},
                               ],
                               value="v",
                               labelStyle={"display": "inline", "padding": 5},
                               className="six columns"
                               )
            ], className="six columns")
        ])
    ], className="row", style={"padding": 10}),

    html.Div([
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
     dash.dependencies.Input("legend", "value"),
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
                "title": f"{x_axis}"
            },
            yaxis={
                "title": f"{y_axis}"
            },
            colorway=["#E20048", "#CEF600", "#FFCB00"],
            legend={"x": xvalue,
                    "y": yvalue,
                    "orientation": position},
            showlegend=bool(legend)
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
