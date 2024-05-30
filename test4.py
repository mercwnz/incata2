import subprocess
import time
from collections import deque

class NMEA:
    def __init__(self):
        self.temp_data = {}
        self.last_sentence_type = ""
        self.latitude_queue = deque(maxlen=5)
        self.longitude_queue = deque(maxlen=5)
        self.speed_queue = deque(maxlen=5)
        self.direction_queue = deque(maxlen=5)
        self.altitude_queue = deque(maxlen=5)
        self.climb_queue = deque(maxlen=5)

    def moving_average(self, queue):
        return sum(queue) / len(queue) if queue else 0

    def checksum(self, nmea):
        nmea = nmea.strip('$').split('*')[0]
        checksum = 0
        for char in nmea:
            checksum ^= ord(char)
        return checksum

    def read_gps_data(self):
        process = subprocess.Popen(['gpspipe', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    line = line.strip()
                    if '*' in line:
                        data, checksum_str = line.split('*')
                        if int(checksum_str, 16) == self.checksum(data):
                            fields = data.split(',')
                            nmea_type = fields[0][1:]
                            if nmea_type in ["GPGGA", "GPVTG", "GPGSA"]:
                                print(f"{checksum_str} ; {nmea_type}")
                                print(f"{data}")
                        else:
                            print("Checksum error")
                else:
                    break
        except KeyboardInterrupt:
            print("Stopping GPS data read...")
        finally:
            process.terminate()
            process.wait()

if __name__ == "__main__":
    tester = NMEA()
    tester.read_gps_data()
