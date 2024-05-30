import subprocess
import threading
import time

def read_gps_data():
    # Start the gpspipe process
    process = subprocess.Popen(['gpspipe', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def read_output(stream):
        while not process.poll():
            line = stream.readline()
            if line.startswith('$'):
                print(f"{line.strip()}")
            else:
                time.sleep(0.1)

    stdout_thread = threading.Thread(target=read_output, args=(process.stdout,))
    stderr_thread = threading.Thread(target=read_output, args=(process.stderr,))

    stdout_thread.start()
    stderr_thread.start()

    try:
        stdout_thread.join()
        stderr_thread.join()
    except KeyboardInterrupt:
        print("Stopping GPS data read...")
        process.terminate()
        process.wait()

if __name__ == "__main__":
    read_gps_data()
