import socket
import string
import numpy as np
import time

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

def encrypt_char(char):
    s = connect()
    while b'>' not in s.recv(4096):
        pass

    s.send(b'1\n')
    s.send(f"{ord(char):02x}\n".encode())

    res = b""
    while b']' not in res:
        chunk = s.recv(4096)
        if not chunk:
            break
        res += chunk

    s.close()

    try:
        start = res.find(b'[')
        end = res.find(b']') + 1
        list_str = res[start:end].replace(b'np.complex128', b'complex')
        ct_char = eval(list_str.decode('utf-8', errors='ignore'))
        return ct_char
    except Exception as e:
        print(f"Error for {char}: {e}")
        return None

# Load flag
with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')
ct_flag = eval(list_str.decode('utf-8', errors='ignore'))
blocks = [ct_flag[i*256 : (i+1)*256] for i in range(len(ct_flag)//256)]

charset = string.ascii_letters + string.digits + "{}_-!@#$%^&*"
found = {}

for char in charset:
    print(f"Encrypting {char}...")
    ct_c = encrypt_char(char)
    if ct_c is None:
        continue

    # Since we found the secret varies per connection! Wait!
    # "secret1 = os.urandom(ROUNDS+1)"
    # Ah! The secret is randomly generated PER connection!
    # Wait, in main():
    # qcipher = QCipher(NQUBITS, ROUNDS)
    # The qcipher object is created once, outside the while loop!
    # So the secret is the same for the whole connection!
    pass
