import serial
import serial.tools.list_ports

class VALIDATE:
    def __init__(self):
        self.validated = 0b0000000
        self.checks = {
            'DEVICES': 1 << 0,
            'GPS': 1 << 1,
            'FT232': 1 << 2
        }
        self.devices_list = {}

    def devices(self):
        self.validated |= self.checks['DEVICES']

        ports = serial.tools.list_ports.comports()

        for port in ports:
            if "GPS" in port.description:
                self.validated |= self.checks['GPS']
                self.devices_list['GPS'] = port
            if "FT232" in port.description:
                self.validated |= self.checks['FT232']
                self.devices_list['FT232'] = port
        
        return self.devices_list
    
    def outputs(self):
        return False
    
    def result(self):
        return self.validated

# Example usage

