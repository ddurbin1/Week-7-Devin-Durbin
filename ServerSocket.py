import socket

port = 9500
servername = "Server 1"
public_key = +1
private_key = -1
confirmation = '12037'

def server():
    cert_auth_connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
    cert_auth_connection.connect((socket.gethostname(), 9501))
    cert_auth_certificate = "Register" + "," + servername + "," + str(public_key)
    cert_auth_connection.send(cert_auth_certificate.encode())
    cert_auth_respond = cert_auth_connection.recv(1024).decode()
    cert_auth_connection.close()
    return (cert_auth_respond == "200")

def decrypt(text):
    decrypted_copy = ''
    for char in text:
        decrypted_copy += chr(ord(char) + private_key)
    return decrypted_copy

def encrypt(text):
    encrypted_copy = ''
    for char in text:
        encrypted_copy += chr(ord(char) + public_key)
    return encrypted_copy

def main():
    if server():
        print("Register Successful")

        while True:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.bind((socket.gethostname(), port))
            connection.listen()
            
            print(socket.gethostname() + ": port " + str(port) + " active")

            session, addr = connection.accept()

            run_server = True
            while run_server:
                    receive_data = session.recv(1024).decode()
                    decrypted_copy = decrypt(receive_data)
                    print(decrypted_copy)
                    
                    if decrypted_copy == 'Hi':
                        output_data = "Hello"
                        print("Response: \'" + output_data +"\'")
                        session.send(output_data.encode())
                        
                    elif decrypted_copy == "Bye":
                        output_data = "Good Bye"
                        session.send(output_data.encode())
                        break
                    
                    else:
                        print("Text received: '" + receive_data + "'")
                        print("Client request: '" + decrypted_copy + "'")
                        if decrypted_copy == confirmation:
                            output_data = encrypt(confirmation + 'validation')
                        else:
                            print("Message handled")
                            output_data = encrypt("Confirmed – Message handled")

                        print("Sending response: \'" + output_data +"\'")
                        session.send(output_data.encode())
    else:
        print("Connection requirements not met.")
        exit
main()