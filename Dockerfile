FROM python:3-slim

RUN apt update && apt upgrade -y
RUN apt install -y gcc python3-dev python3-libgpiod
RUN CFLAGS="-fcommon" pip3 install RPi.GPIO
RUN pip3 install adafruit-circuitpython-dht influxdb-client
RUN apt remove -y gcc python3-dev
RUN apt autoremove -y
RUN apt autoclean
COPY . .
ENTRYPOINT ["python3", "-u", "/dht.py"]
