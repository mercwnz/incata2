import pyubx2
import serial

class ublox:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.ubr = None
    
    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=3)
            self.ubr = pyubx2.UBXReader(self.serial)
            print(f"Connected to {self.port} at {self.baudrate} baudrate.")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def disconnect(self):
        if self.serial:
            self.serial.close()
            print(f"Disconnected from {self.port}.")
        else:
            print("No active connection to close.")
    
    def read_message(self):
        if self.ubr:
            try:
                (raw_data, parsed_data) = self.ubr.read()
                return parsed_data
            except Exception as e:
                print(f"Failed to read message: {e}")
        else:
            print("No active connection.")
    
    def initialize_device(self):
        # This method can be expanded with actual initialization commands as needed
        print("Device initialized.")
        # Example: sending a configuration message
        # msg = pyubx2.UBXMessage('CFG', 'CFG-PRT', SET, baudrate=self.baudrate, ...)
        # self.serial.write(msg.serialize())

def test_ublox():
    device = ublox('/dev/ttyUSB0', 9600)  # Example port and baudrate
    device.connect()
    device.initialize_device()
    print(device.read_message())
    device.disconnect()

if __name__ == "__main__":
    test_ublox()
