
# Modu-Link: Remote Access Controller (RAC)

Modu-Link is a low-cost, open-source IoT project designed to remotely monitor and control connected sensors via Wi-Fi. This repository contains both the ESP32 client-side and server-side implementations, enabling seamless wireless data logging and visualization.

## Features

- **Wireless Data Transmission**: Connects sensors to a remote server for real-time monitoring.
- **Multi-Sensor Support**: Handles temperature and light intensity sensors, with extensibility for more.
- **Data Logging**: Logs sensor data into CSV files for further analysis.
- **Real-Time Visualization**: Plots live temperature and light intensity graphs using `matplotlib`.
- **User Commands**: Supports commands like `START`, `STOP`, `RATE`, and `RESET` for flexible operation.

## Repository Structure

```
📂 Modu-Link
├── main.py               # ESP32 client-side code for sensor reading and data transmission
├── Project.py            # Server-side code for receiving, logging, and visualizing sensor data
├── data.csv              # Example CSV log for sensor data
├── generated_sensor_data.csv  # Generated data for simulation/testing
├── Test.csv              # Additional test dataset
└── README.md             # Project documentation
```
## Overview Diagram 
![image](https://github.com/user-attachments/assets/63a3abef-70a1-4bdf-9193-1e6f22b91baf)

## Requirements

### Hardware
- **ESP32** with Wi-Fi capabilities
- Temperature sensor (e.g., analog thermistor)
- Light intensity sensor (e.g., photodiode)
- Breadboard and prototyping wires
- Wi-Fi router

### Software
- Python 3.x
- Libraries: `socket`, `struct`, `matplotlib`, `csv`, `threading`
- MicroPython for ESP32

## Getting Started

### 1. ESP32 Setup
1. Flash the `main.py` script to your ESP32 using your preferred MicroPython IDE.
2. Update the Wi-Fi credentials and server IP address in `main.py`:
   ```python
   ssid = 'YourSSID'
   password = 'YourPassword'
   SERVER_IP = 'ServerIPAddress'
   ```

### 2. Server Setup
1. Run the `Project.py` script on the server machine.
2. Ensure the server is listening on the appropriate IP and port (default: `0.0.0.0:12345`).

### 3. Sensor Connections
- Connect the temperature sensor to ADC pin 39 on the ESP32.
- Connect the light intensity sensor to ADC pin 34.

### 4. Real-Time Visualization
- `Project.py` provides real-time plots for temperature and light intensity data.
- Use the "Start" and "Stop" buttons in the GUI to control plotting.

## Commands Supported
The server communicates with the ESP32 using the following commands:
- `START`: Begin data transmission.
- `STOP`: Halt data transmission.
- `RATE = X`: Set sampling rate (in seconds).
- `RESET`: Restart the ESP32.

## CSV Data Logging
- Sensor data is logged to `data.csv` with fields:
  - `device_id`
  - `timestamp`
  - `temperature`
  - `light_intensity`

### Data Logging (CSV)
```
device_id,timestamp,temperature,light_intensity
1,1693312675.5,24.5,0.76
1,1693312676.5,24.8,0.82
```

### Real-Time Visualization

https://github.com/user-attachments/assets/7606ce9f-fd0f-488b-8319-b7e4c472062f


### 3D Print Case
![image](https://github.com/user-attachments/assets/9c0b2384-55ec-42b8-8e4e-98cb64e925d1)
![image](https://github.com/user-attachments/assets/15cc3a19-9080-4873-8cbb-640d37689fca)

## Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests for bug fixes or feature enhancements.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Authors
- **Ciril Biju Joseph** - Software Development
- **Benjamin Hughes** - Embedded Systems & Hardware Integration
- **Trevor Standen** - Project Management & Hardware Design
- **Aditya Manoj** - Enclosure Design

