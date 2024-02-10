# import os
from .config import Config
# import json
import signal
import socket
import ssl
import sys
import jwt
from .helpers import log_time_zone
from .db import WeatherDatabase
import time


class WeatherServer:
    def __init__(self, root_folder):
        self.config = Config(root_folder)

    def start(self):
        weather_db = WeatherDatabase(db_file=self.config.get_db_file())
        weather_db.update_devices(self.config.get_clients())

        def handle_signal(signum, frame):
            # Clean up the socket and exit
            wrapped_socket.close()
            print("Server stopped")
            sys.exit(0)

        def bind_socket(host_value, port_value):
            attempt = 0
            max_attempts = 10  # Maximum number of attempts
            delay = 10  # Delay in seconds between attempts

            while True:
                try:
                    # Create a socket and listen for connections
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.bind((host_value, port_value))
                    sock.listen()

                    # Wrap the socket with SSL
                    wrapped_socket_ssl = ssl.wrap_socket(
                        sock,
                        keyfile=self.config.get_certificate_key(),
                        certfile=self.config.get_certificate(),
                        server_side=True
                    )

                    print(f"{log_time_zone()}: Server is listening on {host_value}:{port_value}")
                    print()
                    # Register the signal handler function
                    signal.signal(signal.SIGINT, handle_signal)

                    return wrapped_socket_ssl

                except OSError as e:
                    if e.errno == 98 and attempt < max_attempts:
                        print(f"Address already in use. Retrying in {delay} seconds...")
                        attempt += 1
                        time.sleep(delay)
                    else:
                        print("Failed to start server after multiple attempts. Exiting.")
                        sys.exit(1)

        # Get host and port from configuration
        host = self.config.get_host()
        port = self.config.get_port()

        # Bind the socket
        wrapped_socket = bind_socket(host, port)

        while True:
            conn, addr = wrapped_socket.accept()
            with conn:
                # Receive the data from the device
                data = b""
                length = 1024
                index_len_end = 0
                try:
                    # reload config so we could dynamically react to changes
                    self.config.load_config()
                    weather_db.init_db()
                    weather_db.update_devices(self.config.get_clients())
                    print(f"{log_time_zone()}: someone is knocking")
                    while True:
                        chunk = conn.recv(1024)
                        if chunk.startswith(b'[') and b']' in chunk[:-1]:
                            # process the data
                            index_len_end = chunk.index(b']')
                            len_string = chunk[0:(index_len_end + 1)]
                            length = int(chunk[1:index_len_end]) + len(len_string)

                        data += chunk

                        if not chunk or length == len(data):
                            break

                    data = data[index_len_end + 1:]

                    # Verify the JWT token
                    try:
                        payload = jwt.decode(
                            data,
                            self.config.get_jwt_secret(),
                            algorithms=['HS256']
                        )
                        device = payload['device']
                        print(f"{log_time_zone()}: {device} is connected")
                        clients = self.config.get_clients()
                        if not clients.get(device):
                            conn.sendall(b'Invalid device')
                        else:
                            # json_str_pretty = json.dumps(payload['data'], indent=4)
                            # print(json_str_pretty)
                            status = weather_db.add_data(device, payload['data'])
                            if status.get('status'):
                                conn.sendall(b'OK')
                            else:
                                conn.sendall(bytes(status['message'], 'utf-8'))

                            print(f"{log_time_zone()}: {device} is disconnected")
                            print()
                    except jwt.exceptions.InvalidTokenError:
                        # The token is invalid, send an error response to the device
                        conn.sendall(b'Invalid token')

                except KeyboardInterrupt:
                    # Clean up the socket and exit
                    wrapped_socket.close()
                    print("Server stopped")
