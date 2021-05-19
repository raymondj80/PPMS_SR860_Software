# PyQD
Control of QD PPMS system

The code here works by passing messages to the PPMS computer.

For local use, switch _HOST in server_params.py to "localhost". 
Otherwise, set to the ip address of the PPMS computer.

Using one terminal window, run myserver.py. The PPMS computer
is now listening to commands.

Open a new terminal window, and run commands from the
RemoteQDInstrument package (example set_temperature...).
You can use the notebook as an example or create your own
experiment.

