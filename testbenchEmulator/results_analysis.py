import os
import sys
import math

import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import numpy as np
plt.rcParams.update({'font.size': 20})

def KLD(qiskitProbabilityDistributions, VLSIProbabilityDistributions):
    D = 0
    for i in range(len(qiskitProbabilityDistributions)):
        if VLSIProbabilityDistributions[i] != 0 and qiskitProbabilityDistributions[i] != 0:
            D += qiskitProbabilityDistributions[i] * math.log(
                qiskitProbabilityDistributions[i] / VLSIProbabilityDistributions[i])
    return abs(D)


def HeligerFidelity(qiskitProbabilityDistributions, VLSIProbabilityDistributions):
    temp = 0
    for i in range(len(qiskitProbabilityDistributions)):
        temp += (math.sqrt(qiskitProbabilityDistributions[i]) - math.sqrt(VLSIProbabilityDistributions[i])) ** 2
    H = (1 / math.sqrt(2)) * math.sqrt(temp)
    F = (1 - H ** 2) ** 2
    return F


def MaximumComplexDistance(qiskitStateVector, VLSIStateVector):
    maxDistance = 0
    for i in range(len(qiskitStateVector)):
        diff = math.sqrt((qiskitStateVector[i].real - VLSIStateVector[i].real) ** 2 + (
                    qiskitStateVector[i].imag - VLSIStateVector[i].imag) ** 2)
        if diff > maxDistance:
            maxDistance = diff
    return maxDistance


def AverageComplexDistance(qiskitStateVector, VLSIStateVector):
    AverageDistance = 0
    for i in range(len(qiskitStateVector)):
        AverageDistance += math.sqrt((qiskitStateVector[i].real - VLSIStateVector[i].real) ** 2 + (
                    qiskitStateVector[i].imag - VLSIStateVector[i].imag) ** 2)
    return AverageDistance / len(qiskitStateVector)
# LaTeX settings for matplotlib
rc('text', usetex=True)
plt.rc('text', usetex=True)

rc('text', usetex=True)
plt.rc('text', usetex=True)

kld_res_dict = {}
HF_res_dict = {}
MCD_dict = {}
ACD_dict = {}
RepetitionForLenght = {}

# Floating point
pathEmulatorIstructions = "../file/compiled_mqt_sim/"
pathEmulatorIstructionsRef = "../file/compiled_mqt_dec/"
pathOutputEmulator = "../file/simulated_mqt_vhdl/"
pathOutputQiskit = "../file/qiskit_res_mqt/"
path = "../file/MQTBench_input/"
files = os.listdir(pathOutputEmulator)
for file in files:
    print("\n\execution of " + file + ":\n\n")
    name_circuit = file[:-10]
    instruction_file_path = pathEmulatorIstructions + name_circuit + "_compiled.qasm"
    qasm_file = path + name_circuit + ".qasm"
    f = open(instruction_file_path, "r")
    lines = f.readlines()
    Lenght = len(lines)
    f.close()

    if Lenght in RepetitionForLenght.keys():
        RepetitionForLenght[Lenght] += 1
    else:
        RepetitionForLenght[Lenght] = 1


    # verify the results correctness
    try:
        f_emulator = open(pathOutputEmulator + file, "r")
    except:
        print("It is not possible to open the " + pathOutputEmulator + file + " file\n")
        sys.exit()

    statevector = []
    probabilityDensity = []

    lines = f_emulator.readlines()
    for line in lines:
        val = line[:-1].split(" ")
        if len(val) == 2:
            real = (-2**1)*int(val[0][0])
            real += (2**0)*int(val[0][1])
            power = -1
            for i in range(2, len(val[0])):
                real += int(val[0][i]) * (2 ** power)
                power -= 1

            img = (-2**1)*int(val[1][0])
            img += (2**0)*int(val[1][1])
            power = -1
            for i in range(2, len(val[1])):
                img += int(val[1][i]) * (2 ** power)
                power -= 1

            z = complex(real, img)
            statevector.append(z)
            probability = real ** 2 + img ** 2
            probabilityDensity.append(probability)

    f_emulator.close()

    print("Read qiskit file\n")
    # verify the results correctness
    try:
        f_qiskit = open(pathOutputQiskit + name_circuit + ".txt", "r")
    except:
        print("It is not possible to open the " + pathOutputQiskit + name_circuit + ".txt" + " file\n")
        sys.exit()

    statevectorQiskit = []
    probabilityDensityQiskit = []

    lines = f_qiskit.readlines()

    for line in lines:
        z = complex(line[:-1])
        statevectorQiskit.append(z)
        probability = z.real ** 2 + z.imag ** 2
        probabilityDensityQiskit.append(probability)

    f_qiskit.close()

    print("Figure of merit evaluation\n")

    kld_res = KLD(probabilityDensityQiskit, probabilityDensity)

    print("The divergence is equal to: " + format(kld_res) + "\n")

    HF = HeligerFidelity(probabilityDensityQiskit, probabilityDensity)

    print("The Helinger fidelity is equal to: " + format(HF) + "\n")

    MCD = MaximumComplexDistance(statevectorQiskit, statevector)

    print("The maximum complex distance is equal to: " + format(MCD) + "\n")

    ACD = AverageComplexDistance(statevectorQiskit, statevector)

    print("The average complex distance is equal to: " + format(ACD) + "\n")

    if Lenght in kld_res_dict.keys():
        kld_res_dict[Lenght] += kld_res
        HF_res_dict[Lenght] += HF
        MCD_dict[Lenght] += MCD
        ACD_dict[Lenght] += ACD
    else:
        kld_res_dict[Lenght] = kld_res
        HF_res_dict[Lenght] = HF
        MCD_dict[Lenght] = MCD
        ACD_dict[Lenght] = ACD

    label = []
    for i in range(len(probabilityDensity)):
        label.append(format(i, 'b').zfill(int(math.log2(len(probabilityDensity)))))

    if len(probabilityDensity) < 33:
        barWidth = 0.5
        br1 = np.arange(len(probabilityDensity))
        br2 = [x + barWidth for x in br1]
        plt.bar(br1, probabilityDensityQiskit, color='r', width=barWidth,  label=r'\textit{State Vector Simulator}')
        plt.bar(br2, probabilityDensity, color='g', width=barWidth, label=r'\textit{Emulator}')
        plt.xticks([r + barWidth for r in range(len(probabilityDensity))], label)
        plt.xlabel(r'\textbf{Basis State}', fontsize=20)
        plt.ylabel(r'\textbf{Probability}', fontsize=20)
        leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
        leg.get_frame().set_facecolor('white')
        plt.savefig("../file/probabilityBarPlot_mqt_vhd/" + name_circuit + ".eps", format='eps', bbox_inches='tight')
        plt.savefig("../file/probabilityBarPlot_mqt_vhd/" + name_circuit + ".png", format='png', bbox_inches='tight')
        plt.savefig("../file/probabilityBarPlot_mqt_vhd/" + name_circuit + ".pdf", format='pdf', bbox_inches='tight')
        plt.close()

kld_res_dict = dict(sorted(kld_res_dict.items()))
HF_res_dict = dict(sorted(HF_res_dict.items()))
MCD_dict = dict(sorted(MCD_dict.items()))
ACD_dict = dict(sorted(ACD_dict.items()))
RepetitionForLenght = dict(sorted(RepetitionForLenght.items()))
for key in kld_res_dict.keys():
    kld_res_dict[key] = kld_res_dict[key] / RepetitionForLenght[key]
    HF_res_dict[key] = HF_res_dict[key] / RepetitionForLenght[key]
    MCD_dict[key] = MCD_dict[key] / RepetitionForLenght[key]
    ACD_dict[key] = ACD_dict[key] / RepetitionForLenght[key]

print(kld_res_dict)
DataFramePandas = pd.DataFrame.from_dict(kld_res_dict,  orient='index')
DataFramePandas.to_csv("kld_mqt.csv")
DataFramePandas = pd.DataFrame.from_dict(HF_res_dict,  orient='index')
DataFramePandas.to_csv("HF_mqt.csv")
DataFramePandas = pd.DataFrame.from_dict(MCD_dict,  orient='index')
DataFramePandas.to_csv("MCD_mqt.csv")
DataFramePandas = pd.DataFrame.from_dict(ACD_dict,  orient='index')
DataFramePandas.to_csv("ACD_mqt.csv")

plt.plot(kld_res_dict.keys(), kld_res_dict.values(), linewidth=4, label=r'\textit{KLD}')
plt.plot(HF_res_dict.keys(), HF_res_dict.values(), label=r'\textit{HF}')
plt.plot(MCD_dict.keys(), MCD_dict.values(), linewidth=3, label=r'\textit{MCD}')
plt.plot(ACD_dict.keys(), ACD_dict.values(), label=r'\textit{ACD}')
plt.xlabel(r'\textit{$N_g$}', fontsize=20)
plt.axhline(y=0.95, color='r', linewidth=3, linestyle='--')
plt.fill_between(kld_res_dict.keys(),0.05 , 0.95, alpha=0.2, color='r')
plt.axhline(y=0.05, color='r', linewidth=3, linestyle='--')
leg = plt.legend(loc='center right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("vhd_res_mqt.eps", format='eps',bbox_inches='tight')
plt.savefig("vhd_res_mqt.png", format='png',bbox_inches='tight')
plt.savefig("vhd_res_mqt.pdf", format='pdf', bbox_inches='tight')
plt.close()