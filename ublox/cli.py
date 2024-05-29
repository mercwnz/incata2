# ublox/cli.py
import argparse
from ublox.ublox7 import UBlox7

def main():
    parser = argparse.ArgumentParser(description='Control the UBlox7 device.')
    parser.add_argument('--device', choices=['start', 'stop', 'reset'], help='Start, stop, or reset the device.')
    parser.add_argument('--mode', type=int, help='Set the mode of the device.')
    parser.add_argument('--status', action='store_true', help='Get the status from the device.')
    parser.add_argument('--port', action='store_true', help='Get the current port used by the device.')
    parser.add_argument('--reconnect', action='store_true', help='Disconnect and reconnect the port in use.')
    parser.add_argument('--port_name', default='/dev/ttyACM0', help='Serial port for the UBlox7 device.')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baudrate for the serial communication.')

    args = parser.parse_args()

    ublox = UBlox7(port=args.port_name, baudrate=args.baudrate)

    if args.device:
        if args.device == 'start':
            ublox.startup()
            print("Device started.")
        elif args.device == 'stop':
            ublox.shutdown()
            print("Device stopped.")
        elif args.device == 'reset':
            ublox.initialize()
            print("Device reset.")
    
    if args.mode is not None:
        ublox.set_mode(args.mode)
        print(f"Device mode set to {args.mode}.")
    
    if args.status:
        status = ublox.get_status()
        if status:
            print(f"Device status: {status}")
        else:
            print("Failed to get device status.")
    
    if args.port:
        print(f"Current port: {ublox.get_port()}")
    
    if args.reconnect:
        ublox.perform_reconnect()
        print("Port reconnected.")

    ublox.close()

if __name__ == "__main__":
    main()
