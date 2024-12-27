#ESP CODE

import socket
import network
import time
import struct  # For packing/unpacking data
from machine import ADC, Pin, reset

# Wi-Fi credentials
ssid = 'SSID'
password = 'PASSWORD'

# Server Configuration
SERVER_IP = '192.168.1.x'  # Server IP address
PORT = 12345  # Port number

# Connect to Wi-Fi with a timeout
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # Attempt to connect to Wi-Fi
    wlan.connect(ssid, password)
    print("Connecting to Wi-Fi...")
    
    # Wait for connection with a timeout (e.g., 10 seconds)
    timeout = 10
    while not wlan.isconnected() and timeout > 0:
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print(f"Connected to Wi-Fi. IP: {wlan.ifconfig()[0]}")
        return wlan.ifconfig()[0]  # Return IP address
    else:
        print("Failed to connect to Wi-Fi.")
        return None

def send_receive_data():
    Polling = 0  # Default polling state (off)
    rate = 2  # Default sample rate (1 second)
    while True:  # Keep trying to send data until connection is successful
        try:
            # Create socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((SERVER_IP, PORT))
            print(f"Connected to server at {SERVER_IP}:{PORT}")
            device_id = 1  # Unique device ID for the client

            # Receive initial command from server
            command = s.recv(1024).decode("utf-8")
            print(f"Received from server: {command}")
            if command == "START":
                print("Starting data transmission...")
                Polling = 1
            else:
                print(f"Unknown command: {command}")
                Polling = 0

            while True:
                if Polling == 1:
                    # Read temperature from external sensor
                    adc1 = ADC(39)  # ADC pin for internal temperature sensor
                    tempsensevoltage = adc1.read_uv()
                    tempsensevoltage = tempsensevoltage / 1000  # Convert to mV
                    Temp = (tempsensevoltage - 500) / 10  # Temperature in Celsius

                    # Read light intensity from photodiode
                    adc2 = ADC(Pin(34))  # ADC pin for photodiode sensor
                    photodiodevoltage = adc2.read_uv() / 1000  # Convert to mV

                    # Prepare data transfer
                    timestamp = time.time()  # Current timestamp

                    # Store temperature and light intensity data into array for packing
                    data = [Temp, photodiodevoltage]

                    # Send the number of variables (as a 4-byte unsigned int)
                    num_variables = len(data)
                    header = struct.pack('I', num_variables)
                    s.send(header)

                    # Send the device ID (as 4 bytes - unsigned int)
                    device_id_header = struct.pack('I', device_id)
                    s.send(device_id_header)

                    # Send the timestamp (as 8 bytes - double precision float)
                    timestamp_header = struct.pack('d', timestamp)
                    s.send(timestamp_header)

                    # Send the payload (the data as floats)
                    payload = struct.pack(f"{'f' * num_variables}", *data)
                    s.send(payload)

                    # Receive acknowledgment
                    response = s.recv(1024).decode()
                    print(f"Server response: {response}")
                    time.sleep(rate)
                else:
                    # If not polling, wait for commands
                    command = s.recv(1024).decode("utf-8")
                    print(f"Received from server: {command}")
                    if command == "START":
                        print("Starting data transmission...")
                        Polling = 1
                    elif command == "STOP":
                        print("Stopping data transmission...")
                        Polling = 0
                    elif command.startswith("RATE = "):
                        try:
                            # Extract the rate value
                            rate = float(command.split("=")[1].strip())
                            print(f"Setting sample rate to {rate} seconds.")
                        except ValueError:
                            print("Invalid sample rate value.")
                    elif command == "RESET":
                        print("Resetting ESP32...")
                        reset()  # Reset the ESP32
                    else:
                        print(f"Unknown command: {command}")

        except (OSError, Exception) as e:
            print(f"Error: {e}")
            s.close()  # Close the socket if there was an error
            print("Attempting to reconnect in 2 seconds...")
            time.sleep(2)  # Wait before trying to reconnect
            reset()  # Restart the ESP32 to attempt reconnecting

# Main function
if __name__ == '__main__':
    wifi_ip = connect_wifi()  # Connect to Wi-Fi
    if wifi_ip is None:
        print("Exiting program due to Wi-Fi connection failure.")
        reset()  # Restart ESP32 if Wi-Fi connection failed
    send_receive_data()  # Start sending and receiving data

