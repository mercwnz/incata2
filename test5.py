from serial import Serial
from pynmeagps import NMEAReader
with Serial('/dev/ttyUSB0', 9600, timeout=3) as stream:
  nmr = NMEAReader(stream)
  raw_data, parsed_data = nmr.read()
  print(parsed_data)