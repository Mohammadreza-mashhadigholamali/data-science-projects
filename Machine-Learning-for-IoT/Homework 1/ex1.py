import adafruit_dht
import uuid
import time
from datetime import datetime
from board import D4
import redis
import argparse


# Parse command-line arguments for Redis connection
parser = argparse.ArgumentParser(description="Temperature and Humidity Monitoring with Redis TimeSeries")
parser.add_argument("--host", required=True, help="Redis Cloud host")
parser.add_argument("--port", type=int, required=True, help="Redis Cloud port")
parser.add_argument("--user", required=True, help="Redis Cloud username")
parser.add_argument("--password", required=True, help="Redis Cloud password")
args = parser.parse_args()



# Connect to Redis
redis_client = redis.Redis(
    host=args.host,
    port=args.port,
    username=args.user,
    password=args.password
)

is_connected = redis_client.ping()

# Sensor settings
dht_device = adafruit_dht.DHT11(D4)

mac_address = hex(uuid.getnode())
temperature_ts_name = f'{mac_address}:temperature'
humidity_ts_name = f'{mac_address}:humidity'

one_day_in_ms = 24 * 60 * 60 * 1000




# TimeSeries keys
temperature_key = f'{mac_address}:temperature'
humidity_key = f'{mac_address}:humidity'
temperature_min_key = f'{mac_address}:temperature_min'
temperature_max_key = f'{mac_address}:temperature_max'
temperature_avg_key = f'{mac_address}:temperature_avg'
humidity_min_key = f'{mac_address}:humidity_min'
humidity_max_key = f'{mac_address}:humidity_max'
humidity_avg_key = f'{mac_address}:humidity_avg'

# Create TimeSeries with retention and aggregation rules
try:
    # Temperature TimeSeries (2 seconds interval, 30 days retention)
    redis_client.ts().create(temperature_key, retention_msecs=30 * one_day_in_ms)
    redis_client.ts().create(humidity_key, retention_msecs=30 * one_day_in_ms)

    # Aggregated TimeSeries (1-hour bucket, 365 days retention)
    redis_client.ts().create(temperature_min_key, retention_msecs=365 * one_day_in_ms)
    redis_client.ts().create(temperature_max_key, retention_msecs=365 * one_day_in_ms)
    redis_client.ts().create(temperature_avg_key, retention_msecs=365 * one_day_in_ms)

    redis_client.ts().create(humidity_min_key, retention_msecs=365 * one_day_in_ms)
    redis_client.ts().create(humidity_max_key, retention_msecs=365 * one_day_in_ms)
    redis_client.ts().create(humidity_avg_key, retention_msecs=365 * one_day_in_ms)

    # Add aggregation rules
    redis_client.ts().createrule(temperature_key, temperature_min_key, 'min', bucket_size_msec=3600 * 1000)
    redis_client.ts().createrule(temperature_key, temperature_max_key, 'max', bucket_size_msec=3600 * 1000)
    redis_client.ts().createrule(temperature_key, temperature_avg_key, 'avg', bucket_size_msec=3600 * 1000)

    redis_client.ts().createrule(humidity_key, humidity_min_key, 'min', bucket_size_msec=3600 * 1000)
    redis_client.ts().createrule(humidity_key, humidity_max_key, 'max', bucket_size_msec=3600 * 1000)
    redis_client.ts().createrule(humidity_key, humidity_avg_key, 'avg', bucket_size_msec=3600 * 1000)

    print("TimeSeries and aggregation rules created successfully!")
except redis.ResponseError as e:
    print("Error creating TimeSeries or rules:", e)


# Read data from the DHT-11 sensor and store it in Redis
while True:
    timestamp = int(time.time() * 1000)
    formatted_time = datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')

    try:
        # Read temperature and humidity from the sensor
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is not None and humidity is not None:
            # Store data in Redis TimeSeries
            redis_client.ts().add(temperature_key, timestamp, temperature)
            redis_client.ts().add(humidity_key, timestamp, humidity)

            print(f'{formatted_time} - Temperature: {temperature}°C, Humidity: {humidity}%')
        else:
            print(f'{formatted_time} - Failed to retrieve data from the sensor.')

    except RuntimeError as e:
        print(f"{formatted_time} - Sensor error: {e}. Retrying...")

    except Exception as e:
        print(f"{formatted_time} - Unexpected error: {e}")
    
    # Wait for 2 seconds before the next reading
    time.sleep(2)

