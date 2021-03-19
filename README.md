# PPMS_SR860_Software
Python Software to interface with the Dynacool PPMS and SR860 Lock-in Amplifier

## Introduction

The Dynacool PPMS is a Physical Property Measurement System from Quantum Design used to measure electrical transport, magnetometry, thermal measurements, etc.\
\
General Infoabout the PPMS can be found [here](https://www.qdusa.com/products/dynacool.html) 

### Import 

```
from qcodes.instrument_drivers.QuantumDesign.DynaCoolPPMS.DynaCool import DynaCool
```

Additionally, the Mundy Lab uses a Dual Phase Lock-in Amplifier, the SR860.\
\
General Info about the SR860 Lock-in can be found [here](https://www.thinksrs.com/products/sr860.html)

## Software Documentation

| Name | Usage | URL |
| --- | --- | --- |
| Dynacool PPMS | Docs for PPMS  | https://qcodes.github.io/Qcodes/examples/driver_examples/Qcodes%20example%20with%20DynaCool%20PPMS.html
| SR860 Lock-In | Docs for SR860 Lock-In | https://pymeasure.readthedocs.io/en/latest/api/instruments/srs/sr860.html
| Keithley 6221 | AC/DC current source | https://pymeasure.readthedocs.io/en/latest/api/instruments/keithley/keithley6221.html
| Instrumental | lab controls | https://instrumental-lib.readthedocs.io/en/stable/index.html

