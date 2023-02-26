import sys
import os
import socket
import ssl
import json
import jwt

def send_data_to_server(
        host,
        port,
        device_id,
        jwt_secret,
        data,
        CERTIFICATE_FILE=None
):
    # Create the JWT payload
    payload = {
        'device_id': device_id,
        'data': data
    }
    # Sign the JWT
    encoded_jwt = jwt.encode(payload, jwt_secret, algorithm='HS256').encode()
    jwt_len = len(encoded_jwt)

    # probable workaround for server. Adding "." for end of message
    encoded_jwt = f"[{jwt_len}]".encode() + encoded_jwt

    # Create a socket and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if CERTIFICATE_FILE:
        wrapped_socket = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_REQUIRED, ca_certs=CERTIFICATE_FILE)
    else:
        wrapped_socket = ssl.wrap_socket(sock, cert_reqs=ssl.CERT_NONE, ca_certs=None)

    wrapped_socket.connect((host, port))

    # Send the data to the server
    wrapped_socket.sendall(encoded_jwt)
    # wrapped_socket.shutdown(socket.SHUT_RDWR)

    # Receive the response from the server
    response = wrapped_socket.recv()

    # Close the socket
    wrapped_socket.close()

    return response.decode('utf-8')
