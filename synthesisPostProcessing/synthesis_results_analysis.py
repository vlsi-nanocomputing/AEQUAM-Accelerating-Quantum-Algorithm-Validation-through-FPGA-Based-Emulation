import os
import sys
import math

import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import numpy as np
import matplotlib.ticker as mticker
plt.rcParams.update({'font.size': 20})
rc('text', usetex=True)
plt.rc('text', usetex=True)
dataList = [
        ['[14]' , [[2,965],[3,28980],[4,97574],[5,350230]]],
        ['[15]' , [[2,94104],[3,197524],[4,374021]]],
        ['[16]' , [[2,42000],[3,42000],[4,42000],[5,42000],[6,42000],[7,42000],[8,42000],[9,42000],[10,42000],[11,42000],[12,42000],[13,42000],[14,42000],[15,42000]]],
        ['[17]', [[3, 150], [4, 230], [5, 573], [6, 905], [8, 4019]]],
]


files = os.listdir("Res/")
N_target = 5
Q_target = 4
W_target = 0
dict_varying_W = {}
dict_varying_Q = {}
dict_serial = {}
dict_parallel = {}
dict_windowing = {}

for file in files:
    if file.endswith(".csv"):
        fields = file[:-4].split("_")
        N = int(fields[2])
        W = int(fields[4])
        S = int(fields[6])
        Q = int(fields[8])
        df = pd.read_csv("Res/" + file).to_dict()
        keys_d = list(df['Unnamed: 0'].values())
        values_d = list(df[format(N) + "_" + format(W) + "_" + format(S) + "_" + format(Q)].values())
        if N == N_target and Q == Q_target:
            for i in range(len(keys_d)):
                if keys_d[i] not in dict_varying_W:
                    dict_varying_W[keys_d[i]] = {}
                dict_varying_W[keys_d[i]][W] = values_d[i]
        if N == N_target and W == W_target:
            for i in range(len(keys_d)):
                if keys_d[i] not in dict_varying_Q:
                    dict_varying_Q[keys_d[i]] = {}
                dict_varying_Q[keys_d[i]][Q] = values_d[i]
        if W == 0 and Q == Q_target:
            for i in range(len(keys_d)):
                if keys_d[i] not in dict_parallel:
                    dict_parallel[keys_d[i]] = {}
                dict_parallel[keys_d[i]][N] = values_d[i]
        if W == N-1 and Q == Q_target:
            for i in range(len(keys_d)):
                if keys_d[i] not in dict_serial:
                    dict_serial[keys_d[i]] = {}
                dict_serial[keys_d[i]][N] = values_d[i]
        if Q == Q_target and not W == 0 and not W == N-1:
            if W not in dict_windowing:
                dict_windowing[W] = {}
            dict_windowing[W][N] = values_d[0]


plt.plot(list(dict_varying_W['LogicElements'].keys()), list(dict_varying_W['LogicElements'].values()), linewidth=1.5, label=r'\textit{LE}')
plt.plot(list(dict_varying_W['Registers'].keys()), list(dict_varying_W['Registers'].values()), linewidth=1.5, label=r'\textit{REG}')
#plt.axhline(y = 32070, color = 'r', linewidth=4.0, linestyle = '-')
plt.yscale('log')
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{W}', fontsize=20)
#plt.ylabel(r'Number of logic elements', fontsize=20)
plt.savefig("AreaVaryingW.pdf", format='pdf',  bbox_inches='tight',)
plt.close()

plt.plot(list(dict_varying_W['TotalPower'].keys()), list(dict_varying_W['TotalPower'].values()), linewidth=1.5, label=r'\textit{Tot P}')
plt.plot(list(dict_varying_W['DynamicPower'].keys()), list(dict_varying_W['DynamicPower'].values()), linewidth=1.5,  label=r'\textit{DP}')
plt.plot(list(dict_varying_W['StaticPower'].keys()), list(dict_varying_W['StaticPower'].values()), linewidth=1.5,  label=r'\textit{SP}')
#plt.axhline(y = 32070, color = 'r', linewidth=4.0, linestyle = '-')
#plt.yscale('log')
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{W}', fontsize=20)
plt.ylabel(r'\textbf{Power [mWatt]}', fontsize=20)
plt.savefig("PowerVaryingW.pdf", format='pdf',  bbox_inches='tight',)
plt.close()

plt.plot(list(dict_varying_Q['LogicElements'].keys()), list(dict_varying_Q['LogicElements'].values()), linewidth=1.5, label=r'\textit{LE}')
plt.plot(list(dict_varying_Q['Registers'].keys()), list(dict_varying_Q['Registers'].values()), linewidth=1.5, label=r'\textit{REG}')
#plt.axhline(y = 32070, color = 'r', linewidth=4.0, linestyle = '-')
plt.yscale('log')
leg = plt.legend(loc='upper left', frameon=True, fontsize=15)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{Q}', fontsize=20)
#plt.ylabel(r'Number of logic elements', fontsize=20)
plt.savefig("AreaVaryingQ.pdf", format='pdf',  bbox_inches='tight',)
plt.close()

plt.plot(list(dict_varying_Q['TotalPower'].keys()), list(dict_varying_Q['TotalPower'].values()), linewidth=1.5, label=r'\textit{Tot P}')
plt.plot(list(dict_varying_Q['DynamicPower'].keys()), list(dict_varying_Q['DynamicPower'].values()), linewidth=1.5,  label=r'\textit{DP}')
plt.plot(list(dict_varying_Q['StaticPower'].keys()), list(dict_varying_Q['StaticPower'].values()), linewidth=1.5,  label=r'\textit{SP}')
#plt.axhline(y = 32070, color = 'r', linewidth=4.0, linestyle = '-')
#plt.yscale('log')
leg = plt.legend(loc='upper left', frameon=True, fontsize=15)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{Q}', fontsize=20)
plt.ylabel(r'\textbf{Power [mWatt]}', fontsize=20)
plt.savefig("PowerVaryingQ.pdf", format='pdf',  bbox_inches='tight',)
plt.close()


plt.plot(list(dict_serial['LogicElements'].keys()), list(dict_serial['LogicElements'].values()), linewidth=1.5, label=r'\textit{LE Serial}')
plt.plot(list(dict_serial['Registers'].keys()), list(dict_serial['Registers'].values()), linewidth=1.5, label=r'\textit{REG Serial}')
plt.plot(list(dict_parallel['LogicElements'].keys()), list(dict_parallel['LogicElements'].values()), linewidth=1.5, label=r'\textit{LE Parallel}')
plt.plot(list(dict_parallel['Registers'].keys()), list(dict_parallel['Registers'].values()), linewidth=1.5, label=r'\textit{REG Parallel}')
for w in dict_windowing.keys():
    plt.plot(list(dict_windowing[w].keys()), list(dict_windowing[w].values()), 'c^',  linewidth=1.5)
#plt.axhline(y = 32070, color = 'r', linewidth=4.0, linestyle = '-')
plt.yscale('log')
leg = plt.legend(loc='upper left', frameon=True, fontsize=15)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{$N_q$}', fontsize=20)
#plt.ylabel(r'Number of logic elements', fontsize=20)
plt.savefig("AreaVaryingN.pdf", format='pdf',  bbox_inches='tight',)
plt.close()

plt.plot(list(dict_serial['Frequency'].keys()), list(dict_serial['Frequency'].values()), linewidth=1.5, label=r'\textit{AEQUAM Serial}')
plt.plot(list(dict_parallel['Frequency'].keys()), list(dict_parallel['Frequency'].values()), linewidth=1.5, label=r'\textit{AEQUAM Parallel}')
#plt.axhline(y = 32070, color = 'r', linewidth=4.0, linestyle = '-')
#plt.yscale('log')
leg = plt.legend(loc='lower left', frameon=True, fontsize=15)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{$N_q$}', fontsize=20)
plt.ylabel(r'\textbf{Frequency [MHz]}', fontsize=20)
plt.savefig("FrequencyVaryingN.pdf", format='pdf',  bbox_inches='tight',)
plt.close()

plt.plot(list(dict_serial['TotalPower'].keys()), list(dict_serial['TotalPower'].values()), linewidth=1.5, label=r'\textit{Tot P Serial}')
plt.plot(list(dict_serial['DynamicPower'].keys()), list(dict_serial['DynamicPower'].values()), linewidth=1.5,  label=r'\textit{DP Serial}')
plt.plot(list(dict_serial['StaticPower'].keys()), list(dict_serial['StaticPower'].values()), linewidth=1.5,  label=r'\textit{SP Serial}')
plt.plot(list(dict_parallel['TotalPower'].keys()), list(dict_parallel['TotalPower'].values()), linewidth=1.5, label=r'\textit{Tot P Parallel}')
plt.plot(list(dict_parallel['DynamicPower'].keys()), list(dict_parallel['DynamicPower'].values()), linewidth=1.5,  label=r'\textit{DP Parallel}')
plt.plot(list(dict_parallel['StaticPower'].keys()), list(dict_parallel['StaticPower'].values()), linewidth=1.5,  label=r'\textit{SP Parallel}')
#plt.axhline(y = 32070, color = 'r', linewidth=4.0, linestyle = '-')
#plt.yscale('log')
leg = plt.legend(loc='upper left', frameon=True, fontsize=15)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{$N_q$}', fontsize=20)
plt.ylabel(r'\textbf{Power [mWatt]}', fontsize=20)
plt.savefig("PowerVaryingN.pdf", format='pdf',  bbox_inches='tight',)
plt.close()

plt.plot(list(dict_serial['LogicElements'].keys()), list(dict_serial['LogicElements'].values()), linewidth=1.5, label=r'\textit{AEQUAM Serial}')
plt.plot(list(dict_parallel['LogicElements'].keys()), list(dict_parallel['LogicElements'].values()), linewidth=1.5, label=r'\textit{AEQUAM Parallel}')
for w in dict_windowing.keys():
    plt.plot(list(dict_windowing[w].keys()), list(dict_windowing[w].values()), 'c^',  linewidth=1.5)
for i in range(len(dataList)):
    plt.plot([x[0] for x in dataList[i][1]], [x[1] for x in dataList[i][1]], linewidth=1.5, label=r'\textit{' + dataList[i][0] + '}')
plt.yscale('log')
leg = plt.legend(loc='lower right', frameon=True, fontsize=10)
plt.gca().xaxis.set_major_locator(mticker.MultipleLocator(1))
plt.xlabel(r'\textbf{$N_q$}', fontsize=20)
plt.ylabel(r'\textbf{LE}', fontsize=20)
plt.savefig("AreaComparison.pdf", format='pdf',  bbox_inches='tight',)
plt.close()