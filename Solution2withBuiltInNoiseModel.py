import qiskit as qskt
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute
from qiskit import Aer
from qiskit.providers.aer.noise import NoiseModel, pauli_error

def buildNoiseModel(errorProba, probaType):
    noise_bit_flip = NoiseModel()
    error = pauli_error([('X', probaType * errorProba), ('I', 1 - errorProba), ('Z', (1 - probaType) * errorProba)])
    noise_bit_flip.add_all_qubit_quantum_error(error, ["id"])
    return noise_bit_flip

def signFlipCode(input, ancilla, circuit):
    circuit.h(input)
    bitFlipCode(input, ancilla, circuit)
    circuit.h(input)

def bitFlipCode(input, ancilla, circuit):
# bit flip correction ----------------------------------------------
    circuit.cx(input[0], ancilla[0])
    circuit.cx(input[1], ancilla[0])
    circuit.cx(input[0], ancilla[1])
    circuit.cx(input[2], ancilla[1])

    circuit.ccx(ancilla[0], ancilla[1], input[0])

qb1 = qskt.QuantumRegister(3, 'qb1')
qb2 = qskt.QuantumRegister(3, 'qb2')
ancilla = qskt.QuantumRegister(4, 'ancilla')
c = ClassicalRegister(2)
circ = QuantumCircuit(qb1, qb2, ancilla, c)

# We need the repeated qubits to be synchronize:
circ.h(qb1)
# Introducing error:
circ.id(qb1)
circ.id(qb2)

# # CNOT gate that entangles the two qubits
circ.cx(qb1, qb2)

# First we would fix the sign-flip error on the first qubit
# We uncompute the CNOT
circ.cx(qb1, qb2)
# And we apply the standard sign-flip correction
signFlipCode(qb1, ancilla[:2], circ)
# We apply CNOT again but with the fixed qubit only
circ.cx(qb1[0], qb2)
# Now all copies of the 2nd qubit are synchronized and we  can use the standard bit-flip correction
bitFlipCode(qb2, ancilla[2:], circ)

# Uncomputing the qubits
circ.cx(qb1[0], qb2)
circ.h(qb1)

# Now we measure the main qubits
circ.measure(qb1[0], c[0])
circ.measure(qb2[0], c[1])

cm = qskt.ClassicalRegister(2)

# Perform a noise simulation
noise_bit_flip = buildNoiseModel(0.3, 0.5)
result = execute(circ, Aer.get_backend('qasm_simulator'),
                 # coupling_map=coupling_map,
                 basis_gates=noise_bit_flip.basis_gates,
                 noise_model=noise_bit_flip,
                 shots = 10000).result()
counts = result.get_counts(0)
print(counts)

# def errorCode(input, errorQb, errorTypeQb, errorProba, bitFlipProba, circuit):
#     # circuit.
#     for i in range(len(input)):
#         circuit.initialize([sqrt(1 - errorProba), sqrt(errorProba)], errorQb[i])
#         circuit.initialize([sqrt(1 - bitFlipProba), sqrt(bitFlipProba)], errorTypeQb[i])
#         circuit.ccx(errorQb[i], errorTypeQb[i], input[i])
#
#         circuit.x(errorTypeQb[i])
#         ccz(errorQb[i], errorTypeQb[i], input[i], circuit)

# TODO: write discussion & illustrations
# TODO: Generate noise with one Qubit / try native noise
# TODO: try real QPC
# No correction. 21%
# bit flip only 12%
# sign flip only: 20%
# bit & sign flip : 11%


# noise_bit_flip = NoiseModel()
# errorProba = 0.3
# probaType = 0.7
# error = pauli_error([('X', probaType * errorProba), ('I', 1 - errorProba), ('Z', (1 - probaType) * errorProba)])
# error2 = error.tensor(error)
# noise_bit_flip.add_all_qubit_quantum_error(error, ["u1", "u2", "u3"])
# noise_bit_flip.add_all_qubit_quantum_error(error2, ["cx"])
#
# simulator = qskt.Aer.get_backend('qasm_simulator', noise_model=noise_bit_flip)
# 1# from qiskit.providers.aer import QasmSimulator
# # simulator = QasmSimulator(noise_model=noise_bit_flip)
# nbShots = 10000
# result = qskt.execute(circuit, simulator, shots = nbShots).result()
# # plot_state_qsphere(result.get_statevector(circuit))
# print(result.get_counts())
