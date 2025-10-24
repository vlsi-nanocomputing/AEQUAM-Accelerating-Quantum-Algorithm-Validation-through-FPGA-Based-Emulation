import os
import sys
import time
import numpy as np
from qiskit import BasicAer
from qiskit.execute_function import execute
from qiskit import QuantumCircuit
import time
sys.path.insert(0, r'./floating_point')
from VLSIEmulator import EmulatorWrap 
import math
import cmath
from utiles import testVLSI, testQiskit, KLD, HeligerFidelity, MaximumComplexDistance, AverageComplexDistance
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import cm

rc('text', usetex=True)
plt.rc('text', usetex=True)

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
QiskitTimeForLenght = {}
RepetitionsForLenghtEmulator = {}
RepetitionsForLenghtQiskit = {}    


pathEmulatorIstructions = "../../file/compiled_dec/"
pathOutputEmulator = "../../file/simulated/"
pathOutputQiskit = "../../file/qiskit_res/"
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
            if Lenght in EmulatorTimeForLenght.keys():
                EmulatorTimeForLenght[Lenght] += timeVLSI
                RepetitionsForLenghtEmulator[Lenght] += 1
            else: 
                EmulatorTimeForLenght[Lenght] = timeVLSI
                RepetitionsForLenghtEmulator[Lenght] = 1

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

            #timeQiskit=testQiskit(qasm_file_path, output_qiskit_file_path)
            if done == True:
                print("The time employed by Qiskit state vector is: " + format(timeQiskit) + "\n")
                
                
                if Lenght in QiskitTimeForLenght.keys():
                    QiskitTimeForLenght[Lenght] += timeQiskit
                    RepetitionsForLenghtQiskit[Lenght] += 1
                else: 
                    QiskitTimeForLenght[Lenght] = timeQiskit
                    RepetitionsForLenghtQiskit[Lenght] = 1
                    
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
                    plt.xlabel(r'\textit{Basis State}', fontsize=20)
                    plt.ylabel(r'\textit{Probability}', fontsize=20)
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
    
print("Finish")      
EmulatorTimeForLenght = dict(sorted(EmulatorTimeForLenght.items()))          
QiskitTimeForLenght = dict(sorted(QiskitTimeForLenght.items()))
RepetitionsForLenghtEmulator = dict(sorted(RepetitionsForLenghtEmulator.items()))          
RepetitionsForLenghtQiskit = dict(sorted(RepetitionsForLenghtQiskit.items())) 
for key in EmulatorTimeForLenght.keys():
    EmulatorTimeForLenght[key] = EmulatorTimeForLenght[key]/RepetitionsForLenghtEmulator[key]
    
for key in QiskitTimeForLenght.keys():
    QiskitTimeForLenght[key] = QiskitTimeForLenght[key]/RepetitionsForLenghtQiskit[key]
    

plt.plot(list(EmulatorTimeForLenght.keys()),list(EmulatorTimeForLenght.values()), color='b', linewidth=2,label=r'\textit{My emulator}')
plt.title(r'\textbf{Emulation Time}',fontsize=20)
plt.xlabel(r'\textit{File lenght}', fontsize=20)
plt.ylabel(r'\textit{Time [s]}', fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("EmulatorTime.eps", format='eps')
plt.savefig("EmulatorTime.png", format='png')
plt.savefig("EmulatorTime.pdf", format='pdf')
plt.close()

plt.plot(list(QiskitTimeForLenght.keys()),list(QiskitTimeForLenght.values()), color='g', linewidth=2,label=r'\textit{Qiskit emulator}')
plt.title(r'\textbf{Emulation Time}',fontsize=20)
plt.xlabel(r'\textit{File lenght}', fontsize=20)
plt.ylabel(r'\textit{Time [s]}', fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("QiskitTime.eps", format='eps')
plt.savefig("QiskitTime.png", format='png')
plt.savefig("QiskitTime.pdf", format='pdf')
plt.close()

plt.plot(list(EmulatorTimeForLenght.keys()),list(EmulatorTimeForLenght.values()), color='b', linewidth=2,label=r'\textit{My emulator}')
plt.plot(list(QiskitTimeForLenght.keys()),list(QiskitTimeForLenght.values()), color='g', linewidth=2,label=r'\textit{Qiskit emulator}')
plt.title(r'\textbf{Emulation Time}',fontsize=20)
plt.xlabel(r'\textit{File lenght}', fontsize=20)
plt.ylabel(r'\textit{Time [s]}', fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("ComparisonTime.eps", format='eps')
plt.savefig("ComparisonTime.png", format='png')
plt.savefig("ComparisonTime.pdf", format='pdf')
plt.close()



      
   
     
