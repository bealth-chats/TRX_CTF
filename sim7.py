import socket

s = socket.socket()
s.settimeout(10)
s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
print("Connected")
s.send(b"1\n54\n2\n") # Send 1, then 'T' (0x54), then 2
print("Sent payloads")

res = b""
while True:
    chunk = s.recv(4096)
    if not chunk: break
    res += chunk
    print(f"Received {len(res)} bytes")
    if res.count(b']') >= 2:
        break
print("Done")
