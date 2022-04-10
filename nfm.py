#! /usr/bin/python3
import time, serial, io
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server

class CustomCollector(object):
    def __init__(self):
        pass

    def collect(self):
        g = GaugeMetricFamily("MemoryUsage", 'Help text', labels=['instance'])
        g.add_metric(["instance01.us.west.local"], 20)
        yield g

        c = CounterMetricFamily("HttpRequests", 'Help text', labels=['app'])
        c.add_metric(["example"], 2000)
        yield c


if __name__ == '__main__':
#    start_http_server(8000)
#    REGISTRY.register(CustomCollector())
#    while True:
#        time.sleep(1)

  ser = serial.Serial( 
    port = '/dev/ttyUSB0',
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
    print ("port was already open, was closed and opened again!")
  except Exception as e:
    print("error open serial port: " + str(e))
    exit()

  while True:
    line=ser.readline().decode("utf-8")[:-2]
    print(line)

  print('Done')
  ser.close()