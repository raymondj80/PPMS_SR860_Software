import socket
import sys
from time import sleep
from RemoteQDInstrument import remoteQDInstrument
from server_params import _HOST, _PORT

import RemoteQDInstrument
rQD = remoteQDInstrument(instrument_type="DYNACOOL",host=_HOST, port=_PORT)
rQD.connect_socket()
print(rQD.temperature)
# rQD.set_temperature(302,2,wait=False)
# while(rQD.temperature_status() != 'Stable'):
#     print(rQD.temperature)
rQD.close_socket()