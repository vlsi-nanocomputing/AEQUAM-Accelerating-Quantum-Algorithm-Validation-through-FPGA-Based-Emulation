import sys
import numpy as np
from qiskit import BasicAer
from qiskit.execute_function import execute
from qiskit import QuantumCircuit
from qiskit import Aer
import qiskit
from qiskit import ClassicalRegister, QuantumRegister
from qiskit.circuit.library.standard_gates import *
from qiskit import transpile
import time
sys.path.insert(0, r'./floating_point')
from VLSIEmulator import EmulatorWrap 
sys.path.insert(0, r'./fixed_point_truncation')
from VLSIEmulatorFixedPoint import EmulatorFixedWrap
sys.path.insert(0, r'./fixed_point_nearest') 
from VLSIEmulatorFixedPointNearest import EmulatorFixedNearestWrap
sys.path.insert(0, r'./fixed_point_nearest_even') 
from VLSIEmulatorFixedNearestEven import EmulatorWrap_fixed_nearest_even 
import math
import cmath


def testVLSI(istructionfilename, sinecosinefilename,  outputfilename, parallelism, approximation_mechanism, verbose):
    stop = 0
    start = 0
    if approximation_mechanism == "floating":
        start = time.time()
        ret = EmulatorWrap(istructionfilename, sinecosinefilename, outputfilename, parallelism, verbose)
        stop = time.time()
    elif approximation_mechanism == "truncation":
        start = time.time()
        ret = EmulatorFixedWrap(istructionfilename, sinecosinefilename, outputfilename, parallelism, verbose)
        stop = time.time()
    elif approximation_mechanism == "nearest":
        start = time.time()
        ret = EmulatorFixedNearestWrap(istructionfilename, sinecosinefilename, outputfilename, parallelism, verbose)
        stop = time.time()
    elif approximation_mechanism == "nearest_even":
        start = time.time()
        ret = EmulatorWrap_fixed_nearest_even(istructionfilename, sinecosinefilename, outputfilename, parallelism, verbose)
        stop = time.time()
    return stop-start
    
def testQiskit(QasmFile, outputfile):
    backend = BasicAer.get_backend('statevector_simulator')
    print("Backend chosen\n")
    qc = QuantumCircuit.from_qasm_file(QasmFile)
    print("Circuit generated\n")
    start = time.time()
    job = execute(qc, backend)
    result = job.result()
    state_vector = result.get_statevector()
    stop = time.time()
    print("Circuit executed\n")
    
    try:
        f_out = open(outputfile, "w")
    except:
        print("It is not possible to open the output file\n")
        return -1
        
    for elm in state_vector:
        f_out.write(format(elm) + "\n")
    
    return stop-start
    
def testQiskitQASM(QasmFile, outputfile):
    backend = BasicAer.get_backend('qasm_simulator')
    print("Backend chosen\n")
    qc = QuantumCircuit.from_qasm_file(QasmFile)
    qc.measure_all()
    print("Circuit generated\n")
    start = time.time()
    print("Circuit generated\n")
    start = time.time()
    job = execute(qc, backend)
    result = job.result()
    counts = result.get_counts(qc)
    stop = time.time()
    print("Circuit executed\n")
    
    try:
        f_out = open(outputfile, "w")
    except:
        print("It is not possible to open the output file\n")
        return -1
        
    for elm in counts.keys():
        f_out.write(format(elm) + " " + format(counts[elm])+ "\n")
    
    return stop-start
    
def KLD(qiskitProbabilityDistributions, VLSIProbabilityDistributions):
    D = 0
    for i in range(len(qiskitProbabilityDistributions)):
        if VLSIProbabilityDistributions[i] != 0 and qiskitProbabilityDistributions[i] != 0: 
            D += qiskitProbabilityDistributions[i]*math.log(qiskitProbabilityDistributions[i]/VLSIProbabilityDistributions[i])
    return abs(D)
    
def HeligerFidelity(qiskitProbabilityDistributions, VLSIProbabilityDistributions):
    temp = 0
    for i in range(len(qiskitProbabilityDistributions)):
        temp += (math.sqrt(qiskitProbabilityDistributions[i]) - math.sqrt(VLSIProbabilityDistributions[i]))**2
    H = (1/math.sqrt(2))*math.sqrt(temp)
    F = (1-H**2)**2
    return F
    
def MaximumComplexDistance(qiskitStateVector, VLSIStateVector):
    maxDistance = 0
    for i in range(len(qiskitStateVector)):
        diff = math.sqrt((qiskitStateVector[i].real-VLSIStateVector[i].real)**2 + (qiskitStateVector[i].imag-VLSIStateVector[i].imag)**2)
        if diff > maxDistance:
            maxDistance = diff
    return maxDistance
            
def AverageComplexDistance(qiskitStateVector, VLSIStateVector):
    AverageDistance = 0
    for i in range(len(qiskitStateVector)):
        AverageDistance += math.sqrt((qiskitStateVector[i].real-VLSIStateVector[i].real)**2 + (qiskitStateVector[i].imag-VLSIStateVector[i].imag)**2)
    return AverageDistance/len(qiskitStateVector)
    
def MaximumSphereDistance(qiskitStateVector, VLSIStateVector):
    MinimumDistance = 0
    MaximumDistance = 0
    AverageDistance = 0
    First = True
    for state_VLSI, state_qiskit in zip(VLSIStateVector, qiskitStateVector):
        dot_product = state_VLSI * np.conjugate(state_qiskit)

        if state_VLSI == 0 and state_qiskit != 0:
            distance = abs(state_qiskit)
        elif state_qiskit == 0 and state_VLSI != 0:
            distance = abs(state_VLSI)
        elif state_qiskit == 0 and state_VLSI == 0:
            distance = 0
        else:
            theta = (np.real(dot_product)/(abs(state_VLSI)*abs(state_qiskit)))
            if theta > 1:
                theta = 1
            distance = np.arccos(theta)
            
        AverageDistance += distance
        
        if First:
            First = False
            MinimumDistance = distance
            MaximumDistance = distance
        else:
            if distance < MinimumDistance:
                MinimumDistance = distance
                
            if distance > MaximumDistance:
                MaximumDistance = distance
    
    AverageDistance = AverageDistance/len(VLSIStateVector)
                
    return MinimumDistance, MaximumDistance, AverageDistance
    
        
