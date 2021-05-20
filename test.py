import socket
import sys
from time import sleep
from RemoteQDInstrument import remoteQDInstrument
from server_params import _HOST, _PORT

import RemoteQDInstrument
rQD = remoteQDInstrument(instrument_type="DYNACOOL",host=_HOST, port=_PORT)
rQD.connect_socket()

while(rQD.temperature_status() != 'R'):
    print(rQD.temperature)
    
rQD.close_socket()