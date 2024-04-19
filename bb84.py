import numpy as np
from copy import deepcopy
from qubit import Qubit


class BB84:
    def __init__(self, length=5, alice_message=None, alice_base=None, bob_base=None):
        '''
        alice_message:  list[int], list of 0's and 1's
        alice_base:     list[int], list of 0's and 1's. 1 means appling the Hadamard gate
        bob_base:       list[int], list of 0's and 1's. 1 means appling the Hadamard gate
        '''
        if length <= 0:
            raise Exception("The length of the bits must be greater then 0!")
        
        self.length = length
        self.alice_message = alice_message
        self.alice_base = alice_base
        self.bob_recieved = None
        self.bob_base = bob_base

    def generate_bitstring(self):
        return np.random.randint(low=0, high=2, size=self.length)
    
    def shift_base(self, message, base):
        shifted_message = deepcopy(message)

        for i in range(self.length):
            if base[i] == 1:
                shifted_message[i].hadamard()

        return shifted_message
    
    def clear(self):
        self.bob_recieved = None
        self.alice_message = None
        self.alice_base = None
        self.bob_base = None
    
    def change_message(self, is_attack=False):
        if self.alice_message is None:
            self.alice_message = self.generate_bitstring()

        self.alice_qmessage = Qubit.bit_to_qubit(self.alice_message)

        if self.alice_base is None:
            self.alice_base = self.generate_bitstring()

        self.alice_shifted_message = self.shift_base(self.alice_qmessage, self.alice_base)

        # Alice sends the qubits to Bob
        if is_attack:
            # TODO: add attack
            self.eve_measurements = Qubit.measure_qubits(self.alice_shifted_message)
            self.eve_qmeasurements = Qubit.bit_to_qubit(self.eve_measurements)
            self.eve_base = self.generate_bitstring()
            self.eve_sends = self.shift_base(self.eve_qmeasurements, self.eve_base)

            self.bob_recieved = deepcopy(self.eve_sends)
        else:
            self.bob_recieved = deepcopy(self.alice_shifted_message)

        if self.bob_base is None:
            self.bob_base = self.generate_bitstring()

        self.bob_shifted_message = self.shift_base(self.bob_recieved, self.bob_base)

        self.bob_measurements = Qubit.measure_qubits(self.bob_shifted_message)


        # print(self.alice_message)
        # print(self.alice_base)
        # print(self.alice_qmessage)
        # print(self.alice_shifted_message)
        # print(self.bob_recieved)
        # print(self.bob_base)
        # print(self.bob_shifted_message)
        # print(self.bob_measurements)

    def check(self):
        is_attacked = False
        self.key_alice = None
        self.key_bob = None

        self.same_base = self.alice_base == self.bob_base
        
        n = sum(self.same_base)

        self.alice_check = (self.alice_message[self.same_base])[:n//2]
        self.bob_check = (self.bob_measurements[self.same_base])[:n//2]

        if (self.alice_check == self.bob_check).all():
            self.key_alice = deepcopy((self.alice_message[self.same_base])[n//2:])
            self.key_bob = deepcopy((self.bob_measurements[self.same_base])[n//2:])
        else:
            is_attacked = True

        # print(self.alice_base)
        # print(self.bob_base)
        # print(self.same_base)
        # print()
        # print(self.alice_check)
        # print(self.bob_check)

        return is_attacked
    
    def is_failed(self, is_attack):
        return self.is_attacked != is_attack


    def run(self, is_attack=False):
        self.change_message(is_attack)
        self.is_attacked = self.check()

        # print(self.key_alice)
        # print(self.key_bob)

        return self.is_failed(is_attack)
