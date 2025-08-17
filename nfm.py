#! /usr/bin/python3
import time
import serial
import os
import logging
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

# Logging Setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

SERIAL_PORT = os.environ['SERIAL']

class CustomCollector(object):
    def __init__(self):
        self.buf = 50  # last valid value

    def collect(self):
        try:
            ser = serial.Serial(
                port=SERIAL_PORT,
                baudrate=19200,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=1
            )
            # ensure port is open
            if not ser.is_open:
                ser.open()
        except IOError:
            logging.warning(f"Port {SERIAL_PORT} was already open, trying to reopen")
            try:
                ser.close()
                ser.open()
            except Exception as e:
                logging.error(f"Error opening port: {e}")
                yield GaugeMetricFamily("grid_frequency", 'Frequency of the electricity grid in Hz', value=self.buf)
                return
        except Exception as e:
            logging.error(f"Error opening port: {e}")
            yield GaugeMetricFamily("grid_frequency", 'Frequency of the electricity grid in Hz', value=self.buf)
            return

        try:
            raw_line = ser.readline()
            logging.debug(f"Raw line from serial: {raw_line}")
            line = raw_line.decode("utf-8", errors="ignore").strip()
            logging.debug(f"Decoded line: '{line}'")
            
            frequency = float(line) / 1000 if line else self.buf
        except ValueError:
            logging.warning(f"Failed to parse line '{line}' - using last value {self.buf}")
            frequency = self.buf
        except Exception as e:
            logging.error(f"Error while reading serial: {e}")
            frequency = self.buf
        finally:
            ser.close()

        # Buffer logic unchanged
        if frequency > 45:
            self.buf = frequency
        else:
            frequency = self.buf

        value = GaugeMetricFamily("grid_frequency", 'Frequency of the electricity grid in Hz')
        value.add_metric(["grid_frequency"], frequency)
        logging.info(f"Exported metric: {frequency:.3f} Hz")
        yield value

if __name__ == '__main__':
    start_http_server(8000)
    logging.info("Exporter started on port 8000")
    REGISTRY.register(CustomCollector())
    while True:
        time.sleep(5)  # Get new value every 5 seconds
