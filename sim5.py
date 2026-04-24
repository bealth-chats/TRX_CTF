import numpy as np

with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')
ct = eval(list_str.decode('utf-8', errors='ignore'))
blocks = [ct[i*256 : (i+1)*256] for i in range(len(ct)//256)]

same_blocks = {}
for i in range(len(blocks)):
    for j in range(i+1, len(blocks)):
        if np.allclose(blocks[i], blocks[j]):
            if i not in same_blocks:
                same_blocks[i] = []
            same_blocks[i].append(j)

# Wait... the server gives us `MAX_QUERIES = 1`.
# So we can encrypt ONE byte per connection.
# But wait, does it close the connection?
# "if option == '1': ... queries_left -= 1"
# "if option == '2': ct = qcipher.encrypt(FLAG); print(ct)"
# No, it doesn't close the connection! It loops!
# "while True: ... if option == '1': ... if queries_left < 1: exit()"
# Wait, if we use option 1 when queries_left = 1, it executes and then decrements queries_left.
# Next time we loop, we CAN use option 2 multiple times!
# But we can only use option 1 ONE time per connection!
# Wait! Can we open 256 connections?
# Yes, but each connection will have a DIFFERENT secret, so U will be different!

# What if we can find the secret?

# To recover the plaintext, we have a unitary matrix U.
# We are given 38 columns of U.
# And we know that these 38 columns correspond to the flag bytes.
# Can we determine which columns they are?
# The initial state is just |pt>.
# The columns are exactly the output vectors.
# Wait. For a fixed circuit structure, does U preserve some inner product or something?
# No, U is unitary, so <U|x>, U|y> = <x|y> = 0 if x != y.
# So the inner product of two different blocks is 0!
for i in range(4):
    for j in range(i+1, 4):
        print(f"Inner product {i} and {j}:", np.abs(np.vdot(blocks[i], blocks[j])))
