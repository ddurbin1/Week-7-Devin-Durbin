import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 9500))

client.send(bytes("Hello", "utf-8"))
msg = client.recv(1024)
print(msg.decode("utf-8"))
