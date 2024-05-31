import serial
import time
import logging
import obd
from obd import OBDStatus

class OBD2:
    def test(self, device, wait_time=10, debug=False):
        if debug:
            obd_logger = logging.getLogger('obd')
            obd_logger.setLevel(logging.DEBUG)
            obd_logger.propagate = False
        else:
            obd.logger.removeHandler(obd.console_handler)

        baudrate = 38400
        try:
            with serial.Serial(device[0], baudrate=baudrate, timeout=1) as ser:
                print(f"Connected to OBD device on port: {device[0]} at {baudrate} baud")
                start_time = time.time()
                while time.time() - start_time < wait_time:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if debug:
                        print(line)
                    if 'ELM327' in line:
                        port = device[0]
                        connection = obd.OBD(port)  # create connection with the specified port
                        status = connection.status()
                        if status == OBDStatus.CAR_CONNECTED:
                            print("OBD2 Connection Status: Car Connected")
                        elif status == OBDStatus.OBD_CONNECTED:
                            print("OBD2 Connection Status: OBD Connected (ignition off)")
                        elif status == OBDStatus.ELM_CONNECTED:
                            print("OBD2 Connection Status: ELM Connected")
                        elif status == OBDStatus.NOT_CONNECTED:
                            print("Error: Not Connected")
                        else:
                            print("Failed to connect to OBD2 device")
                        return f"OBD2 status: {status} from {device[0]} ({device[1]})"
                return f"No valid ELM327 response from {device[0]} ({device[1]})"
        except serial.SerialException as e:
            return f"Could not open serial port {device[0]} at {baudrate} baud: {e}"
        except KeyboardInterrupt:
            return "Exiting..."
