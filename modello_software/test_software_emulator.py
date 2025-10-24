import sys
sys.path.insert(0, r'./floating_point')
from VLSIEmulator import EmulatorWrap 

# varify that a sufficient number of argument is provided
if len(sys.argv) < 4:
    print("Error: the provided argoment are not enough\n")
    sys.exit(-1)


#acquire the file path from command line
istructionfilename = sys.argv[1]

#acquire the file path from command line
sinecosinefilename = sys.argv[2]

#acquire the file path from command line
outputfile = sys.argv[3]

#if provided, acquire the parallelism
if len(sys.argv) == 5:
    parallelism = int(sys.argv[4])
else:
    parallelism = 32
    
verbose = True
    
EmulatorWrap(istructionfilename, sinecosinefilename, outputfile, parallelism, verbose)