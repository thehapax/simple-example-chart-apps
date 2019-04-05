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


df = pd.read_csv("https://raw.githubusercontent.com/divyachandran-ds/Datascience/master/bchealth.csv")

app = dash.Dash(__name__)

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
                    daq.BooleanSwitch(
                        id='grid-type',
                        label='Hide______Show',
                        labelPosition="bottom",
                        color="#2b7b26",
                        on=True,
                    ), className="eight columns"
                )
            ], className="row", style={"padding": 5}),
            html.Div([
                html.Span("Tick-Labels", className="four columns", style={"text-align": "right"}),
                html.Div(
                    daq.BooleanSwitch(
                        id='label-type',
                        label='Hide______Show',
                        labelPosition="bottom",
                        color="#2b7b26",
                        on=True,
                    ), className="eight columns"
                )
            ], className="row", style={"padding": 5}),
            html.Div([
                html.Span("Line", className="four columns", style={"text-align": "right"}),
                html.Div(
                    daq.BooleanSwitch(
                        id='line-type',
                        label='Hide______Show',
                        labelPosition="bottom",
                        color="#2b7b26",
                        on=True,
                    ), className="eight columns"
                )
            ], className="row", style={"padding": 5}),
        ], className="row", style={"border-bottom": "1px solid #979797"}),
        html.Div([
            html.Span("Range of Y-Axes", className="column",
                      style={"text-align": "center", "text-decoration": "underline"}),
            html.Div([dcc.RangeSlider(id='range',
                                      min=0,
                                      max=100,
                                      value=[0, 50],
                                      marks={i * 10: i * 10 for i in range(0, 11)}),
                      ], className="column", style={"margin": 0, "padding": 10})
        ], className="row", style={"border-bottom": "1px solid #979797", "padding": 15}),

        html.Div([
            html.Div([
                html.P("Tick : Color and Style (all axes)", className="row",
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
                    html.Span("Tick Size: Input length & width", className="row", style={"text-align": "center"}),
                    html.Div([dcc.Input(id='length', type='number', value=10, style={"width": "25%"}),
                              dcc.Input(id='width', type='number', value=10, style={"width": "25%"}),
                              html.Button('Submit', id='size-button', style={"width": "40%", "padding": 1})
                              ], className="row", style={"padding": 3})
                ], className="row", style={"padding-top": 15, "padding-bottom": 15}),
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
                ], className="row", style={"padding-top": 15, "padding-bottom": 15, "padding-left": 10}),

            ], className="six columns", style={"width": "48%", "margin": 0, "float": "left"}),

        ], className="row", style={"padding": 5})

    ], className="five columns", style={"border": "1px solid #979797", "width": "48%", "margin": 0, "float": "left"}),

    html.Div([
        html.Span("Health Service Delivery Areas", className="row", style={"text-align": "center"}),
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
    [Input('grid-type', 'on'),
     Input('label-type', 'on'),
     Input('line-type', 'on'),
     Input("range", 'value'),
     Input('tick-color-picker', 'value'),
     Input('axes-color-picker', 'value'),
     Input('axes-font', 'value'),
     Input('select-hsda', 'value'),
     Input('size-button', 'n_clicks')],
    [State('length', 'value'),
     State('width', 'value'),
     ])
def update_figure(grid, label, line, range, tick_color, axes_color, axes_font, selected, n_clicks, len, width):
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
        height=600,
        xaxis={
            "showgrid": grid,
            "showline": line,
            "showticklabels": label,
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
            "showgrid": grid,
            "showline": line,
            "showticklabels":label,
            "tickcolor": color1,
            "range": [range[0] + 1000, range[1] * 100000],
            "ticklen": len,
            "tickwidth": width,
            "title": {
                "text": f"Expenses (CAD)",
                "font": {"family": axes_font, "color": color2}
            }

        },
        yaxis2={
            "showgrid": grid,
            "showline": line,
            "showticklabels":label,
            "tickcolor": color1,
            "range": [range[0], range[1]],
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


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
