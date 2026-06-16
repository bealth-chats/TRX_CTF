import socket
import numpy as np

# Let's test the timeout again, maybe we can just reconnect faster.
def test_char(char):
    s = socket.socket()
    s.settimeout(5)
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))

    # Send both requests at once!
    # Wait, the server needs to receive "1\n" and then prompt for "What do you wanna encrypt?".
    # If we send "1\n54\n2\n" it might buffer it correctly.
    # Let's try!
    s.send(f"1\n{ord(char):02x}\n2\n".encode())

    res = b""
    while b']' not in res:
        chunk = s.recv(8192)
        if not chunk: break
        res += chunk

    start1 = res.find(b'[')
    end1 = res.find(b']') + 1
    list_str1 = res[start1:end1].replace(b'np.complex128', b'complex')
    ct_char = eval(list_str1.decode('utf-8', errors='ignore'))

    res = res[end1:]
    while b']' not in res:
        chunk = s.recv(8192)
        if not chunk: break
        res += chunk

    start2 = res.find(b'[')
    end2 = res.find(b']') + 1
    list_str2 = res[start2:end2].replace(b'np.complex128', b'complex')
    ct_flag = eval(list_str2.decode('utf-8', errors='ignore'))
    s.close()

    blocks = [ct_flag[i*256 : (i+1)*256] for i in range(len(ct_flag)//256)]
    matches = []
    for i, b in enumerate(blocks):
        if np.allclose(ct_char, b):
            matches.append(i)
    return matches

print("Testing T...")
print(test_char('T'))
