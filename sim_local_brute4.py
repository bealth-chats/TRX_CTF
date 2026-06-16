import socket

# Is there any issue with the server right now?
s = socket.socket()
s.settimeout(10)
s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
print("Connected")
print("Banner:", s.recv(1024).decode())
s.send(b"1\n")
print("Prompt 1:", s.recv(1024).decode())
s.send(b"54\n")
res = b""
while True:
    chunk = s.recv(8192)
    if not chunk: break
    res += chunk
    print("Received chunk of size", len(chunk))
    if b']' in res: break
print("Got char ct")

# Now request flag
s.send(b"2\n")
res2 = b""
while True:
    chunk = s.recv(8192)
    if not chunk: break
    res2 += chunk
    print("Received flag chunk of size", len(chunk))
    if b']' in res2: break
print("Got flag ct")
s.close()
