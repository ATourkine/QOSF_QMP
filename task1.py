import qiskit as qskt
import random as rnd
import numpy as np
import matplotlib as mpl
import scipy.optimize as opt

def BuildCircuit(dimension, nbLayers, params):
    circuit = qskt.QuantumCircuit(dimension, dimension)

    for i in range(nbLayers):
        ind = 2*i*dimension
        thetaEven = params[ind:ind+dimension]
        thetaOdd = params[ind+dimension:ind+dimension*2]

        for q in range(dimension):
            circuit.rz(thetaEven[q], q)
        for i in range(dimension):
            for j in range(i+1,dimension):
                circuit.cz(i,j)
        circuit.barrier()

        for q in range(dimension):
            circuit.ry(thetaOdd[q], q)
        circuit.barrier()
    # circuit.draw("mpl")

    return circuit

def calcDistance(theta, nbLayers, phiVector):

    circuit = BuildCircuit(dimension, nbLayers, theta)
    for i in range (dimension):
        circuit.measure(i, i)

    simulator = qskt.Aer.get_backend('qasm_simulator')
    nbShots = 100000

    counts = qskt.execute(circuit, simulator, shots = nbShots).result().get_counts()
    sum = 0

    for state in counts:
        score = 0
        for i in range(len(state)):
            # The PhiVector could have been stored inverted right from the beginning
            if int(state[i]) != phiVector[len(state) - i - 1]: score +=1
        sum += counts[state] * np.sqrt(score)
    sum = sum / nbShots

    return sum

def calcMin(nbLayers, phiVector, theta):

    thetaDim = nbLayers * dimension * 2
    thetaBounds=list(zip([0.0] * thetaDim, [2 * 3.14159] * thetaDim))
    func = lambda x: calcDistance(x, nbLayers, phiVector)

    if len(theta) == 0:
        theta = 2 * 3.14159 * np.random.rand(1, thetaDim)
    else:
        theta = np.concatenate([theta, (2 * 3.14159 * np.random.rand(1, 2 * dimension))[0]])
    optResult = opt.minimize(func, theta, method='SLSQP',bounds = thetaBounds, tol = 1e-1, options={'ftol': 1e-2, 'eps': 1e-2})
    return optResult.fun, optResult.x

dimension = 4
result = []
phiVector = []

for i in range(dimension): phiVector.append(rnd.randint(0,1))
print("Phi vector:")
print(phiVector)
theta = []

for n in range(15):
    minDistance, theta = calcMin(n+1, phiVector, theta)
    print("#Layers: " + str(n+1) + " Distance: {:.2f}".format(minDistance))
    result.append(minDistance)
mpl.pyplot.plot(result)
print(result)
