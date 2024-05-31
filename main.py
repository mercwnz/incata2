from modules.validate import VALIDATE
from modules.nmea import NMEA
from modules.obd2 import OBD2

if __name__ == "__main__":
    validate = VALIDATE()
    print(validate.devices())

    print(f"Validate result\t{bin(validate.result())}")

    nmea = NMEA()
    nmea.read_gps_json()

