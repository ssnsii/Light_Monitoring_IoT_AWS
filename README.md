Light Monitoring IoT System

End-to-end real-time IoT light monitoring system:
ESP32 collects sensor data, publishes to AWS IoT Core via MQTT, stores in MongoDB Atlas, and uses Python and Dash for data aggregation, analysis, and interactive visualization.

Light Exposure in the Lobby

This project monitors light levels in the NIC building lobby.

Sensor: LM393 light sensor

Output: Digital binary signal (0 = high, 1 = low) based on a reference voltage threshold

Data Collection: From 13:00 PM to 17:00 PM in one day

Storage & Analysis: Data stored in MongoDB Atlas and analyzed using aggregation pipelines

Task 01 – Hardware Setup

LM393 sensor → ESP32 connection:

Sensor Pin	ESP32 Pin
VCC	3.3V
GND	GND
DO	GPIO 34

Connections made using a solderless breadboard

ESP32 reads binary output every minute, timestamps it, and sends data over WiFi to MongoDB Atlas

IoT System Data Flow

LM393 sensor detects light and outputs digital signal.

ESP32 reads signal, formats with timestamp, connects to WiFi.

MongoDB Atlas stores readings in the light_readings collection.

Python/Dash scripts retrieve data for aggregation and interactive visualization.

Task 02 – Database Structure

Database: add232iotdb
Collection: light_readings

Field	Description
_id	Unique identifier
light_reading	Binary output (0 or 1)
unit	Measurement unit (digital value)
time	Timestamp of reading

Indexes:

Single-field index on time – improves time-based query performance

Compound index on light_reading and time – optimizes queries filtering by both fields

Time Conversion:

Converted from string to ISODate for efficient date-based queries and aggregation

Task 03 – Aggregate Pipelines & Visualization

Data is retrieved and analyzed using Python with pymongo:

from pymongo import MongoClient
import pandas as pd
from urllib.parse import quote_plus
import warnings
from cryptography.utils import CryptographyDeprecationWarning

warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

password = quote_plus("123sn@sasa")
client = MongoClient(f"mongodb+srv://sithunissanka18:{password}@cluster0.a2qkogg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client['add232iotdb']
collection = db['light_readings']

# Retrieve all documents
for doc in collection.find():
    print(doc)


Detailed analysis, aggregation pipelines, and visualizations are available in analysis_notebook.ipynb
.

Project Structure
Light_Monitoring_IoT_AWS/
├── thonny_main.py          # ESP32 data collection script
├── atlas_iot.py            # AWS IoT communication
├── viz.py                  # Visualization scripts
├── analysis_notebook.ipynb # Jupyter Notebook for analysis
├── .gitignore
├── requirements.txt
├── credentials_thonny.py   # Local only
└── credentials2.py         # Local only

Setup Instructions

Clone the repository:

git clone https://github.com/ssnsii/Light_Monitoring_IoT_AWS.git
cd Light_Monitoring_IoT_AWS


Install dependencies:

pip install -r requirements.txt


Add AWS IoT and MongoDB credentials locally (not in GitHub).

Run ESP32 data collection:

python thonny_main.py


Analyze and visualize data:

python viz.py
# or
jupyter notebook analysis_notebook.ipynb

Highlights

Real-time IoT monitoring from sensor to cloud

Interactive visualization of lobby light levels

Optimized database queries using indexes and aggregation pipelines

End-to-end integration: hardware, cloud, database, and analytics
