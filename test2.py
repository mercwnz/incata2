# test2.py

import serial
import time
from datetime import datetime
from threading import Event
from gps.devices import DEVICES as GPS_DEVICES
from gps.nmea import NMEA
from config import MAX_ENTRIES, BAUD_RATE_GPS

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

def read_gps_data(serial_port, nmea_parser, should_exit, max_entries):
    entries_count = 0
    last_data_time = time.time()
    while not should_exit.is_set() and entries_count < max_entries:
        line = serial_port.readline().decode('ascii', errors='replace').strip()
        if line.startswith('$') and '*' in line:
            if nmea_parser.parse_sentence(line):
                last_sentence_type = nmea_parser.get_last_sentence_type()

                if last_sentence_type in ['GPGGA', 'GPVTG']:
                    print_data(nmea_parser.get_data())
                    entries_count += 1
                    last_data_time = time.time()

                if "$GPGGA" in line and ",0," not in line:
                    last_data_time = time.time()

        if time.time() - last_data_time > 10:
            print("No raw data received for 10 seconds, reconnecting...")
            serial_port.close()
            time.sleep(1)
            serial_port.open()
            last_data_time = time.time()

def connect_to_gps_device(max_retries=MAX_ENTRIES, debug=False):
    gps_devices = GPS_DEVICES()
    found_devices = gps_devices.find_gps_devices()
    if not found_devices:
        print("No GPS devices found.")
        return None
    
    retries = 0
    while retries < max_retries:
        print("Found GPS devices:")
        for device in found_devices:
            print(f"Port: {device[0]}, Description: {device[1]}")
            result = gps_devices.test_device(device, debug=debug)
            print(result)
            if "NMEA response" in result:
                return device[0]
        retries += 1
        print(f"Invalid response. Retrying... {retries} / {max_retries}")
        time.sleep(1)

    print("Max retries reached. Could not find a valid GPS device.")
    return None

def main(debug=False):
    port = connect_to_gps_device(debug=debug)
    if port:
        nmea_parser = NMEA()
        should_exit = Event()
        try:
            with serial.Serial(port, baudrate=BAUD_RATE_GPS, timeout=1) as serial_port:
                print(f"Connected to GPS device on port: {port}")
                read_gps_data(serial_port, nmea_parser, should_exit, MAX_ENTRIES)
        except serial.SerialException as e:
            print(f"Could not open serial port {port}: {e}")
        except KeyboardInterrupt:
            print("Exiting...")

if __name__ == "__main__":
    main(debug=True)
