import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/laucnty16.csv')
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([html.H1("3D-Surface Plots")],className="row", style={
        'textAlign': "center",
        'border-style': 'outset',
        'border-color': '#ffffcc',
        "background-color":'#ffffcc',
        "margin-left": "auto",
        "margin-right": "auto",
         "color": "#8533eb"
    }),
    html.Div([
        dcc.Dropdown(id="state-selected",
                     options=[{'label': i, 'value': i} for i in df['State FIPS Code'].unique()],
                     value=45,
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "60%",
                         'textAlign': "center",

                     }
                     )
    ],className="row" ,style={
        'padding-top': 20
    }),
    dcc.Graph(id="my-graph"),

],style={"margin": "50px"})


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("state-selected", "value")]
)
def update_figure(selected):
    dff = df[df['State FIPS Code'] == selected]
    trace = [go.Surface(
        z=dff.values,
        colorscale="Viridis",
        opacity=0.8,

    )]
    return {
        "data": trace,
        "layout": go.Layout(
            title=f'Employment rate for the state:FIPS Code({selected})',
            autosize=False,
            width=1000,
            height=650,
            margin={'l': 65, 'r': 50, 'b': 65, 't': 90}

        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)
