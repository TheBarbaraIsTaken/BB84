import random

def random_bits(length):
    """Create a random bit string of the given length."""
    return [random.randint(0, 1) for _ in range(length)]

def encode_qubits(bits, bases):
    """Encode bits into qubits based on the chosen bases."""
    qubits = []
    for bit, base in zip(bits, bases):
        if base == 0:  # Standard basis
            qubits.append(bit)
        else:  # Hadamard basis
            if bit == 0:
                qubits.append('+')  # |+⟩ state
            else:
                qubits.append('-')  # |-⟩ state
    return qubits

def measure_qubits(qubits, measurement_bases):
    measured_bits = []
    for qubit, base in zip(qubits, measurement_bases):
        if base == 0:  # Measuring in standard basis
            if qubit in ['+', '-']:
                measured_bits.append(random.randint(0, 1))  
            else:
                measured_bits.append(qubit) 
        else:  # Measuring in Hadamard basis
            if qubit in ['+', '-']:
                measured_bits.append(0 if qubit == '+' else 1)
            else:
                measured_bits.append(random.randint(0, 1))  
    return measured_bits

def sift_keys(alice_bases, bob_bases, bob_bits):
    sifted_key = []
    for a_base, b_base, bit in zip(alice_bases, bob_bases, bob_bits):
        if a_base == b_base:
            sifted_key.append(bit)
    return sifted_key

def bb84_protocol(n, delta):
    # Step 1: Alice generates random bits and encodes them into qubits
    length = int((4 + delta) * n)
    alice_bits = random_bits(length) # Alice's random bits
    alice_bases = random_bits(length) # Choose random bases for qubit encoding
    # Step 2: For Alice chosen string b, she creates the state
    qubits = encode_qubits(alice_bits, alice_bases)
    # Step 3: Alice sends the result qubits to Bob
    ## Public channel
    alice_announced_bases = alice_bases # Alice announces her bases
    ## Public channel
    # Bob's random measurement bases
    bob_bases = random_bits(length)
    bob_measured_bits = measure_qubits(qubits, bob_bases)
    # Bob discards bits where the bases don't match
    bob_sifted_key = sift_keys(alice_announced_bases, bob_bases, bob_measured_bits)   
    return bob_sifted_key

n = 10  # Number of bits in the final key
delta = 0.2  # Delta value (From the paper, I guess it is the additional bits)
sifted_key = bb84_protocol(n, delta)
length = int((4 + delta) * n)
# Test 1: The sifted key should not be longer than the number of qubits sent
assert len(sifted_key) <= length, "Sifted key is longer than the number of qubits sent."   
# Test 2: The sifted key should only contain bits (0s and 1s)
assert all(bit in [0, 1] for bit in sifted_key), "Sifted key contains invalid values."
print("Key length:", len(sifted_key))
print("Sifted key:", sifted_key)