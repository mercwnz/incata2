import subprocess
import json

from gps.nmea import NMEA

def read_gps_data():
    # Start the gpspipe process
    process = subprocess.Popen(['gpspipe', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    nmea_parser = NMEA()

    try:
        while True:
            # Read a line of output from gpspipe
            line = process.stdout.readline() # type: ignore
            if line:
                try:
                    # Attempt to parse the line as JSON
                    data = json.loads(line)
                    # Process the GPS data (for now, just print it)
                    print(json.dumps(data, indent=4))
                except json.JSONDecodeError:
                    print(nmea_parser.parse_sentence(line))
                    # print(f"Non-JSON data: {line.strip()}")
            else:
                break
    except KeyboardInterrupt:
        # Handle the user interrupting the script
        print("Stopping GPS data read...")
    finally:
        # Clean up the process
        process.terminate()
        process.wait()

if __name__ == "__main__":
    read_gps_data()
