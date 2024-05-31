import json
import serial
import serial.tools.list_ports
import subprocess
import obd
from obd import OBDStatus

class VALIDATE:
    def __init__(self):
        self.checks = {
            'GPS_DEVICE': 1 << 0,
            'GPS_OUTPUT': 1 << 1,
            'FT232_DEVICE': 1 << 2,
            'FT232_OUTPUT': 1 << 3,
            'FT232_CONNECTED': 1 << 4,
        }
        self.devices_list = {}
        self.validated = 0b0000000

        self.devices()
        self.gps_output()
        self.ft232_output()

    def devices(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "GPS" in port.description:
                self.validated |= self.checks['GPS_DEVICE']
                self.devices_list['GPS'] = port.device
            if "FT232" in port.description:
                self.validated |= self.checks['FT232_DEVICE']
                self.devices_list['FT232'] = port.device
        
        return self.devices_list
    
    def gps_output(self):
        process = subprocess.Popen(['gpspipe', '-w -n 100'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            lines_read = 0
            while lines_read < 100:  # Limit the number of lines read
                line = process.stdout.readline()  # type: ignore
                if line:
                    json_data = json.loads(line.strip())
                    
                    if json_data["class"] == "DEVICES":
                        devices = json_data.get('devices', [])
                        if devices:
                            for data in devices:
                                path = data.get('path', 'N/A')
                                driver = data.get('driver', 'N/A')

                                if path == self.devices_list.get('GPS') and driver == 'NMEA0183':
                                    self.validated |= self.checks['GPS_OUTPUT']
                                    print(f"GPS Connection Status: Available")
                                    break
                lines_read += 1

        except KeyboardInterrupt:
            print("Stopping GPS read...")
        finally:
            process.terminate()
            process.wait()


    def ft232_output(self):
        port = self.devices_list.get('FT232')
        if not port:
            print("FT232 device not found")
            return
        
        connection = None  # Initialize the connection variable
        try:
            obd.logger.removeHandler(obd.console_handler)
            connection = obd.OBD(port)
            status = connection.status()

            if status == OBDStatus.CAR_CONNECTED:
                print("OBD2 Connection Status: Car Connected")
                self.validated |= self.checks['FT232_CONNECTED']

            elif status == OBDStatus.OBD_CONNECTED:
                print("OBD2 Connection Status: OBD Connected (ignition off)")
                self.validated |= self.checks['FT232_CONNECTED']

            elif status == OBDStatus.ELM_CONNECTED:
                print("OBD2 Connection Status: ELM Connected")
                self.validated |= self.checks['FT232_CONNECTED']

            elif status == OBDStatus.NOT_CONNECTED:
                raise Exception("Device Not Connected")
            
            else:
                raise Exception("Failed To Connect")

            if connection.status() in [OBDStatus.CAR_CONNECTED, OBDStatus.OBD_CONNECTED, OBDStatus.ELM_CONNECTED]:
                self.validated |= self.checks['FT232_OUTPUT']
                
        except Exception as e:
            print(f"Caught an exception: {e}")
        finally:
            if connection:
                connection.close()
                
    def result(self):
        return self.validated
