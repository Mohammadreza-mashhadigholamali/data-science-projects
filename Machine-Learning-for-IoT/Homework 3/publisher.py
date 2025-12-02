import time
import json
import paho.mqtt.client as mqtt
import uuid
import adafruit_dht
from board import D4

mac_address = hex(uuid.getnode())
student_id = "s327874"
dht_device = adafruit_dht.DHT11(D4)

def run():
    client = mqtt.Client()
    client.connect("mqtt.eclipseprojects.io", 1883)
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            
            message = json.dumps({
                "mac_address": mac_address,
                "timestamp": int(time.time() * 1000),
                "temperature": temperature,
                "humidity": humidity
            })
            client.publish(f"{student_id}", message)
        except:
            print('sensor failure')

        time.sleep(2)

if __name__ == "__main__":
    run()
