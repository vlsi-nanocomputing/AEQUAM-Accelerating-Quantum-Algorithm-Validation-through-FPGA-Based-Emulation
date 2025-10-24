import os
from testbench_utils import testVLSIemulator
import sys



# Floating point
pathEmulatorIstructions = "compiled_mqt_sim/"
pathEmulatorIstructionsRef = "../file/compiled_mqt_dec/"
pathOutputEmulator = "../file/simulated_mqt_vhdl/"
pathOutputQiskit = "../file/qiskit_res/"
pathOutputQiskitQASM = "../file/qiskit_qasm_res/"
path = "../file/MQTBench_input/"
files = os.listdir(path)
for file in files:
    print("\n\execution of " + file + ":\n\n")
    qasm_file_path = path + file
    circuit = file[:-5]
    instruction_file_path = pathEmulatorIstructions + circuit + "_compiled.qasm"
    sincos_file_path = pathEmulatorIstructions + circuit + "_sincos.qasm"
    output_emulator_file_path = pathOutputEmulator + circuit + ".txt"

    f = open(pathEmulatorIstructionsRef + circuit + "_compiled.qasm", "r")
    windows = 1
    qubit = int(f.readline().strip('\n'))
    print(qubit)
    lines = f.readlines()
    Lenght = len(lines)
    print(Lenght)

    f.close()

    expected_output_file = pathOutputEmulator + file[:-5] + "_state.txt"

    if qubit <= 8 and qubit > 1:
        if not os.path.exists(expected_output_file):

            windows = 0


            done = False
            try:
                timeVLSI = testVLSIemulator(path, file, pathEmulatorIstructions,  pathOutputEmulator, qubit, windows)
                print("Well done\n")
                done = True
            except:
                print("Problems\n")
                done = False
