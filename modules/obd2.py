import obd
from obd import OBDStatus

class OBD2:
    def __init__(self):
        self.connection = None

    def start_obd(self):
        self.connection = obd.OBD()  # auto-connects to USB or RF port

        if self.connection.status() == OBDStatus.NOT_CONNECTED:
            print("Failed to connect to OBD-II device.")
            return False
        else:
            print("Connected to OBD-II device.")
            return True

    def get_speed(self):
        if self.connection:
            cmd = obd.commands.SPEED  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No speed data available.")
            else:
                print(f"Speed: {response.value}")

    def get_rpm(self):
        if self.connection:
            cmd = obd.commands.RPM  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No RPM data available.")
            else:
                print(f"RPM: {response.value}")

    def get_throttle_position(self):
        if self.connection:
            cmd = obd.commands.THROTTLE_POS  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No throttle position data available.")
            else:
                print(f"Throttle Position: {response.value}")

    def get_engine_load(self):
        if self.connection:
            cmd = obd.commands.ENGINE_LOAD  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No engine load data available.")
            else:
                print(f"Engine Load: {response.value}")

    def get_coolant_temp(self):
        if self.connection:
            cmd = obd.commands.COOLANT_TEMP  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No coolant temperature data available.")
            else:
                print(f"Coolant Temperature: {response.value}")

    def get_fuel_pressure(self):
        if self.connection:
            cmd = obd.commands.FUEL_PRESSURE  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No fuel pressure data available.")
            else:
                print(f"Fuel Pressure: {response.value}")

    def get_intake_temp(self):
        if self.connection:
            cmd = obd.commands.INTAKE_TEMP  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No intake temperature data available.")
            else:
                print(f"Intake Temperature: {response.value}")

    def get_run_time(self):
        if self.connection:
            cmd = obd.commands.RUN_TIME  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No run time data available.")
            else:
                print(f"Run Time: {response.value}")

    def get_fuel_rate(self):
        if self.connection:
            cmd = obd.commands.FUEL_RATE  # type: ignore # select an OBD command (sensor)
            response = self.connection.query(cmd)  # send the command, and parse the response
            
            if response.is_null():
                print("No fuel rate data available.")
            else:
                print(f"Fuel Rate: {response.value}")

