# calculator_client.py

import socket                                      # TCP socket communication
import json                                        # JSON serialization

HOST = "54.226.222.239"                               # Server IP address.
PORT = 8080                                          # Server port

a = input("Enter first number: ")                  # Read first value as text
b = input("Enter second number: ")                 # Read second value as text
operation = input("Enter operation (add, sub, mul, div): ") # Read operation as text

payload = {                                        # Create request dictionary
    "a": a,                                        # Store first value
    "b": b,                                        # Store second value
    "operation": operation                         # Store requested operation
}

s = socket.socket()                    # Create TCP socket
s.connect((HOST, PORT))                # Connect to server
s.send(json.dumps(payload).encode())   # Serialize and send request. json.dumps(payload) converts the payload dictionary into a JSON string, and .encode() converts that string into bytes, which is the format required for sending data over a socket.

response = s.recv(1024).decode()       # Receive server response
print("Server response:", response)                # Display response
s.close()                              # Close connection
