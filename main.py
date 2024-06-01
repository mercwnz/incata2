from modules.validate import VALIDATE
from modules.nmea import NMEA
from modules.obd2 import OBD2
import concurrent.futures
import time

def run_obd_tasks(obd2):
    if obd2.start_obd():
        try:
            while True:
                obd2.get_speed()
                obd2.get_rpm()
                obd2.get_throttle_position()
                obd2.get_engine_load()
                obd2.get_coolant_temp()
                obd2.get_fuel_pressure()
                obd2.get_intake_temp()
                obd2.get_run_time()
                obd2.get_fuel_rate()
                time.sleep(1)  # 1 second interval between data retrieval
        except KeyboardInterrupt:
            print("OBD-II data retrieval aborted...")

if __name__ == "__main__":
    validate = VALIDATE()
    print(f"Validate result\t{bin(validate.result())}")

    nmea = NMEA()
    obd2 = OBD2()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(nmea.start_gps, True)
        executor.submit(run_obd_tasks, obd2)
