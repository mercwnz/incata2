import serial
import struct
import time

class UBlox7:
    def __init__(self, port='/dev/ttyACM0', baudrate=9600):
        self.serial = serial.Serial(port, baudrate, timeout=1)
        self.sync_chars = b'\xb5\x62'

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
        msg_length = len(payload)
        header = struct.pack('<BBH', msg_class, msg_id, msg_length)
        checksum = self.calc_checksum(msg_class, msg_id, payload)
        message = self.sync_chars + header + payload + bytes(checksum)
        self.serial.write(message)

    def receive_ubx_message(self):
        while True:
            sync = self.serial.read(2)
            if sync == self.sync_chars:
                header = self.serial.read(4)
                msg_class, msg_id, msg_length = struct.unpack('<BBH', header)
                payload = self.serial.read(msg_length)
                checksum = self.serial.read(2)
                if self.calc_checksum(msg_class, msg_id, payload) == struct.unpack('<BB', checksum):
                    return msg_class, msg_id, payload

    def set_nav_mode(self, mode):
        payload = struct.pack('<B', mode)
        self.send_ubx_message(0x06, 0x24, payload)

    def get_nav_mode(self):
        self.send_ubx_message(0x06, 0x24, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x06 and msg_id == 0x24:
            return struct.unpack('<B', payload)[0]

    def initialize(self):
        self.send_ubx_message(0x06, 0x04, b'\x00\x00')
        time.sleep(1)  # Wait for the receiver to reset

    def startup(self):
        self.send_ubx_message(0x06, 0x04, b'\x01\x00')
        time.sleep(1)  # Wait for the receiver to reset

    def get_status(self):
        self.send_ubx_message(0x01, 0x03, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x01 and msg_id == 0x03:
            status = struct.unpack('<BBBBIBBBB', payload)
            return status

    def close(self):
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
    print(f"Receiver status: {status}")
    
    # Set navigation mode to Pedestrian
    ublox.set_nav_mode(2)
    nav_mode = ublox.get_nav_mode()
    print(f"Current navigation mode: {nav_mode}")
    
    ublox.close()
