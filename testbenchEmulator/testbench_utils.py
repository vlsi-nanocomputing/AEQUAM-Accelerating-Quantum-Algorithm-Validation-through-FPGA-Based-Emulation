import sys
import os
sys.path.insert(0, r'../compilatore')
from compilatore.utils_f import translator
import subprocess

def testVLSIemulator(path, filename, folder_output,  outputfilepath, qubit, windows):

    configuration_file_name = '../configurazione/emulator_configuration_hw.txt'

    #write the necessary information from the configuration file
    #open the file with circuit description
    try:
        fileInConfig = open(configuration_file_name, 'w')
    except:
        print("Error! The input file " + configuration_file_name + " does not exist\n")
        return False
    fileInConfig.write(format(qubit) + " " + format(windows) + " " + format(0) + " " + format(8) + '\n')
    fileInConfig.close()
    ret = translator(path + filename, configuration_file_name, folder_output, 20, "nearest", binary=True, hardware=True, package_lenght=20)
    if ret < 0:
        print("It was not possible to complete the compilation procedure\n")
        return False
    else:
        print("Compilation procedure terminate successfully\n")
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the target Python script
    os.chdir('../design/hdl_generation')

    # Run the vhdl generator,
    subprocess.run(['python', "emulator_gen.py", format(qubit), format(windows), "0", "8"])
    os.chdir(script_dir)
    testbenchgenerator(qubit, windows, filename, folder_output, outputfilepath)
    tlc_generator(qubit, windows)
    LanchModelsimWindows()
    return True


def testbenchgenerator(qubit, windows, filename,  filepath, outputfilepath):
    filename_fields = filename[:-5].split("/")
    filename_output = ""
    for i in range(len(filename_fields) - 2):
        filename_output += filename_fields[i] + "/"

    filename_output += filepath + filename_fields[len(filename_fields) - 1] + "_compiled.qasm"

    filename_sincos = ""
    for i in range(len(filename_fields) - 2):
        filename_sincos += filename_fields[i] + "/"

    filename_sincos += filepath + filename_fields[len(filename_fields) - 1] + "_sincos.qasm"

    filename_res = ""
    for i in range(len(filename_fields) - 2):
        filename_res += filename_fields[i] + "/"

    filename_res += outputfilepath + filename_fields[len(filename_fields) - 1] + "_state.txt"

    testbenchRef = open('../design/emulator/sim/tb_emulator.vhd', 'r')
    emulatorstring = "EMULATOR_N_" + format(qubit) + "_W_" + format(windows) + "_S_0_Q_" + format(8)
    new_file_content = ""
    for line in testbenchRef:
        stripped_line = line.strip()
        new_line = stripped_line.replace("EMULATOR_N_3_W_0_S_0_Q_2", emulatorstring).replace("bell_state3_compiled.qasm", "../../../file/" + filename_output).replace("bell_state3_sincos.qasm", "../../../file/" + filename_sincos).replace("res_file.txt", "../../../file/" + filename_res)
        new_file_content += new_line + "\n"

    testbenchRef.close()
    testbench = open('../design/emulator/sim/tb.vhd', 'w')
    testbench.write(new_file_content)
    testbench.close()


def tlc_generator(qubit, windows):

    tlc_commonblock_Ref = open('../design/emulator/sim/common_basic_block_base.do', 'r')
    new_file_content = ""
    First = True
    for line in tlc_commonblock_Ref:
        if "multiplexers" in line:
            if First:
                new_line = "vcom ../../basic_blocks/multiplexers/src/multiplexer_"+ format(qubit) + "_1.vhd" + "\n"
                new_line += "vcom ../../basic_blocks/multiplexers/src/multiplexer_2_1.vhd" + "\n"
                new_line += "vcom ../../basic_blocks/multiplexers/src/multiplexer_" + format(2**qubit) + "_1.vhd" + "\n"
                new_line += "vcom ../../basic_blocks/multiplexers/src/multiplexer_" + format(2**8) + "_1.vhd" + "\n"
                new_line += "vcom ../../basic_blocks/multiplexers/src/multiplexer_" + format(2**windows) + "_1.vhd"
                new_file_content += new_line + "\n"
                First = False
        elif "decoders" in line:
            new_line = "vcom ../../basic_blocks/decoders/src/state_decoder_N_" + format(qubit) + ".vhd"
            new_file_content += new_line + "\n"
        else:
            new_line = line.strip()
            new_file_content += new_line + "\n"

    tlc_commonblock_Ref.close()
    tlc_commonblock = open('../design/emulator/sim/common_basic_block.do', 'w')
    tlc_commonblock.write(new_file_content)
    tlc_commonblock.close()

    emulatorstring = "EMULATOR_N_" + format(qubit) + "_W_" + format(windows) + "_S_0_Q_" + format(8)
    QEPString = "QEP_N_" + format(qubit) + "_W_" + format(windows) + "_S_0"
    tlc_emulator_Ref = open('../design/emulator/sim/common_emulator_base.do', 'r')
    new_file_content = ""
    for line in tlc_emulator_Ref:
        if "QEP" in line:
            new_line = "vcom ../../QEP/src/" + QEPString + ".vhd"
        elif "emulator" in line:
            new_line = "vcom ../src/" + emulatorstring + ".vhd"
        else:
            new_line = line.strip()

        new_file_content += new_line + "\n"

    tlc_emulator_Ref.close()
    tlc_emulator = open('../design/emulator/sim/common_emulator.do', 'w')
    tlc_emulator.write(new_file_content)
    tlc_emulator.close()
    
    
    

def LanchModelsimWindows():
    cwd = os.getcwd()
    os.chdir("../design/emulator/sim/")
    os.environ["PATH"] += os.pathsep + r'C:/altera/11.0sp1/modelsim_ase/win32aloem'
    try:
        os.rmdir("work")
    except OSError:
        pass
    try:
        os.remove("transcript")
    except OSError:
        pass
    try:
        os.remove("vsim.wlf")
    except OSError:
        pass
    print ("Starting simulation...")
    os.system("vsim -modelsimini C:/altera/11.0sp1/modelsim_ase/modelsim.ini -c -do transcript.tcl")
    #process = subprocess.call(["vsim", "-c", "-do", "transcript.tcl"])
    print ("Simulation completed")
    os.chdir(cwd)


