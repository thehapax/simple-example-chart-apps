import dash
import dash_core_components as dcc
import dash_html_components as html
# from plotly import tools
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/mtl2013ternary.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Montreal 2013")

    ], className="eight columns offset-by-two", style={'textAlign': "center", 'padding-right': 150}),
    html.Div([
        dcc.RadioItems(id="selected-result",
                       options=[{"label": i, "value": i} for i in df.result.unique()],
                       value="plurality",
                       labelStyle={'display': 'inline-block'}
                       )], style={
                                'padding-right': 600,
                                'padding-left': 400,
                                'textAlign': 'center'
                        }),
    html.Div([
        dcc.Graph(id="my-graph")], className="eight columns offset-by-two")

])


@app.callback(
    Output("my-graph", "figure"),
    [Input("selected-result", "value")])
def update_figure(selected):
    dff = df[df["result"] == selected]

    trace = go.Heatmap(
        y=dff["district"].values,
        x=["Coderre", "Bergeron", "Joly"],
        z=dff[["Coderre", "Bergeron", "Joly"]].values
    )
    return {

        "data": [trace],
        "layout": go.Layout(

            margin={"l": 200}
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)
