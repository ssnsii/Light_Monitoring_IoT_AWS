"""
This MicroPython script runs on an ESP32 to monitor light intensity using an LM393 light sensor.
It connects to Wi-Fi, reads the sensor’s digital output (0 = dark, 1 = bright), and securely publishes
these readings with timestamps to AWS IoT Core every minute using MQTT over TLS.
"""

import time
import machine
import network
import ujson
from umqtt.simple import MQTTClient
import ubinascii
import ssl
import ntptime
from credentials_thonny import SSID, PASS, AWS_ENDPOINT, CA_CERT_FILE, CLIENT_CERT_FILE, CLIENT_KEY_FILE

# Wi-Fi and AWS IoT credentials are imported from a separate local file (credentials_thonny.py)
# that is not uploaded to GitHub for security reasons.

# Wi-Fi credentials
# SSID = b''
# PASS = b''

# AWS Endpoint
# AWS_ENDPOINT = b''

# AWS IoT Core publish and subscribe topics
PUB_TOPIC = b'light_readings'

# Path to certificate files
# CA_CERT_FILE = ''
# CLIENT_CERT_FILE = ''
# CLIENT_KEY_FILE = ''

# Define light (Onboard LED) and set its default state to off
light = machine.Pin(2, machine.Pin.OUT)
light.off()

# Setup digital pin for LM393 sensor output (GPIO34)
sensor_pin = machine.Pin(34, machine.Pin.IN)

# Function to connect to Wi-Fi
def wifi_connect():
    print('Connecting to Wi-Fi...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASS)
    while not wlan.isconnected():
        light.on()
        print('Waiting for connection...')
        time.sleep(0.5)
        light.off()
        time.sleep(0.5)
    print('Connection details: %s' % str(wlan.ifconfig()))

# Function to load certificate files
def load_certificate(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

# Load certificates
ca_cert = load_certificate(CA_CERT_FILE)
client_cert = load_certificate(CLIENT_CERT_FILE)
client_key = load_certificate(CLIENT_KEY_FILE)

# Create SSL context for secure MQTT connection
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(certfile=CLIENT_CERT_FILE, keyfile=CLIENT_KEY_FILE)
context.load_verify_locations(cafile=CA_CERT_FILE)

# Function to connect to MQTT
def connect_mqtt():
    client_id = ubinascii.hexlify(machine.unique_id())
    mqtt = MQTTClient(
        client_id=client_id,
        server=AWS_ENDPOINT,
        port=8883,
        keepalive=60,
        ssl=context
    )
    while True:
        try:
            mqtt.connect()
            print("MQTT connected")
            break
        except Exception as e:
            print("MQTT connection failed:", e)
            time.sleep(5)
    return mqtt

# Initial Wi-Fi and MQTT setup
wifi_connect()
mqtt = connect_mqtt()

# Synchronize time using NTP
ntptime.settime()

# Function to get the light sensor reading
def get_light_reading():
    return sensor_pin.value()

# Main loop
while True:
    try:
        light_value = get_light_reading()
        # Get current time (localtime returns a tuple with (year, month, day, hour, minute, second, weekday, yearday))
        current_time = "{}-{}-{} {}:{}:{}".format(
            time.localtime()[0], time.localtime()[1], time.localtime()[2],
            time.localtime()[3], time.localtime()[4], time.localtime()[5]
        )
        message = ujson.dumps({"light_reading": light_value, "unit": "Digital value", "time": current_time})
        print('Publishing topic %s message %s' % (PUB_TOPIC, message))
        mqtt.publish(PUB_TOPIC, message)
    except Exception as e:
        print("Failed to publish message:", e)
    time.sleep(60)  # 1 minute

