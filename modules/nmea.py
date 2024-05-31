import subprocess
import json
import sqlite3

class NMEA:
   
    def get_cardinal_direction(self, degrees):
        dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
        if degrees is None:
            return "N/A"
        ix = round(degrees / 22.5) % 16
        return dirs[ix]

    def read_gps_json(self):

        process = subprocess.Popen(['gpspipe', '-w'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        try:
            while True:
                line = process.stdout.readline()  # type: ignore
                if line:
                    try:
                        json_data = json.loads(line.strip())
                       
                        if json_data["class"] == "TPV":
                            lat = json_data.get('lat', 'N/A')
                            lon = json_data.get('lon', 'N/A')
                            speed = json_data.get('speed', 'N/A')
                            magtrack = json_data.get('magtrack', 'N/A')

                            print(f"Maps:       https://www.google.com/maps?q={lat},{lon}")
                            print(f"Latitude:   {lat}")
                            print(f"Longitude:  {lon}")
                            print(f"Speed:      {round(speed * 3.6)} km/h")
                            print(f"Magtrack:   {round(magtrack)}°")
                            print(f"Direction:  {self.get_cardinal_direction(magtrack)}")
                            print(f"\n")

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

    def write_to_db(self, data):
        conn = sqlite3.connect('example.db')
        cursor = conn.cursor()

        # Create a table (if it doesn't already exist)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS track (
                lat REAL,
                lon REAL,
                speed INTEGER,
                magtrack REAL,
                direction TEXT
            )
        ''')
        conn.commit()

        # Insert data into the table
        for entry in data:
            cursor.execute('''
                INSERT INTO track (lat, lon, speed, magtrack, direction)
                VALUES (?, ?, ?, ?, ?)
            ''', (entry['lat'], entry['lon'], entry['speed'], entry['magtrack'], entry['direction']))

        conn.commit()

        # Close the connection
        conn.close()