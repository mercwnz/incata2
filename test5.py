import subprocess
import json
import sqlite3

class NMEA:

    def read_gps_json(self):
        process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    try:
                        json_data = json.loads(line.strip())
                        pretty_json = json.dumps(json_data, indent=4)
                        print(f"{json_data['lat']}")
                        print(f"{json_data['lon']}")
                        print(f"{json_data['speed']}")
                        print(f"{json_data['magtrack']}")
                    except json.JSONDecodeError:
                        print(f"Failed to decode JSON: {line.strip()}")
                else:
                    break
        except KeyboardInterrupt:
            print("Stopping GPS data read...")
        finally:
            process.terminate()
            process.wait()

if __name__ == "__main__":
    tester = NMEA()
    tester.read_gps_json()
