# obd2/devices.py

import serial
import serial.tools.list_ports
import time
import obd
from obd import OBDStatus
import logging

class DEVICES:
    def __init__(self):
        self.devices_list = []

    def find_obd_devices(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "FT232" in port.description:
                self.devices_list.append(port)
        return [(port.device, port.description) for port in self.devices_list]

    def test_device(self, device, wait_time=10, debug=False):
        if debug:
            # Configure the obd logger separately to avoid double logging
            obd_logger = logging.getLogger('obd')
            obd_logger.setLevel(logging.DEBUG)
            obd_logger.propagate = False  # Prevent propagation to the root logger
        else:
            obd.logger.removeHandler(obd.console_handler)

        baudrate = 38400
        command = b'ATZ\r'  # Example ELM327 command
        try:
            with serial.Serial(device[0], baudrate=baudrate, timeout=1) as ser:
                print(f"Connected to OBD device on port: {device[0]} at {baudrate} baud")
                if debug:
                    print(f"Sending command to OBD device: {command}")
                ser.write(command)
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
                            print("Successfully connected to OBD2 device")
                            print("OBD2 Connection Status: Car Connected")
                        elif status == OBDStatus.OBD_CONNECTED:
                            print("Successfully connected to OBD2 device")
                            print("OBD2 Connection Status: OBD Connected (ignition off)")
                        elif status == OBDStatus.ELM_CONNECTED:
                            print("Successfully connected to OBD2 device")
                            print("OBD2 Connection Status: ELM Connected")
                        elif status == OBDStatus.NOT_CONNECTED:
                            print("Failed to connect to OBD2 device")
                            print("Error: Not Connected")
                        else:
                            print("Failed to connect to OBD2 device")
                            print(f"Error: {status}")
                        return f"OBD2 status: {status} from {device[0]} ({device[1]})"
                return f"No valid ELM327 response from {device[0]} ({device[1]})"
        except serial.SerialException as e:
            return f"Could not open serial port {device[0]} at {baudrate} baud: {e}"
        except KeyboardInterrupt:
            return "Exiting..."
