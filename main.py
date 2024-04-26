from qubit import Qubit
from bb84 import BB84
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Test
    # q = Qubit(sqrt(0.5), sqrt(0.5))
    # q = Qubit(1, 0)
    
    # print(Qubit.estimate_probs(q))

    # print(q)
    # q.hadamard()
    # print(q)
    # q.hadamard()
    # print(q)
    
    # protocol = BB84(length=100_000)

    # is_failed = protocol.run(is_attack=False)
    # print(protocol.joint_distr())

    # print(is_failed)

    
    # BB84 protocol failure for no attack
    protocol = BB84()
    N = 10_000
    failures = []

    lengths = list(range(1, 25))

    for length in lengths:
        protocol.length = length

        tmp = []
        for i in range(N):
            is_failed = protocol.run(is_attack=False)
            protocol.clear()
            tmp.append(is_failed)

        failures.append(sum(tmp))

    # BB84 protocol failure with attack
    protocol = BB84()
    N_ATTACK = 10_000
    failures_attack = []

    lengths_attack = list(range(1, 25, 1))

    for length in lengths_attack:
        protocol.length = length

        tmp = []
        for i in range(N_ATTACK):
            is_failed = protocol.run(is_attack=True)
            protocol.clear()
            tmp.append(is_failed)

        failures_attack.append(sum(tmp))

    plt.scatter(lengths, np.array(failures) / N, c='g')
    plt.show()

    plt.scatter(lengths_attack, np.array(failures_attack) / N_ATTACK, c='g')
    plt.show()
