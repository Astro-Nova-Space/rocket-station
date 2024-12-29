import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# InfluxDB connection parameters
INFLUXDB_URL = os.getenv('INFLUXDB_URL')
INFLUXDB_USERNAME = os.getenv('INFLUXDB_USERNAME')
INFLUXDB_PASSWORD = os.getenv('INFLUXDB_PASSWORD')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG')
INFLUXDB_BUCKET = os.getenv('INFLUXDB_BUCKET')