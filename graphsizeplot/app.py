import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df1 = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/Aids%20Data.csv")
df = df1.groupby(['Indicator', 'Time Period']).mean().reset_index()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("AIDS statistics over time")

    ], style={'textAlign': "center"}),

    html.Div([
        dcc.Dropdown(
            id="selected-type",
            options=[
                {"label": "Death", "value": 'AIDS-related deaths'},
                {"label": "Receiving ART", "value": 'Coverage of people receiving ART'},
                {"label": "Death averted by ART", "value": 'Deaths averted due to ART'},
                {"label": "New infections", "value": 'New HIV Infections'},
                {"label": "Pregnant women needing ART", "value": 'Pregnant women needing ARV for preventing MTCT'},
                {"label": "Pregnant women received ART", "value": 'Pregnant women who received ARV for preventing MTCT'}
            ],
            multi=True,
            value=['AIDS-related deaths']

        )], style={
        "display": "block",
        "margin-left": "auto",
        "margin-right": "auto",
        "width": "60%",
    }

    ),
    html.Div([
        dcc.Graph(id="my-graph", style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "100%"
        })]),
    html.Div(
        dcc.Slider(
            id="graph-size",
            min=300,
            max=900,
            value=450,
            step=100,
            marks={
                300: "300px",
                400: "400px",
                500: "500px",
                600: "600px",
                700: "700px",
                800: "800px",
                900: "900px",

            }
        ), style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "40%"
        }
    )

], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-type', 'value'),
     Input('graph-size', 'value')])
def update_figure(selected, size_selected):

    traces = []
    for select in selected:
        traces.append(go.Scatter(
            x=df[df['Indicator'] == select]['Time Period'],
            y=df[df['Indicator'] == select]['Data Value'],
            mode='lines+markers',
            marker={"size": 6,},
            showlegend=False
        ))
    layout = go.Layout(
        title=f"Cases vs time",
        xaxis={
            "title": "Time period"
        },
        yaxis={
            "title": f"Number of cases",
            "tickangle": -45,
            "tickfont": {"size": 10},
        },
        height=size_selected,
        width=2 * size_selected,
        autosize=True,
        colorway=["#003f5c","#955196","#dd5182","#ff6e54","#ffa600","#061460"]
    )

    figure = {
        "data": traces,
        "layout": layout
    }

    return figure


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
