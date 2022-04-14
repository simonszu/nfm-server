# Netzfrequenzmessung

This small script aims to be a prometheus exporter for the [Netzfrequenz-Messung](https://pc-projekte.lima-city.de/nfa_rpi.html) project.

Currently only the first mode is supported where the measured grid frequency is exported as a single number via serial, representing the frequency in millihertz. The exporter is converting this number to a value in Hertz.

To start the container, have a look at `helper/run_container.sh`.

Pullrequests gladly accepted. 
