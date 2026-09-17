# calculator_client.py
 
import socket                                      # TCP socket communication
import json                                        # JSON serialization
 
HOST = "54.226.222.239"                               # Server IP address.
PORT = 8080                                          # Server port
 
while True:
    operation = input("Enter operation (add, sub, mul, div, exit): ") # Read operation as text
 
    if operation == "exit":                         # Let the user end the client loop
        print("Saliendo del cliente...")
        break                                        # NOTE: this only stops asking for more
                                                       # operations. No TCP connection is open
                                                       # at this point to close, because each
                                                       # operation below opens and closes its
                                                       # OWN socket.
 
    a = input("Enter first number: ")                # Read first value as text
    b = input("Enter second number: ")                # Read second value as text
 
    payload = {                                        # Create request dictionary
        "a": a,                                        # Store first value
        "b": b,                                        # Store second value
        "operation": operation                         # Store requested operation
    }
 
    # --- One connection per operation, as required by the lab spec ---
    s = socket.socket()                    # Create a NEW TCP socket for this operation
    s.connect((HOST, PORT))                # Connect to server
    s.send(json.dumps(payload).encode())   # Serialize and send request. json.dumps(payload) converts the payload dictionary into a JSON string, and .encode() converts that string into bytes, which is the format required for sending data over a socket.
 
    response = s.recv(1024).decode()       # Receive server response
    print("Server response:", response)                # Display response
    s.close()                              # Close THIS connection before looping again
    # -------------------------------------------------------------
