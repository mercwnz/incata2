import pyubx2
import serial

# https://github.com/semuconsulting/pyubx2/tree/master
# https://github.com/semuconsulting/pyubx2/tree/master
# https://github.com/semuconsulting/pyubx2/tree/master

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
    
    def reset_to_defaults(self):
        if self.serial:
            try:
                # Create the UBX-CFG-CFG message to reset to defaults
                msg = pyubx2.UBXMessage('CFG', 'CFG-CFG', pyubx2.SET, clearMask=0x1F1F, saveMask=0, loadMask=0x1F1F)
                self.serial.write(msg.serialize())
                print("Device reset to default settings.")
            except Exception as e:
                print(f"Failed to reset device: {e}")
        else:
            print("No active connection.")

    def read_and_print_stream(self):
        if self.ubr:
            try:
                while True:
                    (raw_data, parsed_data) = self.ubr.read()
                    if parsed_data:
                        print(parsed_data)
            except KeyboardInterrupt:
                print("Stream reading interrupted by user.")
            except Exception as e:
                print(f"Failed to read stream: {e}")
        else:
            print("No active connection.")

def test_ublox():
    device = ublox('/dev/ttyUSB0', 9600)  # Example port and baudrate
    device.connect()
    device.initialize_device()
    device.reset_to_defaults()
    device.read_and_print_stream()
    device.disconnect()

if __name__ == "__main__":
    test_ublox()
