import numpy as np

# Let's think about the structure of the quantum circuit.
# The qubits are 0 to 7 (plaintext) and 8 to 15 (secret).
# Only cry(pi/15, NQUBITS+KEY1_INDEX[i], i) couples the secret to the plaintext!
# Wait, and then:
# iswap(PERMUTATION[i], PERMUTATION[(i+1)%NQUBITS]) -> only acts on plaintext qubits 0 to 7!
# rzx(pi/e, RXZ_INTERACTION[i][0], RXZ_INTERACTION[i][1]) -> only acts on plaintext qubits 0 to 7!
#
# The secret qubits are JUST controls for the cry gates.
# Since the secret qubits NEVER change their basis (they just flip between 0 and 1 via X gates),
# for the plaintext qubits, the circuit is just a sequence of:
# ry(pi/15) applied to qubit i IF secret bit is 1
# iswap ...
# rzx ...
#
# This means the unitary U on the 8 plaintext qubits is completely determined by the sequence of secret bits!
# Wait! How many secret bits are there?
# At each round, the secret bits determine which ry gates are applied.
# The secret bits for round `r` are EXACTLY the bits of `secret[r]`!
# Wait, let's look at the code:
# "state_string = state[::-1] + bin(self.secret[0])[2:].rjust(8, '0')[::-1]"
# So initially, the second register is `secret[0]`.
# Then in round `r`, we add_key: cry(pi/15, 8+KEY1_INDEX[i], i)
# Then apply_permutation, apply_rxz.
# Then evolve_key: x(8+i) if bit_prev != bit_new.
# So in round `r`, the control bits are EXACTLY the bits of `secret[r]`!

# Wow!
# The entire unitary U applied to the 8 plaintext qubits is completely determined by `secret[0:12]`.
# `secret` is 13 bytes.
# Wait, `secret[12]` is used for the last round (round 11 uses secret[11], then evolves to secret[12]).
# Does the last round apply `add_key` with `secret[12]`? No, because the loop is `for round in range(ROUNDS)` (0 to 11).
# So in round 11, it uses `secret[11]` as control, then evolves to `secret[12]`.
# Then `secret[12]` is used as `index_ct`!
# "self.index_ct = self.secret[-1]*2**self.nqubits"
# Since `secret[-1]` is `secret[12]`, it exactly points to the block of 256 amplitudes corresponding to the final state of the second register being `secret[12]`.
# Which is guaranteed to be true, because we evolved it to `secret[12]`!
# So `ct` is EXACTLY the Statevector of the 8 plaintext qubits after applying the sequence of unitaries parameterized by `secret[0:12]`!

# Is there any other connection?
# The sequence of unitaries is:
# U = prod_{r=0}^{11} ( RXZ * ISWAP * RY_layer(secret[r]) )
#
# Wait, this means `ct` is just U |pt>.
# Can we compute U? We don't know `secret[0:12]`.
# `secret[0:12]` is 12 bytes. That's 96 bits. Still too large to brute force.
# But wait... we don't need to brute force it!
# The server allows us to encrypt ONE byte per connection!
# But wait, the timeout brute forcer is working!
