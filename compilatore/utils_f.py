#utils_f.py#
# file created by Deborah Volpe in 20/03/2022
# it containts all the methods for quantum circuit compilation
# the circuit must be described in OpenQASM 2.0 and the compiled circuit targets the AEQUAM emulator
# the instruction format is | gateOPCODE | targetADDR | controlADDR | angleADDR |
# The reported code is obtained starting from the preliminary version developed by Lorenzo Lagostina

from math import sin
from math import cos
from math import pi
import math

 

#list of rotational gates
rotationalGates = [
        'rx','ry','rz', 'u1', 'p',
        'crx','cry','crz', 'cu1', 'cp'
 ]
 
#list of allowed gate
nonRotationalGates = [
        'x', 'cx', 'y', 'cy', 'z', 
        'cz', 'h', 's', 'cs', 'sdg', 'ch',
        'csdg', 't', 'ct', 'tdg', 'ctdg'
 ]
 
#dictionary with gate-opcode association
gatesOPCODE = {

    'x' : 0,
    'y' : 1,
    'z' : 2,
    'h' : 3,
    's' : 4,
    'sdg' : 5,
    't' : 6,
    'tdg' : 7,
    'rx' : 8,
    'ry' : 9,
    'rz' : 10,
    'u1' : 11,
    'p' : 11
}

#dictionary with special gates 
SpecialGatesEquivalentStandardGate = {
    'u' : ["rz(lambda) q\nry(theta) q\nrz(phi) q", ["theta", "phi", "lambda", "q"]], 
    #'cu3' : ["crz(-lambda) q1,q2\ncry(theta) q1,q2\ncrz(lambda) q1,q2\ncu1(phi+lambda) q1,q2", ["theta", "phi", "lambda", "q1", "q2"]],  
    'cu' : ["u1(lambda/2+phi/2) q1\nu1(lambda/2-phi/2) q2\ncx q1,q2\nu3(-theta/2,0,-lambda/2-phi/2) q2\ncx q1,q2\nu3(theta/2,phi,0) q2", ["theta", "phi", "lambda", "q1", "q2"]],    
   # 'u2' : ["rz(lambda) q\nry(pi/2) q\nrz(phi) q", ["phi", "lambda", "q"]], 
    'u2' : ["rz(lambda) q\nry(pi/2) q\nrz(-lambda) q\nu1(lambda+phi) q", ["phi", "lambda", "q"]],    
    'cu2' : ["crz(lambda) q1,q2\ncry(pi/2) q1,q2\ncrz(-lambda) q1,q2\ncu1(lambda+phi) q1,q2", ["phi", "lambda", "q1", "q2"]],  
    'u3' : ["rz(lambda) q\nry(theta) q\nrz(-lambda) q\nu1(lambda+phi) q", ["theta", "phi", "lambda", "q"]],       
    #'cu3' : ["crz(-lambda) q1,q2\ncry(theta) q1,q2\ncrz(lambda) q1,q2\ncu1(phi+lambda) q1,q2", ["theta", "phi", "lambda", "q1", "q2"]],  
    'cu3' : ["u1(lambda/2+phi/2) q1\nu1(lambda/2-phi/2) q2\ncx q1,q2\nu3(-theta/2,0,-lambda/2-phi/2) q2\ncx q1,q2\nu3(theta/2,phi,0) q2", ["theta", "phi", "lambda", "q1", "q2"]], 
    'ccx' : ["h c\ncx b,c\ntdg c\ncx a,c\nt c\ncx b,c\ntdg c\ncx a,c\nt b\nt c\nh c\ncx a,b\nt a\ntdg b\ncx a,b", ["a", "b", "c"]],
    'swap' : ["cx q1,q2\ncx q2,q1\ncx q1,q2", ["q1", "q2"]],
    'rzz' : ["cx q1,q2\nrz(theta) q2\ncx q1,q2", ["theta", "q1", "q2"]],
    'cswap' : ["cx q2,q3\nccx q1,q3,q2\ncx q2,q3", ["q1", "q2", "q3"]],
    'rccx' : ["ry(pi/4) c\ncx b,c\nry(pi/4) c\ncx a,c\nry(-pi/4) c\ncx b,c\nry(-pi/4) c", ["a", "b", "c"]],
    'sx' : ["rx(pi/2) q", ["q"]],
    'rxx': ["h q1\nh q2\nrzz(theta) q1,q2\nh q1\nh q2", ["theta", "q1", "q2"]],
    'sxdg' : ["rx(-pi/2) q", ["q"]]   
}


#Function for adding a new quantum register in the proper dictionary
#with the format name : offset
#and updating the TotalNumberQubits variable with its dimension
def add_qreg(line, TotalNumberQubits):
    #obtain name and number of qubits
    #expected format: qreg name[qubits];
    l = line[:-1].split(" ")
    #mantain name[qubits]
    temp = l[1].split("[")
    #name of the quantum register
    name = temp[0]
    #dimention of the quantum register: qubits 
    dim =  temp[1][:-2]
    try:
        qubits = int(dim)
    except:
        print("Error! Invalid format for the file")
    if name in quantumRegisters.keys():
        print("Error! This quantum register is already defined\n")
        return -3
    else:
        #offset to apply to recover the number of qubits of 
        #the quantum register in the effective architecture 
        offset = TotalNumberQubits
        #increment the total number of qubit of the effective architecture
        TotalNumberQubits += qubits
        #add the register in the dictionary {name: (offset, qubits)}
        quantumRegisters[name] = (offset, qubits)
        return TotalNumberQubits
        
        
#Function for substitute the register name and position with the number
#of the qubit to manipulate in the effective architecture
def qubits_conversion(l_qubits):
    #create an empty qubit list of tuples for managing the possibility to apply
    #the gate to the all quantum register
    qubitlist = []
    #if there is a single qubit and it is apply to the all quantum register
    if len(l_qubits) == 1 and l_qubits[0].find("[") < 0:
        #recover the register info: offset and lenght
        qreg_info = quantumRegisters[l_qubits[0]]
        offset = qreg_info[0]
        lenght = qreg_info[1]
        # write in the list the tuples of qubits on which it 
        # is necessary to apply the gate
        for j in range(lenght):
            q1 = j + offset
            q2 = q1
            qubitlist.append((q2,q1))
    #if there is a two qubit gate and it is apply to the all quantum registers
    elif  len(l_qubits) == 1 and l_qubits[0].find("[") < 0:
        #recover the register info: offset and lenght
        qreg_info_1 = quantumRegisters[l_qubits[0]]
        offset_1 = qreg_info_1[0]
        lenght_1 = qreg_info_1[1]
        #recover the register info: offset and lenght
        qreg_info_2 = quantumRegisters[l_qubits[1]]
        offset_2 = qreg_info_2[0]
        lenght_2 = qreg_info_2[1]
        if lenght_1 == lenght_2 and l_qubits[0] != l_qubits[1]:
            #write in the list the tuples of qubits on which it 
            #is necessary to apply the gate
            for j in range(lenght_1):
                q1 = j + offset_1
                q2 = j + offset_2
                qubitlist.append((q2,q1))
    #if the gate is not applyed to the overall quantum register 
    else:
        #extract the quantum register name
        q1_temp = l_qubits[0].split("[")
        try:
            #extract position and offset associated with the quantum register
            q1 = int(q1_temp[1].split("]")[0]) + quantumRegisters[q1_temp[0]][0]
        except:
            print("Wrong format for gate declaration\n")
            return -5
        # if it is a two qubit gate    
        if len(l_qubits) == 2:
            #extract the quantum register name
            q2_temp = l_qubits[1].split("[")
        
            try:
                #extract position and offset associated with the quantum register
                q2 = int(q2_temp[1].split("]")[0]) + quantumRegisters[q2_temp[0]][0]
            except:
                print("Wrong format for gate declaration\n")
                return -5
        else:
            q2 = q1
            
        qubitlist.append((q2,q1))
        
    return qubitlist
        

#Function for translating gate line 
#gate_name is the name of the gate to apply, eg: rx, x
#index is different from 0 only for rotational gate and is the position 
#of sine and cosine in the register file
#qubits is the piece of string related to qubits q1[x],q2[y]
#Output string is the string on which the outcome should be written
def gate_translator(gate_name, index, qubits,OutputString, index_sin_cos, verbose):
    #extract list of qubit involved in the gate translation
    qubitlist = qubits_conversion(qubits.strip().split(","))    
    #if the list is empty
    if not qubitlist:
        print("Format error\n")
        return -6        
    for k in range(len(qubitlist)):
        qubit1 = qubitlist[k][0]
        qubit2 = qubitlist[k][1]
        
        #associate the gate name to the opcode    
        if gate_name.startswith('c'):
            # controlled gates have the same opcode of their not controlled counter part
            try:
                opcode = gatesOPCODE[gate_name[1:]]
            except:
                return -6
            
            # target and control qubit must be different
            if qubit1 == qubit2:
                print("Format error\n")
                return -6
        else:
            opcode = gatesOPCODE[gate_name]  
            
        #write the number required for the final instruction
        OutputString += format(opcode) + " " + format(qubit1) + " " + format(qubit2) + " " + format(index) + "\n"
        if verbose:
            print(format(opcode) + " " + format(qubit1) + " " + format(qubit2) + " " + format(index) + "\n")

    return OutputString, index_sin_cos
        
        
#Perform the approximation of the sine and cosine value, converting them in the fixed point format
def SinCosConvertion(sinTheta, cosTheta, approximation_mechanism, parallelism):
    # we want consider fixed point numbers with 2 integer part bits and parallelism-2 fractional bits
    # wanted final format xx.xxxxxxxxxxxxx
    # obtain the floating point number d.f where d cointains all the wanted final bits
    sinThetaFixTemp = sinTheta*(2**(parallelism-2)) 
    cosThetaFixTemp = cosTheta*(2**(parallelism-2))
    
    # approximation with truncation
    # gives for d.6 --> d
    if approximation_mechanism == 'truncation':
        sinThetaFix = int(sinThetaFixTemp)
        cosThetaFix = int(cosThetaFixTemp)
    # approximation to nearest
    # gives for d.6 --> d+1
    # gives for d.4 --> d
    # gives for d.5 --> d+1
    elif approximation_mechanism ==  'nearest':
        sinThetaFix = math.ceil(sinThetaFixTemp)
        cosThetaFix = math.ceil(cosThetaFixTemp)
    # approximation to nearest even
    # gives for d.6 --> d+1
    # gives for d.4 --> d
    # gives for d.5 --> one time d, the other d+1
    elif approximation_mechanism ==  'nearest_even':
        sinThetaFix = round(sinThetaFixTemp)
        cosThetaFix = round(cosThetaFixTemp)
    #if something wrong or not supported, perform nearest
    else: 
        sinThetaFix = math.ceil(sinThetaFixTemp)
        cosThetaFix = math.ceil(cosThetaFixTemp)
        
    return sinThetaFix, cosThetaFix        
        
#Function for translating a rotational gate line
def rot_gate(l, l_2, approximation_mechanism, parallelism, OutputString, index_sin_cos, verbose):
    #discard parentesys ) to indentify the angle
    theta = eval(l_2[1][:-1])  
    #for u1 and p and their controlled version sine and cosine of theta are required
    if l_2[0] == 'u1' or l_2[0] == 'cu1' or l_2[0] == 'p' or l_2[0] == 'cp':
        sinTheta = sin(theta)
        cosTheta = cos(theta)
    #for rx, ry and rz sine and cosine of theta/2 are required
    else:
        sinTheta = sin(theta/2)
        cosTheta = cos(theta/2)
    
    if verbose:
        print("Sine unconvereted " + format(sinTheta) + " Cosine unconvereted " + format(cosTheta) + "\n") 

    #obtain fixed point values of sine and cosine
    sinThetaFixedPoint, cosThetaFixedPoint = SinCosConvertion(sinTheta, cosTheta, approximation_mechanism, parallelism)
    
    #Store sine and cosine in the dictionary
    if not((sinThetaFixedPoint, cosThetaFixedPoint) in dictSinCos.keys()):
        dictSinCos[(sinThetaFixedPoint, cosThetaFixedPoint)] = index_sin_cos
        index = index_sin_cos
        index_sin_cos += 1
    else:
        index = dictSinCos[(sinThetaFixedPoint, cosThetaFixedPoint)]
        
    if verbose:
        print("Sine " + format(sinThetaFixedPoint) + " Cosine " + format(cosThetaFixedPoint) + "\n")
        
    #for managing eventual space betweem a, b       
    q = ""
    if len(l) > 2:
        for i in range(1, len(l)):
            q += l[i] 
    else:
       q = l[1]
       
    OutputString, index_sin_cos = gate_translator(l_2[0] , index, q, OutputString, index_sin_cos, verbose)
    return OutputString, index_sin_cos  

#Function for substituting the parameter of the user defined gate or the special gate supported
#translation is the gate description
#parameter the gate parameter
#data the effective data employed
def substitute_parameter(translation, param, data):
    
    #divide in line
    lines_tr = translation.split("\n")
    translation = ""
    print(param)
    # for each line not empty
    for el in lines_tr:
        if el != "":
            #expected format name(angle) q1,q2 or name q1,q2
            #par=["name" "angle)q1,q2"] or par = ["name q1,q2"]
            par = el.lstrip().rstrip().split("(")
            # if there is the angle parameter
            if len(par) == 2:
                j = 0
                translation += par[0] + "("
               
                temp = par[1].lstrip().rstrip().split(")")
                               
                #isolate the angle
                angles = temp[0].split(",")
                #substitute the parametric angle name, with the effective one
                for j in range(len(angles)-1):
                    ang = angles[j]
                    for p in param:
                        ang = ang.replace(p, str(data[param.index(p)])) 
                    translation += format(eval(ang)) + ","
                ang = angles[-1]
                for p in param:
                    ang = ang.replace(p, str(data[param.index(p)])) 
                translation += format(eval(ang)) + ") "
                #isolate the qubits q1,q2
                d = temp[1].lstrip().rstrip().split(",")
                #substitute the parametric qubit name, with the effective one
                for j in range(len(d)-1):
                    i = param.index(d[j])
                    translation += data[i] + ","
                i = param.index(d[-1])
                translation += data[i] + "\n"
            # if there isn't angle parameter
            else:
                #isolate the qubits q1,q2
                par = el.lstrip().rstrip().split(" ")
                d = par[1].split(",")
                translation += par[0] + " "
                #substitute the parametric qubit name, with the effective one
                for j in range(len(d)-1):
                    i = param.index(d[j])
                    translation += data[i] + ","
                i = param.index(d[-1])
                translation += data[i] + "\n"  
             
    return translation    

#Function for managing standard line
def linemanager(line, approximation_mechanism, parallelism, OutputString, index_sin_cos, verbose):

    #for obtaing ["gate_name", "a,b"]
    l = line.replace("\n", "").replace(";", "").split(" ")
    if line.replace("\n", "").replace(";", "") != "":
        #for managing eventual space between a, b
        q = ""
        if len(l) > 2:
            for i in range(1, len(l)):
                if not l[i].endswith(")"): 
                    q += l[i]
                else: 
                    q += l[i] + " "
        else:
            q = l[1]
           
        #for rotational gate l[0] = "gate_name(angle)"
        #l_2 = ["gate_name", "angle)"]
        l_2 = l[0].split("(")
        #if the line contain a standar non rotational gate (without an angle parameter
        if l[0] in nonRotationalGates: 
            try:
                OutputString, index_sin_cos = gate_translator(l[0], 0, q, OutputString, index_sin_cos, verbose)
            except:
                print("Wrong format for the line\n")
                return "-7"
            return OutputString, index_sin_cos
        #if it is a rotational gate    
        #expected format: gate_name(angle) q[i]
        elif l_2[0] in rotationalGates:
            try:
                OutputString, index_sin_cos = rot_gate(l, l_2, approximation_mechanism, parallelism, OutputString, index_sin_cos, verbose)
            except:
                print("Wrong format for the line\n")
                return "-7"
            return OutputString, index_sin_cos
        #if it is an user define gate or a special gate
        elif l[0] in SpecialGatesEquivalentStandardGate.keys() or l[0] in UserDefineGatesEquivalentStandardGate.keys() or l_2[0] in SpecialGatesEquivalentStandardGate.keys() or l_2[0] in UserDefineGatesEquivalentStandardGate.keys():
            #recover the information about the gate, i.e. translation, parameters and data to substitute
            if l[0] in SpecialGatesEquivalentStandardGate.keys():
                translation = SpecialGatesEquivalentStandardGate[l[0]][0]
                param = SpecialGatesEquivalentStandardGate[l[0]][1]
                data = q.strip().split(",")
            elif l[0] in UserDefineGatesEquivalentStandardGate.keys():
                translation = UserDefineGatesEquivalentStandardGate[l[0]][0]
                param = UserDefineGatesEquivalentStandardGate[l[0]][1]
                data = q.strip().split(",")
            elif l_2[0] in SpecialGatesEquivalentStandardGate.keys():
                translation = SpecialGatesEquivalentStandardGate[l_2[0]][0]
                param = SpecialGatesEquivalentStandardGate[l_2[0]][1]
                if ")" in l_2[1]:
                    data = l_2[1].strip().replace(")", "").split(",") + q.strip().split(",")
                else:
                    data = l_2[1].strip().replace(")", "").split(",") + q.strip().replace(")", ",").split(",")
                
            else:
                translation = UserDefineGatesEquivalentStandardGate[l_2[0]][0]
                param = UserDefineGatesEquivalentStandardGate[l_2[0]][1]
                if ")" in l_2[1]:
                    data = l_2[1].strip().replace(")", "").split(",") + q.strip().split(",")
                else:
                    data = l_2[1].strip().replace(")", "").split(",") + q.strip().replace(")", ",").split(",")
                
            if "" in data:
                data.remove("")
            #substitute parameter with effective data
            translation=substitute_parameter(translation, param, data)
            #compile line by line
            linesInside = translation.split("\n")
            if verbose:
                print(linesInside)
            for lineInside in linesInside:
                OutputString, index_sin_cos = linemanager(lineInside, approximation_mechanism, parallelism, OutputString, index_sin_cos, verbose)
                if OutputString.isnumeric():
                    print("Wrong format for the line\n")
                    return "-7"                
            return OutputString, index_sin_cos
        else:
            if verbose:
                print("line not converted in an instruction\n")
            return OutputString, index_sin_cos
    else:
        return OutputString, index_sin_cos
      
# Function for converting a binary number into a binary string      
def binary_string(number, parallelism):
    if number < 0:
        temp = (2**parallelism)+number
        return format(temp, 'b').zfill(parallelism)
    else:
        return format(number, 'b').zfill(parallelism)

#Top function for compilation
#read the input file and write the output one
def translator(filename,configuration_file_name, folder_output, parallelism=32,approximation_mechanism='nearest', binary=True, verbose= False, hardware=False, package_lenght=20):
    #Clean the dictionaries
    
    #dictionary for user define gates
    global UserDefineGatesEquivalentStandardGate 
    UserDefineGatesEquivalentStandardGate = {}

    #define quantum registers dictionary
    #format name : offset to apply
    global quantumRegisters
    quantumRegisters= {}


    #define the directory of sine and cosine
    global dictSinCos
    dictSinCos = {}

    #define total numer of qubits 
    TotalNumberQubits = 0
    
    #counter for number of stored sin-cosin
    index_sin_cos = 0


    #read the necessary information from the configuration file
    #open the file with circuit description
    try:
        fileInConfig = open(configuration_file_name, 'r')
    except:
        print("Error! The input file " + configuration_file_name + " does not exist\n")
        return -1
    configList = fileInConfig.readline().split()
    fileInConfig.close()

    N = int(configList[0])
    W = int(configList[1])
    S = int(configList[2])
    Q = int(configList[3])

    #open the file with circuit description
    try:
        fileIn = open(filename, 'r')
    except:
        print("Error! The input file " + filename + " does not exist\n")
        return -1 

    #define the file name of of the of compiled circuit description        
    filename_output = ""    
    filename_fields = filename[:-5].split("/")
    for i in range(len(filename_fields)-2):
        filename_output += filename_fields[i] + "/"
    
    filename_output += folder_output + filename_fields[len(filename_fields)-1]   + "_compiled.qasm"
    
    #open the file for the output description
    try:
        fileOut = open(filename_output, 'w')
    except:
        print("Error! The output file " + filename_output + " cannot be created\n")
        return -2

    #define the file name of of the of compiled circuit description        
    filename_output_sincos = ""   
    for i in range(len(filename_fields)-2):
        filename_output_sincos += filename_fields[i] + "/"
        

    filename_output_sincos +=folder_output + filename_fields[len(filename_fields)-1] + "_sincos.qasm"
    
    #open the file for the output description
    try:
        fileSinCos = open(filename_output_sincos, 'w')
    except:
        print("Error! The output file " + filename + " cannot be created\n")
        return -2
        
    OutputString = ""
        
    lines = fileIn.readlines()
    
    fileIn.close()
    
    #in order to not consider the heder lines
    i = 2
    
    while i < len(lines):
    
        #remove the comment
        if lines[i].find('//'):
            line = lines[i].split('//')[0]
        else:
            line = lines[i]
            
        if verbose:
            print(line)
        #if the line define a quantum register
        if line.startswith("qreg"):
            TotalNumberQubits = add_qreg(line, TotalNumberQubits)
            if TotalNumberQubits == -3: 
                return -3
               
        #if there is an user define gate 
        #add them in the dictionary
        #Expected format:
        #gate gate_name(angle,angle2) a,b,c 
        #{ 
        #  standard_gate c,b; 
        #  standard_gate c,a; 
        #  standard_gate a,b,c; 
        #} 
        #identify the keyword gate for knowing that there is a user define gate
        elif line.startswith("gate"):
            #split in ["gate(angle1,angle2)", "gate_name", "a,b,c"]
            l = line[:-1].split(" ")
            
            # in case of angular parameter
            if l[1].find("(") >= 0:
                l_2 = l[1][:-1].split("(")
                gate_name = l_2[0]
                involved_variable_name = l_2[1].strip().split(",") + l[2].strip().split(",")
            else:
                gate_name = l[1]
                #to obtain ["a", "b", "c"]
                involved_variable_name = l[2].strip().split(",")
            
            #for obtaining gateDefineContent="standard_gate c,b;\nstandard_gate c,a;\nstandard_gate a,b,c;\n" 
            gateDefineContent = ""
            i += 1
            while lines[i].find('}') < 0:
                #remove eventual comment
                if lines[i].find('//'):
                    line = lines[i].split('//')[0]
                else:
                    line = lines[i]
                # remove { }
                line = line.replace("{", "").replace("}", "")
                if line.lstrip().rstrip()  != "\n" and line.lstrip().rstrip()  != "":
                    gateDefineContent += line.lstrip().rstrip().replace(";", "") + "\n"
                i += 1
            #verify if the gate is already present in the dictionary of the custom gate
            if gate_name in UserDefineGatesEquivalentStandardGate.keys():
                print("Error! This custom gate is already defined\n")
                return -4
            else:
                #Add the custum gate in the dictionary
                UserDefineGatesEquivalentStandardGate[gate_name] = []
                UserDefineGatesEquivalentStandardGate[gate_name].append(gateDefineContent)
                UserDefineGatesEquivalentStandardGate[gate_name].append(involved_variable_name)
        
        #for managing standar line
        else:
            OutputString, index_sin_cos = linemanager(line, approximation_mechanism, parallelism, OutputString, index_sin_cos, verbose) 
        i += 1
        
    #Write the number of qubits on the top of the file
    if TotalNumberQubits > N:
        print("Unfeasible on the current architecture configuration\n")
        return -8
        
    if binary:
        if hardware:
            stringBinary = binary_string(TotalNumberQubits,N)
            if len(stringBinary) < package_lenght:
                fileOut.write("0"*(package_lenght-len(stringBinary)) + stringBinary + "\n")
            else:
                fileOut.write(stringBinary + "\n")
        else:
            fileOut.write(binary_string(TotalNumberQubits,N) + "\n")
    else: 
        fileOut.write(format(TotalNumberQubits) + "\n")   
    
    #Convert in the correct binary format each output line and write it in the file
    outputlines = OutputString.split("\n")
    for out in outputlines:
        if out != "":
            IstructionElement = out.split(" ")
            if binary:
                if hardware:
                    stringIstruction = binary_string(int(IstructionElement[0]),math.ceil(math.log2(len(gatesOPCODE)))) + binary_string(int(IstructionElement[1]),math.ceil(math.log2(N))) + binary_string(int(IstructionElement[2]),math.ceil(math.log2(N))) + binary_string(int(IstructionElement[3]),Q)
                    if len(stringIstruction) < package_lenght:
                        fileOut.write("0"*(package_lenght-len(stringIstruction)) + stringIstruction+ "\n")
                    else:
                        fileOut.write(stringIstruction + "\n")
                else:
                    fileOut.write(binary_string(int(IstructionElement[0]),math.ceil(math.log2(len(gatesOPCODE)))) + binary_string(int(IstructionElement[1]),math.ceil(math.log2(N))) + binary_string(int(IstructionElement[2]),math.ceil(math.log2(N))) + binary_string(int(IstructionElement[3]),Q) + "\n")
            else:
                fileOut.write(format(IstructionElement[0])+ " "  + format(IstructionElement[1]) + " "+ format(IstructionElement[2])+ " " + format(IstructionElement[3]) + "\n")        
    fileOut.close()
    
 
    #Write the file of sine and cosine
    fileSinCos.write(format(len(dictSinCos)) + "\n")
    for key in dictSinCos.keys():
        if binary:
            fileSinCos.write(binary_string(key[0],parallelism) + " " + binary_string(key[1],parallelism) + "\n")
        else: 
            fileSinCos.write(format(key[0]) + " " + format(key[1]) + "\n")
    
    fileSinCos.close()
    
    return 0
        
        
                    
                
                        

                
    