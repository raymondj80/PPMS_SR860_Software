from flask import Flask
from qcodes.instrument_drivers.QuantumDesign.DynaCoolPPMS.DynaCool import DynaCool

app = Flask(__name__)

# Connects to the local TCPIP address from running server.py on the local machine"
dynacool = DynaCool('dynacool', address="TCPIP0::127.0.0.1::5000::SOCKET")
dynacool.print_readable_snapshot(update=True)

@app.route('/idn')
def idn():
    return dynacool.get_idn()

app.run('0.0.0.0',1234)
# Basic tests


dynacool.close()