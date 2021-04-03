import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_html_components as html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dbc.Button("Open", id="open-centered"),
        dbc.Modal(
            [
                dbc.ModalHeader("Select Command"),
                dbc.ModalBody(
                        html.Div([
                            dcc.Dropdown(
                                id='param',
                                options=[
                                    {'label': 'Set Temperature', 'value': 'temperature (K)'},
                                    {'label': 'Set Field', 'value': 'field (T)'},
                                    {'label': 'Set Position', 'value': 'position (nm)'}
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
def update_input(value):
    return "target {}".format(value)

@app.callback(
    Output("modal-centered", "is_open"),
    [Input("open-centered", "n_clicks"), Input("close-centered", "n_clicks"), Input("add-command", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, n3, is_open):
    if n1 or n2 or n3:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)