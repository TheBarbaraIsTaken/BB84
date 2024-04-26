import random
import matplotlib.pyplot as plt
from math import ceil
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

def bb84_protocol(length, middle_man_eve = False):
    # Step 1: Alice generates random bits and encodes them into qubits
    #length = int((4 + delta) * n)
    alice_bits = random_bits(length) # Alice's random bits
    alice_bases = random_bits(length) # Choose random bases for qubit encoding
    # Step 2: For Alice chosen string b, she creates the state
    qubits = encode_qubits(alice_bits, alice_bases)
    # Step 3: Alice sends the result qubits to Bob
    ## Public channel
    alice_announced_bases = alice_bases # Alice announces her bases
    ## Public channel
    #eve = random.randint(0, 1)  # Eve's presence (0: absent, 1: present)
    middle_man = False
    if middle_man_eve == 1:
        ## Eve measures the qubits
        eve_measured_bits = measure_qubits(qubits, [0]*length)
        ## Eve re-encodes the qubits
        eve_bases = random_bits(length)
        ## Eve sends the result qubits to Bob
        qubits = encode_qubits(eve_measured_bits, eve_bases)
    # Bob's random measurement bases
    bob_bases = random_bits(length)
    bob_measured_bits = measure_qubits(qubits, bob_bases)
    # Bob discards bits where the bases don't match
    bob_sifted_key = sift_keys(alice_announced_bases, bob_bases, bob_measured_bits)  
    # Check bit is the first half of the sifted key
    check_bit = bob_sifted_key[:ceil(len(bob_sifted_key)/2)]
    check_bit_mma= sift_keys(alice_bases, bob_bases, alice_bits)
    # Compare it with the alice_bits
    if check_bit != check_bit_mma[:ceil(len(check_bit_mma)/2)]:
        middle_man = True
    return bob_sifted_key, middle_man

fail_no_attack = 0
fail_attack = 0
fail_count_attack = {}
fail_count_no_attack = {}
N = 10000
for length in range(1, 16, 1):
    for index in range(N):
        sifted_key, middle_man_attack = bb84_protocol(length, True)
        if ((len(sifted_key) == 0 or len(sifted_key) == 1)) or not middle_man_attack:
            fail_attack += 1
            if length in fail_count_attack:
                fail_count_attack[length] += 1/N
            else:
                fail_count_attack[length] = 1/N
        sifted_key_no_attack = bb84_protocol(length)[0]
        if ((len(sifted_key_no_attack) == 0 or len(sifted_key_no_attack) == 1)):
            fail_no_attack += 1
            if length in fail_count_no_attack:
                fail_count_no_attack[length] += 1/N
            else:
                fail_count_no_attack[length] = 1/N
        

plt.scatter(fail_count_attack.keys(), fail_count_attack.values(), zorder=2)
plt.grid(zorder=1)
plt.xlabel('Length')
plt.ylabel('Probability of failure')
plt.show()
plt.scatter(fail_count_no_attack.keys(), fail_count_no_attack.values(), zorder=2)
plt.grid(zorder=1)
plt.xlabel('Length')
plt.ylabel('Probability of failure')
plt.show()