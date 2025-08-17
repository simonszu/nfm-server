#! /usr/bin/python3
import time
import serial
import os
import logging
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

# Setup logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(message)s")

SERIAL_PORT = os.environ.get('SERIAL', '/dev/ttyUSB0')

class CustomCollector(object):
    def __init__(self):
        self.buf = 50.0  # default frequency

    def collect(self):
        try:
            ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=19200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1  # avoid blocking forever
            )

            line = ser.readline()
            logging.debug(f"Raw line from serial: {line}")

            try:
                frequency = float(line.decode("utf-8").strip()) / 1000
            except ValueError as e:
                logging.warning(f"Failed to parse line '{line}': {e}")
                frequency = self.buf

            ser.close()

        except Exception as e:
            logging.error(f"Serial error: {e}")
            frequency = self.buf

        # Some logic to rule out invalid serial readings.
        if frequency > 45:
            self.buf = frequency
        else:
            frequency = self.buf

        value = GaugeMetricFamily("grid_frequency", 'Frequency of the electricity grid in Hz')
        value.add_metric(["grid_frequency"], frequency)
        yield value


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(CustomCollector())
    logging.info("Exporter started on port 8000")
    while True:
        time.sleep(5)  # Get new value every 5 seconds
