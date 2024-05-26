# test.py

import sys
import argparse
import serial.tools.list_ports
from gps.devices import DEVICES as GPS_DEVICES
from obd2.devices import DEVICES as OBD_DEVICES

def list_all_devices():
    ports = serial.tools.list_ports.comports()
    devices_list = [(port.device, port.description) for port in ports]
    
    if not devices_list:
        print("No devices found.")
    else:
        print("All connected devices:")
        for device in devices_list:
            print(f"Port: {device[0]}, Description: {device[1]}")

def test_gps_devices(wait_time, debug):
    gps_devices = GPS_DEVICES()
    found_devices = gps_devices.find_gps_devices()
    if not found_devices:
        print("No GPS devices found.")
    else:
        print("Found GPS devices:")
        for device in found_devices:
            print(f"Port: {device[0]}, Description: {device[1]}")
            result = gps_devices.test_device(device, wait_time, debug)
            print(result)

def test_obd_devices(wait_time, debug):
    obd_devices = OBD_DEVICES()
    found_devices = obd_devices.find_obd_devices()
    if not found_devices:
        print("No OBD devices found.")
    else:
        print("Found OBD devices:")
        for device in found_devices:
            print(f"Port: {device[0]}, Description: {device[1]}")
            result = obd_devices.test_device(device, wait_time, debug)
            print(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test GPS and OBD devices')
    parser.add_argument('--list-all-devices', '-LAD', action='store_true', help='List all connected devices')
    parser.add_argument('--wait', '-W', type=int, default=10, help='Wait time in seconds for device response')
    parser.add_argument('--debug', '-D', action='store_true', help='Show raw data while testing')
    parser.add_argument('--gps', action='store_true', help='Only test GPS devices')
    parser.add_argument('--obd', action='store_true', help='Only test OBD devices')
    
    args = parser.parse_args()
    
    if args.list_all_devices:
        list_all_devices()
    else:
        wait_time = args.wait
        debug = args.debug
        if args.gps:
            print(f"Testing GPS Devices with a wait time of {wait_time} seconds")
            test_gps_devices(wait_time, debug)
        elif args.obd:
            print(f"Testing OBD Devices with a wait time of {wait_time} seconds")
            test_obd_devices(wait_time, debug)
        else:
            print(f"Testing GPS Devices with a wait time of {wait_time} seconds")
            test_gps_devices(wait_time, debug)
            print(f"\nTesting OBD Devices with a wait time of {wait_time} seconds")
            test_obd_devices(wait_time, debug)
