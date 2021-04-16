import dash
from pymeasure.instruments.srs import SR860
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly
import random 
import plotly.graph_objs as go
from collections import deque

X = deque(maxlen=20)
Y = deque(maxlen=20)
X.append(1)
Y.append(1)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        
        dcc.Graph(id='live-graph', animate=True),
        dcc.Interval(
            id='graph-update',
            interval=1000
        ),
        dbc.Button("Open", id="open-centered"),
        dbc.Modal(
            [

                dbc.ModalHeader("Select Command"),
                dbc.ModalBody(
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
                                        id="target-val",
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
                        ]
                        )
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button(
                            "Add", id='add-command', className='ml-auto'
                        ),
                        dbc.Button(
                            "Close", id="close-centered", className="ml-auto"
                        ),
                        
                    ]
                    
                ),
            ],

            id="modal-centered",
            centered=True,
            size="lg",
        ),
    ]
)

@app.callback(
    Output("target-val", "placeholder"),
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
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks"), Input("add-command", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open

@app.callback(Output('live-graph', 'figure'),
                [Input('graph-update', 'n_intervals')])
def update_graph(input_data):
    global X
    global Y
    X.append(X[-1]+1)
    Y.append(Y[-1]+Y[-1]*random.uniform(-0.1,0.1))
    data = go.Scatter(
        x=list(X),
        y=list(Y),
        name='Scatter',
        mode = 'lines+markers'
    )
    return {'data':[data], 'layout': go.Layout(xaxis = dict(range=[min(X), max(X)]),
                                                yaxis = dict(range=[min(Y), max(Y)])
    )}

# @app.route('/')
# def index():
#     l = []
#     # work on copy of joblist,
#     for job in list(joblist):
#         # task may be expired, refresh() will fail
#         try:
#             job.refresh()
#         except rq.exceptions.NoSuchJobError:
#             joblist.remove(job)
#             continue

#         l.append({
#             'id': job.get_id(),
#             'state': job.get_status(),
#             'progress': job.meta.get('progress'),
#             'result': job.result
#             })

#     return render_template('index.html', joblist=l)


# @app.route('/enqueuejob', methods=['GET', 'POST'])
# def enqueuejob():
#     job = jobs.approximate_pi.queue(int(request.form['num_iterations']))
#     joblist.append(job)
#     return redirect('/')


# @app.route('/deletejob', methods=['GET', 'POST'])
# def deletejob():
#     if request.args.get('jobid'):
#         job = rq.job.Job.fetch(request.args.get('jobid'), connection=jobs.rq.connection)
#         job.delete()
#     return redirect('/')



if __name__ == '__main__':
    app.run_server(debug=True)