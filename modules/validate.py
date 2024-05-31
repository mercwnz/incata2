import serial
import serial.tools.list_ports
import obd
from obd import OBDStatus
class VALIDATE:
    def __init__(self):
        self.validated = 0b0000000
        self.checks = {
            'DEVICE_GPS': 1 << 0,
            'DEVICE_FT232': 1 << 1,
            'OUTPUT_GPS': 1 << 2,
            'OUTPUT_FT232': 1 << 3,
        }
        self.devices_list = {}

    def devices(self):
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "GPS" in port.description:
                self.validated |= self.checks['DEVICE_GPS']
                self.devices_list['GPS'] = port.device
            if "FT232" in port.description:
                self.validated |= self.checks['DEVICE_FT232']
                self.devices_list['FT232'] = port.device
        
        return self.devices_list
    
    def outputs(self):
        port = self.devices_list['FT232']
        try:
            obd.logger.removeHandler(obd.console_handler)
            connection = obd.OBD(port)
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
            if connection:
                self.validated |= self.checks['OUTPUT_FT232']
                connection.close()
        except:
            return False
    
    def result(self):
        return self.validated