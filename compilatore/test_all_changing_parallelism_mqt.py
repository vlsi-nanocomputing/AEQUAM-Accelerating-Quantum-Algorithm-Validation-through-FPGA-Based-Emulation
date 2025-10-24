import os
import sys
import time
from utils_f import translator
from ortography_control import *
from gate_substitution import *
from extension import *
from mapping import *
import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.pyplot import cm

rc('text', usetex=True)
plt.rc('text', usetex=True)

configuration_file_name = '../configurazione/emulator_configuration.txt'

approximation_mechanisms = ['nearest', 'nearest_even', 'truncation']

approximation_mechanisms_acronym = {'nearest': 'n', 'nearest_even': 'ne', 'truncation': 't'}

parallelisms =range(8, 33,2)


print("Start compilation of all the files\n")

  

path = "../file/MQTBench_input/"
files = os.listdir(path)

for approximation_mechanism in approximation_mechanisms:
    for parallelism in parallelisms: 
    
        output_folder = "../file/compiled_mqt_dec_" + approximation_mechanisms_acronym[approximation_mechanism] + "_" + format(parallelism) 
    
        if not os.path.exists(output_folder):

            os.makedirs(output_folder)
            
        print("Start mechanism " + approximation_mechanism + " with parallelism " + format(parallelism) + "\n")

        for file in files:
            print("\n\ncompilation of " + file +":\n\n")
            filename_path = path + file
           
            folder_out = "compiled_mqt_dec_" + approximation_mechanisms_acronym[approximation_mechanism] + "_" + format(parallelism) + "/"
            ret = translator(filename_path,configuration_file_name,folder_out, parallelism,approximation_mechanism,False)
           
        


      
   
     
