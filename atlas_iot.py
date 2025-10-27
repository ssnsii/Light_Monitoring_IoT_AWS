"""
This script subscribes to an AWS IoT Core MQTT topic and stores received light readings into MongoDB Atlas.

MongoDB credentials and AWS IoT certificate paths are stored in a separate local file `credentials2.py`.
"""

import pymongo
import paho.mqtt.client as mqtt
import json
import urllib.parse
import warnings
from credentials2 import MONGO_USER, MONGO_PASS, AWS_CA, AWS_CERT, AWS_KEY


# Suppress cryptography deprecation warnings
warnings.filterwarnings("ignore", category=Warning)

# MongoDB Atlas credentials
username = urllib.parse.quote_plus(MONGO_USER)
password = urllib.parse.quote_plus(MONGO_PASS)

# MongoDB Atlas connection string
MONGO_URI = f"mongodb+srv://{username}:{password}@cluster0.a2qkogg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = 'add232iotdb'
COLLECTION_NAME = 'light_readings'

# MQTT settings
MQTT_BROKER = 'a3knr6ehf2lkw-ats.iot.us-east-1.amazonaws.com'
MQTT_PORT = 8883
MQTT_TOPIC = 'light_readings'

# Certificate files
CA_CERT = AWS_CA
CLIENT_CERT = AWS_CERT
CLIENT_KEY = AWS_KEY

# Initialize MongoDB client
try:
    mongo_client = pymongo.MongoClient(MONGO_URI)
    db = mongo_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    print("Connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# Callback function for handling incoming MQTT messages
def on_message(client, userdata, message):
    try:
        # Parse the JSON data from the message
        payload = json.loads(message.payload.decode())
        print(f"Received message: {payload}")

        # Store the message in MongoDB
        collection.insert_one(payload)
        print("Data inserted into MongoDB")

    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Error processing message: {e}")

# Initialize MQTT client with the latest Callback API version
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Set TLS parameters
try:
    mqtt_client.tls_set(ca_certs=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    print("TLS parameters set successfully")
except Exception as e:
    print(f"Failed to set up TLS: {e}")

# Set up callback for incoming messages
mqtt_client.on_message = on_message

# Connect to AWS IoT Core
try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
    print("Connected to MQTT broker")
except Exception as e:
    print(f"Connection to MQTT broker failed: {e}")

# Subscribe to the MQTT topic
try:
    mqtt_client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic {MQTT_TOPIC}")
except Exception as e:
    print(f"Failed to subscribe to topic: {e}")

# Start the MQTT client loop
try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("Interrupted by user")
except Exception as e:
    print(f"Error in MQTT loop: {e}")
