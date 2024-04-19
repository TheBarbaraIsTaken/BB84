import numpy as np
from math import sqrt

class Qubit:
    def __init__(self, alpha, beta):
        '''
        alpha:  float, the amplitude corresponding to state |0⟩
        beta:   float, the amplitude corresponding to state |1⟩
        '''
        probabilities = (abs(alpha)**2, abs(beta)**2)

        eps = 10e-10
        if abs(sum(probabilities) - eps) > 1:
            raise Exception("Amplitudes are incorrect!\nThe square sum of the absolute values should be equal to 1!")

        self.alpha = alpha
        self.beta = beta

    @property
    def vec(self):
        '''The vector representation of the state'''
        return np.array([self.alpha, self.beta])
    
    @property
    def probabilities(self):
        return {0: abs(self.alpha)**2, 1: abs(self.beta)**2}
    
    def update_amplitude(self, new_alpha, new_beta):
        self.alpha = new_alpha
        self.beta = new_beta

    def measure(self):
        'One measurement of the state'
        return np.random.choice(list(self.probabilities.keys()), size=1, p=list(self.probabilities.values()))[0]
    
    def measure_n(self, n=10_000):
        'Measure n times the stored state'
        return np.random.choice(list(self.probabilities.keys()), size=n, p=list(self.probabilities.values()))

    def hadamard(self):
        '''
        Mapping: |0⟩ to |+⟩, |1⟩ to |-⟩
        '''
        # Definition of Hadamard gate
        H = 1/sqrt(2) * np.array([[1, 1], [1, -1]])

        # Apply Hadamard gate on the state
        new_amplitdes = (H @ self.vec)
        self.update_amplitude(*new_amplitdes)
    
    def __repr__(self):
        if round(self.beta, 2) == 0:
            return f"|0⟩"
        elif round(self.alpha, 2) == 0:
            return f"|1⟩"
        elif round(self.beta, 2) < 0:
            return f"{round(self.alpha, 2)}|0⟩ - {abs(round(self.beta, 2))}|1⟩"
        else:
            return f"{round(self.alpha, 2)}|0⟩ + {round(self.beta, 2)}|1⟩"

    @staticmethod
    def estimate_probs(q, n=10_000):
        measurement_sum = sum(q.measure_n(n))
        p_one = round(measurement_sum/n, 3)

        return {0: 1-p_one, 1: p_one}
    
    @staticmethod
    def bit_to_qubit(bits):
        qubits = []
        for bit in bits:
            if bit == 0:
                qubits.append(Qubit(alpha=1, beta=0))
            elif bit == 1:
                qubits.append(Qubit(alpha=0, beta=1))

        if len(bits) != len(qubits):
            raise Exception("Bit list can only contain 0's and 1's!")
        
        return qubits
    
    @staticmethod
    def measure_qubits(qubits):
        return np.array([qubit.measure() for qubit in qubits])
