import serial
import struct

class UBlox7:
    def __init__(self, port, baudrate=9600):
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

    def close(self):
        self.serial.close()

# Example usage
if __name__ == "__main__":
    ublox = UBlox7(port='/dev/ttyUSB0', baudrate=9600)
    ublox.set_nav_mode(2)  # Set navigation mode to Pedestrian
    nav_mode = ublox.get_nav_mode()
    print(f"Current navigation mode: {nav_mode}")
    ublox.close()