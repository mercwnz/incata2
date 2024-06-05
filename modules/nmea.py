import subprocess
import json
import sqlite3
from typing import Optional

class NMEA:
    def __init__(self):
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

    def create_table(self):
        if self.cursor:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS track (
                    timestamp TEXT UNIQUE,
                    lat REAL,
                    lon REAL,
                    speed REAL,
                    magtrack REAL,
                    alt REAL
                )
            ''')
            if self.conn:
                self.conn.commit()
            else:
                print("Connection is not initialized in create_table.")
        else:
            print("Cursor is not initialized in create_table.")

    def start_gps(self, insert=False, debug=False):
        try:
            process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except Exception as e:
            print(f"Failed to start gpspipe subprocess: {e}")
            return

        if process.stdout is None:
            print("Failed to obtain stdout from gpspipe subprocess.")
            return

        # Create SQLite connection and cursor in this thread
        try:
            self.conn = sqlite3.connect('track.db')
            self.cursor = self.conn.cursor()
            print("SQLite connection and cursor initialized.")
            self.create_table()
        except sqlite3.Error as e:
            print(f"SQLite error during initialization: {e}")
            return

        try:
            while True:
                line = process.stdout.readline()
                if not line:
                    print("No more lines from gpspipe, exiting.")
                    break

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

                        if data['timestamp'] and data['lat'] and data['lon'] and insert:
                            self.insert_or_update_db(data)

                    elif json_data["class"] == "SKY":
                        nSat = json_data.get('nSat', None)
                        uSat = json_data.get('uSat', None)
                        print(f"Satellites:   {uSat}/{nSat}")

                    elif debug:
                        print(f"{json_data['class']}")
                        print(f"{json.dumps(json_data, indent=4)}")

                except json.JSONDecodeError:
                    print(f"Failed to decode JSON: {line.strip()}")
        except KeyboardInterrupt:
            print("Stopping GPS data read...")
        finally:
            process.terminate()
            process.wait()
            self.close_db()

    def insert_or_update_db(self, data):
        if not self.cursor or not self.conn:
            print("Cursor or connection is not initialized in insert_or_update_db.")
            return

        try:
            self.cursor.execute('''
                INSERT INTO track (timestamp, lat, lon, speed, magtrack, alt)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(timestamp) DO UPDATE SET
                    lat=excluded.lat,
                    lon=excluded.lon,
                    speed=excluded.speed,
                    magtrack=excluded.magtrack,
                    alt=excluded.alt
            ''', (data['timestamp'], data['lat'], data['lon'], data['speed'], data['magtrack'], data['alt']))
            self.conn.commit()
            print(f"Data inserted or updated: {data}")
        except sqlite3.Error as e:
            print(f"SQLite error during insert_or_update: {e}")

    def close_db(self):
        if self.conn:
            self.conn.close()
            print("SQLite connection closed.")
        else:
            print("Connection already closed or not initialized.")

# Example usage:
nmea = NMEA()
nmea.start_gps(insert=True, debug=True)
