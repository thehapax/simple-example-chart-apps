import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df1 = pd.read_csv('https://raw.githubusercontent.com/divyachandran-ds/dataset/master/Air_Quality.csv')
df = df1[df1["MeasureName"] == 'Annual average ambient concentrations of PM2.5 in micrograms per cubic meter (based on seasonal averages and daily measurement)']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H1("Air Quality Around United States")
    ],className="row",style={"text-align":"center"}),
    html.Div([
        html.Span("State Name",style={"text-align":"center","display":"block"}),
        dcc.Dropdown(id="select-state",
                    options=[{'label': i, 'value': i} for i in df.StateName.unique()],
                    value='New York'
                     )
    ],className="row",style={ "display": "block",
                                "margin-left": "auto",
                                "margin-right": "auto",
                                "width": "60%"}),
    html.Div([
        dcc.Graph(id="my-graph")
    ],className="row"),
    html.Div([
        dcc.RangeSlider(id="select-year",
                        min=df['ReportYear'].min(),
                        max=df['ReportYear'].max(),
                        value=[1999,2000],
                        marks={str(year): year for year in df['ReportYear'].unique()}
                        )
    ],className="row",style={"margin":20,"padding":30}),
    html.Div([
        html.Span("Hover Text & Formatting",className="row",style={"text-align":"center","text-decoration":"underline","display":"block"}),
        html.Div([
            html.Span("Input Hover Text",className="row",style={"text-align":"center","display":"block"}),
            html.Div([dcc.Input(id="hover-text",type='text',value='state',style={"width":"60%","margin":0}),
                      html.Button('Submit', id='button')
                    ],className="row")
            ],className="eight columns",style={"width":"60%"}),
        html.Div([
            html.Span("Select Hover Format",style={"text-align":"center","display":"block"}),
            dcc.Dropdown(id = "hover-format",
                              options=[{'label': i, 'value': i} for i in [".0%","($.2f","+20",".^20",".2s","#x",",.2r",'.2f']],
                              value='.2f'
                              )],className="four columns",style={"width":"30%","margin":0})
    ],className="row",style={"margin":10,"padding":20,"border": "1px solid black"})

],className="container")



@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("select-state", "value"),
     dash.dependencies.Input("select-year", "value"),
     dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State("hover-text", "value"),
     dash.dependencies.State("hover-format", "value")]
)
def update_graph(state,year,n_clicks,text,format):
    print(year)
    dff = df[df["StateName"] == state]
    df_year = dff[(dff["ReportYear"] >= year[0]) & (dff["ReportYear"] <= year[1])]

    trace = go.Scatter(
        x=dff["CountyName"],
        y=df_year['Value'],
        hovertext=text,
        mode='markers',
        marker={
            "color": "#FFE194",
            "size": 10,
        },

    )
    layout =go.Layout(
        title = "Set hover text formatting<br><a href= https://github.com/d3/d3-time-format/blob/master/README.md#locale_format>https://github.com/d3/d3-time-format/blob/master/README.md#locale_format</a>",
        yaxis={
            "title":"Concentrations of PM2.5(micrograms/cu.m)",
            "hoverformat": format
        },
        xaxis={
            "title":"County Names"
        }
    )

    figure = {

        "data": [trace],
        "layout": layout
    }

    return figure




server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)



