import serial
import logging
from prometheus_client import start_http_server, Gauge
import time

# Logging Setup
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Prometheus Metric
grid_frequency = Gauge("grid_frequency_hz", "Grid frequency in Hertz")

def read_serial(port="/dev/ttyUSB0", baudrate=9600):
    ser = serial.Serial(port, baudrate, timeout=1)
    logging.info(f"Opened serial port {port} at {baudrate} baud")

    while True:
        try:
            raw_line = ser.readline()
            logging.debug(f"Raw line from serial: {raw_line}")

            # Bytes -> String und Nullbytes entfernen
            line = raw_line.decode(errors="ignore").replace("\x00", "").strip()
            logging.debug(f"Cleaned line: '{line}'")

            if not line:
                logging.debug("Ignored empty/invalid line")
                continue

            try:
                value = float(line) / 1000  # Umrechnung: z. B. 50010 → 50.010 Hz
                grid_frequency.set(value)
                logging.info(f"Updated metric with value: {value:.3f} Hz")
            except ValueError:
                logging.warning(f"Could not parse line '{line}'")

        except Exception as e:
            logging.error(f"Error while reading serial: {e}")
            time.sleep(1)

if __name__ == "__main__":
    start_http_server(8000)
    logging.info("Exporter started on port 8000")
    read_serial()
