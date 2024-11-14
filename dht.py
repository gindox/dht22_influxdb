import time
import board
import adafruit_dht

import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


dhtDevice = adafruit_dht.DHT22(board.D4)

influxdb_token = os.getenv('influxdb_token')
influxdb_org = os.getenv('influxdb_org')
influxdb_url = os.getenv('influxdb_url')

influxdb_bucket = os.getenv('influxdb_bucket')
device_id = os.getenv('device_id')


while True:
    try:
        client = influxdb_client.InfluxDBClient(url=influxdb_url, token=influxdb_token, org=influxdb_org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        temperature_c = dhtDevice.temperature
        humidity = dhtDevice.humidity
        

        print("Temp: {:.1f} C, Humidity: {}% ".format(
                temperature_c, humidity
            )
        )
        
        data_t = (
            Point("temperature")
            .tag("device",device_id)
            .field("temp",temperature_c)
            )
        write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=data_t)


        data_h = (
            Point("humidity")
            .tag("device",device_id)
            .field("humidity",humidity)
            )
        write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=data_h)

    except Exception as error:
        print(error.args[0])
        time.sleep(2.0)
        continue
    time.sleep(2.0)
