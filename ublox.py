import serial
import struct
import time

class UBlox7:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.sync_chars = b'\xb5\x62'
        self.connect()

    def connect(self):
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            print("Connected to serial port.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.reconnect()

    def reconnect(self):
        if self.serial and self.serial.is_open:
            self.serial.close()
        time.sleep(2)  # Wait before reconnecting
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            print("Reconnected to the serial port.")
        except serial.SerialException as e:
            print(f"Failed to reconnect: {e}")
            self.serial = None

    def calc_checksum(self, msg_class, msg_id, payload):
        ck_a = 0
        ck_b = 0
        msg_length = len(payload)
        ck_a += msg_class
        ck_b += ck_a
        ck_a += msg_id
        ck_b += ck_a
        ck_a += msg_length & 0xFF
        ck_b += ck_a
        ck_a += (msg_length >> 8) & 0xFF
        ck_b += ck_a
        for byte in payload:
            ck_a += byte
            ck_b += ck_a
        return ck_a & 0xFF, ck_b & 0xFF

    def send_ubx_message(self, msg_class, msg_id, payload):
        if self.serial and self.serial.is_open:
            msg_length = len(payload)
            header = struct.pack('<BBH', msg_class, msg_id, msg_length)
            checksum = self.calc_checksum(msg_class, msg_id, payload)
            message = self.sync_chars + header + payload + bytes(checksum)
            try:
                self.serial.write(message)
            except serial.SerialException as e:
                print(f"Error writing to serial port: {e}")
                self.reconnect()
        else:
            print("Serial port is not open. Unable to send message.")

    def receive_ubx_message(self):
        if self.serial and self.serial.is_open:
            try:
                while True:
                    sync = self.serial.read(2)
                    if sync == self.sync_chars:
                        header = self.serial.read(4)
                        if len(header) < 4:
                            continue
                        msg_class, msg_id, msg_length = struct.unpack('<BBH', header)
                        payload = self.serial.read(msg_length)
                        if len(payload) < msg_length:
                            continue
                        checksum = self.serial.read(2)
                        if len(checksum) < 2:
                            continue
                        if self.calc_checksum(msg_class, msg_id, payload) == struct.unpack('<BB', checksum):
                            return msg_class, msg_id, payload
            except serial.SerialException as e:
                print(f"Error reading from serial port: {e}")
                self.reconnect()
        else:
            print("Serial port is not open. Unable to receive message.")
        return None, None, None

    def set_nav_mode(self, mode):
        payload = struct.pack('<B', mode)
        self.send_ubx_message(0x06, 0x24, payload)

    def get_nav_mode(self):
        self.send_ubx_message(0x06, 0x24, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x06 and msg_id == 0x24 and payload:
            return struct.unpack('<B', payload)[0]
        return None

    def initialize(self):
        self.send_ubx_message(0x06, 0x04, b'\x00\x00')
        time.sleep(1)  # Wait for the receiver to reset

    def startup(self):
        self.send_ubx_message(0x06, 0x04, b'\x01\x00')
        time.sleep(1)  # Wait for the receiver to reset

    def get_status(self):
        self.send_ubx_message(0x01, 0x03, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x01 and msg_id == 0x03 and payload:
            status = struct.unpack('<BBBBIBBBB', payload)
            return status
        return None

    def configure_port(self, port_id, baudrate, in_proto_mask, out_proto_mask):
        payload = struct.pack('<BBHIIHH', port_id, 0, 0, baudrate, in_proto_mask, out_proto_mask, 0)
        self.send_ubx_message(0x06, 0x00, payload)

    def set_power_mode(self, mode):
        payload = struct.pack('<B', mode)
        self.send_ubx_message(0x06, 0x3B, payload)

    def get_power_mode(self):
        self.send_ubx_message(0x06, 0x3B, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x06 and msg_id == 0x3B and payload:
            return struct.unpack('<B', payload)[0]
        return None

    def save_configuration(self):
        payload = struct.pack('<III', 0xFFFF, 0x00, 0x00)
        self.send_ubx_message(0x06, 0x09, payload)

    def load_configuration(self):
        payload = struct.pack('<III', 0x00, 0xFFFF, 0x00)
        self.send_ubx_message(0x06, 0x09, payload)

    def clear_configuration(self):
        payload = struct.pack('<III', 0x00, 0x00, 0xFFFF)
        self.send_ubx_message(0x06, 0x09, payload)

    def get_antenna_status(self):
        self.send_ubx_message(0x06, 0x13, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x06 and msg_id == 0x13 and payload:
            return payload
        return None

    def set_gnss_configuration(self, config):
        payload = config
        self.send_ubx_message(0x06, 0x3E, payload)

    def get_gnss_configuration(self):
        self.send_ubx_message(0x06, 0x3E, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x06 and msg_id == 0x3E and payload:
            return payload
        return None

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()

# Example usage
if __name__ == "__main__":
    ublox = UBlox7(port='/dev/ttyACM0', baudrate=9600)
    
    # Initialize the receiver
    ublox.initialize()
    print("Receiver initialized")
    
    # Startup the receiver
    ublox.startup()
    print("Receiver started up")
    
    # Get and print receiver status
    status = ublox.get_status()
    if status:
        print(f"Receiver status: {status}")
    else:
        print("Failed to get receiver status.")
    
    # Set navigation mode to Pedestrian
    ublox.set_nav_mode(2)
    nav_mode = ublox.get_nav_mode()
    if nav_mode is not None:
        print(f"Current navigation mode: {nav_mode}")
    else:
        print("Failed to get navigation mode.")

    # Configure the UART port
    ublox.configure_port(port_id=1, baudrate=9600, in_proto_mask=0x01, out_proto_mask=0x01)
    print("UART port configured")

    # Set and get power mode
    ublox.set_power_mode(1)
    power_mode = ublox.get_power_mode()
    if power_mode is not None:
        print(f"Current power mode: {power_mode}")
    else:
        print("Failed to get power mode.")

    # Save, load, and clear configuration
    ublox.save_configuration()
    print("Configuration saved")
    ublox.load_configuration()
    print("Configuration loaded")
    ublox.clear_configuration()
    print("Configuration cleared")

    # Get antenna status
    antenna_status = ublox.get_antenna_status()
    if antenna_status:
        print(f"Antenna status: {antenna_status}")
    else:
        print("Failed to get antenna status.")

    # Set and get GNSS configuration
    gnss_config = b'\x00' * 32  # Example configuration payload
    ublox.set_gnss_configuration(gnss_config)
    print("GNSS configuration set")
    current_gnss_config = ublox.get_gnss_configuration()
    if current_gnss_config:
        print(f"Current GNSS configuration: {current_gnss_config}")
    else:
        print("Failed to get GNSS configuration.")
    
    ublox.close()
