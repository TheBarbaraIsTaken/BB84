from qubit import Qubit
from bb84 import BB84

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
    
    # BB84 protocol
    protocol = BB84(length=10)

    for i in range(10):
        print(protocol.run(is_attack=True))
    