# gps/devices.py

import serial
import serial.tools.list_ports
import time
from .nmea import NMEA

class DEVICES:
    def __init__(self):
        self.devices_list = []

    def find_gps_devices(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "GPS" in port.description:
                self.devices_list.append(port)
        return [(port.device, port.description) for port in self.devices_list]

    def test_device(self, device, wait_time=10, debug=False):
        baudrate = 9600
        nmea_parser = NMEA()
        command = b'\xB5\x62'  # Example U-Blox command
        line_count = 0
        try:
            with serial.Serial(device[0], baudrate=baudrate, timeout=1) as ser:
                print(f"Connected to GPS device on port: {device[0]} at {baudrate} baud")
                if debug:
                    print(f"Sending command to GPS device: {command}")
                ser.write(command)
                start_time = time.time()
                while line_count < 10 and (time.time() - start_time < wait_time):
                    line = ser.readline().decode('ascii', errors='replace').strip()
                    if line:
                        line_count += 1
                        if debug:
                            print(line)
                        if "*" in line:
                            if not nmea_parser.parse_sentence(line):
                                return f"Failed to parse NMEA sentence from {device[0]} ({device[1]})"
                            if nmea_parser.get_last_sentence_type():
                                return f"NMEA response ({nmea_parser.get_last_sentence_type()}) received from {device[0]} ({device[1]})"
                return f"No valid NMEA response from {device[0]} ({device[1]})"
        except serial.SerialException as e:
            return f"Could not open serial port {device[0]} at {baudrate} baud: {e}"
        except KeyboardInterrupt:
            return "Exiting..."
