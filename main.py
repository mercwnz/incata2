from modules.validate import VALIDATE
from modules.nmea import NMEA
from modules.obd2 import OBD2

if __name__ == "__main__":
    validate = VALIDATE()

    print(f"Validate result\t{bin(validate.result())}")

nmea = NMEA()
nmea.start_gps(insert=True)