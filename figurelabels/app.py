import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/data.csv')
df = df1.iloc[0:50]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

font = ["Arial", "Balto", "Courier New", "PT Sans Narrow", "Times New Roman", "Comic Sans MS",
        "cursive"]

app.layout = html.Div([
    html.Div([
        html.H1("Credit Score Statistics")

    ], style={
        'textAlign': "center"
    }),

    html.Div([
        html.Div([
            html.Div([
                dcc.Input(id='size-input', type='number', value=15),
                html.Button(id='submit-button', children="Submit font size"),

            ], style={"display": "block",
                      "margin-left": "auto",
                      "margin-right": "auto",
                      "width": "40%",
                      "padding": "10"
                      }),
            html.Div([daq.ColorPicker(
                id='my-color-picker',
                label='Color Picker',
                value={"hex": "#08EBF1"},
            )], style={"display": "block",
                       "margin-left": "auto",
                       "margin-right": "auto",
                       "padding": 10}),

            html.Div([dcc.Dropdown(id="select-font",
                                   options=[{'label': i, 'value': i} for i in font],
                                   value="Helvetica Neue",
                                   placeholder="Select a font",
                                   style={
                                       "display": "block",
                                       "margin-left": "auto",
                                       "margin-right": "auto",
                                       "width": "70%",

                                   }
                                   )], style={"padding": 10})

        ], className="six columns"),
        html.Div([
            html.Div([
                html.Div(
                    dcc.Dropdown(
                        id="selected-type",
                        options=[
                            {'label': "Past-due(30-59days)", 'value': 'NumberOfTime30-59DaysPastDueNotWorse'},
                            {'label': "Debt-ratio", 'value': 'DebtRatio'},
                            {'label': "Income", 'value': 'MonthlyIncome'},
                            {'label': "Open Credits/loans", 'value': 'NumberOfOpenCreditLinesAndLoans'},
                            {'label':"Past-due(90 days)",'value':'NumberOfTimes90DaysLate'},
                            {'label':"Real estate loans",'value':'NumberRealEstateLoansOrLines'},
                            {'label':"Past-due(60-89 days)",'value':'NumberOfTime60-89DaysPastDueNotWorse'},
                            { 'label':"Dependents",'value':'NumberOfDependents'}
                        ],
                        value='MonthlyIncome',
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

], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-type', 'value'),
     Input("my-color-picker", 'value'),
     Input('select-font', 'value'),
     Input('submit-button', 'n_clicks')],
    [State('size-input', 'value')])
def update_figure(selected_type, selected_color, selected_font, n_clicks, size):

    color = selected_color["hex"]
    dropdown = {
         'NumberOfTime30-59DaysPastDueNotWorse':"Past-due(30-59days)",
        'DebtRatio':"Debt-ratio",
        'MonthlyIncome': "Income",
        'NumberOfOpenCreditLinesAndLoans':"Open Credits/loans",
        'NumberOfTimes90DaysLate':"Past-due(90 days)",
        'NumberRealEstateLoansOrLines': "Real estate loans",
        'NumberOfTime60-89DaysPastDueNotWorse':"Past-due(60-89 days)",
        'NumberOfDependents':"Dependents"}

    trace = go.Scatter(
        x=df["age"],
        y=df[selected_type],
        name=dropdown[selected_type],
        mode='markers',
        marker={'size': 10,
                "color": color,
                "opacity": 0.8,
                }, )

    return {
        "data":[trace],

        "layout": go.Layout(
            title={"text": f'{dropdown[selected_type]} Vs Age',
                   "font": {"family": selected_font,
                            "size": size + 4,
                            "color": color}
                   },
            xaxis={
                'title': 'Age',
                'titlefont': {'family': selected_font,
                              "size": size,
                              "color": color}},
            yaxis={'title': f'{dropdown[selected_type]}',
                   'titlefont': {'family': selected_font,
                                 "size": size,
                                 "color": color}}
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)

# TODO : remove circle from color picker
