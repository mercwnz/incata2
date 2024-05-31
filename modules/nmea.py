import subprocess
import json
import sqlite3
from datetime import datetime

class NMEA:

    def __init__(self):
        self.conn = sqlite3.connect('track.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS track (
                timestamp TEXT UNIQUE,
                lat REAL,
                lon REAL,
                speed INTEGER,
                magtrack REAL,
                alt REAL
            )
        ''')
        self.conn.commit()

    def start_gps(self, insert=False, debug=False):
        process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    try:
                        json_data = json.loads(line.strip())

                        if json_data["class"] == "TPV":
                            data = {
                                'timestamp': json_data.get('time', None),
                                'lat': json_data.get('lat', None),
                                'lon': json_data.get('lon', None),
                                'speed': json_data.get('speed', None),
                                'magtrack': json_data.get('magtrack', None),
                                'alt': json_data.get('alt', None)
                            }

                            if data['lat'] and data['lon'] and insert:
                                self.insert_into_db(data)

                        elif json_data["class"] == "SKY":
                            nSat = json_data.get('nSat', None)
                            uSat = json_data.get('uSat', None)
                            print(f"Satellites:   {uSat}/{nSat}")

                        elif debug:
                            print(f"{json_data['class']}")
                            print(f"{json.dumps(json_data, indent=4)}")

                    except json.JSONDecodeError:
                        print(f"Failed to decode JSON: {line.strip()}")
                else:
                    break
        except KeyboardInterrupt:
            print("Stopping GPS data read...")
        finally:
            process.terminate()
            process.wait()
            self.close_db()

    def insert_into_db(self, data):
        try:
            self.cursor.execute('''
                INSERT INTO track (timestamp, lat, lon, speed, magtrack, alt)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (data['timestamp'], data['lat'], data['lon'], data['speed'], data['magtrack'], data['alt']))
            self.conn.commit()
        except sqlite3.IntegrityError as e:
            return
            # print(f"Failed to insert data into database: {e}")
        finally:
            print(f"{data}")


    def close_db(self):
        self.conn.close()
