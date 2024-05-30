import subprocess

def checksum(nmea):
    nmea = nmea.strip('$').split('*')[0]
    checksum = 0
    for char in nmea:
        checksum ^= ord(char)
    return checksum

def read_gps_data():
    # Start the gpspipe process
    process = subprocess.Popen(['gpspipe', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    try:
        while True:
            # Read a line of output from gpspipe
            line = process.stdout.readline() # type: ignore
            if line:
                line = line.strip()
                if '*' in line:
                    data, checksum_str = line.split('*')
                    checksum_val = int(checksum_str, 16)
                    calculated_checksum = checksum(data)
                    print(f"{checksum_val} {calculated_checksum} : {data}")
            else:
                break
    except KeyboardInterrupt:
        print("Stopping GPS data read...")
    finally:
        # Clean up the process
        process.terminate()
        process.wait()

if __name__ == "__main__":
    read_gps_data()
