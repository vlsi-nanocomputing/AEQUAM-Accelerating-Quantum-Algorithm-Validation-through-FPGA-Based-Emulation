from libcpp.string cimport string
from libcpp cimport bool
from libcpp.vector cimport vector
from libcpp cimport int

cdef extern from "emulator_fixed.h":
	int emulatorVLSI_fixed(string istructionfilename, string sinecosinefilename, string outputfilename, int parallelism, bool verbose);
	
def EmulatorFixedWrap(istructionfilename, sinecosinefilename, outputfilename, parallelism, verbose):
	istructionfilename_ = istructionfilename.encode('utf-8')
	sinecosinefilename_ = sinecosinefilename.encode('utf-8')
	outputfilename_ = outputfilename.encode('utf-8')
	ret = emulatorVLSI_fixed(istructionfilename_, sinecosinefilename_, outputfilename_ , parallelism, verbose)
	return ret
