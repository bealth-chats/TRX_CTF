import socket
import string
import numpy as np
import time

def connect():
    s = socket.socket()
    s.connect(('nc.quantumcipher.ctf.theromanxpl0.it', 9099))
    return s

def brute_force():
    s = connect()
    while b'>' not in s.recv(4096):
        pass

    # The server has queries_left = MAX_QUERIES, which is 1.
    # We can only encrypt 1 byte per connection. But we need both the encrypted byte and the flag to compare them if they share the same secret.
    # Ah! The flag is Option 2, it doesn't decrement queries_left!
    # "if option == '2': ct = qcipher.encrypt(FLAG); print(ct)"
    pass
