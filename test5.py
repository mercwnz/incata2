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
                        if json_data["class"] == "TPV":
                            lat = json_data.get('lat', 'N/A')
                            lon = json_data.get('lon', 'N/A')
                            speed = json_data.get('speed', 'N/A')
                            magtrack = json_data.get('magtrack', 'N/A')
                            print(f"Latitude: {lat}")
                            print(f"Longitude: {lon}")
                            print(f"Speed: {speed}")
                            print(f"Magtrack: {magtrack}")
                        else:
                            print(f"{json_data['class']}")
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
