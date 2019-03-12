import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_daq as daq
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/data.csv')
df = df1.iloc[0:50]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

font = ["Arial", "Balto", "Courier New", "Droid Sans", "Droid Serif", "Droid Sans Mono", "Gravitas One", "Old Standard TT", "Open Sans", "Overpass", "PT Sans Narrow", "Raleway", "Times New Roman","Comic Sans MS","cursive"]

app.layout = html.Div([
    html.Div([
        html.H1("Credit Score")

    ], style={
        'textAlign': "center"
    }),

    html.Div([
        html.Div([
            html.Div([
                dcc.Input(id='size-input', type='number', value= 10),
                html.Button(id='submit-button', children="Type & Submit font size"),

            ], style={"display": "block",
                      "margin-left": "auto",
                      "margin-right": "auto",
                      "width": "45%",
                      "padding": "10"
                      }),
            html.Div([daq.ColorPicker(
                id='my-color-picker',
                label='Color Picker',
                value={"hex": "#08EBF1"},
            ), ]),
            html.Div([dcc.Dropdown(id="select-font",
                                   options=[{'label': i, 'value': i} for i in font],
                                   value="Helvetica Neue",
                                   placeholder="Select a font",
                                   style={
                                       "display": "block",
                                       "margin-left": "auto",
                                       "margin-right": "auto",
                                       "width": "70%",
                                       "padding": "10"
                                   }
                                   )])

        ], className="six columns"),
        html.Div([
            html.Div([
                html.Div(
                        dcc.Dropdown(
                            id="selected-type",
                            options=[{
                                "label": i, "value": i
                            } for i in df.columns.values[3:]],
                            value=['MonthlyIncome'],
                            multi=True,

                        ), style={
                            "display": "block",
                            "margin-left": "auto",
                            "margin-right": "auto",
                            "width": "70%"

                        }

                    ),

                dcc.Graph(id="my-graph")], className="six columns"),
            ])
    ])



],className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-type', 'value'),
     Input("my-color-picker",'value'),
     Input('select-font','value'),
     Input('submit-button','n_clicks')],
    [State('size-input','value')])

def update_figure(selected_type,selected_color,selected_font,n_clicks,size):
    trace = []
    color = selected_color["hex"]
    for type in selected_type:
        trace.append(go.Scatter(
            x=df["age"],
            y=df[type],
            name=type,
            mode='markers',
            marker={'size': 8,
                    "color": color,
                    "opacity": 0.8,
                    }, ))

    return {
        "data": trace,

        "layout": go.Layout(
            title={"text":f'{selected_type} Vs Age',
                   "font":{"family": selected_font,
                           "size": size + 2,
                           "color":color}
                   },
            xaxis={
                'title': 'Date',
                'titlefont': {'family': selected_font,
                              "size": size,
                              "color":color}},
            yaxis={'title': 'Rainfall in mm',
                   'titlefont': {'family': selected_font,
                                 "size": size,
                                 "color":color}}
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
