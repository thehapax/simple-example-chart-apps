#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 15:38:16 2019

@author: divyachandran
"""

import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv("https://raw.githubusercontent.com/divyachandran-ds/Datascience/master/bchealth.csv")

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

font = ["Arial", "Open Sans", "Balto", "Courier New", "PT Sans Narrow", "Times New Roman", "Comic Sans MS",
        "cursive"]

app.layout = html.Div([
    html.Div([
        html.H1("British Columbia Health")], style={"text-align": "center"}),
    html.Div([
        html.Div([
            html.P("Toggling Axes Lines, Ticks, Labels", className="row",
                   style={"text-align": "center", "text-decoration": "underline"}),
            html.Div([
                html.Span("Grid-Lines", className="four columns", style={"text-align": "right"}),
                html.Div(
                    dcc.RadioItems(
                        id='grid-type',
                        options=[{'label': "Show", 'value': 1}, {'label': "Hide", 'value': 0}],
                        value=1,
                        labelStyle={'display': 'inline', "padding": 10}
                    ), className="eight columns"
                )
            ], className="row"),
            html.Div([
                html.Span("Tick-Labels", className="four columns", style={"text-align": "right"}),
                html.Div(
                    dcc.RadioItems(
                        id='label-type',
                        options=[{'label': "Show", 'value': 1}, {'label': "Hide", 'value': 0}],
                        value=1,
                        labelStyle={'display': 'inline', "padding": 10}
                    ), className="eight columns"
                )
            ], className="row"),
            html.Div([
                html.Span("Line", className="four columns", style={"text-align": "right"}),
                html.Div(
                    dcc.RadioItems(
                        id='line-type',
                        options=[{'label': "Show", 'value': 1}, {'label': "Hide", 'value': 0}],
                        value=1,
                        labelStyle={'display': 'inline', "padding": 10}
                    ), className="eight columns"
                )
            ], className="row"),
        ], className="row", style={"border-bottom": "1px solid #979797"}),
        html.Div([
            html.Span("Range of Axes", className="column",
                      style={"text-align": "center", "text-decoration": "underline"}),
            html.Div([dcc.Input(id='min-range', type='number', value=0, style={"width": "25%"}),
                      dcc.Input(id='max-range', type='number', value=50, style={"width": "25%"}),
                      html.Button('Submit', id='button', style={"width": "40%"})
                      ], className="column")
        ], className="row", style={"border-bottom": "1px solid #979797", "padding": 5}),

        html.Div([
            html.Div([
                html.P("Tick : Color and Style", className="row",
                       style={"text-align": "center", "text-decoration": "underline"}),

                html.Div([
                    html.Div(
                        daq.ColorPicker(
                            id='tick-color-picker',
                            label='Tick color',
                            size=150,
                            value={"hex": "#CFD0E0"},
                        )
                    )
                ], className="row"),
                html.Div([
                    html.Span("Tick Size", className="row", style={"text-align": "center"}),
                    html.Div([dcc.Input(id='length', type='number', value=10, style={"width": "25%"}),
                              dcc.Input(id='width', type='number', value=10, style={"width": "25%"}),
                              html.Button('Submit', id='size-button', style={"width": "40%", "padding": 1})
                              ], className="row", style={"padding": 3})
                ], className="row"),
            ], className="six columns",
                style={"width": "48%", "margin": 0, "float": "left", "border-right": "1px solid #979797"}),

            html.Div([
                html.P("Axes : Color and Style", className="row",
                       style={"text-align": "center", "text-decoration": "underline"}),
                html.Div([
                    html.Div(
                        daq.ColorPicker(
                            id='axes-color-picker',
                            label='Axes Color',
                            size=150,
                            value={"hex": "#080808"},
                        )
                    )
                ], className="row"),
                html.Div([
                    html.Span("Axes Font", className="row", style={"text-align": "center"}),
                    html.Div(
                        dcc.Dropdown(id="axes-font",
                                     options=[{'label': i, 'value': i} for i in font],
                                     value="Open Sans",
                                     placeholder="Select a font", ), className="row"
                    )
                ], className="row", style={"padding": 8}),

            ], className="six columns", style={"width": "48%", "margin": 0, "float": "left"}),

        ], className="row", style={"padding": 5})

    ], className="five columns", style={"border": "1px solid #979797", "width": "48%", "margin": 0, "float": "left"}),

    html.Div([
        dcc.Dropdown(id="select-hsda",
                     options=[{'label': 'East Kootenay', 'value': '11 - East Kootenay'},
                              {'label': 'Kootenay/Boundary', 'value': '12 - Kootenay/Boundary'},
                              {'label': "Okanagan", 'value': '13 - Okanagan'},
                              {'label': 'Thompson/Cariboo', 'value': '14 - Thompson/Cariboo'},
                              {'label': 'Fraser East', 'value': '21 - Fraser East'},
                              {'label': 'Fraser North', 'value': '22 - Fraser North'},
                              {'label': 'Fraser South', 'value': '23 - Fraser South'},
                              {'label': 'Richmond', 'value': '31 - Richmond'},
                              {'label': "Vancouver", 'value': '32 - Vancouver'},
                              {'label': "North Shore/Coast Garibaldi", 'value': '33 - North Shore/Coast Garibaldi'},
                              {'label': "South Vancouver Island", 'value': '41 - South Vancouver Island'},
                              {'label': "Central Vancouver Island", 'value': '42 - Central Vancouver Island'},
                              {'label': "North Vancouver Island", 'value': '43 - North Vancouver Island'},
                              {'label': "Northwest", 'value': '51 - Northwest'},
                              {'label': "Northern Interior", 'value': '52 - Northern Interior'},
                              {'label': "Northeast", 'value': '53 - Northeast'}, ],
                     value='31 - Richmond', ),
        dcc.Graph(id="my-graph"),
    ], className="seven columns", style={"width": "48%", "margin": 0, "float": "right"})

], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('grid-type', 'value'),
     Input('label-type', 'value'),
     Input('line-type', 'value'),
     Input('tick-color-picker', 'value'),
     Input('size-button', 'n_clicks'),
     Input('axes-color-picker', 'value'),
     Input('axes-font', 'value'),
     Input('select-hsda', 'value'),
     Input('button', 'n_clicks')],
    [State('length', 'value'),
     State('width', 'value'),
     State('min-range', 'value'),
     State('max-range', 'value')])
def update_figure(grid, label, line, tick_color, n_clicks1, axes_color, axes_font, selected, n_clicks2, len, width, min,
                  max):
    color1 = tick_color["hex"]
    color2 = axes_color["hex"]
    dff = df[df["HSDA"] == selected]
    list = []
    for n in df['SPECIALTY'].unique():
        word = n.split('- ')[1]
        list.append(word.title())

    trace1 = go.Scatter(

        x=df['SPECIALTY'],
        y=dff['PAYMENTS'],
        mode='markers',
        name="Expenses",
        marker={
            "color": "#008D00",
            "size": 8
        }

    )
    trace2 = go.Scatter(

        x=df['SPECIALTY'],
        y=dff['PRACTITIONERS'],
        mode='markers',
        marker={
            "color": "#FF6262",
            "size": 8
        },
        name="Practitioners",
        yaxis="y2"
    )
    layout = go.Layout(
        title="Expenditure & Number of Practitioners vs Speciality",
        showlegend=False,
        height=500,
        xaxis={
            "showgrid": bool(grid),
            "showline": bool(line),
            "showticklabels": bool(label),
            "tickcolor": color1,
            "ticklen": len - 4,
            "tickwidth": width - 4,
            "title": {
                "text": f"Speciality",
                "font": {"family": axes_font, "color": color2}
            },
            "tickmode": "array",
            "tickangle": 40,
            "tickvals": df['SPECIALTY'].unique(),
            "ticktext": list,
            "tickfont": {"size": 7},

        },

        yaxis={
            "showgrid": bool(grid),
            "showline": bool(line),
            "showticklabels": bool(label),
            "tickcolor": color1,
            "range": [min + 1000, max * 100000],
            "ticklen": len,
            "tickwidth": width,
            "title": {
                "text": f"Expenses (CAD)",
                "font": {"family": axes_font, "color": color2}
            }

        },
        yaxis2={
            "showgrid": bool(grid),
            "showline": bool(line),
            "showticklabels": bool(label),
            "tickcolor": color1,
            "range": [min, max],
            "ticklen": len,
            "tickwidth": width,
            "title": {
                "text": f"Number of Practitioners",
                "font": {"family": axes_font, "color": color2}
            },
            "overlaying": 'y',
            "side": 'right'
        }

    )

    return {

        "data": [trace1, trace2],
        "layout": layout

    }


if __name__ == '__main__':
    app.run_server(debug=True)
