import random
import time
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from config import (
    INFLUXDB_URL,
    INFLUXDB_USERNAME,
    INFLUXDB_PASSWORD,
    INFLUXDB_ORG,
    INFLUXDB_BUCKET
)

# Initialize InfluxDB client
client = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG
)
write_api = client.write_api(write_options=SYNCHRONOUS)

def generate_sensor_data():
    """Generate random sensor data."""
    return {
        "temperature": random.uniform(20.0, 30.0),
        "humidity": random.uniform(30.0, 70.0),
        "pressure": random.uniform(980.0, 1020.0)
    }

def write_to_influxdb(data):
    """Write data points to InfluxDB."""
    timestamp = datetime.utcnow()
    
    for measurement, value in data.items():
        point = Point("sensors") \
            .field(measurement, value) \
            .time(timestamp)
        
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

def main():
    print("Starting serial data generator...")
    try:
        while True:
            data = generate_sensor_data()
            write_to_influxdb(data)
            print(f"Generated data: {data}")
            time.sleep(1)  # Generate data every second
            
    except KeyboardInterrupt:
        print("\nStopping data generation...")
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    main()