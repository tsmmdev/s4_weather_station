import os
import sys
import json

ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
MODULES_DIRECTORY = os.path.join(ROOT_FOLDER, "modules")

sys.path.append(MODULES_DIRECTORY)
import server

CONFIG_PATH = os.path.join(ROOT_FOLDER, "config.json")
# Read the config file
with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)
CLIENTS = CONFIG.get("clients", {})
CERT_CONFIG = CONFIG.get("certificates", {})
CERT_FOLDER = os.path.join(ROOT_FOLDER, CERT_CONFIG["folder"])
SERVER_KEY = os.path.join(CERT_FOLDER, CERT_CONFIG["key"])
SERVER_CERTIFICATE = os.path.join(CERT_FOLDER, CERT_CONFIG["certificate"])
# Define the JWT secret key
JWT_SECRET = CONFIG.get("jwt_secret", "r6Aur&A$nLyf*npUhYvv@i5j*D8$5PKY")
# Define the host and port to listen on
HOST = CONFIG.get("host", "0.0.0.0")  # Listen on all available network interfaces
PORT = CONFIG.get("port", 12345)  # Listen on port 12345
KEY_FILE = os.path.join(CERT_FOLDER, SERVER_KEY)
CERTIFICATE_FILE = os.path.join(CERT_FOLDER, SERVER_CERTIFICATE)

server.server_socket(
    CLIENTS,
    JWT_SECRET,
    HOST,
    PORT,
    KEY_FILE,
    CERTIFICATE_FILE
)

# 
# 
# def handle_signal(signum, frame):
#     # Clean up the socket and exit
#     wrapped_socket.close()
#     print("Server stopped")
#     sys.exit(0)
# 
# # Create a socket and listen for connections
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.bind((HOST, PORT))
# sock.listen()
# 
# # Wrap the socket with SSL
# wrapped_socket = ssl.wrap_socket(sock, keyfile=KEY_FILE, certfile=CERTIFICATE_FILE, server_side=True)
# 
# # Print the status of the socket
# print(f"Server is listening on {HOST}:{PORT}")
# 
# 
# # Register the signal handler function
# signal.signal(signal.SIGINT, handle_signal)
# 
# # Accept connections and handle requests
# while True:
#     conn, addr = wrapped_socket.accept()
#     with conn:
#         # Receive the data from the device
#         data = b""
#         length = 1024
#         index_len_end = 0
#         try:
#             while True:
#                 chunk = conn.recv(1024)
#                 if chunk.startswith(b'[') and b']' in chunk[:-1]:
#                     # process the data
#                     index_len_end = chunk.index(b']')
#                     len_string = chunk[0:(index_len_end + 1)]
#                     length = int(chunk[1:index_len_end]) + len(len_string)
# 
#                 data += chunk
# 
#                 if not chunk or length == len(data):
#                     break
# 
#             data = data[index_len_end + 1:]
# 
#             # Verify the JWT token
#             try:
#                 payload = jwt.decode(data, JWT_SECRET, algorithms=['HS256'])
#                 device_id = payload['device_id']
#                 if not CLIENTS[device_id]:
#                     conn.sendall(b'Invalid device')
#                 else:
#                     # print(payload['data'])
#                     json_str_prety = json.dumps(payload['data'], indent=4)
#                     print(json_str_prety)
#                     # TODO: add data to sql
#                     conn.sendall(b'OK')
#             except jwt.exceptions.InvalidTokenError:
#                 # The token is invalid, send an error response to the device
#                 conn.sendall(b'Invalid token')
# 
#         except KeyboardInterrupt:
#             # Clean up the socket and exit
#             wrapped_socket.close()
#             print("Server stopped")
