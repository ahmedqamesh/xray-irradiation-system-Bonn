
''' Example how to use different laboratory devices (Source, pulsers, etc.) that understand SCPI.
    The language (SCPI) is independent of the interface (TCP, RS232, GPIB, USB, etc.). The interfaces
    can be choosen by an appropriate transportation layer (TL). This can be a VISA TL and
    a Serial TL at the moment. VISA TL is recommendet since it gives you access to almost
    all laboratory devices (> 90%) over TCP, RS232, USB, GPIB (Windows only so far).
    '''
from basil.dut import Dut
import os
rootdir = os.path.dirname(os.path.abspath(__file__))

# Talk to a Keithley device via serial port using pySerial
dut = Dut(rootdir+"/keithley2400_pyserial.yaml")
dut.init()
dut['Keithley'].write(":OUTP ON")
dut['Keithley'].write("*RST")
dut['Keithley'].write(":SOUR:VOLT:RANG 60")
dut['Keithley'].IV_test(directory = rootdir+"/sourcemeter_scan_results",
                        currentLimit=1.0e-06,
                        start_V=0,
                        step_V=2,
                        end_V=20,
                        stat_delay=2,
                        Itterations=2,
                        Plot=True,
                        diodes=["C"])
dut['Keithley'].write(":OUTP OFF")