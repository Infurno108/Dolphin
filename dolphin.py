import socket
import threading
import rsa

# key production
public_key, private_key = rsa.newkeys(1024)
public_partner = None

choice = input("Enter 1 for server and 2 for client: ")

if choice == '1':
    ip = input("Please enter your ip address: ")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # tcp
    # Currently rigidly my internal ipv4, the actual app will just use the cloud box as the listener
    server.bind((ip, 9999))
    server.listen()

    client, _ = server.accept()  # accepted client
    client.send(public_key.save_pkcs1("PEM"))  # sending public key to client
    public_partner = rsa.PublicKey.load_pkcs1(
        client.recv(1024))  # recieving public key from client

elif choice == '2':
    ip = input("Please enter the server's ip address: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # currently just looping internally on my own machine for testing, this will need to be changed
    client.connect(("192.168.1.69", 9999))
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
