# import sys
import socket
import ssl
import jwt


class ServerConnect:

    def __init__(
            self,
            config
    ):
        self.config = config
        self.host = config.get_host()
        self.port = config.get_port()
        self.device = config.get_device()
        self.jwt_secret = config.get_jwt_secret()

    def send_data_to_server(self, data: dict) -> str:
        # Create the JWT payload
        payload = {
            'device': self.device,
            'data': data
        }
        # Sign the JWT
        encoded_jwt = jwt.encode(payload, self.jwt_secret, algorithm='HS256').encode()
        jwt_len = len(encoded_jwt)

        # probable workaround for server. Adding length in front of the message, ofcourse that length is recalculated
        # because of the new string in front
        encoded_jwt = f"[{jwt_len}]".encode() + encoded_jwt

        # Create a socket and connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        wrapped_socket = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE, ca_certs=None)

        wrapped_socket.connect((self.host, self.port))

        # Send the data to the server
        wrapped_socket.sendall(encoded_jwt)
        # wrapped_socket.shutdown(socket.SHUT_RDWR)

        # Receive the response from the server
        response = wrapped_socket.recv()

        # Close the socket
        wrapped_socket.close()

        return response.decode('utf-8')
