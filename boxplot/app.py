import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/medicare.csv')
df = df1[['City, State', 'Classification', 'Average Covered Charges ', 'Reimbursement Rate',
          'Total Discharges ', 'Total Payment']]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("MEDICARE")

    ], style={'textAlign': "center"}),

    html.Div(
        dcc.Dropdown(
            id="selected-type",
            options=[{
                "label": i, "value": i
            } for i in df.Classification.unique()],
            value='Alcohol and Drug Use',

        ), style={
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto",
            "width": "60%"

        }

    ),
    dcc.Graph(id="my-graph")

], style={'margin': "20px"})


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-type', 'value')])
def update_figure(selected):
    dff = df[df['Classification'] == selected]
    traces = []
    for category in dff.columns.values[2:]:
        traces.append(go.Box(
            x=dff[category],
            name=category,
            marker={"size": 4}

        ))

    return {

        "data": traces,
        "layout": go.Layout(
            title=f"Charges:{selected}",
            autosize=True,
            margin={"l": 200, "b": 100, "r": 200},
            xaxis={
                "title": selected,
                "type": "log",

            },

        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
