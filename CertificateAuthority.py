import socket

CA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

CA.bind((socket.gethostname(), 9501))
CA.listen(5)

