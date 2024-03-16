import socket

HOST = '10.10.0.197'
PORT = 10524

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello from the client!')
    data = s.recv(1024)
    print(f'Received from server: {data.decode()}')
