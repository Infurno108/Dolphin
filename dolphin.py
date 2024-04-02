import socket
import threading
import rsa

# key production
# public_key, private_key = rsa.newkeys(1024)
public_partner = None

with open('public.bin', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read(1024))
with open('private.bin', 'rb') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read(1024))

# destination = input("Who would you like to talk to?: ")
# user = input("What is your name?: ")
ip = input("TEMPORARY: Please enter the servers ip address: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, 9999))
# print("Connected to server")
public_partner = rsa.PublicKey.load_pkcs1(
    client.recv(1024))  # Apon connecting the server will try and send over public key
# print("revieced key from server")
# The server wants a response with the public key
client.send(public_key.save_pkcs1("PEM"))
# print("sent key to server")


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
