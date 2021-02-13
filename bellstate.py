import qiskit as qskt
from math import sqrt

dimension = 1
qb1 = qskt.QuantumRegister(dimension, 'qb1')
qb2 = qskt.QuantumRegister(dimension, 'qb2')
cm = qskt.ClassicalRegister(2)

circuit = qskt.QuantumCircuit(qb1, qb2, cm)

# Basic circuit
circuit.h(qb1)
circuit.cx(qb1, qb2)

circuit.measure(qb1, cm[0])
circuit.measure(qb2, cm[1])

simulator = qskt.Aer.get_backend('qasm_simulator')
nbShots = 10000
result = qskt.execute(circuit, simulator, shots = nbShots).result()
print(result.get_counts())
