import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

df1 = pd.read_csv("https://raw.githubusercontent.com/divyachandran-ds/dash1/master/Energy2.csv")
df = df1.dropna()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Energy Consumption Profile by Country")
    ], style={'textAlign': "center"}),
    html.Div([
        dcc.Dropdown(id="selected-type",
                     options=[{"label": i, "value": i} for i in df["Indicator Name"].unique()],
                     value='CO2 emissions from gaseous fuel consumption (% of total)',
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "80%"
                     }
                     )
    ]),
    dcc.Graph(id="my-graph")
], className="container")


@app.callback(
    Output("my-graph", "figure"),
    [Input("selected-type", "value")])
def update_figure(selected):
    dff = df[df["Indicator Name"] == selected]
    trace = go.Heatmap(
        x=dff.columns.values[3:],
        y=dff['Country Name'].unique(),
        z=dff[['2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012',
               '2013', '2014']].values,
        colorscale='Electric',
        colorbar={"title": "Percentage"},
        showscale=True
    )
    return {

        "data": [trace],
        "layout": go.Layout(
            title=f"Energy Indicators vs Year",
            xaxis={
                "title": "Year"
            },
            yaxis={
                "title": "Countries",
                "tickmode": "array",
                "tickvals": dff['Country Name'].unique(),
                "ticktext": ['Afghanistan', 'Arab World', 'Australia', 'Belgium', 'Bangladesh',
                             'Brazil', 'Canada', 'Colombia', 'Germany', 'East Asia & Pacific',
                             'Europe & Central Asia', 'India', 'Japan',
                             'Latin America & Caribbean', 'Middle East & North Africa',
                             'Mexico', 'North America', 'Saudi Arabia', 'Singapore',
                             'Virgin Islands (U.S.)', 'South Africa', 'Zimbabwe'],
                "tickfont": {"size": 8},
                "tickangle": -20
            },
            margin={"l": 300, "r": 100}
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO: adjust the margin layout
