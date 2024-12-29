#!/usr/bin/env python3

import serial
import time
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Serial port configuration
SERIAL_PORT = '/dev/ttyUSB0'  # Adjust this based on your system
BAUD_RATE = 9600
TIMEOUT = 1

# InfluxDB configuration
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "your-token-here"
INFLUX_ORG = "your-org"
INFLUX_BUCKET = "XXXXXXXXXXX"

def setup_serial():
    """Initialize and return serial connection"""
    try:
        ser = serial.Serial(
            port=SERIAL_PORT,
            baudrate=BAUD_RATE,
            timeout=TIMEOUT,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def parse_data(raw_data):
    """Parse the raw data from RS485
    Modify this function according to your specific data format
    """
    try:
        # Example parsing - modify according to your data format
        # Assuming data comes as: "value1,value2,value3"
        data = raw_data.decode().strip()
        values = data.split(',')
        
        return {
            'value1': float(values[0]),
            'value2': float(values[1]),
            'value3': float(values[2])
        }
    except Exception as e:
        print(f"Error parsing data: {e}")
        return None

def write_to_influxdb(client, data):
    """Write parsed data to InfluxDB"""
    try:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        point = Point("sensor_data") \
            .field("value1", data['value1']) \
            .field("value2", data['value2']) \
            .field("value3", data['value3'])
        
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        print("Data written to InfluxDB successfully")
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

def main():
    # Setup serial connection
    ser = setup_serial()
    if not ser:
        print("Failed to setup serial connection")
        return

    # Setup InfluxDB client
    client = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG
    )

    print("Starting data collection...")
    
    try:
        while True:
            if ser.in_waiting > 0:
                # Read data from serial port
                raw_data = ser.readline()
                
                # Parse the data
                parsed_data = parse_data(raw_data)
                
                if parsed_data:
                    # Write to InfluxDB
                    write_to_influxdb(client, parsed_data)
            
            time.sleep(0.1)  # Small delay to prevent CPU overuse
            
    except KeyboardInterrupt:
        print("\nStopping data collection...")
    finally:
        ser.close()
        client.close()

if __name__ == "__main__":
    main()