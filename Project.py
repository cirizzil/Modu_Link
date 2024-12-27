#SERVER CODE

import socket
import struct
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button
from threading import Thread
import queue
import csv  # Import csv module

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345      # Port number

temperature_data = queue.Queue()
light_intensity_data = queue.Queue()

def recvall(sock, n):
    """Helper function to receive n bytes or return None if EOF is hit."""
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def write_to_csv(device_id, timestamp, values, filename='data.csv'):
    """Function to write data into a CSV file."""
    # Check if file exists to determine if header is needed
    try:
        with open(filename, 'x', newline='') as csvfile:
            # File doesn't exist, write header
            fieldnames = ['device_id', 'timestamp'] + [f'value_{i+1}' for i in range(len(values))]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass  # File exists, proceed to append data

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['device_id', 'timestamp'] + [f'value_{i+1}' for i in range(len(values))]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        row = {'device_id': device_id, 'timestamp': timestamp}
        for i, value in enumerate(values):
            row[f'value_{i+1}'] = value
        writer.writerow(row)

def server_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")

            # Send "START" command to client
            command = "START"
            client_socket.send(command.encode())

            while True:
                try:
                    # Receive the number of variables (4 bytes)
                    data = recvall(client_socket, 4)
                    if not data:
                        break
                    num_variables = struct.unpack('I', data)[0]

                    # Receive the device ID (4 bytes)
                    data = recvall(client_socket, 4)
                    if not data:
                        break
                    device_id = struct.unpack('I', data)[0]

                    # Receive the timestamp (8 bytes)
                    data = recvall(client_socket, 8)
                    if not data:
                        break
                    timestamp = struct.unpack('d', data)[0]

                    # Receive the payload (num_variables * 4 bytes)
                    data = recvall(client_socket, num_variables * 4)
                    if not data:
                        break
                    values = struct.unpack(f"{'f' * num_variables}", data)

                    print(f"Received from device {device_id} at {timestamp}: {values}")

                    # Write data to CSV file
                    write_to_csv(device_id, timestamp, values)

                    # Put data into queues
                    temperature_data.put(values[0])
                    light_intensity_data.put(values[1])

                except Exception as e:
                    print(f"Error: {e}")
                    break

            client_socket.close()
            print(f"Connection closed with {client_address}")
    except KeyboardInterrupt:
        print("Shutting down server.")
    finally:
        server_socket.close()

def update_plot(frame):
    while not temperature_data.empty() and not light_intensity_data.empty():
        temp = temperature_data.get()
        light = light_intensity_data.get()
        x_data.append(len(x_data))
        temp_data.append(temp)
        light_data.append(light)

    if plotting and x_data:
        temp_line.set_data(x_data, temp_data)
        ax1.set_xlim(max(0, len(x_data) - 500), len(x_data))
        ax1.set_ylim(min(temp_data[-500:]), max(temp_data[-500:]))
        light_line.set_data(x_data, light_data)
        ax2.set_xlim(max(0, len(x_data) - 500), len(x_data))
        ax2.set_ylim(min(light_data[-500:]), max(light_data[-500:]))

server = Thread(target=server_thread, daemon=True)
server.start()

x_data = []
temp_data = []
light_data = []

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

temp_line, = ax1.plot([], [], label='Temperature (°C)')
ax1.set_title("Temperature Data")
ax1.set_xlabel("Time")
ax1.set_ylabel("Temperature (°C)")
ax1.legend()
ax1.grid(True)

light_line, = ax2.plot([], [], label='Light Intensity (V)', color='orange')
ax2.set_title("Light Intensity Data")
ax2.set_xlabel("Time")
ax2.set_ylabel("Light Intensity (V)")
ax2.legend()
ax2.grid(True)

plt.tight_layout()

from matplotlib.widgets import Button
plt.subplots_adjust(bottom=0.2)

ax_start = plt.axes([0.7, 0.05, 0.1, 0.075])    
ax_stop = plt.axes([0.81, 0.05, 0.1, 0.075])

btn_start = Button(ax_start, 'Start')
btn_stop = Button(ax_stop, 'Stop')

plotting = False

def start_plotting(event):
    global plotting
    plotting = True
    x_data.clear()
    temp_data.clear()
    light_data.clear()
    while not temperature_data.empty():
        temperature_data.get()
    while not light_intensity_data.empty():
        light_intensity_data.get()
    print("Plotting started.")

def stop_plotting(event):
    global plotting
    plotting = False
    print("Plotting stopped.")

btn_start.on_clicked(start_plotting)
btn_stop.on_clicked(stop_plotting)

ani = FuncAnimation(fig, update_plot, interval=50)  # Update every 50ms

plt.show()
