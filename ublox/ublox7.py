# ublox/ublox7.py
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

    def initialize(self):
        self.send_ubx_message(0x06, 0x04, b'\x00\x00')
        time.sleep(1)  # Wait for the receiver to reset

    def startup(self):
        self.send_ubx_message(0x06, 0x04, b'\x01\x00')
        time.sleep(1)  # Wait for the receiver to reset

    def shutdown(self):
        self.send_ubx_message(0x06, 0x04, b'\x00\x08')  # Example payload to stop the receiver

    def close(self):
        if self.serial and self.serial.is_open:
            self.serial.close()

    def set_mode(self, mode):
        payload = struct.pack('<B', mode)
        self.send_ubx_message(0x06, 0x24, payload)

    def get_status(self):
        self.send_ubx_message(0x01, 0x03, b'')
        msg_class, msg_id, payload = self.receive_ubx_message()
        if msg_class == 0x01 and msg_id == 0x03 and payload:
            status = struct.unpack('<BBBBIBBBB', payload)
            return status
        return None

    def get_port(self):
        return self.port

    def perform_reconnect(self):
        self.reconnect()
