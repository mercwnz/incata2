import subprocess
import json
import sqlite3

class NMEA:

    def __init__(self):
        self.conn = sqlite3.connect('example.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        # Create a table (if it doesn't already exist)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS track (
                lat REAL,
                lon REAL,
                speed INTEGER,
                magtrack REAL,
                direction TEXT
            )
        ''')
        self.conn.commit()

    def get_cardinal_direction(self, degrees):
        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        if degrees is None:
            return "N/A"
        try:
            degrees = float(degrees)
        except ValueError:
            return "N/A"
        ix = round(degrees / 22.5) % 16
        return dirs[ix]

    def start_gps(self, insert=False):
        process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    try:
                        json_data = json.loads(line.strip())

                        if json_data["class"] == "TPV":

                            data = []
                            data.append({
                                'lat': json_data.get('lat', 'N/A'),
                                'lon': json_data.get('lon', 'N/A'),
                                'speed': json_data.get('speed', 'N/A'),
                                'magtrack': json_data.get('magtrack', 'N/A'),
                                'direction': self.get_cardinal_direction(json_data.get('magtrack', '0'))
                            })

                            
                            if json_data.get('lat', 'N/A') != 'N/A' and json_data.get('lon', 'N/A') != 'N/A' and insert:
                                print(data)
                                self.insert_into_db(data)

                        elif json_data["class"] == "SKY":
                            nSat = json_data.get('nSat', 'N/A')
                            uSat = json_data.get('uSat', 'N/A')

                            print(f"Satellites:   {uSat}/{nSat}")
                            print(f"\n")

                        else:
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
        self.cursor.execute('''
            INSERT INTO track (lat, lon, speed, magtrack, direction)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['lat'], data['lon'], data['speed'], data['magtrack'], data['direction']))
        self.conn.commit()

    def close_db(self):
        # Close the connection
        self.conn.close()
