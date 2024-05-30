import subprocess

def checksum(nmea_sentence):
    nmea_sentence = nmea_sentence.strip('$').split('*')[0]
    checksum = 0
    for char in nmea_sentence:
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
                print(f"{checksum(line.strip())} : {line.strip()}")
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
