import subprocess
import time
import threading
import serial

def is_port_available(port):
    try:
        ser = serial.Serial(port)
        ser.close()
        return True
    except serial.SerialException:
        return False

def run_cgps_for_10_seconds():
    port = '/dev/ttyACM0'
    
    if not is_port_available(port):
        print(f"Error: Serial port {port} is busy or not available.")
        return
    
    try:
        print("Starting cgps...")
        # Start the cgps command
        process = subprocess.Popen(['cgps', '-s'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Function to read and print output from the cgps command
        def read_output():
            while True:
                output = process.stdout.readline()
                if output:
                    print(f"cgps output: {output.strip()}")
                else:
                    break

        # Start a thread to read the output
        output_thread = threading.Thread(target=read_output)
        output_thread.start()

        print("cgps is running. Output will be printed for 10 seconds.")
        # Run for 10 seconds
        time.sleep(10)

        print("Terminating cgps...")
        # Terminate the cgps process
        process.terminate()
        output_thread.join()

        # Check for any remaining output
        stdout, stderr = process.communicate()
        if stdout:
            print(f"Remaining cgps output: {stdout.strip()}")
        if stderr:
            print(f"Error: {stderr.strip()}")
    
    except FileNotFoundError:
        print("Error: cgps command not found. Make sure it is installed and in your PATH.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    run_cgps_for_10_seconds()
