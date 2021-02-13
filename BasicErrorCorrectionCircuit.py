import qiskit as qskt
from math import sqrt

def bitFlipCode(input, ancilla, circuit):
# bit flip correction ----------------------------------------------
    circuit.cx(input[0], ancilla[0])
    circuit.cx(input[1], ancilla[0])
    circuit.cx(input[0], ancilla[1])
    circuit.cx(input[2], ancilla[1])

    circuit.ccx(ancilla[0], ancilla[1], input[0])

def signFlipCode(input, ancilla, circuit):
    circuit.h(input)
    bitFlipCode(input, ancilla, circuit)
    circuit.h(input)

def ccz(x1, x2, y, circuit):
    circuit.h(y)
    circuit.ccx(x1, x2, y)
    circuit.h(y)

def errorCode(input, errorQb, errorTypeQb, errorProba, bitFlipProba, circuit):
    # circuit.
    for i in range(len(input)):
        circuit.initialize([sqrt(1 - errorProba), sqrt(errorProba)], errorQb[i])
        circuit.initialize([sqrt(1 - bitFlipProba), sqrt(bitFlipProba)], errorTypeQb[i])
        circuit.ccx(errorQb[i], errorTypeQb[i], input[i])

        circuit.x(errorTypeQb[i])
        ccz(errorQb[i], errorTypeQb[i], input[i], circuit)

dimension = 3
qb1 = qskt.QuantumRegister(dimension, 'qb1')
errorQB = qskt.QuantumRegister(dimension * 2, 'error')
ancilla = qskt.QuantumRegister(2, 'ancilla')
cm = qskt.ClassicalRegister(3)

circuit = qskt.QuantumCircuit(qb1, errorQB, ancilla, cm)

# Bit flip testing
# Error code
errorCode(qb1, errorQB[:dimension], errorQB[dimension : (2*dimension)], 0.3, 0.7, circuit)
# bit-flip correction code
bitFlipCode(qb1, ancilla, circuit)
# measuring
circuit.measure(qb1[0], cm[0])

# # Sign  flip testing
# circuit.h(qb1)
# # Error code
# errorCode(qb1, errorQB[:dimension], errorQB[dimension : (2*dimension)], 0.3, 0.7, circuit)
# # sign -flip correction code
# signFlipCode(qb1, ancilla, circuit)
# # measuring
# circuit.h(qb1)
# circuit.measure(qb1[0], cm[0])


simulator = qskt.Aer.get_backend('qasm_simulator')
nbShots = 10000
result = qskt.execute(circuit, simulator, shots = nbShots).result()
print(result.get_counts())
