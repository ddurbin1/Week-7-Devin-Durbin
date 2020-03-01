import socket
from datetime import datetime

port = 9501

def main():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.bind((socket.gethostname(), port))

    connection.listen()
    certificates = {}

    run_server = True
    while run_server:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        response = ""
        session, addr = connection.accept()
        received_data = session.recv(1024).decode().split(',')
        action = received_data[0]
        host = received_data[1]
        public_key = received_data[2]
        print("Validation date:", current_time)
        print(action + "," + socket.gethostname() + "," + public_key)

        if action == 'Register':
            certificates[socket.gethostname()] = public_key
            response = "200"

        elif action == 'Validate':
            if socket.gethostname() in certificates:
                response = certificates[socket.gethostname()]
            else:
                response = None

        else:
            response = ""

        if response != "":
            session.send(response.encode())

        session.close()
main()