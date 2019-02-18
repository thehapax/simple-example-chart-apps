import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_with_codes.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("GapMinder")
    ], style={
        'textAlign': "center",
        "padding-bottom": "30"}),
    html.Div([
        dcc.Dropdown(id="value-selected",
                     options=[{'label': "Population", 'value': 'pop'},
                            {'label': "GDP Per Capita", 'value': 'gdpPercap'},
                            {'label': "Life Expectancy", 'value': 'lifeExp'}],
                     value="pop",
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "70%"

                     }
                     )
    ], style={
        'textAlign': "center",
        "padding-bottom": "30"}),
    dcc.Graph(id="my-graph")

])


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")]
)
def update_figure(selected):

    dff = df.groupby(['iso_alpha','country']).mean().reset_index()
    trace = {'type': 'choropleth',
             'locations': dff['iso_alpha'],
             'z': dff[selected],
             'text': dff['country'],
             'autocolorscale': False,
             "colorscale": "Rainbow",
             'marker': {'line': {'color': 'rgb(180,180,180)',
                                 'width': 0.5}},
             'colorbar': {'autotick': False, 'title': selected.title()}}

    return {
        "data": [trace],
        "layout": dict(title=selected.title(),
                        height = 600,
                       geo={'showframe': False,
                            'showcoastlines': False,
                            'projection': {'type': 'Mercator'}})

    }


if __name__ == '__main__':
    app.run_server(debug=True)
