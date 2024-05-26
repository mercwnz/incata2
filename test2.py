# test2.py

import serial
import time
from datetime import datetime
from threading import Event
from gps.devices import DEVICES as GPS_DEVICES
from gps.nmea import NMEA

def format_field(name, value):
    name_width = 20
    value_width = 20
    return f"{name:<{name_width}} {value:<{value_width}}"

def format_timestamp(epoch_time):
    if epoch_time == 'N/A':
        return epoch_time
    return datetime.fromtimestamp(epoch_time).strftime('%H:%M:%S')

def print_data(data):
    fields = [
        ("Timestamp:", format_timestamp(data.get('timestamp', 'N/A'))),
        ("Latitude:", f"{data.get('latitude', 0):.8f}"),
        ("Longitude:", f"{data.get('longitude', 0):.8f}"),
        ("Altitude (m):", f"{data.get('altitude', 0):.2f}"),
        ("Status:", data.get('status', 'N/A')),
        ("Available Sats:", data.get('available_satellites', 'N/A')),
        ("Speed (km/h):", f"{data.get('speed', 0):.2f}"),
        ("Direction (°):", f"{data.get('direction', 0):.2f}"),
        ("Direction:", data.get('direction_cardinal', 'N/A')),
        ("Climb (m):", f"{data.get('climb', 0):.2f}")
    ]

    output = "\n".join(format_field(name, value) for name, value in fields)
    output += "\n" + "-" * 40
    print(output)

def read_gps_data(port, nmea_parser, should_exit):
    try:
        with serial.Serial(port, baudrate=9600, timeout=1) as ser:
            print(f"Connected to GPS device on port: {port}")
            last_fix_time = time.time()
            while not should_exit.is_set():
                line = ser.readline().decode('ascii', errors='replace')
                if line:
                    nmea_parser.parse_sentence(line)
                    last_sentence_type = nmea_parser.get_last_sentence_type()

                    if last_sentence_type in ['GPGGA', 'GPVTG']:
                        print_data(nmea_parser.get_data())

                    if "$GPGGA" in line and ",0," not in line:
                        last_fix_time = time.time()

                if time.time() - last_fix_time > 60:
                    print("No valid fix for 60 seconds, reconnecting...")
                    ser.close()
                    time.sleep(1)
                    ser.open()
                    last_fix_time = time.time()

    except serial.SerialException as e:
        print(f"Could not open serial port {port}: {e}")
    except KeyboardInterrupt:
        print("Exiting...")

def connect_and_read_gps(debug=False):
    gps_devices = GPS_DEVICES()
    found_devices = gps_devices.find_gps_devices()
    if not found_devices:
        print("No GPS devices found.")
        return None
    else:
        print("Found GPS devices:")
        for device in found_devices:
            print(f"Port: {device[0]}, Description: {device[1]}")
            # Test the device before attempting to read data
            result = gps_devices.test_device(device, debug=debug)
            print(result)
            if "NMEA response" in result:
                # Use the first valid device's port
                port = device[0]
                nmea_parser = NMEA()
                should_exit = Event()
                read_gps_data(port, nmea_parser, should_exit)
                break

if __name__ == "__main__":
    connect_and_read_gps(debug=True)
