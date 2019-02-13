import dash
import dash_core_components as dcc
import dash_html_components as html
#from plotly import tools
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/iris-data.csv')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
        html.Div([
            html.H1("IRIS")

            ],style = {'textAlign' : "center" }),

        html.Div(
            dcc.Dropdown(
                id="selected-dropdown",
                options=[{
                    "label":i,"value":i
                } for i in df.columns.values[:4]],
                value = 'sepal length',


            ),style = {
                 'margin' : {
                       'right': 200,
                       'left': 200

                         },
                 'padding-right': 600,
                 'padding-left': 600,
                 'textAlign': 'center'
                         }


        ),
        dcc.Graph(id="my-graph")


])


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-dropdown', 'value')])
def update_figure(selected):

    traces=[]
    for i in df['class'].unique():
        dff = df[df['class'] == i]
        traces.append(go.Box(
                y= dff[selected],
                name= i,
                marker={"size": 4}

        ))

    return {

        "data": traces,
        "layout": go.Layout(
                    #width = 1000,
                    margin={"l":100,"b":100,"r":100},
                    xaxis={
                        "title": "Species",

                    },
                    yaxis={
                        "title": selected.title(),
                        "range": [0,8],
                        "tick0": 0,
                        "dtick" : 0.5,
                        "showgrid": False
                    }
        )



    }
if __name__ == '__main__':
    app.run_server(debug=True)



