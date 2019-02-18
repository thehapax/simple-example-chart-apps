import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("3D Scatter Plot")
    ], style={
        'textAlign': "center",
        "padding-bottom": "10",
        "padding-top": "10"}),
    html.Div([
        dcc.Dropdown(id="continent-selected",
                     options=[{'label': i, 'value': i} for i in df.continent.unique()],
                     value='Europe',
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "60%"

                     }
                     )

    ]),
    html.Div([dcc.Graph(id="my-graph")])

])


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("continent-selected", "value")]

)
def ugdate_figure(selected):
    dff = df[df["continent"] == selected]
    z = dff["pop"]
    trace = [go.Scatter3d(
        x=dff["gdpPercap"],
        y=dff["lifeExp"],
        z=z,
        mode='markers',
        marker={'size': 8, 'color': z, 'colorscale': 'Rainbow', 'opacity': 0.8, "showscale": True}

    )]
    return {
        "data": trace,
        "layout": go.Layout(
            height=700,
            title=f"For {selected}",

        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO: minimize window colorscale goes off
