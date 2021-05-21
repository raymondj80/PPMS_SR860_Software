import dash
from datetime import datetime
from pymeasure.instruments.srs import SR860
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_daq as daq
import dash_table
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly
import random 
import plotly.graph_objs as go
from time import sleep
import pandas as pd
from RemoteQDInstrument import remoteQDInstrument
from server_params import _HOST, _PORT

queue = []

# rQD.temperature

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
buttonText = 'Start'
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.DataFrame(
    columns = ['task', 'target value', 'target rate', 'timestamp']
    )
     
app.layout = html.Div(
    [
        dcc.Tabs([
        dcc.Tab(label='Control Panel', children=[
            html.Div([
                            dcc.Dropdown(
                                id='param',
                                options=[
                                    {'label': 'Set Temperature', 'value': 'temperature'},
                                    {'label': 'Set Field', 'value': 'field'},
                                    {'label': 'Set Position', 'value': 'position'}
                                ],
                                value='temp'
                            ),
                            html.Div([
                                    dcc.Input(
                                        id="target_val",
                                        type='number',
                                        placeholder="target",
                                    ),
                                    dcc.Input(
                                        id="rate",
                                        type='number',
                                        placeholder="rate",
                                    ),
                                    daq.BooleanSwitch(
                                        id='my-boolean-switch',
                                        on=False
                                    ),
                                    html.Div(id='boolean-switch-output'),   
                                ],
                                style={'flex-direction':'row'}
                            ),
                            html.Button('Add', id='add-command', n_clicks=0),
                            dash_table.DataTable(
                                id='task-queue',
                                columns=[{
                                    'name': i,
                                    'id': i,
                                    'deletable': True,
                                    'renamable': True
                                } for i in df.columns],
                                data=df.to_dict('records'),
                                editable=True,
                                row_deletable=True
                      ),
                        ]),
                        html.Div(id='body-div'),
                        daq.StopButton(buttonText='Start', id='start-button', n_clicks=0),
                        daq.StopButton(buttonText='Stop', id='stop-button', n_clicks=0),
                        html.Div(id='queue-output'),
                        daq.Gauge(
                            showCurrentValue=True,
                            id='gauge-temp',
                            label='temperature',
                            max=400,
                            min=0,
                            value=6
                        ),
                        daq.Gauge(
                            id='gauge-field',
                            label='field',
                            max=9,
                            min=-9,

                            value=6
                        ),
                        html.Button('Gauge', id='gauge-button', n_clicks=0)
                        # dcc.Interval(
                        #     id='gauge-update',
                        #     interval=5000
                        # )
        ]),
        dcc.Tab(label='Graphs', children=[
            dcc.Graph(id='live-graph', animate=True),
            dcc.Interval(
                id='graph-update',
                interval=1000
            ),
        ]),
        ]),
    ]
)

@app.callback(
    Output("target_val", "placeholder"),
    [Input("param", "value")]
)
def update_target_val(value):
    return "target {}".format(value)

@app.callback(
    Output("rate", "placeholder"),
    [Input("param", "value")]
)
def update_input_rate(value):
    return "{} rate".format(value)

@app.callback(
    Output('task-queue', 'data'),
    Input('add-command', 'n_clicks'),
    State('task-queue', 'data'),
    State('task-queue', 'columns'),
    State(component_id='param',component_property='value'),
    State(component_id='target_val', component_property='value'),
    State(component_id='rate', component_property='value'))
def add_row(n_clicks, rows, columns, param, target_val, rate):
    if n_clicks > 0:
        rows.append({'task': param, 'target value':target_val, 'target rate': rate, 'timestamp': ''})
    return rows

@app.callback(
    Output('queue-output', 'children'),
    Input('start-button', 'n_clicks'),
    State('task-queue', 'data'),
    State('task-queue', 'columns')
)
def start_queue(n_clicks, rows, columns):
    df = pd.DataFrame(rows, columns=[c['name'] for c in columns])
    # print('hi')
    if n_clicks > 0:
        return df.to_string()

# @app.callback(
#     Output('gauge-temp', 'value'),
#     Input('gauge-button', 'n_clicks')
# )    
# def update_gauge_temp(n_clicks):
#     if n_clicks > 0:
#         rQD = remoteQDInstrument(instrument_type="DYNACOOL",host=_HOST, port=_PORT)
#         rQD.connect_socket()
#         temp=rQD.temperature
#         rQD.close_socket()
#         return float(temp)


@app.callback(
    Output('gauge-field', 'value'),
    Input('gauge-button', 'n_clicks')
)    
def update_gauge_field(n_clicks):
    if n_clicks > 0:
        rQD = remoteQDInstrument(instrument_type="DYNACOOL",host=_HOST, port=_PORT)
        rQD.connect_socket()
        field=rQD.field
        rQD.close_socket()
        return float(field)

if __name__ == '__main__':
    app.run_server(debug=True)