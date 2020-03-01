import socket

confirmation = '12037'
public_key = +1
private_key = -1

def validate_server(server_name):
    CA_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CA_connection.connect((socket.gethostname(), 9501))

    CA_certs = "Validate," + server_name + "," + "1"
    CA_connection.send( CA_certs.encode())
    CA_response = CA_connection.recv(1024).decode()
    print("Certificate Authority: " + CA_response)
    CA_connection.close( )
    if CA_response== None:
        return 0
    else:
        return int( CA_response)

def encrypt(text, publickey):
    encryptedText = ''
    for char in text:
        encryptedText += chr(ord(char) + publickey)
    return encryptedText

def decrypt(text):
    decrypted_copy = ''
    for char in text:
        decrypted_copy += chr(ord(char) + private_key)
    return decrypted_copy

def main():
    server_publickey = 0
    server_valiated = False

    server_connection = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    server_connection.connect((socket.gethostname(), 9500))
    print("Connecting . . .")
    server_connection.send('Hi'.encode())
    server_response = server_connection.recv(1024).decode()
    print(decrypt(server_response))
    server_publickey = validate_server(server_response)
    print("Server is validated.")

    
    print("Response: " + decrypt(server_response))

    if (server_publickey == None):
        server_connection.send('Closing'.encode())
        server_response = server_connection.recv(1024).decode()
    else:
        print("Connection is active")
        server_connection.send(encrypt(confirmation, server_publickey).encode())

        server_response = server_connection.recv(1024).decode()
        
        print("Server response: " + decrypt(server_response))
        if (server_response == encrypt(confirmation + 'validation', server_publickey)):
            server_valiated = True

    while server_valiated:
        user_input = input("(E)xit or (Hi) ")
       
        if user_input == "E":
            server_valiated = False
            server_connection.send('Bye'.encode())
        elif user_input == "Hi":
            server_connection.send( encrypt(user_input, server_publickey).encode())
            server_response = server_connection.recv(1024).decode()
            if server_response == encrypt('Okay', server_publickey):
                print('Response recieved ' + user_input)
            else:
                print("Encrypted response from the server: " + decrypt(server_response))
        else:
            pass
main()
