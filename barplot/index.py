import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app1 import app
from apps import new, code

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    print(pathname)
    if pathname == '/apps/code':
         return code.code_layout
    else:
        return new.app_layout


if __name__ == '__main__':
    app.run_server(debug=True)