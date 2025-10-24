import os
import sys
import time
import numpy as np
from qiskit import BasicAer
from qiskit.execute_function import execute
from qiskit import QuantumCircuit
import pandas as pd
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
from utiles import testVLSI, testQiskit, testQiskitQASM, KLD, HeligerFidelity, MaximumComplexDistance, AverageComplexDistance, MaximumSphereDistance
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import cm
import matplotlib as mpl

filename = "log_file.txt"
try:
    sys.stdout = open(filename, "w")
except:
    print("Not possible to create the log file\n")
    sys.exit(0)

    
fileErrorsname = "errors_file.txt"
try:
    fileErrors = open(fileErrorsname, "w")
except:
    print("Not possible to create the errors file\n")
    sys.exit(0)
    
print("Start executions of all files\n")

EmulatorTimeForLenght = {}
kld_res_dict = {}
HF_res_dict = {}
MCD_dict = {}
ACD_dict = {}
MSD_dict = {}
ASD_dict = {}
MinSD_dict = {}
RepetitionForLenght = {}    

EmulatorTimeForLenght_float = {}
QiskitTimeForLenght = {}
QiskitQASMTimeForLenght = {}
kld_res_dict_float = {}
HF_res_dict_float = {}
MCD_dict_float = {}
ACD_dict_float = {}
MSD_dict_float = {}
ASD_dict_float = {}
MinSD_dict_float = {}
RepetitionForLenght_float = {} 
RepetitionForLenght_float_qiskit = {}
RepetitionForLenght_float_qiskit_qasm = {}



approximation_mechanisms = ['nearest', 'nearest_even', 'truncation']

approximation_mechanisms_acronym = {'nearest': 'n', 'nearest_even': 'ne', 'truncation': 't'}

parallelisms = range(8, 32, 2)



path = "../../file/input/"
files = os.listdir(path)


#Floating point
pathEmulatorIstructions = "../../file/compiled_dec/"
pathOutputEmulator = "../../file/simulated/"
pathOutputQiskit = "../../file/qiskit_res/"
pathOutputQiskitQASM = "../../file/qiskit_qasm_res/"
path = "../../file/input/"
files = os.listdir(path)
for file in files:
    print("\n\execution of " + file +":\n\n")
    qasm_file_path = path + file
    circuit = file[:-5]
    instruction_file_path = pathEmulatorIstructions +  circuit + "_compiled.qasm"
    sincos_file_path = pathEmulatorIstructions +  circuit + "_sincos.qasm"
    output_emulator_file_path = pathOutputEmulator +  circuit + ".txt"
    output_qiskit_file_path = pathOutputQiskit +  circuit + ".txt"
    output_qiskit_qasm_file_path = pathOutputQiskitQASM +  circuit + ".txt"
    
    f = open(instruction_file_path, "r") 
    
    qubit = int(f.readline().strip('\n'))
    print(qubit)
    lines = f.readlines()
    Lenght = len(lines)
    print(Lenght)
    
    
    f.close()
    
    if qubit <= 16:
    
        parallelism = 32
        
        verbose = False
        
        done = False
        timeVLSI = 0
        try:
            timeVLSI = testVLSI(instruction_file_path, sincos_file_path, output_emulator_file_path, parallelism, "floating", verbose)
            print("Well done\n")
            done = True
        except:
            print("Problems\n")
            done = False
                
        if done:
            if Lenght in EmulatorTimeForLenght_float.keys():
                EmulatorTimeForLenght_float[Lenght] += timeVLSI
                RepetitionForLenght_float[Lenght] += 1
            else: 
                EmulatorTimeForLenght_float[Lenght] = timeVLSI
                RepetitionForLenght_float[Lenght] = 1

            print("The time employed by VLSIEmulator is: " + format(timeVLSI) + "\n")
            
            timeQiskit = 0
            done = False
            
            try:
                print("Qiskit solver execution\n")
                timeQiskit = testQiskit(qasm_file_path, output_qiskit_file_path)
                print("Well done\n")
                done = True
            except:
                print("Problems\n")
                done = False
            timeQiskitQASM = 0            
            try:
                print("Qiskit QASM solver execution\n")
                timeQiskitQASM = testQiskitQASM(qasm_file_path, output_qiskit_qasm_file_path)
                print("Well done\n")
                print("The time employed by Qiskit QASM  is: " + format(timeQiskitQASM) + "\n")
            except: 
                print("Problems\n")
                
            if Lenght in QiskitQASMTimeForLenght.keys():
                QiskitQASMTimeForLenght[Lenght] += timeQiskitQASM
                RepetitionForLenght_float_qiskit_qasm[Lenght] += 1
            else: 
                QiskitQASMTimeForLenght[Lenght] = timeQiskitQASM
                RepetitionForLenght_float_qiskit_qasm[Lenght] = 1
                
            #timeQiskit=testQiskit(qasm_file_path, output_qiskit_file_path)
            if done == True:
                print("The time employed by Qiskit state vector is: " + format(timeQiskit) + "\n")
                
                
                if Lenght in QiskitTimeForLenght.keys():
                    QiskitTimeForLenght[Lenght] += timeQiskit
                    RepetitionForLenght_float_qiskit[Lenght] += 1
                else: 
                    QiskitTimeForLenght[Lenght] = timeQiskit
                    RepetitionForLenght_float_qiskit[Lenght] = 1
                    
                #verify the results correctness
                try:
                    f_emulator = open(output_emulator_file_path, "r")
                except:
                    print("It is not possible to open the " + output_emulator_file_path + " file\n")
                    sys.exit()
                    
                statevector = []
                probabilityDensity = []
                
                lines = f_emulator.readlines()
                
                for line in lines:
                    val = line[:-1].split(" ")
                    if len(val) == 2:
                        real = float(val[0])
                        img = float(val[1][:-1])
                        z = complex(real, img)
                        statevector.append(z)
                        probability = real**2 + img**2  
                        probabilityDensity.append(probability)
                        
                f_emulator.close()
                

                
                print("Read qiskit file\n")        
                    #verify the results correctness
                try:
                    f_qiskit = open(output_qiskit_file_path, "r")
                except:
                    print("It is not possible to open the " + output_qiskit_file_path + " file\n")
                    sys.exit()
                    
                statevectorQiskit = []
                probabilityDensityQiskit = []
                
                lines = f_qiskit.readlines()
                
                for line in lines:
                    z = complex(line[:-1])
                    statevectorQiskit.append(z)
                    probability = z.real**2 + z.imag**2  
                    probabilityDensityQiskit.append(probability)
                        
                f_qiskit.close()

                print("Figure of merit evaluation\n")
                
                kld_res = KLD(probabilityDensityQiskit, probabilityDensity)
                
                print("The divergence is equal to: " + format(kld_res) + "\n")
                
                
                if kld_res > 0.05:
                    fileErrors.write("The circuit " + circuit + " presents a too high divergence, i.e., equal to: " + format(kld_res) +  "\n")
                    
                HF = HeligerFidelity(probabilityDensityQiskit, probabilityDensity)
                
                print("The Helinger fidelity is equal to: " + format(HF) + "\n")
                
                
                if HF < 0.95:
                    fileErrors.write("The circuit " + circuit + " presents a too low Helinger Fidelity, i.e., equal to: " + format(HF) +  "\n")
                    
                MCD = MaximumComplexDistance(statevectorQiskit, statevector)
                
                print("The maximum complex distance is equal to: " + format(MCD) + "\n")
                
                ACD = AverageComplexDistance(statevectorQiskit, statevector)
                
                print("The average complex distance is equal to: " + format(ACD) + "\n")
                
                MinSD, MSD, ASD = MaximumSphereDistance(statevectorQiskit, statevector)
                
                if Lenght in kld_res_dict_float.keys():
                    kld_res_dict_float[Lenght] += kld_res
                    HF_res_dict_float[Lenght] += HF
                    MCD_dict_float[Lenght] += MCD
                    ACD_dict_float[Lenght] += ACD
                    MSD_dict_float[Lenght] += MSD
                    MinSD_dict_float[Lenght] += MinSD
                    ASD_dict_float[Lenght] += ASD
                else: 
                    kld_res_dict_float[Lenght] = kld_res
                    HF_res_dict_float[Lenght] = HF
                    MCD_dict_float[Lenght] = MCD
                    ACD_dict_float[Lenght] = ACD
                    MSD_dict_float[Lenght] = MSD
                    MinSD_dict_float[Lenght] = MinSD
                    ASD_dict_float[Lenght] = ASD
                
                label = []
                for i in range(len(probabilityDensity)):
                    label.append(format(i, 'b').zfill(int(math.log2(len(probabilityDensity)))))
                
                if len(probabilityDensity) < 33:
                    barWidth = 0.25
                    br1 = np.arange(len(probabilityDensity))
                    br2 = [x + barWidth for x in br1]
                    plt.bar(br1, probabilityDensity, color ='r', width = barWidth, edgecolor ='grey', label ='Emulator')
                    plt.bar(br2, probabilityDensityQiskit, color ='g', width = barWidth, edgecolor ='grey', label ='Qiskit')
                    plt.xticks([r + barWidth for r in range(len(probabilityDensity))],label)
                    plt.xlabel("Basis State", fontsize=20)
                    plt.ylabel("Probability", fontsize=20)
                    leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
                    leg.get_frame().set_facecolor('white')
                    plt.savefig("../../file/probabilityBarPlot/" + circuit + ".eps", format='eps')
                    plt.savefig("../../file/probabilityBarPlot/" + circuit + ".png", format='png')
                    plt.savefig("../../file/probabilityBarPlot/" + circuit + ".pdf", format='pdf')
                    plt.close()
            else:
                print("Qiskit cannot simulate the file\n")
        else:
            print("My solver cannot simulate the file\n")   
    else:
        print("Too large problem to be simulated in software\n")
        
        

EmulatorTimeForLenght_float = dict(sorted(EmulatorTimeForLenght_float.items()))
QiskitTimeForLenght = dict(sorted(QiskitTimeForLenght.items()))
QiskitQASMTimeForLenght =  dict(sorted(QiskitQASMTimeForLenght.items()))
kld_res_dict_float =  dict(sorted(kld_res_dict_float.items()))
HF_res_dict_float = dict(sorted(HF_res_dict_float.items()))
MCD_dict_float = dict(sorted(MCD_dict_float.items()))
ACD_dict_float = dict(sorted(ACD_dict_float.items()))
MSD_dict_float = dict(sorted(MSD_dict_float.items()))
MinSD_dict_float = dict(sorted(MinSD_dict_float.items()))
ASD_dict_float = dict(sorted(ASD_dict_float.items()))
RepetitionForLenght_float = dict(sorted(RepetitionForLenght_float.items()))
RepetitionForLenght_float_qiskit = dict(sorted(RepetitionForLenght_float_qiskit.items()))
RepetitionForLenght_float_qiskit_qasm = dict(sorted(RepetitionForLenght_float_qiskit_qasm.items()))
for key in EmulatorTimeForLenght_float.keys():
    EmulatorTimeForLenght_float[key] = EmulatorTimeForLenght_float[key]/RepetitionForLenght_float[key]

for key in RepetitionForLenght_float_qiskit_qasm.keys():
    QiskitQASMTimeForLenght[key] = QiskitQASMTimeForLenght[key]/RepetitionForLenght_float_qiskit_qasm[key]

for key in RepetitionForLenght_float_qiskit.keys():
    QiskitTimeForLenght[key] = QiskitTimeForLenght[key]/RepetitionForLenght_float_qiskit[key]
    kld_res_dict_float[key] = kld_res_dict_float[key]/RepetitionForLenght_float_qiskit[key]
    HF_res_dict_float[key] = HF_res_dict_float[key]/RepetitionForLenght_float_qiskit[key]
    MCD_dict_float[key] = MCD_dict_float[key]/RepetitionForLenght_float_qiskit[key]
    ACD_dict_float[key] = ACD_dict_float[key]/RepetitionForLenght_float_qiskit[key]
    MSD_dict_float[key] = MSD_dict_float[key]/RepetitionForLenght_float_qiskit[key]
    MinSD_dict_float[key] = MinSD_dict_float[key]/RepetitionForLenght_float_qiskit[key]
    ASD_dict_float[key] = ASD_dict_float[key]/RepetitionForLenght_float_qiskit[key]
    
DataFramePandas = pd.DataFrame.from_dict(EmulatorTimeForLenght_float, orient='index')
DataFramePandas.to_csv("Time.csv")
DataFramePandas = pd.DataFrame.from_dict(QiskitTimeForLenght, orient='index')
DataFramePandas.to_csv("Time_qiskit_state_vector.csv")
DataFramePandas = pd.DataFrame.from_dict(QiskitQASMTimeForLenght, orient='index')
DataFramePandas.to_csv("Time_qiskit_qasm_simulator.csv")
DataFramePandas = pd.DataFrame.from_dict(kld_res_dict_float, orient='index')
DataFramePandas.to_csv("kld.csv")
DataFramePandas = pd.DataFrame.from_dict(HF_res_dict_float, orient='index')
DataFramePandas.to_csv("HF.csv")
DataFramePandas = pd.DataFrame.from_dict(MCD_dict_float, orient='index')
DataFramePandas.to_csv("MCD.csv")
DataFramePandas = pd.DataFrame.from_dict(ACD_dict_float, orient='index')
DataFramePandas.to_csv("ACD.csv")
DataFramePandas = pd.DataFrame.from_dict(MSD_dict_float, orient='index')
DataFramePandas.to_csv("MSD.csv")
DataFramePandas = pd.DataFrame.from_dict(MinSD_dict_float, orient='index')
DataFramePandas.to_csv("MinSD.csv")
DataFramePandas = pd.DataFrame.from_dict(ASD_dict_float, orient='index')
DataFramePandas.to_csv("ASD.csv")
    
plt.plot(list(EmulatorTimeForLenght_float.keys()),list(EmulatorTimeForLenght_float.values()), color='b', linewidth=2,label="My emulator")
plt.title("Emulation Time",fontsize=20)
plt.xlabel("File lenght", fontsize=20)
plt.ylabel("Time [s]", fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("EmulatorTime.eps", format='eps')
plt.savefig("EmulatorTime.png", format='png')
plt.savefig("EmulatorTime.pdf", format='pdf')
plt.close()

plt.plot(list(QiskitTimeForLenght.keys()),list(QiskitTimeForLenght.values()), color='g', linewidth=2,label="Qiskit emulator state vector")
plt.title("Emulation Time",fontsize=20)
plt.xlabel("File lenght", fontsize=20)
plt.ylabel("Time [s]", fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("QiskitTime.eps", format='eps')
plt.savefig("QiskitTime.png", format='png')
plt.savefig("QiskitTime.pdf", format='pdf')
plt.close()


plt.plot(list(QiskitQASMTimeForLenght.keys()),list(QiskitQASMTimeForLenght.values()), color='r', linewidth=2,label="Qiskit emulator qasm")
plt.title("Emulation Time",fontsize=20)
plt.xlabel("File lenght", fontsize=20)
plt.ylabel("Time [s]", fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("QiskitQASMTime.eps", format='eps')
plt.savefig("QiskitQASMTime.png", format='png')
plt.savefig("QiskitQASMTime.pdf", format='pdf')
plt.close()

plt.plot(list(EmulatorTimeForLenght_float.keys()),list(EmulatorTimeForLenght_float.values()), color='b', linewidth=2,label="My emulator")
plt.plot(list(QiskitTimeForLenght.keys()),list(QiskitTimeForLenght.values()), color='g', linewidth=2,label="Qiskit emulator")
plt.plot(list(QiskitQASMTimeForLenght.keys()),list(QiskitQASMTimeForLenght.values()), color='r', linewidth=2,label="Qiskit emulator qasm")
plt.title("Emulation Time",fontsize=20)
plt.xlabel("File lenght", fontsize=20)
plt.ylabel("Time [s]", fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("ComparisonTime.eps", format='eps')
plt.savefig("ComparisonTime.png", format='png')
plt.savefig("ComparisonTime.pdf", format='pdf')
plt.close()






#fixed point, approximation mechanism and parallelism exploration
for approximation_mechanism in approximation_mechanisms:

    if not(approximation_mechanism in EmulatorTimeForLenght.keys()):  
        EmulatorTimeForLenght[approximation_mechanism] = {}
        kld_res_dict[approximation_mechanism] = {}
        HF_res_dict[approximation_mechanism] = {}
        MCD_dict[approximation_mechanism] = {}
        ACD_dict[approximation_mechanism] = {}
        MSD_dict[approximation_mechanism] = {}
        ASD_dict[approximation_mechanism] = {}
        MinSD_dict[approximation_mechanism] = {}
        RepetitionForLenght[approximation_mechanism] = {}    

    for parallelism in parallelisms: 

        if not(parallelism in EmulatorTimeForLenght[approximation_mechanism].keys()):  
            EmulatorTimeForLenght[approximation_mechanism][parallelism] = {}
            kld_res_dict[approximation_mechanism][parallelism] = {}
            HF_res_dict[approximation_mechanism][parallelism] = {}
            MCD_dict[approximation_mechanism][parallelism] = {}
            ACD_dict[approximation_mechanism][parallelism] = {}
            MSD_dict[approximation_mechanism][parallelism] = {}
            MinSD_dict[approximation_mechanism][parallelism] = {}
            ASD_dict[approximation_mechanism][parallelism] = {}
            RepetitionForLenght[approximation_mechanism][parallelism] = {}   
    
        pathOutputEmulator = "../../file/simulated_" + approximation_mechanisms_acronym[approximation_mechanism] + "_" + format(parallelism)  + "/"
    
        if not os.path.exists(pathOutputEmulator):
            os.makedirs(pathOutputEmulator)
            
        pathOutputQiskit = "../../file/qiskit_res/"
    
        if not os.path.exists(pathOutputQiskit):
            os.makedirs(pathOutputQiskit)
        
        pathEmulatorIstructions = "../../file/compiled_dec_" + approximation_mechanisms_acronym[approximation_mechanism] + "_" + format(parallelism)  + "/"



        for file in files:
            print("\n\execution of " + file + " with approximation mechanism " + approximation_mechanism + " and parallelism " + format(parallelism) + ":\n\n")
            qasm_file_path = path + file
            circuit = file[:-5]
            instruction_file_path = pathEmulatorIstructions +  circuit + "_compiled.qasm"
            sincos_file_path = pathEmulatorIstructions +  circuit + "_sincos.qasm"
            output_emulator_file_path = pathOutputEmulator +  circuit + ".txt"
            output_qiskit_file_path = pathOutputQiskit +  circuit + ".txt"
            
            f = open(instruction_file_path, "r") 
            
            qubit = int(f.readline().strip('\n'))
            print(qubit)
            lines = f.readlines()
            Lenght = len(lines)
            
            
            f.close()
            
            if qubit <= 16:
                
                verbose = False
                
                done = False
                timeVLSI = 0
                try:
                    timeVLSI = testVLSI(instruction_file_path, sincos_file_path, output_emulator_file_path, parallelism, approximation_mechanism, verbose)
                    print("Well done\n")
                    done = True
                except:
                    print("Problems\n")
                    done = False
                        
                if done:

                    print("The time employed by VLSIEmulator is: " + format(timeVLSI) + "\n")
                                               
                    #verify the results correctness
                    try:
                        f_emulator = open(output_emulator_file_path, "r")
                    except:
                        print("It is not possible to open the " + output_emulator_file_path + " file\n")
                        sys.exit(1)
                        
                    statevector = []
                    probabilityDensity = []
                    
                    lines = f_emulator.readlines()
                    
                    for line in lines:
                         val = line[:-1].split(" ")
                         if len(val) == 2:
                            real = float(val[0])/2**(parallelism-2)
                            img = float(val[1][:-1])/2**(parallelism-2)
                            z = complex(real, img)
                            statevector.append(z)
                            probability = real**2 + img**2  
                            probabilityDensity.append(probability)
                            
                    f_emulator.close()
                        

                    doneQiskit = True  
                    print("Read qiskit file\n")        
                        #verify the results correctness
                    try:
                        f_qiskit = open(output_qiskit_file_path, "r")
                    except:
                        print("It is not possible to open the " + output_qiskit_file_path + " file\n")
                        doneQiskit = False
                    if doneQiskit: 
                        if Lenght in EmulatorTimeForLenght[approximation_mechanism][parallelism].keys():
                            EmulatorTimeForLenght[approximation_mechanism][parallelism][Lenght] += timeVLSI
                            RepetitionForLenght[approximation_mechanism][parallelism][Lenght] += 1
                        else: 
                            EmulatorTimeForLenght[approximation_mechanism][parallelism][Lenght] = timeVLSI
                            RepetitionForLenght[approximation_mechanism][parallelism][Lenght] = 1
                        statevectorQiskit = []
                        probabilityDensityQiskit = []
                    
                        lines = f_qiskit.readlines()
                    
                        for line in lines:
                            z = complex(line[:-1])
                            statevectorQiskit.append(z)
                            probability = z.real**2 + z.imag**2  
                            probabilityDensityQiskit.append(probability)
                            
                        f_qiskit.close()

                        print("Figure of merit evaluation\n")
                    
                        kld_res = KLD(probabilityDensityQiskit, probabilityDensity)
                    
                        print("The divergence is equal to: " + format(kld_res) + "\n")
                    
                    
                        if kld_res > 0.05:
                            fileErrors.write("The circuit " + circuit + " presents a too high divergence, i.e., equal to: " + format(kld_res) +  "\n")
                        
                        HF = HeligerFidelity(probabilityDensityQiskit, probabilityDensity)
                    
                        print("The Helinger fidelity is equal to: " + format(HF) + "\n")
                    
                    
                        if HF < 0.95:
                            fileErrors.write("The circuit " + circuit + " presents a too low Helinger Fidelity, i.e., equal to: " + format(HF) +  "\n")
                        
                        MCD = MaximumComplexDistance(statevectorQiskit, statevector)
                    
                        print("The maximum complex distance is equal to: " + format(MCD) + "\n")
                    
                        ACD = AverageComplexDistance(statevectorQiskit, statevector)
                    
                        print("The average complex distance is equal to: " + format(ACD) + "\n")
                        
                        MinSD, MSD, ASD = MaximumSphereDistance(statevectorQiskit, statevector)
                    
                        if Lenght in kld_res_dict[approximation_mechanism][parallelism].keys():
                            kld_res_dict[approximation_mechanism][parallelism][Lenght] += kld_res
                            HF_res_dict[approximation_mechanism][parallelism][Lenght] += HF
                            MCD_dict[approximation_mechanism][parallelism][Lenght] += MCD
                            ACD_dict[approximation_mechanism][parallelism][Lenght] += ACD
                            MSD_dict[approximation_mechanism][parallelism][Lenght] += MSD
                            MinSD_dict[approximation_mechanism][parallelism][Lenght] += MinSD
                            ASD_dict[approximation_mechanism][parallelism][Lenght] += ASD
                        else: 
                            kld_res_dict[approximation_mechanism][parallelism][Lenght] = kld_res
                            HF_res_dict[approximation_mechanism][parallelism][Lenght] = HF
                            MCD_dict[approximation_mechanism][parallelism][Lenght] = MCD
                            ACD_dict[approximation_mechanism][parallelism][Lenght] = ACD
                            MSD_dict[approximation_mechanism][parallelism][Lenght] = MSD
                            MinSD_dict[approximation_mechanism][parallelism][Lenght] = MinSD
                            ASD_dict[approximation_mechanism][parallelism][Lenght] = ASD
                    
                        label = []
                        for i in range(len(probabilityDensity)):
                            label.append(format(i, 'b').zfill(int(math.log2(len(probabilityDensity)))))
                    
                        if len(probabilityDensity) < 33:
                            barWidth = 0.25
                            br1 = np.arange(len(probabilityDensity))
                            br2 = [x + barWidth for x in br1]
                            plt.bar(br1, probabilityDensity, color ='r', width = barWidth, edgecolor ='grey', label ='Emulator')
                            plt.bar(br2, probabilityDensityQiskit, color ='g', width = barWidth, edgecolor ='grey', label ='Qiskit')
                            plt.xticks([r + barWidth for r in range(len(probabilityDensity))],label)
                            plt.xlabel("Basis State", fontsize=20)
                            plt.ylabel("Probability", fontsize=20)
                            leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
                            leg.get_frame().set_facecolor('white')
                            plt.savefig("../../file/probabilityBarPlot/" + circuit + "_" + approximation_mechanism + "_" +format(parallelism) + ".eps", format='eps')
                            plt.savefig("../../file/probabilityBarPlot/" + circuit + "_" + approximation_mechanism + "_" +format(parallelism) +".png", format='png')
                            plt.savefig("../../file/probabilityBarPlot/" + circuit + "_" + approximation_mechanism + "_" +format(parallelism) +".pdf", format='pdf')
                            plt.close()                       
																																																																																																																																																																																																																																																																																																																																																																																																	
                else:
                    print("My solver cannot simulate the file\n")   
            else:
                print("Too large problem to be simulated in software\n")
           
                
                
                
    
print("Finish")  

listofcolors=list(mpl.colormaps)

for approximation_mechanism in approximation_mechanisms:
    for parallelism in parallelisms:
        EmulatorTimeForLenght[approximation_mechanism][parallelism] = dict(sorted(EmulatorTimeForLenght[approximation_mechanism][parallelism].items()))
        kld_res_dict[approximation_mechanism][parallelism] = dict(sorted(kld_res_dict[approximation_mechanism][parallelism].items()))
        HF_res_dict[approximation_mechanism][parallelism] = dict(sorted(HF_res_dict[approximation_mechanism][parallelism].items()))
        MCD_dict[approximation_mechanism][parallelism] = dict(sorted(MCD_dict[approximation_mechanism][parallelism].items()))
        ACD_dict[approximation_mechanism][parallelism] = dict(sorted(ACD_dict[approximation_mechanism][parallelism].items()))
        MSD_dict[approximation_mechanism][parallelism] = dict(sorted(MSD_dict[approximation_mechanism][parallelism].items()))
        MinSD_dict[approximation_mechanism][parallelism] = dict(sorted(MinSD_dict[approximation_mechanism][parallelism].items()))        
        ASD_dict[approximation_mechanism][parallelism] = dict(sorted(ASD_dict[approximation_mechanism][parallelism].items()))
        RepetitionForLenght[approximation_mechanism][parallelism] = dict(sorted(RepetitionForLenght[approximation_mechanism][parallelism].items())) 
        for key in EmulatorTimeForLenght[approximation_mechanism][parallelism].keys():
            EmulatorTimeForLenght[approximation_mechanism][parallelism][key] = EmulatorTimeForLenght[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
            kld_res_dict[approximation_mechanism][parallelism][key] = kld_res_dict[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
            HF_res_dict[approximation_mechanism][parallelism][key] = HF_res_dict[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
            MCD_dict[approximation_mechanism][parallelism][key] = MCD_dict[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
            ACD_dict[approximation_mechanism][parallelism][key] = ACD_dict[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
            MSD_dict[approximation_mechanism][parallelism][key] = MSD_dict[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
            MinSD_dict[approximation_mechanism][parallelism][key] = MinSD_dict[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
            ASD_dict[approximation_mechanism][parallelism][key] = ASD_dict[approximation_mechanism][parallelism][key]/RepetitionForLenght[approximation_mechanism][parallelism][key]
    
    DataFramePandas = pd.DataFrame.from_dict(EmulatorTimeForLenght[approximation_mechanism])
    DataFramePandas.to_csv("Time_"+ approximation_mechanism +".csv")
    DataFramePandas = pd.DataFrame.from_dict(kld_res_dict[approximation_mechanism])
    DataFramePandas.to_csv("kld_"+ approximation_mechanism +".csv")
    DataFramePandas = pd.DataFrame.from_dict(HF_res_dict[approximation_mechanism])
    DataFramePandas.to_csv("HF_"+ approximation_mechanism +".csv")
    DataFramePandas = pd.DataFrame.from_dict(MCD_dict[approximation_mechanism])
    DataFramePandas.to_csv("MCD_"+ approximation_mechanism +".csv")
    DataFramePandas = pd.DataFrame.from_dict(ACD_dict[approximation_mechanism])
    DataFramePandas.to_csv("ACD_"+ approximation_mechanism +".csv")
    DataFramePandas = pd.DataFrame.from_dict(MSD_dict[approximation_mechanism])
    DataFramePandas.to_csv("MSD_"+ approximation_mechanism +".csv")
    DataFramePandas = pd.DataFrame.from_dict(MinSD_dict[approximation_mechanism])
    DataFramePandas.to_csv("MinSD_"+ approximation_mechanism +".csv")
    DataFramePandas = pd.DataFrame.from_dict(ASD_dict[approximation_mechanism])
    DataFramePandas.to_csv("ASD_"+ approximation_mechanism +".csv")

    i = 0 
    for parallelism in parallelisms:
        plt.plot(list(EmulatorTimeForLenght[approximation_mechanism][parallelism].keys()),list(EmulatorTimeForLenght[approximation_mechanism][parallelism].values()), color=listofcolors[i], linewidth=2,label=format(parallelism)+" bits") 
        i +=1
    plt.title("Emulation Time",fontsize=20)
    plt.xlabel("File lenght", fontsize=20)
    plt.ylabel("Time [s]", fontsize=20)
    leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
    leg.get_frame().set_facecolor('white')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("EmulatorTime_" + approximation_mechanism + ".eps", format='eps')
    plt.savefig("EmulatorTime_" + approximation_mechanism + ".png", format='png')
    plt.savefig("EmulatorTime_" + approximation_mechanism + ".pdf", format='pdf')
    plt.close() 

    i = 0 
    for parallelism in parallelisms:
        plt.plot(list(HF_res_dict[approximation_mechanism][parallelism].keys()),list(HF_res_dict[approximation_mechanism][parallelism].values()), color=listofcolors[i], linewidth=2,label=format(parallelism)+" bits")
        i += 1
    plt.axhline(y = 0.95, color = 'r', linewidth=3,  linestyle = '--')     
    pt.fill_between(x,0.95, 1, alpha=0.2, color='r')  
    plt.xlim([0, 1])    
    plt.title("Fidelity",fontsize=20)
    plt.xlabel("File lenght", fontsize=20)
    plt.ylabel("Fidelity", fontsize=20)
    leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
    leg.get_frame().set_facecolor('white')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("HF_" + approximation_mechanism + ".eps", format='eps')
    plt.savefig("HF_" + approximation_mechanism + ".png", format='png')
    plt.savefig("HF_" + approximation_mechanism + ".pdf", format='pdf')
    plt.close()    

    i = 0 
    for parallelism in parallelisms:
        plt.plot(list(kld_res_dict[approximation_mechanism][parallelism].keys()),list(kld_res_dict[approximation_mechanism][parallelism].values()), color=listofcolors[i], linewidth=2,label=format(parallelism)+" bits")   
        i += 1
    plt.axhline(y = 0.05, color = 'r', linewidth=3,  linestyle = '--')   
    pt.fill_between(x,0, 0.05, alpha=0.2, color='r') 
    plt.xlim([0, 1])     
    plt.title("kld",fontsize=20)
    plt.xlabel("File lenght", fontsize=20)
    plt.ylabel("kld", fontsize=20)
    leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
    leg.get_frame().set_facecolor('white')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("Kld_" + approximation_mechanism + ".eps", format='eps')
    plt.savefig("Kld_" + approximation_mechanism + ".png", format='png')
    plt.savefig("Kld_" + approximation_mechanism + ".pdf", format='pdf')
    plt.close() 

    i = 0 
    for parallelism in parallelisms:
        plt.plot(list(MCD_dict[approximation_mechanism][parallelism].keys()),list(MCD_dict[approximation_mechanism][parallelism].values()), color=listofcolors[i], linewidth=2,label=format(parallelism)+" bits")   
        i += 1
    plt.axhline(y = 0.05, color = 'r', linewidth=3,  linestyle = '--')  
    pt.fill_between(x,0, 0.05, alpha=0.2, color='r')    
    plt.xlim([0, 1])     
    plt.title("Maximum complex distance",fontsize=20)
    plt.xlabel("File lenght", fontsize=20)
    plt.ylabel("Maximum complex distance", fontsize=20)
    leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
    leg.get_frame().set_facecolor('white')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("MCD_" + approximation_mechanism + ".eps", format='eps')
    plt.savefig("MCD_" + approximation_mechanism + ".png", format='png')
    plt.savefig("MCD_" + approximation_mechanism + ".pdf", format='pdf')
    plt.close()  

    i = 0 
    for parallelism in parallelisms:
        plt.plot(list(ACD_dict[approximation_mechanism][parallelism].keys()),list(ACD_dict[approximation_mechanism][parallelism].values()), color=listofcolors[i], linewidth=2,label=format(parallelism)+" bits")   
        i += 1
    plt.axhline(y = 0.05, color = 'r', linewidth=3,  linestyle = '--')  
    pt.fill_between(x,0, 0.05, alpha=0.2, color='r')    
    plt.xlim([0, 1])     
    plt.title("Average complex distance",fontsize=20)
    plt.xlabel("File lenght", fontsize=20)
    plt.ylabel("Average complex distance", fontsize=20)
    leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
    leg.get_frame().set_facecolor('white')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.savefig("ACD_" + approximation_mechanism + ".eps", format='eps')
    plt.savefig("ACD_" + approximation_mechanism + ".png", format='png')
    plt.savefig("ACD_" + approximation_mechanism + ".pdf", format='pdf')
    plt.close()     



      
   
     
