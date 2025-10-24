import os
import sys
import pandas as pd
import subprocess

def synthesisEmulator(N, W, S, Q, path ):
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the target Python script
    os.chdir('../design/hdl_generation')

    # Run the vhdl generator,
    subprocess.run(['python', "emulator_gen.py", format(N), format(W), format(S), format(Q)])
    os.chdir(script_dir)
    create_the_tcl_file(N, W, S, Q, path)
    QuartusSynthesis(N, W, S, Q, path)
    read_and_resume_results(N, W, S, Q, path)
    return True

def create_the_tcl_file(N, W, S, Q, path):
    if not os.path.exists(path):
        os.makedirs(path)
        print("New Path created\n")
    tcl_file_name =path + "Current.tcl"
    tcl_file_name_ref =  "Emulator.tcl"

    try:
        TCLFile = open(tcl_file_name, 'w')
    except:
        print("Error: it is not possible to open or create the file" + tcl_file_name + "\n")
        sys.exit()

    try:
        TCLFileRef = open(tcl_file_name_ref, 'r')
    except:
        print("Error: it is not possible to open the file" + tcl_file_name_ref + "\n")
        sys.exit()
    new_file_content = ""
    emulatorstring = "EMULATOR_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S) + "_Q_" + format(Q)
    QEPstring = "QEP_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S)
    for line in TCLFileRef:
        if "multiplexer" in line:
            new_line = "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_"+ format(N) + "_1.vhd" + "\n"
            new_line += "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_2_1.vhd" + "\n"
            new_line += "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_3_1.vhd" + "\n"
            new_line += "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_4_1.vhd" + "\n"
            new_line += "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_5_1.vhd" + "\n"
            new_line += "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_" + format(2**N) + "_1.vhd" + "\n"
            new_line += "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_" + format(2**Q) + "_1.vhd" + "\n"
            new_line += "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplexers/src/multiplexer_" + format(2**W) + "_1.vhd"
            new_file_content += new_line + "\n"
        elif "decoder" in line:
            new_line = "set_global_assignment -name VHDL_FILE ../../design/basic_blocks/decoders/src/state_decoder_N_" + format(N) + ".vhd"
            new_file_content += new_line + "\n"
        else:
            new_line = line.strip().replace("EMULATOR_N_3_W_0_S_0_Q_2", emulatorstring).replace("QEP_N_3_W_0_S_0", QEPstring)
            new_file_content += new_line + "\n"

    TCLFileRef.close()
    TCLFile.write(new_file_content)
    TCLFile.close()

    # open both files
    with open(path + "EMULATOR_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S) + "_Q_" + format(Q) + ".sdc", 'w') as file_sdc:
        file_sdc.write("create_clock -name {EMULATOR_N_" + format(N) + "_W_"  + format(W) + "_S_" + format(S) + "_Q_" + format(Q) + "_IN_CLK} -period 20.000 -waveform {0.000 10.000} { EMULATOR_N_" + format(N) + "_W_"  + format(W) + "_S_" + format(S) + "_Q_" + format(Q) + "_IN_CLK }\n")


def read_and_resume_results(N, W, S, Q, path):
    Results = {}
    Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)] = {}
    AreaFileName = path + "output_files/EMULATOR_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S) + "_Q_" + format(Q) + ".fit.summary"
    PowFileName = path + "output_files/EMULATOR_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S) + "_Q_" + format(Q) + ".pow.summary"
    TimeFileName = path + "output_files/EMULATOR_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S) + "_Q_" + format(Q) + ".sta.summary"

    try:
        AreaFile = open(AreaFileName, "r")
    except:
        print("Error: it is not possible to open or create the file" + AreaFileName + "\n")
        sys.exit()
    lines = AreaFile.readlines()
    for line in lines:
        if line.startswith("Total logic elements :"):
            try:
                LogicUtilization = int(line.split(" ")[5].replace(",", ""))
            except:
                sys.exit()
            Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["LogicElements"] = LogicUtilization
        elif line.startswith("Total registers :"):
            try:
                Registers = int(line.split(" ")[3].replace(",", ""))
            except:
                sys.exit()
            Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["Registers"] = Registers
        elif line.startswith("Total DSP Blocks :"):
            try:
                DSP = int(line.split(" ")[4].replace(",", ""))
            except:
                print("Here2")
                sys.exit()
            Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["DSP"] = DSP
    AreaFile.close()
    try:
        PowFile = open(PowFileName, "r")
    except:
        print("Error: it is not possible to open or create the file" + PowFileName + "\n")
        sys.exit()
    lines = PowFile.readlines()
    for line in lines:
        if line.startswith("Total Thermal Power Dissipation :"):
            try:
                TotalPower = float(line.split(" ")[5].replace(",", ""))
            except:
                sys.exit()
            Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["TotalPower"] = TotalPower
        elif line.startswith("Core Dynamic Thermal Power Dissipation :"):
            try:
                DynamicPower = float(line.split(" ")[6].replace(",", ""))
            except:
                sys.exit()
            Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["DynamicPower"] = DynamicPower
        elif line.startswith("Core Static Thermal Power Dissipation :"):
            try:
                StaticPower = float(line.split(" ")[6].replace(",", ""))
            except:
                sys.exit()
            Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["StaticPower"] = StaticPower
    PowFile.close()
    try:
        TimeFile = open(TimeFileName, "r")
    except:
        print("Error: it is not possible to open or create the file" + TimeFileName + "\n")
        sys.exit()
    lines = TimeFile.readlines()
    i = 0
    while not lines[i].startswith("Type  : Fast 1200mV 0C Model Setup"):
        i += 1
    i += 1
    try:
        Time = 20 - float(lines[i].split(" ")[2].replace(",", ""))
    except:
        sys.exit()
    Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["Time"] = Time
    Results[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)]["Frequency"] = 1000 / Time
    TimeFile.close()
    DataFramePandas = pd.DataFrame.from_dict(Results)
    DataFramePandas.to_csv(path + "EMULATOR_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S) + "_Q_" + format(Q) + ".csv")


def QuartusSynthesis(N, W, S, Q, path):

    currentPath = os.getcwd()
    os.chdir(path)
    tclfilename = "Current.tcl"
    print(tclfilename)
    os.environ["PATH"] += os.pathsep + r'C:/intelFPGA_lite/17.0/quartus/bin64'
    print("Starting synthesis...")
    process = subprocess.call(["quartus_sh", "-t",  tclfilename])
    # os.system("quartus_sh -t " + tclfilename)
    os.system("quartus_sh --flow compile EMULATOR_N_" + format(N) + "_W_" + format(W) + "_S_" + format(S) + "_Q_" + format(Q))
    print("Sythesys completed")
    os.chdir(currentPath)

