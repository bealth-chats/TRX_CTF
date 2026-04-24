import numpy as np

with open("flag_ct.txt", "rb") as f:
    data = f.read()

start = data.find(b'[')
end = data.rfind(b']') + 1
list_str = data[start:end].replace(b'np.complex128', b'complex')
ct = eval(list_str.decode('utf-8', errors='ignore'))

blocks = []
for i in range(len(ct) // 256):
    blocks.append(ct[i*256 : (i+1)*256])

# Is it possible to reverse the process without the secret?
#
# Let's think about this. The state is initialized as:
# state_string = bin(pt)[2:].rjust(8, '0')[::-1] + bin(secret[0])[2:].rjust(8, '0')[::-1]
#
# Then for 12 rounds:
# 1. cry(np.pi/15, NQUBITS+KEY1_INDEX[i], i)
# 2. iswap(PERMUTATION[i], PERMUTATION[(i+1)%NQUBITS])
# 3. rzx(np.pi/np.e, RXZ_INTERACTION[i][0], RXZ_INTERACTION[i][1])
# 4. x(NQUBITS+i) if bit_prev != bit_new
#
# Finally, ct is the slice of 256 amplitudes determined by secret[-1].
#
# Notice that operations on the second register (the secret) are:
# - Initialization to secret[0]
# - cry uses second register as control!
# - rzx uses only first register? RXZ_INTERACTION = [(0, 3), (4, 5), (7, 2), (1, 6)]
#   Yes, these are all < NQUBITS (0 to 7)
# - x gates applied to second register to evolve it to secret[round+1]
#
# So the second register (qubits 8-15) is ALWAYS in a computational basis state!
# Because we only apply X gates to it, and use it as control for CRY gates.
# It is never in a superposition!

# Yes! The control qubits (8-15) are always 0 or 1.
# This means the CRY gates are either applied or not applied!
# cry(theta, control, target) -> if control is 1, apply ry(theta) to target.
# And ry is just a rotation.
#
# But wait, there's NO superposition created in the second register!
# Wait!
# index_ct = secret[-1]*256
# ct_c = Statevector(qc).data
#
# Statevector has 2^16 = 65536 amplitudes.
# They are ordered as amplitude for |q_15 ... q_0>
# Since the second register (q_15 ... q_8) is always in a computational basis state,
# ONLY ONE block of 256 amplitudes will be non-zero!
# And this block corresponds exactly to the state of the second register at the end of the circuit!
# At the end of the circuit, the second register is in state secret[-1] !
# So the non-zero amplitudes are exactly at `secret[-1] * 256` !
# And those are exactly the 256 amplitudes returned!
# All other amplitudes in the full Statevector are zero!

# And since the second register is just classical bits (0 or 1),
# the whole quantum circuit is equivalent to a sequence of operations on an 8-qubit system!
# The operations on the 8-qubit system depend on the second register (the secret).
# But wait, the secret is FIXED!
# So for a given connection, the quantum circuit is just a FIXED unitary matrix U acting on the initial state!
# The initial state is just the computational basis state |pt>.
# So ct = U |pt>.
# U is a 256x256 unitary matrix.
# |pt> is a computational basis state, which is a column vector with a 1 at index `pt` and 0 elsewhere.
# So U |pt> is exactly the `pt`-th column of U!
# This means ct is just the `pt`-th column of U!

# Wow!
# We can find `pt` by looking at the magnitude of the amplitudes?
# No, `ct` is exactly the `pt`-th column of U.
# Since U is unitary, its columns are orthonormal.
# And each different `pt` will give a different column of U.
# This is why the sorted magnitudes are different for different `pt`!
# BUT the sorted magnitudes are NOT independent of the secret!
# Because U depends on the secret.

# BUT we have a single set of 38 blocks encrypted with the SAME secret!
# And we know that `ct` for 'T' (block 0) has a certain sorted magnitude profile.
# Actually, we have the exact `ct` for 'T' under this secret!
# Can we compute U without knowing the secret? No.
# BUT can we brute force the secret?
# The secret is 13 bytes: secret[0] to secret[12]. Wait!
# 13 bytes is 104 bits. That's too large to brute force.

# Let's think again about the quantum circuit.
# Is it really just U |pt>?
# Let's check how pt is converted to state.
# state_string = bin(pt)[2:].rjust(8, '0')[::-1] + bin(secret[0])[2:].rjust(8, '0')[::-1]
# So q_0 to q_7 are set to `pt[::-1]`.
# Yes, the initial state of the first 8 qubits is exactly |pt[::-1]>.
# So ct is the `pt[::-1]`-th column of U!

# If we compute the norm of each block, it's 1.0.
# Is there some structure we can exploit?
# Let's see the operations on the 8 qubits:
# cry(pi/15, control, target) -> If control is 1, apply ry(pi/15) to target.
# iswap(..., ...) -> Swap and phase.
# rzx(pi/e, ..., ...) -> Rotation.

# Wait, `r` goes from 0 to ROUNDS-1 (12).
# What if we analyze the unitary?
# No, we only have the flag encrypted.
