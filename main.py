from modules.validate import VALIDATE
from modules.nmea import NMEA
from modules.obd2 import OBD2

if __name__ == "__main__":
    validate = VALIDATE()
    print(f"Validate result\t{bin(validate.result())}")

nmea = NMEA()
nmea.start_gps(insert=True)

obd2 = OBD2()
if obd2.start_obd():
    obd2.get_speed()
    obd2.get_rpm()
    obd2.get_throttle_position()
    obd2.get_engine_load()
    obd2.get_coolant_temp()
    obd2.get_fuel_pressure()
    obd2.get_intake_temp()
    obd2.get_run_time()
    obd2.get_fuel_rate()
