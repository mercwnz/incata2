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
            'FT232_CONNECTED' : 1 << 4,
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
        process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    json_data = json.loads(line.strip())
                    
                    if json_data["class"] == "DEVICES":
                        devices = json_data.get('devices', 'N/A')
                        print(devices)
                        self.validated |= self.checks['GPS_OUTPUT']
                        break

        except KeyboardInterrupt:
            print("Stopping GPS data read...")
        finally:
            process.terminate()
            process.wait()


    def ft232_output(self):
        port = self.devices_list['FT232']
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

            if connection:
                self.validated |= self.checks['FT232_OUTPUT']
                connection.close()
                
        except ValueError as e:
            print(f"Caught an exception: {e}")
            
    def result(self):
        return self.validated