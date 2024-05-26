# gps/nmea.py

import time
from datetime import datetime
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

    def calculate_checksum(self, nmea_sentence):
        nmea_sentence = nmea_sentence.strip('$').split('*')[0]
        checksum = 0
        for char in nmea_sentence:
            checksum ^= ord(char)
        return checksum

    def moving_average(self, queue):
        return sum(queue) / len(queue) if queue else 0

    def parse_sentence(self, sentence, cursor=None):
        try:
            if "*" not in sentence:
                raise ValueError("Sentence does not contain a checksum delimiter (*)")
            data, checksum = sentence.split('*')
            checksum = int(checksum, 16)
            calculated_checksum = self.calculate_checksum(data)

            if checksum != calculated_checksum:
                print(f"Checksum mismatch for sentence: {sentence}")
                self.last_sentence_type = ""
                return False

            fields = data.split(',')
            self.last_sentence_type = fields[0][1:]

            if self.last_sentence_type == 'GPGGA':
                self.parse_gpgga(fields)
            elif self.last_sentence_type == 'GPVTG':
                self.parse_gpvtg(fields)
            elif self.last_sentence_type == 'GPGSA':
                self.parse_gpgsa(fields)
            return True
        except ValueError as e:
            print(f"Error parsing sentence: {sentence}, error: {e}")
            self.last_sentence_type = ""
            return False

    def parse_gpgga(self, fields):
        if len(fields) >= 15 and fields[2] and fields[4]:
            latitude = float(fields[2][:2]) + float(fields[2][2:]) / 60.0
            if fields[3] == 'S':
                latitude = -latitude
            longitude = float(fields[4][:3]) + float(fields[4][3:]) / 60.0
            if fields[5] == 'W':
                longitude = -longitude

            timestamp = int(time.time())
            altitude = float(fields[9]) if fields[9] else 0.0

            self.latitude_queue.append(latitude)
            self.longitude_queue.append(longitude)
            self.altitude_queue.append(altitude)

            self.temp_data['timestamp'] = timestamp
            self.temp_data['latitude'] = self.moving_average(self.latitude_queue)
            self.temp_data['longitude'] = self.moving_average(self.longitude_queue)
            self.temp_data['altitude'] = round(self.moving_average(self.altitude_queue), 2)
            self.temp_data['status'] = self.interpret_status(fields[6])
            self.temp_data['available_satellites'] = int(fields[7])

    def parse_gpvtg(self, fields):
        try:
            speed_knots = float(fields[7]) if fields[7] else 0.0
        except ValueError:
            speed_knots = 0.0
        speed_kmh = speed_knots * 1.852  # Convert speed from knots to km/h

        try:
            direction = float(fields[1]) if fields[1] else 0.0
        except ValueError:
            direction = 0.0
        
        try:
            climb = float(fields[8]) if len(fields) > 8 and fields[8] else 0.0
        except ValueError:
            climb = 0.0

        self.speed_queue.append(speed_kmh)
        self.direction_queue.append(direction)
        self.climb_queue.append(climb)

        self.temp_data['speed'] = self.moving_average(self.speed_queue)
        self.temp_data['direction'] = self.moving_average(self.direction_queue)
        self.temp_data['climb'] = round(self.moving_average(self.climb_queue), 2)

    def parse_gpgsa(self, fields):
        if len(fields) >= 18:
            self.temp_data['used_satellites'] = len([field for field in fields[3:15] if field])

    def get_cardinal_direction(self, degrees):
        if degrees is None:
            return "N/A"
        dirs = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
        ix = round(degrees / 45) % 8
        return dirs[ix]

    def interpret_status(self, status):
        status_dict = {
            "0": "Fix not available or invalid",
            "1": "GPS fix (SPS)",
            "2": "DGPS fix (Differential GPS)"
        }
        return status_dict.get(status, "Unknown")

    def get_data(self):
        self.temp_data['direction_cardinal'] = self.get_cardinal_direction(self.temp_data.get('direction'))
        return self.temp_data

    def get_last_sentence_type(self):
        return self.last_sentence_type
