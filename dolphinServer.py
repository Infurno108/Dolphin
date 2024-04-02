import socket
import threading
import rsa

# below produces new keys, and writes them unencrypted to bin
# public_key, private_key = rsa.newkeys(1024)
# public_partner = None
# with open('public.bin', 'wb') as f:
#    f.write(public_key.save_pkcs1("PEM"))
# with open('private.bin', 'wb') as f:
#    f.write(private_key.save_pkcs1("PEM"))
public_partner = None

# Below pulls the keys out of the bins
with open('public.bin', 'rb') as f:
    public_key = rsa.PublicKey.load_pkcs1(f.read(1024))
with open('private.bin', 'rb') as f:
    private_key = rsa.PrivateKey.load_pkcs1(f.read(1024))

ip = input("Please enter your ip address: ")
# Socket() -> creates a new socket, AF_INET saying ipv4, and sock_stream saying tcp
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind() -> binds the socket to adress and port number
server.bind((ip, 9999))
server.listen()  # Listen() -> listens for incoming connections

# accpet() recieves connections, and returns touple: (socket, address of new connection)
client, _ = server.accept()
#print(_[0])
# sending public key to client first
client.send(public_key.save_pkcs1("PEM"))

public_partner = rsa.PublicKey.load_pkcs1(
    client.recv(1024))  # recieving public key from client



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
