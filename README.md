# Light Monitoring IoT System
## Project Overview

## End-to-end Real-Time IoT Light Monitoring System

This project demonstrates a complete IoT pipeline for monitoring light exposure. The system uses an ESP32 microcontroller with an LM393 light sensor to collect real-time light data, publishes it to AWS IoT Core via MQTT, stores it in MongoDB Atlas, and uses Python and Dash for aggregation, analysis, and interactive visualization.

## Key Highlights:

Real-time light monitoring with automated data collection.

Cloud integration using AWS IoT Core.

Efficient storage and query with MongoDB Atlas.

Interactive visualization and analysis using Python and Dash.


## System Architecture

<img width="1162" height="617" alt="image" src="https://github.com/user-attachments/assets/a80d908e-0586-48bc-a2af-b07c2a26f91d" />

## Dataflow

<img width="1262" height="835" alt="image" src="https://github.com/user-attachments/assets/abb3c97e-7447-467e-96dc-7cdeebc54684" />
The system implements an end-to-end real-time IoT light monitoring pipeline. The LM393 light sensor detects lobby light levels and outputs binary readings (0 or 1), which are read and timestamped every minute by the ESP32 microcontroller. The ESP32 publishes these readings securely to AWS IoT Core via MQTT, which then forwards the data to MongoDB Atlas for storage. Each record includes the light value, unit, and timestamp. Python and Dash applications retrieve the stored data to perform aggregation, analysis, and generate interactive visualizations, enabling real-time monitoring and historical trend analysis.

## Hardware Setup

## Components Used:

ESP32 Microcontroller

LM393 Light Sensor

Solderless Breadboard

Jumper Wires

## Sensor Pin Connections:

VCC        -> 3.3V         -> Power supply

GND        -> GND          -> Ground connection

DO         -> GPIO 34      -> Digital output signal to ESP32

The LM393 sensor provides a binary output based on the comparison between ambient light intensity and a reference threshold.

## Data Analysis & Visualization

Aggregated and processed data is retrieved using Python scripts.
Dash dashboard provide interactive visualizations for:
Real-time light exposure monitoring
Trend analysis over time intervals
Binary time series representation of light intensity
Benefits:
Enables quick detection of unusual light patterns in the lobby.
Facilitates decision-making for building lighting management.

## Technologies Used

Hardware: ESP32, LM393 light sensor, breadboard, jumper wires

Cloud: AWS IoT Core

Database: MongoDB Atlas

Programming & Analysis: Python, Pandas, PyMongo

Visualization: Dash, Plotly

## Setup & Running Instructions

1. Clone the Repository

```
git clone https://github.com/ssnsii/Light_Monitoring_IoT_AWS.git
cd Light_Monitoring_IoT_AWS
```

3. Configure Credentials

Add your AWS IoT Core credentials and MongoDB connection details in credentials_thonny.py (local only).

3. Run the ESP32 Firmware

Flash thonny_main.py (or your ESP32 script) onto the ESP32 using Thonny.

Ensure the device connects to your Wi-Fi network.

4. Collect & Publish Data

The ESP32 will read the LM393 sensor every minute and publish data to AWS IoT Core, which forwards it to MongoDB Atlas.

5. Run Data Analysis & Visualization

```
python viz.py
```
This will launch a Dash web dashboard to visualize light intensity over time.
