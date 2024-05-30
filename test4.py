import subprocess, time
from collections import deque

def __init__(self):
    self.temp_data = {}
    self.last_sentence_type = ""
    self.latitude_queue = deque(maxlen=5)
    self.longitude_queue = deque(maxlen=5)
    self.speed_queue = deque(maxlen=5)
    self.direction_queue = deque(maxlen=5)
    self.altitude_queue = deque(maxlen=5)
    self.climb_queue = deque(maxlen=5)

def moving_average(queue):
    return sum(queue) / len(queue) if queue else 0

def checksum(nmea):
    nmea = nmea.strip('$').split('*')[0]
    checksum = 0
    for char in nmea:
        checksum ^= ord(char)
    return checksum

def read_gps_data():
    process = subprocess.Popen(['gpspipe', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        while True:
            line = process.stdout.readline() # type: ignore
            if line:
                line = line.strip()
                if '*' in line:
                    data, checksum_str = line.split('*')
                    if int(checksum_str, 16) == checksum(data):
                        fields = data.split(',')
                        print(f"{checksum_str} ; {fields[0][1:]}")
                    else:
                        raise ValueError("checksum error")
            else:
                break
    except KeyboardInterrupt:
        print("Stopping GPS data read...")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    read_gps_data()
