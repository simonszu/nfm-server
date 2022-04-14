#! /usr/bin/python3
import time, serial, io, os
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

SERIAL_PORT = os.environ['SERIAL']

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
      ser = serial.Serial( 
        port = SERIAL_PORT,
        baudrate = 19200,
        bytesize = serial.EIGHTBITS,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE
      )
      try:
        ser.open()
      except IOError: # if port is already opened, close and open it again
        ser.close()
        ser.open()
      except Exception as e:
        print("error open serial port: " + str(e))
        exit()

      frequency = float(ser.readline().decode("utf-8")[:-2]) / 1000
      ser.close()

      value = GaugeMetricFamily("grid_frequency", 'Frequency of the electricity grid in Hz')
      value.add_metric(["grid_frequency"], frequency)

      yield value

if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(1) # Get new value every 1 second




