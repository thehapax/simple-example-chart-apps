import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

mapbox_access_token = "pk.eyJ1IjoicHJpeWF0aGFyc2FuIiwiYSI6ImNqbGRyMGQ5YTBhcmkzcXF6YWZldnVvZXoifQ.sN7gyyHTIq1BSfHQRBZdHA"

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Airport traffic")
    ], style={
        'textAlign': "center",
        "padding-bottom": "10",
        "padding-top": "10"}),
    html.Div([
        dcc.Dropdown(id="state-selected",
                     options=[{'label': i, 'value': i} for i in df.state.unique()],
                     value=['CA'],
                     multi=True,
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "50%"

                     }
                     )
    ]),
    html.Div(dcc.Graph(id="my-graph"))

])


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("state-selected", "value")]

)
def update_figure(selected):
    trace = []
    for state in selected:
        dff = df[df["state"] == state]
        trace.append(go.Scattermapbox(
            lat=dff["lat"],
            lon=dff["long"],
            mode='markers',
            marker={'size': 10, 'opacity': 0.7},
            text=dff['airport'],
            hoverinfo='text',
            name=state
        ))
    return {
        "data": trace,
        "layout": go.Layout(
            title=f'Airport locations in the state: {selected}',
            autosize=True,
            hovermode='closest',
            showlegend=False,
            height=700,
            mapbox={'accesstoken': mapbox_access_token,
                    'bearing': 0,
                    'center': {'lat': 38, 'lon': -94},
                    'pitch': 30, 'zoom': 3,
                    "style": 'mapbox://styles/mapbox/navigation-preview-day-v4'},
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)
