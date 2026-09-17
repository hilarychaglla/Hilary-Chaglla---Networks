import socket                                      # TCP socket communication
import json                                        # JSON parsing and serialization

HOST = "0.0.0.0"                                    # Listen on all network interfaces
PORT = 8080                                         # Server port

def handle_request(data):                           # Process one client request
    try:
        payload = json.loads(data)                 # Convert JSON string into dictionary
        a = payload.get("a")                       # Get first value
        b = payload.get("b")                       # Get second value
        operation = payload.get("operation")       # Get requested operation

        # TODO 1: Check if any required parameter is missing
        if a is None or b is None or operation is None:
            return {"result": None, "error": "MISSING_PARAMETERS", "code": 400}

        # Validate that operation, a and b arrive as strings (per spec)
        if not isinstance(a, str) or not isinstance(b, str) or not isinstance(operation, str):
            return {"result": None, "error": "INVALID_TYPE", "code": 400}

        # TODO 2: Validate that a and b can be converted to numbers
        try:
            a_num = float(a)
            b_num = float(b)
        except ValueError:
            return {"result": None, "error": "INVALID_NUMBER", "code": 422}

        # TODO 3: Implement the supported operations (add, sub, mul, div)
        # TODO 4: Handle division by zero
        if operation == "add":
            result = a_num + b_num
        elif operation == "sub":
            result = a_num - b_num
        elif operation == "mul":
            result = a_num * b_num
        elif operation == "div":
            if b_num == 0:
                return {"result": None, "error": "DIVISION_BY_ZERO", "code": 422}
            result = a_num / b_num
        else:
            # TODO 5: Handle unsupported operations
            return {"result": None, "error": "UNSUPPORTED_OPERATION", "code": 400}

        # TODO 6: Return a successful response using the standardized format
        return {"result": result, "error": None, "code": 200}

    except json.JSONDecodeError:
        # TODO 7: Return an appropriate error for invalid JSON
        return {"result": None, "error": "INVALID_JSON", "code": 400}
    except Exception:
        # Unexpected server-side errors
        return {"result": None, "error": "INTERNAL_ERROR", "code": 500}

# Create TCP socket
server_socket = socket.socket()                    # Create IPv4 TCP socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))                   # Bind socket to IP and port
server_socket.listen(5)                            # Start listening for connections

print(f"Calculator server running on {HOST}:{PORT}") # Display server status

while True:                                        # Keep server running
    conn, addr = server_socket.accept()            # Accept incoming connection
    print(f"Connection from {addr}")               # Display client address
    data = conn.recv(1024).decode()                # Receive client data
    response = handle_request(data)                # Process request on server
    response_json = json.dumps(response)           # Convert response to JSON

    # Log the operation (client IP, operation, values, result/error, code)
    try:
        payload = json.loads(data)
        operation_log = payload.get("operation")
        a_log = payload.get("a")
        b_log = payload.get("b")
    except json.JSONDecodeError:
        operation_log = a_log = b_log = None

    print(f"Client: {addr[0]}")
    print(f"Operation: {operation_log}")
    print(f"a: {a_log}")
    print(f"b: {b_log}")
    if response["error"] is None:
        print(f"Result: {response['result']}\nCode: {response['code']}\n")
    else:
        print(f"Error: {response['error']}\nCode: {response['code']}\n")

    conn.send(response_json.encode())              # Send response to client
    conn.close()                                   # Close client connection
