from utils_f import translator
import sys

# varify that a sufficnet number of argument is provided
if len(sys.argv) < 2:
    print("Error: the provided argoment are not enough\n")
    sys.exit(-1)


#acquire the file path from command line
filename = sys.argv[1]

#if provided, acquire the parallelism
if len(sys.argv) == 3:
    parallelism = sys.argv[2]
else:
    parallelism = 32
    
configuration_file_name = '../configurazione/emulator_configuration.txt'

approximation_mechanism = 'nearest'
    
ret = translator(filename,configuration_file_name, parallelism,approximation_mechanism)
if ret < 0:
    print("It was not possible to complete the compilation procedure\n")
    sys.exit(ret)
else:
    print("Compilation procedure terminate successfully\n")
    sys.exit(ret)