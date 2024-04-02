import socket
import threading
import rsa

# key production
public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Enter 1 for server and 2 for client: ")

if choice == '1':
    ip = input("Please enter your ip address: ")
    # Socket() -> creates a new socket, AF_INET saying ipv4, and sock_stream saying tcp
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind() -> binds the socket to adress and port number
    server.bind((ip, 9999))

    server.listen()  # Listen() -> listens for incoming connections

    # accpet() recieves connections, and returns touple: (socket, address of new connection)
    client, _ = server.accept()
    print(_)

    # sending public key to client first
    client.send(public_key.save_pkcs1("PEM"))
    public_partner = rsa.PublicKey.load_pkcs1(
        client.recv(1024))  # recieving public key from client

elif choice == '2':
    ip = input("Please enter the server's ip address: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # currently just looping internally on my own machine for testing, this will need to be changed
    client.connect((ip, 9999))
    public_partner = rsa.PublicKey.load_pkcs1(
        client.recv(1024))  # receive first, send second
    client.send(public_key.save_pkcs1("PEM"))
else:
    exit()


def send(c):
    while True:
        message = input("Enter message: ")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("Message sent")


def receive(c):
    while True:
        message = rsa.decrypt(c.recv(1024), private_key).decode()
        print("Received: ", message)


threading.Thread(target=send, args=(client,)).start()
threading.Thread(target=receive, args=(client,)).start()
