# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim-buster

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Specifies the device where the serial connector to the NFM device is located
ENV SERIAL=/dev/ttyUSB0

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD [ "python", "/app/nfm.py" ]