# import os
import json
import signal
import socket
import ssl
import sys
import jwt
import datetime
from .db import WeatherDatabase


class WeatherServer:
    def __init__(
            self,
            config
    ):
        self.config = config

    # TODO: helper function for time string with given timezone
    # TODO: in client in config add logs that are not interesting for parsing like mixin ...
    def start(self):
        weather_db = WeatherDatabase(db_file=self.config.get_db_file())
        weather_db.update_devices(self.config.get_clients())

        def handle_signal(signum, frame):
            # Clean up the socket and exit
            wrapped_socket.close()
            print("Server stopped")
            sys.exit(0)

        # Create a socket and listen for connections
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.config.get_port()
        host = self.config.get_host()
        sock.bind((host, port))
        sock.listen()

        # Wrap the socket with SSL
        wrapped_socket = ssl.wrap_socket(
            sock,
            keyfile=self.config.get_certificate_key(),
            certfile=self.config.get_certificate(),
            server_side=True
        )

        # Print the status of the socket
        now_utc = datetime.datetime.utcnow()
        utc_str = now_utc.strftime('%Y-%m-%d %H:%M:%S.%f UTC')[:-3] + "UTC: "
        print(f"{utc_str}Server is listening on {host}:{port}")
        print()
        # Register the signal handler function
        signal.signal(signal.SIGINT, handle_signal)

        while True:
            conn, addr = wrapped_socket.accept()
            with conn:
                # Receive the data from the device
                data = b""
                length = 1024
                index_len_end = 0
                try:
                    now_utc = datetime.datetime.utcnow()
                    utc_str = now_utc.strftime('%Y-%m-%d %H:%M:%S.%f UTC')[:-3] + "UTC: "
                    print(f"{utc_str} someone is knocking")
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
                        now_utc = datetime.datetime.utcnow()
                        utc_str = now_utc.strftime('%Y-%m-%d %H:%M:%S.%f UTC')[:-3] + "UTC: "
                        print(f"{utc_str} {device} is connected")
                        clients = self.config.get_clients()
                        if not clients[device]:
                            conn.sendall(b'Invalid device')
                        else:
                            # print(payload['data'])
                            json_str_pretty = json.dumps(payload['data'], indent=4)
                            # print(json_str_pretty)
                            status = weather_db.add_data(device, payload['data'])
                            if status['status']:
                                conn.sendall(b'OK')
                            else:
                                conn.sendall(bytes(status['message'], 'utf-8'))

                            now_utc = datetime.datetime.utcnow()
                            utc_str = now_utc.strftime('%Y-%m-%d %H:%M:%S.%f UTC')[:-3] + "UTC: "
                            print(f"{utc_str} {device} is disconnected")
                            print()
                    except jwt.exceptions.InvalidTokenError:
                        # The token is invalid, send an error response to the device
                        conn.sendall(b'Invalid token')

                except KeyboardInterrupt:
                    # Clean up the socket and exit
                    wrapped_socket.close()
                    print("Server stopped")
