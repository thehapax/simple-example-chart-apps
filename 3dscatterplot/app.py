import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("US Exports")
    ], style={
        'textAlign': "center",
        "padding-bottom": "10",
        "padding-top": "10"}),
    html.Div([
        html.Div(dcc.Dropdown(id="select-xaxis",
                              options=[{'label': i.title(), 'value': i} for i in df.columns[3:]],
                              value='beef',

                              ), className="four columns", style={"display": "block",
                                                                  "margin-left": "auto",
                                                                  "margin-right": "auto",
                                                                  "width": 310
                                                                  }),
        html.Div(dcc.Dropdown(id="select-yaxis",
                              options=[{'label': i.title(), 'value': i} for i in df.columns[3:]],
                              value='pork',

                              ), className="four columns", style={"display": "block",
                                                                  "margin-left": "auto",
                                                                  "margin-right": "auto",
                                                                  "width": 310
                                                                  }),
        html.Div(dcc.Dropdown(id="select-zaxis",
                              options=[{'label': i.title(), 'value': i} for i in df.columns[3:]],
                              value='poultry',

                              ), className="four columns", style={"display": "block",
                                                                  "margin-left": "auto",
                                                                  "margin-right": "auto",
                                                                  "width": 310
                                                                  })

    ], className="row", style={"padding": 14}),
    html.Div([dcc.Graph(id="my-graph")])

], className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("select-xaxis", "value"),
     dash.dependencies.Input("select-yaxis", "value"),
     dash.dependencies.Input("select-zaxis", "value")]

)
def ugdate_figure(selected_x, selected_y, selected_z):
    z = df[selected_z]
    trace = [go.Scatter3d(
        x=df[selected_x],
        y=df[selected_y],
        z=df[selected_z],
        mode='markers',
        marker={'size': 8,
                'color': z,
                'colorscale': 'Blackbody', 'opacity': 0.8,
                "showscale": True,
                "colorbar": {"thickness": 15,
                             "len": 0.5,
                             "x": 0.8,
                             "y": 0.6,
                             },
                }

    )]
    return {
        "data": trace,
        "layout": go.Layout(

            height=700,
            title=f"Exports",
            paper_bgcolor="#A9BBCB",
            scene={
                "aspectmode": "cube",

                "xaxis": {
                    "title": f"{selected_x.title()}",
                },
                "yaxis": {
                    "title": f"{selected_y.title()}",
                },
                "zaxis": {
                    "title": f"{selected_z.title()}",
                }}

        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO: minimize window colorscale goes off
