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

queue = []
# dict = {'Name':['Martha', 'Tim', 'Rob', 'Georgia'],
#         'Maths':[87, 91, 97, 95],
#         'Science':[83, 99, 84, 76]
#        }
# df = pd.DataFrame(dict)



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
                                id='adding-rows-table',
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
                        daq.StopButton(buttonText=buttonText, id='submit-val', n_clicks=0)
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
    Output('adding-rows-table', 'data'),
    Input('add-command', 'n_clicks'),
    State('adding-rows-table', 'data'),
    State('adding-rows-table', 'columns'),
    State(component_id='param',component_property='value'),
    State(component_id='target_val', component_property='value'),
    State(component_id='rate', component_property='value'))
def add_row(n_clicks, rows, columns, param, target_val, rate):
    if n_clicks > 0:
        rows.append({'task': param, 'target value':target_val, 'target rate': rate, 'timestamp': ''})
    return rows


# @app.callback(Output('live-graph', 'figure'),
#                 [Input('graph-update', 'n_intervals')])
# def update_graph(input_data):
#     global X
#     global Y
#     X.append(X[-1]+1)
#     Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
#     data = go.Scatter(
#         x=list(X),
#         y=list(Y),
#         name='Scatter',
#         mode = 'lines+markers'
#     )
#     return {'data':[data], 'layout': go.Layout(xaxis = dict(range=[min(X), max(X)]),
#                                                 yaxis = dict(range=[min(Y), max(Y)])
#     )}

# @app.callback(
#     Output(component_id='table', component_property=''),
#     Input(component_id='add-command', component_property='n_clicks'),

# )
# def update_queue(param,target_val,rate,n_clicks):
#     #g current date and time
#     now = datetime.now()
#     n_clicks = None
#     if n_clicks != None:
#         df2 = {'task': param, 'target value':target_val, 'target rate': rate, 'timestamp': datetime.now(now)}
#         df = df.append(df2, ignore_index = True)
#         print("hi")

#     return df.to_dict('records')

# @app.callback(
#     Output('table', 'columns'),
#     Input('add-command', 'n_clicks'),
#     State('table', 'data'),
#     State('table', 'columns'))
# def add_row(n_clicks, rows, columns):
#     if n_clicks > 0:
#         rows.append({c['id']: '' for c in columns})
#     return rows

@app.callback(
    Output(component_id='submit-val', component_property='buttonText'),
    Input(component_id='submit-val', component_property='n_clicks')
)
def toggle_queue(n_clicks):
    if n_clicks != None:
        buttonText = 'False'
        
        

if __name__ == '__main__':
    app.run_server(debug=True)