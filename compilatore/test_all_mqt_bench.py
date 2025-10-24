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

def translator_ll(filename,parallelism):

    ortography_control(filename)

    gateSubtitution(filename)

    extension(filename)

    #### ONLY NEAREST APPROXIMATION IS EXPECTED FOR CURRENT ARCHITECURE

    #mapping(filename,parallelism,'truncation')

    mapping(filename,parallelism,'nearest')
    
    
configuration_file_name = '../configurazione/emulator_configuration.txt'

approximation_mechanism = 'nearest'

parallelism = 32

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
    
print("Start compilation of all the files\n")

MyCompilerTimeForLenght = {}
LLCompilerTimeForLenght = {}
RepetitionsForLenghtMy = {}
RepetitionsForLenghtLL = {}    

path = "../file/MQTBench_input/"
files = os.listdir(path)
for file in files:
    print("\n\ncompilation of " + file +":\n\n")
    filename_path = path + file
   
    f = open(filename_path)
    
    print(file)
    
    Lenght = len(f.readlines())
   
    f.close()
    
    start = time.time()
    ret = translator(filename_path,configuration_file_name,"compiled_mqt_dec/", parallelism,approximation_mechanism,False, True)
    stop = time.time()
    time_required = stop-start
    output_filename = "../file/compiled/" + file[:-5] + "_compiled.qasm"
    
    if Lenght in MyCompilerTimeForLenght.keys():
        MyCompilerTimeForLenght[Lenght] += time_required
        RepetitionsForLenghtMy[Lenght] += 1
    else: 
        MyCompilerTimeForLenght[Lenght] = time_required
        RepetitionsForLenghtMy[Lenght] = 1
    
    if ret < 0:
        print("It was not possible to complete the compilation procedure in " +  format(time_required) + " s\n")
        fileErrors.write("\n\ncompilation of " + file +":\n\n")
        fileErrors.write("It was not possible to complete the compilation procedure in " +  format(time_required) + " s\n")
    else:
        print("Compilation procedure terminate successfully in " +  format(time_required) + " s\n")
        
    print(ret)
    start = time.time()      
    try:    
        translator_ll(file,parallelism)
    except:
        print("ll compiler cannot compile the file " + format(file) + "\n")
        fileErrors.write("ll compiler cannot compile the file " + format(file) + "\n")
    else:
        stop = time.time()
        time_requiredLL = stop-start
        print("Compilation procedure of ll translator terminate successfully in " +  format(time_requiredLL) + " s\n")
        output_filenamell = "../file/compiled_mqt_ll/" + file[:-5] + "_mapped_fixed_round_0_nearest.qasm"
        
        if Lenght in LLCompilerTimeForLenght.keys():
            LLCompilerTimeForLenght[Lenght] += time_requiredLL
            RepetitionsForLenghtLL[Lenght] += 1
        else: 
            LLCompilerTimeForLenght[Lenght] = time_requiredLL
            RepetitionsForLenghtLL[Lenght] = 1
            
        if time_requiredLL > time_required:
            print("My compiler is faster\n\n")
        else: 
            print("LL compiler is faster\n\n")
        
        fout = open(output_filename, "r")
        foutll = open(output_filenamell, "r")
        
        outline = fout.readlines()
        outlinell = foutll.readlines()
        
        print("\nStart output file comparison\n")
        Difference = False
        
        if len(outline) == len(outlinell):
            for i in range(len(outline)):
                if outline[i].replace("\n", "") != outlinell[i].replace("\n", ""):
                    fileErrors.write("\n\ncompilation of " + file +":\n\n")
                    print("line " + format(i) + " is equal to:\n")
                    fileErrors.write("line " + format(i) + " is equal to:\n")
                    print(outline[i] + "\n")
                    fileErrors.write(outline[i] + "\n")
                    print("Instead of:\n")
                    fileErrors.write("Instead of:\n")
                    print(outlinell[i] + "\n")
                    fileErrors.write(outlinell[i] + "\n")
                    Difference = True
        elif len(outline) > len(outlinell):
            i = 0
            j = 0
            MissingLine = False
            Difference = True
            while i < len(outline) and j  < len(outlinell):
                if outline[i].replace("\n", "") != outlinell[j].replace("\n", "") and MissingLine == False:
                    i += 1
                    MissingLine = True   
                elif outline[i].replace("\n", "") != outlinell[j].replace("\n", "") and MissingLine == True:
                    fileErrors.write("\n\ncompilation of " + file +":\n\n")
                    fileErrors.write("line " + format(i) + " is equal to:\n")                 
                    print("line " + format(i) + " is equal to:\n")
                    fileErrors.write(outline[i] + "\n")    
                    print(outline[i] + "\n")
                    fileErrors.write("Instead of:\n")   
                    print("Instead of:\n")
                    fileErrors.write(outlinell[j] + "\n")  
                    print(outlinell[j] + "\n")
                    MissingLine = False 
                    j +=1 
                elif outline[i].replace("\n", "") == outlinell[j].replace("\n", "") and MissingLine == True: 
                    print("ll compiler miss the line: " + outline[i-1] + "\n")
                    fileErrors.write("\n\ncompilation of " + file +":\n\n")
                    fileErrors.write("ll compiler miss the line: " + outline[i-1] + "\n")
                    i += 1
                    j += 1
                    MissingLine = False 
                else:
                    i += 1
                    j += 1
                    MissingLine = False 
        else: 
            i = 0
            j = 0
            MissingLine = False
            Difference = True
            while i < len(outline) and j  < len(outlinell):
                if outline[i].replace("\n", "") != outlinell[j].replace("\n", "") and MissingLine == False:
                    j += 1
                    MissingLine = True   
                elif outline[i].replace("\n", "") != outlinell[j].replace("\n", "") and MissingLine == True: 
                    fileErrors.write("\n\ncompilation of " + file +":\n\n")
                    fileErrors.write("line " + format(i) + " is equal to:\n")                
                    print("line " + format(i) + " is equal to:\n")
                    fileErrors.write(outline[i] + "\n")  
                    print(outline[i] + "\n")
                    fileErrors.write("Instead of:\n") 
                    print("Instead of:\n")
                    fileErrors.write(outlinell[i] + "\n")
                    print(outlinell[i] + "\n")
                    MissingLine = False 
                    i +=1 
                elif outline[i].replace("\n", "") == outlinell[j].replace("\n", "") and MissingLine == True: 
                    print("My compiler miss the line: " + outlinell[j-1] + "\n")
                    fileErrors.write("\n\ncompilation of " + file +":\n\n")
                    fileErrors.write("My compiler miss the line: " + outlinell[j-1] + "\n")
                    i += 1
                    j += 1
                    MissingLine = False 
                else:
                    i += 1
                    j += 1
                    MissingLine = False
                    
                    
                    
         
        
        if Difference == False:
            print("The two files are perfectly equal\n\n")
            
        fout.close()
        foutll.close()
    
      
MyCompilerTimeForLenght = dict(sorted(MyCompilerTimeForLenght.items()))          
LLCompilerTimeForLenght = dict(sorted(LLCompilerTimeForLenght.items()))
RepetitionsForLenghtMy = dict(sorted(RepetitionsForLenghtMy.items()))          
RepetitionsForLenghtLL = dict(sorted(RepetitionsForLenghtLL.items())) 
for key in MyCompilerTimeForLenght.keys():
    MyCompilerTimeForLenght[key] = MyCompilerTimeForLenght[key]/RepetitionsForLenghtMy[key]
    
for key in LLCompilerTimeForLenght.keys():
    LLCompilerTimeForLenght[key] = LLCompilerTimeForLenght[key]/RepetitionsForLenghtLL[key]
    

plt.plot(list(MyCompilerTimeForLenght.keys()),list(MyCompilerTimeForLenght.values()), color='b', linewidth=2,label=r'\textit{My compiler}')
plt.title(r'\textbf{Compilation Time}',fontsize=20)
plt.xlabel(r'\textit{File lenght}', fontsize=20)
plt.ylabel(r'\textit{Time [s]}', fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("MyTime.eps", format='eps')
plt.savefig("MyTime.png", format='png')
plt.savefig("MyTime.pdf", format='pdf')
plt.close()

plt.plot(list(LLCompilerTimeForLenght.keys()),list(LLCompilerTimeForLenght.values()), color='g', linewidth=2,label=r'\textit{LL compiler}')
plt.title(r'\textbf{Compilation Time}',fontsize=20)
plt.xlabel(r'\textit{File lenght}', fontsize=20)
plt.ylabel(r'\textit{Time [s]}', fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("LLTime.eps", format='eps')
plt.savefig("LLTime.png", format='png')
plt.savefig("LLTime.pdf", format='pdf')
plt.close()

plt.plot(list(MyCompilerTimeForLenght.keys()),list(MyCompilerTimeForLenght.values()), color='b', linewidth=2,label=r'\textit{My compiler}')
plt.plot(list(LLCompilerTimeForLenght.keys()),list(LLCompilerTimeForLenght.values()), color='g', linewidth=2,label=r'\textit{LL compiler}')
plt.title(r'\textbf{Compilation Time}',fontsize=20)
plt.xlabel(r'\textit{File lenght}', fontsize=20)
plt.ylabel(r'\textit{Time [s]}', fontsize=20)
leg = plt.legend(loc='upper right', frameon=True, fontsize=15)
leg.get_frame().set_facecolor('white')
plt.savefig("ComparisonTime.eps", format='eps')
plt.savefig("ComparisonTime.png", format='png')
plt.savefig("ComparisonTime.pdf", format='pdf')
plt.close()



      
   
     
