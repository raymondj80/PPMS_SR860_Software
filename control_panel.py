import sys
import random
import tempfile
from time import sleep

import logging
log = logging.getLogger('')
log.addHandler(logging.NullHandler())

from qcodes.instrument_drivers.QuantumDesign.DynaCoolPPMS.DynaCool import Dynacool
from pymeasure.log import console_log
from pymeasure.experiment import Procedure, IntegerParameter, Parameter, FloatParameter, ListParameter, BooleanParameter
from pymeasure.experiment import Results
from pymeasure.display.Qt import QtGui
from pymeasure.display.windows import ManagedWindow

class RunPPMS(Procedure):
    command_list = {
        'Set Field': 0,
        'Set Temp': 1
    }

    execute = 0
    command = ListParameter('Command',choices=['Set Field','Set Temp'])
    use_rate = BooleanParameter('Use Rate', default=1)
    rate = FloatParameter('Rate',default=0,units=None)
    target = FloatParameter('Target',units=None)
    delay = FloatParameter('Delay Time', units='s', default=0.2)

    DATA_COLUMNS = ['Temperature', 'Field']

    def startup(self):
        log.info("Intializing PPMS")
        dynacool = Dynacool('dynacool', address="TCPIP0::127.0.0.1::5000::SOCKET")
        log.info("Printing PPMS snapshot...")
        dynacool.print_readable_snapshot(update=True)

    def execute(self):
        log.info("Executing command...")
        command_id = command_list[self.command]

        if command_id == 0:
            if self.use_rate:
                log.info("Setting Non-blocking Field...")
                dynacool.field_rate(self.rate)
                dyancool.ramp(mode='non-blocking')
            else:
                log.info("Setting Blocking Field...")
                dynacool.ramp(mode='blocking')
            log.info("Setting Target Field...")
            dynacool.field_target(self.target)

        elif command_id == 1:
            if self.use_rate:
                log.info("Setting Gradual Temp...")
                dynacool.temperature_rate(self.rate)
            log.info("Setting Temperature Target")
            dynacool.temperature_setpoint(self.target)

        while (not target_reached):
            data = {
                'Temperature': dynacool.temperature(),
                'Field': dynacool.field_measured()
            }

            log.debug("Temp: %.2f Field: %.2f" %(data['Temperature'], data['Field']))
            var = DATA_COLUMNS[command_id]
            self.emit('results', data)
            self.emit('progress',100.*data[var]/self.target)
            
            target_reached = {
                'Set Field': self.target <= data['Magnitization'],
                'Set Temp': self.target <= data['Temperature']
            }[self.command]
                
            if self.should_stop():
                log.warning("Catch stop command in procedure")
                break

    def shutdown(self):
        log.info("Finished")


class MainWindow(ManagedWindow):

    def __init__(self):
        super(MainWindow, self).__init__(
            procedure_class=RunPPMS,
            inputs=['command','use_rate','rate','target','delay'],
            displays=['command','use_rate','rate','target','delay'],
            x_axis='Iteration',
            y_axis='Random Number'
        )
        self.setWindowTitle('Control Panel')

    def queue(self):
        filename = tempfile.mktemp()
        procedure = self.make_procedure()
        results = Results(procedure, filename)
        experiment = self.new_experiment(results)

        self.manager.queue(experiment)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())