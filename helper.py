import socket
import sys
from time import sleep
from RemoteQDInstrument import remoteQDInstrument
from server_params import _HOST, _PORT
import RemoteQDInstrument

class RemoteQDHelper:
    def __init__(self):
        self.rQD = remoteQDInstrument(instrument_type="DYNACOOL",host=_HOST, port=_PORT)
        self.rQD.connect_socket()

    def get_temp(self):
        temp = float(self.rQD.temperature)
        return temp

rqdh = RemoteQDHelper()
rqdh.get_temp()
rqdh.get_temp()
rqdh.get_temp()


        