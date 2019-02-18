import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/mtl2013ternary.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Montreal 2013")

    ], style={'textAlign': "center"}),
    html.Div([
        dcc.RadioItems(id="selected-result",
                       options=[{"label": i.title(), "value": i} for i in df.result.unique()],
                       value="plurality",
                       labelStyle={'display': 'inline-block'}
                       )], style={
        'position': 'relative',

        "text-align": "center",
    }),

    dcc.Graph(id="my-graph")

])


@app.callback(
    Output("my-graph", "figure"),
    [Input("selected-result", "value")])
def update_figure(selected):
    dff = df[df["result"] == selected]

    trace = go.Heatmap(
        y=dff["district"].values,
        x=["Coderre", "Bergeron", "Joly"],
        z=dff[["Coderre", "Bergeron", "Joly"]].values,
        colorscale='Viridis',
        showscale=True
    )
    return {

        "data": [trace],
        "layout": go.Layout(
            title=f"Montreal-{selected.title()}",
            # width= 400,
            xaxis={
                "title": "Candidates"
            },
            yaxis={
                "title": "Regions"
            },
            margin={"l": 200}
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)


