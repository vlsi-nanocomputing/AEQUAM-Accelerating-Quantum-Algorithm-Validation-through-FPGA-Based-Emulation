import sys
import numpy as np
from qiskit import BasicAer
from qiskit.execute_function import execute
from qiskit import QuantumCircuit
import time
sys.path.insert(0, r'./floating_point')
from VLSIEmulator import EmulatorWrap 
import math
import cmath
from utiles import testVLSI, testQiskit

# varify that a sufficient number of argument is provided
if len(sys.argv) < 6:
    print("Error: the provided argoment are not enough\n")
    sys.exit(-1)

#acquire the file path from command line
qasmfilename = sys.argv[1]

#acquire the file path from command line
outputfilenameqiskit = sys.argv[2]

#acquire the file path from command line
istructionfilename = sys.argv[3]

#acquire the file path from command line
sinecosinefilename = sys.argv[4]

#acquire the file path from command line
outputfile = sys.argv[5]

#if provided, acquire the parallelism
if len(sys.argv) == 7:
    parallelism = int(sys.argv[6])
else:
    parallelism = 32
    
verbose = True

timeVLSI = testVLSI(istructionfilename, sinecosinefilename, outputfile, parallelism, "floating", verbose)

print("The time employed by VLSIEmulator is " + format(timeVLSI) + "\n")

timeQiskit=testQiskit(qasmfilename, outputfilenameqiskit)

print("The time employed by Qiskit state vector is " + format(timeQiskit) + "\n")