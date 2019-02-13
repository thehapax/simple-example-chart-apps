import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_with_codes.csv')



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Gapminder Data")
    ],style={
        'textAlign': "center",
        "padding-bottom": "30"}),
    html.Div([
        dcc.Dropdown(id = "value-selected",
                     options=[{'label': i.title(), 'value': i} for i in df.columns[3:6].tolist()],
                     value="pop",
                     style={
                            "display": "block",
                            "margin-left": "auto",
                            "margin-right": "auto",
                            "width" : "50%"

                     }
                     )
    ],style={
        'textAlign': "center",
        "padding-bottom": "30"}),
    dcc.Graph(id= "my-graph")

])



@app.callback(
 dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")]
)

def update_figure(selected):

    trace = {'type': 'choropleth',
             'locations': df['iso_alpha'],
             'z': df[selected],
             'text': df['country'],
             'autocolorscale': False,
             "colorscale" : "Cividis",
             'marker': {'line': {'color': 'rgb(180,180,180)',
                                 'width': 0.5}},
             'colorbar': {'autotick': False, 'title': selected.title()}}

    return {
        "data": [trace],
        "layout": dict( title=selected.title(),
                        width = 1000,
                        geo={'showframe': False,
                            'showcoastlines': False,
                            'projection': {'type': 'Mercator'}})

    }


if __name__ == '__main__':
    app.run_server(debug=True)

