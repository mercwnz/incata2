from nmea import input_stream, data_frame, database_wrapper

stream = input_stream.GenericInputStream.open_stream('/dev/ttyACM0', 9600)


print(stream)

with stream:
    while True:
        new_frame = data_frame.DataFrame.get_next_frame(stream)

        print("Current GPS time:", new_frame.gps_time)
        print("Current Latitude:", new_frame.latitude)
        print("Current Longitude:", new_frame.longitude)
        print("Current Speed:", new_frame.velocity)
        print("Current heading:", new_frame.track)
        print("Number of Satellites above:", new_frame.nsats)
        print("Individual Observations:")
        for obs in new_frame.sv_observations:
            print('\tPRN:', obs.prn)
            print('\t\tSignal to Noise:', obs.snr)
            print('\t\tAzimuth:', obs.azimuth)
            print('\t\tElevation:', obs.elevation)
