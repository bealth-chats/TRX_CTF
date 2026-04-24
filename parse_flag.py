import ast

with open("flag_ct.txt", "rb") as f:
    data = f.read()

# Try to extract the first occurrence of a list
start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end]
list_str = list_str.replace(b'np.complex128', b'complex')

try:
    ct = eval(list_str.decode('utf-8', errors='ignore'))
    print(f"Parsed {len(ct)} complex numbers.")
except Exception as e:
    print(e)
