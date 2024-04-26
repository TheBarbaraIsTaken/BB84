**BB84 Protocol Simulation**

This repository contains a Python implementation of the BB84 protocol, a quantum key distribution (QKD) algorithm, along with supporting classes for simulating quantum states and operations and analyzing the performance of the protocal against main-in-the-middle attack.

The project was created for the course Information Theory and Statistics at University of Twente.

**Contents:**

- `main.py`: Main Python script for running the BB84 protocol simulation.
- `README.md`: Readme file providing an overview of the project and instructions for running the simulation.
- `qubit.py`: Python script defining the `Qubit` class, which represents a quantum bit (qubit) and provides methods for qubit manipulation and measurement.
- `bb84.py`: Python script defining the `BB84` class, which encapsulates the BB84 protocol implementation and includes methods for running the simulation and checking for the failure of the protocol.
- `failure.ipynb`: File for plotting failure probability estimations.

**How to Run:**

To run the BB84 protocol simulation, follow these steps:

1. Ensure you have Python installed on your system (version 3.6 or higher).
2. Clone this repository to your local machine.
3. Install the required packages using the requirements.txt file.
4. Navigate to the repository directory using the command line.
5. Run the `main.py` script using Python:

```
python3 main.py
```

6. The simulation will execute, and the output will display the estimated probabilities of protocol failure.

**References:**

- Peter W. Shor and John Preskill. "Simple Proof of Security of the BB84 Quantum Key Distribution Protocol." [arXiv:quant-ph/0003004](https://arxiv.org/pdf/quant-ph/0003004.pdf).
- Stephen M. Barnett. "Introduction to Quantum Information." [Link](https://www.gla.ac.uk/media/Media_344957_smxx.pdf).

**Author:**

This BB84 protocol simulation was implemented by Barbara Noemi Szabo and Ken Yeh. 

**License:**

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute the code for any purpose.
