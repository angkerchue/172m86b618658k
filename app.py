import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
# import plotly.graph_objs as go

# import colorlover as cl
# import datetime as dt
import flask
# import os
import pandas as pd
# from pandas_datareader.data import DataReader
# import time
from dash.dependencies import Input, Output

app = dash.Dash('historical-vol')
server = app.server

app.scripts.config.serve_locally = False

df_symbol = pd.read_csv('vol-tickers.csv')
df_data = pd.read_csv('vol-data.csv', sep = ',', header = 0)
df_data['Date']=  pd.to_datetime(df_data['Date'], dayfirst = True)

app.layout = html.Div(children = [
    html.H2('Historical Volatility Explorer',
        style = {'display': 'inline',
            'float': 'left',
            'font-size': '1.88em',
            'margin-left': '8px',
            'font-weight': 'bolder',
            'font-family': 'Product Sans',
            'color': "rgba(118, 118, 118, 0.98)",
            'margin-top': '18px',
            'margin-bottom': '0'
        }
    ),

    dcc.Dropdown(
        id = 'vol-ticker-input',
        options = [{'label': s[0], 'value': str(s[1])}
                 for s in zip(df_symbol.Index, df_symbol.Symbol)],
        value = 'VIX',
    ),

    html.Div(id = 'output-graph'),

    # html.Div(dcc.RangeSlider(
    #     id = 'year-slider',
    #     min = min(df_data.Date),
    #     max = max(df_data.Date),
    #     step = 1,
    #     value = [min, max]
    #     ),
    #     style = {'padding': '0px 60px'}
    # )
])

@app.callback(
    Output(component_id = 'output-graph', component_property = 'children'),
    [Input(component_id = 'vol-ticker-input', component_property = 'value'),
    #Input(component_id = 'year-slider', component_property = 'value')
    ]
)

def update_value(input_data):
    
    # df.reset_index(inplace=True)
    # df.set_index("Date", inplace=True)
    # df = df.drop("Symbol", axis=1)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df_data.Date, 'y': df_data[str(input_data)], 'type': 'line', 'name': input_data},
            ],
            'layout': {
                # 'title': input_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True, port = 8050, host = '0.0.0.0')
