import subprocess
import time
from collections import deque

class NMEA:

    gps_fix_types = [
        "Fix not available",
        "GPS fix",
        "Differential GPS fix",
        "PPS fix",
        "Real Time Kinematic",
        "Float RTK",
        "Estimated (dead reckoning)",
        "Manual input mode",
        "Simulation mode"
    ]

    def __init__(self):
        self.temp_data = {}
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
    
    def parse_gps_data(self, fields):
        nmea_type = fields[0][1:]

        timestamp = int(time.time())

        if nmea_type == "GPGGA":
            if len(fields) >= 15 and fields[2] and fields[4]:
                latitude = float(fields[2][:2]) + float(fields[2][2:]) / 60.0
                if fields[3] == 'S':
                    latitude = -latitude
                longitude = float(fields[4][:3]) + float(fields[4][3:]) / 60.0
                if fields[5] == 'W':
                    longitude = -longitude

                altitude = float(fields[9]) if fields[9] else 0.0
                            
                self.latitude_queue.append(latitude)
                self.longitude_queue.append(longitude)
                self.altitude_queue.append(altitude)

                self.temp_data['timestamp'] = timestamp
                self.temp_data['latitude'] = self.moving_average(self.latitude_queue)
                self.temp_data['longitude'] = self.moving_average(self.longitude_queue)
                self.temp_data['altitude'] = round(self.moving_average(self.altitude_queue), 2)
                self.temp_data['status'] = self.gps_fix_types[int(fields[6])]
                self.temp_data['available_satellites'] = int(fields[7])

        if nmea_type == "GPVTG":
            try:
                speed = float(fields[7]) if fields[7] else 0.0
            except ValueError:
                speed = 0.0

            try:
                direction = float(fields[1]) if fields[1] else 0.0
            except ValueError:
                direction = 0.0
            
            try:
                climb = float(fields[8]) if len(fields) > 8 and fields[8] else 0.0
            except ValueError:
                climb = 0.0

            self.speed_queue.append(speed)
            self.direction_queue.append(direction)
            self.climb_queue.append(climb)

            self.temp_data['speed'] = self.moving_average(self.speed_queue)
            self.temp_data['direction'] = self.moving_average(self.direction_queue)
            self.temp_data['climb'] = round(self.moving_average(self.climb_queue), 2)

    def read_gps_data(self):
        process = subprocess.Popen(['gpspipe', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    line = line.strip()
                    if '*' in line:
                        print(f"{line}")
                        data, checksum_str = line.split('*')
                        if int(checksum_str, 16) == self.checksum(data):
                            fields = data.split(',')
                            if fields[0][1:] in ["GPGGA", "GPVTG", "GPGSA"]:
                               self.parse_gps_data(fields)
                            #    print(f"{self.temp_data}")
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
