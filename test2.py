import numpy as np

with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')

ct = eval(list_str.decode('utf-8', errors='ignore'))
print(f"Parsed {len(ct)} complex numbers.")

blocks = []
for i in range(len(ct) // 256):
    blocks.append(ct[i*256 : (i+1)*256])

# Notice we have 'T' at 0, 'R' at 1, 'X' at 2, '{' at 3. Let's see if we can find magnitudes for different blocks.
for i in range(4):
    magnitudes = np.abs(blocks[i])
    print(f"Block {i}: Max mag {np.max(magnitudes)}, Sum mag^2 {np.sum(magnitudes**2)}")

# Let's compare magnitudes of T blocks.
T_mag = np.abs(blocks[0])
T_mag_sorted = np.sort(T_mag)[::-1]
print("T top 10 mags:", T_mag_sorted[:10])

# Let's compare magnitudes of another block.
block4_mag = np.abs(blocks[4])
block4_mag_sorted = np.sort(block4_mag)[::-1]
print("Block4 top 10 mags:", block4_mag_sorted[:10])

# Are the sorted magnitudes the same?
print("Are sorted magnitudes same for T and Block4?", np.allclose(T_mag_sorted, block4_mag_sorted))

# Let's see if the sorted magnitudes are unique per byte!
for i in range(4):
    print(f"Block {i} sorted sum:", np.sum(np.sort(np.abs(blocks[i]))))
