import subprocess
import json
from collections import deque

class NMEA:

    def read_gps_json(self):
        process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    print(line.strip())
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
