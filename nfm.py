#! /usr/bin/python3
import serial
import time
import logging
from prometheus_client import start_http_server, Gauge

# Logging Setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

SERIAL_PORT = "/dev/ttyUSB0"  # Standard, kann via ENV überschrieben werden
BAUDRATE = 9600

# Prometheus Metric
grid_frequency = Gauge("grid_frequency_hz", "Grid frequency in Hertz")

def open_serial(port=SERIAL_PORT, baud=BAUDRATE, retries=5, delay=1):
    """Öffnet den Serial-Port, mit automatischen Retries bei Fehlern."""
    for attempt in range(1, retries+1):
        try:
            ser = serial.Serial(port, baud, timeout=1)
            logging.info(f"Serial port {port} opened at {baud} baud")
            return ser
        except serial.SerialException as e:
            logging.warning(f"Attempt {attempt}/{retries} - cannot open {port}: {e}")
            time.sleep(delay)
    raise RuntimeError(f"Failed to open {port} after {retries} attempts")

def read_loop():
    ser = open_serial()
    while True:
        try:
            raw_line = ser.readline()
            logging.debug(f"Raw line from serial: {raw_line}")

            # Nullbytes entfernen + strip
            line = raw_line.decode(errors="ignore").replace("\x00", "").strip()

            if not line:
                logging.debug("Ignored empty line")
                continue

            if not line.isdigit():
                logging.debug(f"Ignored non-numeric line: '{line}'")
                continue

            # Wert umrechnen: Millihertz -> Hertz
            value = float(line) / 1000
            grid_frequency.set(value)
            logging.info(f"Updated metric: {value:.3f} Hz")

        except serial.SerialException as e:
            logging.error(f"Serial exception: {e} - reopening port")
            try:
                ser.close()
            except Exception:
                pass
            time.sleep(1)
            ser = open_serial()
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    start_http_server(8000)
    logging.info("Exporter started on port 8000")
    read_loop()
