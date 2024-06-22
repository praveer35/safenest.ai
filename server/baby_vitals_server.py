import socket
import time
import json
import random

# Initial values centered around typical baby vitals
initial_bpm = 120
initial_temp = 36.5
breathe_state = "Breathe in"

current_bpm = initial_bpm
current_temp = initial_temp

# Function to update vitals every 3 seconds
def update_vitals():
    global current_bpm, current_temp, breathe_state
    # Randomize BPM by +-3 beats, keeping it within a realistic range
    current_bpm = max(100, min(160, initial_bpm + random.randint(-3, 3)))
    
    # Randomize temperature by +-0.05 degrees, keeping it within a realistic range
    current_temp = max(36.0, min(37.5, initial_temp + random.uniform(-0.05, 0.05)))
    
    # Switch breathing state
    breathe_state = "Breathe out" if breathe_state == "Breathe in" else "Breathe in"


def handle_client(client_socket):
    try:
        while True:
            update_vitals()
            vitals = {
                "BPM": current_bpm,
                "Temperature": current_temp,
                "Breathing": breathe_state
            }
            client_socket.sendall(json.dumps(vitals).encode('utf-8'))
            time.sleep(3)
    except BrokenPipeError:
        print("Client disconnected")
    finally:
        client_socket.close()

# Function to start the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(1)  # Handle one client at a time
    print("Server started on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        handle_client(client_socket)

# Start the server
start_server()
