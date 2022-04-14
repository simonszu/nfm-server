#! /usr/bin/env bash

docker run -d --publish 8000:8000 --device /dev/ttyUSB0 -e SERIAL='/dev/ttyUSB0' --name nfm nfm