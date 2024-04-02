from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
# I have no real clue what is going on exactly here, I am just be lining through a youtube tutorial real quick
#9:44 Flint here, I now understand what is going on and am going to go back w/comments.


#salt generation, 32 bytes of completely random data. I already ran it and copied it into a static string below, we could use fresh salt per message, or per session for more security. But it would also increase the amount of data needed to be shared.
#salt = get_random_bytes(32)

salt = b'\x8co)x\x0b/\x17\x9e/\xcbV\xb9\xb8\xc1h\xc4\xcbQ\xaa\r\xa4m\xe8v=v\xb7L\xad\x08\xe8o'

password = "rockyou"
#With the salt, and the password a key for encryption can be derived. This is symmetrical encryption, which we might not want to use, but this is just to get moving. 

#going to go eat tacos and come back for more comments.
test_key = PBKDF2(password, salt, dkLen=32)
print(test_key)

message = b"I want to kill the pope"

cipher = AES.new(test_key, AES.MODE_CBC)
ciphertext = cipher.encrypt(pad(message, AES.block_size))

print("#"*50)
print(ciphertext)

with open('encrypted.bin', 'wb') as f:
    f.write(cipher.iv)
    f.write(ciphertext)

with open('encrypted.bin', 'rb') as f:
    writtenIv = f.read(16)
    writtenText = f.read()

cipher = AES.new(test_key, AES.MODE_CBC, iv=writtenIv)
originlMessage = unpad(cipher.decrypt(writtenText), AES.block_size)
print(originlMessage)

# new_salt = get_random_bytes(32)
# print(new_salt)
