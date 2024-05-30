import subprocess

def checksum(line):
    line = line.strip('$').split('*')[0]
    checksum = 0
    for char in line:
        checksum ^= ord(char)
    return checksum

def read_gps_data():
    process = subprocess.Popen(['gpspipe', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        while True:
            line = process.stdout.readline() # type: ignore
            if line.startswith("$"):
                print(f"{checksum(line.strip())} : {line.strip()}")
            else:
                break
    except KeyboardInterrupt:
        print("Stopping GPS data read...")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    read_gps_data()