//emulator.cpp
//create in 22/05/2023
//code developed by Lorenzo Lagostina and Deborah Volpe
//this files containts functions for emulation
//They work with fixed point data respresentation considering nearest even rounding technique
#include "emulator_fixed_nearest_even.h"
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <vector>
using namespace std;


//definition of the known value 1/sqrt(2)
long long int INV_SQRT_2;
long long int frac;

//function for nearest even approximation
long long int round_nearest_even(double val){
	long long int val_int = (int) val;
	//if even
	if ((val_int % 2) == 0){
		return (long long int) floor(val);
	}else{
		return (long long int) ceil(val);
	}
}

//considering state x = a+ib and y = c+di

//function for the x gate exectution
//x matrix is equal to ((0, 1)
//                    , (1, 0))
// it correspond to exchange the probability amplitude of 
// the state 0 and the state 1
//x = c+di, y = a+bi
void execute_X (qstate &x, qstate &y){

    long long int tmp_r, tmp_i;
    
    tmp_r = x.real;
    tmp_i = x.img;

    x.real = y.real;
    x.img = y.img;

    y.real = tmp_r;
    y.img = tmp_i;

}

//function for the y gate exectution
//y matrix is equal to ((0 -i)
//                    , (i, 0))
////x = -ci+d, y = ai-b
void execute_Y (qstate &x, qstate &y){

    long long int tmp_r, tmp_i;
    
    tmp_r = x.real;
    tmp_i = x.img;

    x.real = y.img;
    x.img = -y.real;

    y.real = -tmp_i;
    y.img = tmp_r;

}

//function for the z gate exectution
//z matrix is equal to ((1, 0)
//                    , (0, -1))
//change the sign of y
////x = a+bi, y = -c-di
void execute_Z (qstate &y){

    y.real = -y.real;
    y.img = -y.img;

}

//function for the H gate exectution
//H matrix is equal to 1/sqrt(2) ((1, 1)
//                    , (1, -1))
//create superposition
////x = 1/sqrt(2)*(a+bi+c+di), y = 1/sqrt(2)*(a+bi-c-di)
void execute_H (qstate &x, qstate &y){

    long long int tmp_r, tmp_i;
    
    tmp_r = x.real;
    tmp_i = x.img;

    x.real =  (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( tmp_r + y.real ))/pow(2.0, frac));
    x.img =  (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( tmp_i + y.img ))/pow(2.0, frac));

    y.real =  (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( tmp_r - y.real ))/pow(2.0, frac));
    y.img = (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( tmp_i - y.img ))/pow(2.0, frac));    

}

//function for the sdagger gate exectution
//s matrix is equal to ((1, 0)
//                    , (0, i))
//rotation of pi/2
////x = a+bi, y = ci-d
void execute_S (qstate &y){

    long long int tmp;

    tmp = y.real;

    y.real = -y.img;
    y.img = tmp;

}

//function for the s gate exectution
//s dagger matrix is equal to ((1, 0)
//                           , (0, -i))
//rotation of -pi/2
////x = a+bi, y = -ci+d
void execute_SDG (qstate &y){

    long long int tmp;

    tmp = y.real;

    y.real = y.img;
    y.img = -tmp;
}

//function for the t gate exectution
//t matrix is equal to ((1, 0)
//                    , (0, e^(ipi/4)))
//rotation of pi/4
////x = a+bi, y = 1/sqrt(2)*((c-d) +i(c+d))
void execute_T (qstate &y){

    long long int tmp;

    tmp = y.real;

    y.real = (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( tmp - y.img ))/pow(2.0, frac));
    y.img = (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( tmp + y.img))/pow(2.0, frac));

}

//function for the t dagger gate exectution
//t dagger matrix is equal to ((1, 0)
//                    		 , (0, e^(-ipi/4)))
//rotation of -pi/
////x = a+bi, y = 1/sqrt(2)*((c+d) +i(d-c))
void execute_TDG (qstate &y){

    long long int tmp;

    tmp = y.real;

    y.real = (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( tmp + y.img ))/pow(2.0, frac));
    y.img = (long long int)round_nearest_even(((double)INV_SQRT_2 * (double)( y.img - tmp ))/pow(2.0, frac));

}

//function for the rx gate exectution
//rx matrix is equal to ((cos(t/2), -isin(t/2))
//                     , (-isin(t/2), cos(t/2))
//rotation of t along the x axis
////x = (acos(t/2)+ dsin(t/2))+i(bcos(t/2)-csin(t/2)), 
////y = (bsin(t/2)+ ccos(t/2))+i(dcos(t/2)-asin(t/2))
void execute_RX (qstate &x, qstate &y, gon &imm){

    long long int tmp_r, tmp_i;
    
    tmp_r = x.real;
    tmp_i = x.img;

    x.real  = (long long int) round_nearest_even(((double)tmp_r * (double)imm.cos)/pow(2.0, frac)) + (long long int) round_nearest_even(((double)y.img * (double)imm.sin)/pow(2.0, frac));
    x.img = (long long int)round_nearest_even(((double)tmp_i * (double)imm.cos)/pow(2.0, frac)) - (long long int) round_nearest_even(((double)y.real * (double)imm.sin)/pow(2.0, frac));

    y.real = (long long int) round_nearest_even(((double)tmp_i * (double)imm.sin)/pow(2.0, frac)) + (long long int)round_nearest_even(((double)y.real * (double)imm.cos)/pow(2.0, frac));
    y.img = (long long int) round_nearest_even(((double)y.img * (double)imm.cos)/pow(2.0, frac)) - (long long int)round_nearest_even(((double)tmp_r * (double)imm.sin)/pow(2.0, frac));

}

//function for the ry gate exectution
//ry matrix is equal to ((cos(t/2), -sin(t/2))
//                    , (sin(t/2), cos(t/2))
//rotation of t along the y axis
////x = (acos(t/2) - csin(t/2))+i(bcos(t/2)+dsin(t/2)), 
////y = (asin(t/2)+ccos(t/2))+i(dcos(t/2)+bsin(t/2))
void execute_RY (qstate &x, qstate &y, gon &imm){

    long long int tmp_r, tmp_i;
    
    tmp_r = x.real;
    tmp_i = x.img;

    x.real = (long long int) round_nearest_even(((double)tmp_r * (double)imm.cos)/pow(2.0, frac)) - (long long int)round_nearest_even(((double)y.real * (double)imm.sin)/pow(2.0, frac));
    x.img = (long long int) round_nearest_even(((double)tmp_i * (double)imm.cos)/pow(2.0, frac)) - (long long int) round_nearest_even(((double)y.img * (double)imm.sin)/pow(2.0, frac));

    y.real = (long long int) round_nearest_even(((double)tmp_r * (double)imm.sin)/pow(2.0, frac)) + (long long int) round_nearest_even(((double)y.real * (double)imm.cos)/pow(2.0, frac));
    y.img = (long long int) round_nearest_even(((double)tmp_i * (double)imm.sin)/pow(2.0, frac)) + (long long int) round_nearest_even(((double)y.img * (double)imm.cos)/pow(2.0, frac));
}

//function for the rz gate exectution
//rz matrix is equal to ((e^(-it/2), 0)
//                    , (0, e^it/2)
//rotation of t along the y axis
////x = (acos(t/2) + bsin(t/2))+i(-asin(t/2) + cos(t/2)), 
////y = (ccos(t/2) - dsin(t/2))+i(csin(t/2)+dcos(t/2))
void execute_RZ (qstate &x, qstate &y, gon &imm){

    long long int tmp;
    
    tmp = x.real;
    
    x.real = (long long int) round_nearest_even(((double)tmp * (double)imm.cos)/pow(2.0, frac)) + (long long int) round_nearest_even(((double)x.img * (double)imm.sin)/pow(2.0, frac));
    x.img = (long long int) round_nearest_even(((double)x.img * (double)imm.cos)/pow(2.0, frac)) - (long long int) round_nearest_even(((double)tmp * (double)imm.sin)/pow(2.0, frac));

    tmp = y.real;

    y.real = (long long int)round_nearest_even(((double)tmp * (double)imm.cos)/pow(2.0, frac)) - (long long int) round_nearest_even(((double)y.img * (double)imm.sin)/pow(2.0, frac));
    y.img = (long long int)round_nearest_even(((double)tmp * (double)imm.sin)/pow(2.0, frac)) + (long long int) round_nearest_even(((double)y.img * (double)imm.cos)/pow(2.0, frac));
    
}

//function for the U1 gate exectution
//U2 matrix is equal to ((1, 0)
//                     , (0, e^il)
//rotation of t along the y axis
////x = a+bi, 
////y = (ccos(l) - dsin(l))+i(csin(l)+dcos(l))
void execute_U1 (qstate &y, gon &imm){

    long long int tmp;

    tmp = y.real;

    y.real = (long long int) round_nearest_even(((double)tmp * (double)imm.cos)/pow(2.0, frac)) - (long long int) round_nearest_even(((double)y.img * (double)imm.sin)/pow(2.0, frac));
    y.img = (long long int) round_nearest_even(((double)tmp * (double)imm.sin)/pow(2.0, frac)) + (long long int) round_nearest_even(((double)y.img * (double)imm.cos)/pow(2.0, frac));
}

//function for the complete emulation
//it accepts as input the istruction filename, the sinecosine filename and the neme of the output file
int emulatorVLSI_fixed_nearest_even(string istructionfilename, string sinecosinefilename, string outputfilename, int parallelism, bool verbose){

	
	//declare the string line
	string line;
	
	//declare the variable for number of qubits
	unsigned int qubitNumber;
	
	//declare the variable for the number of state
	unsigned int stateNumber;
	
	// declare the variable for the number of interacting couple
	unsigned int couplesNumber;
	
	//declare the variable for the number of sinecosine
	unsigned int sincosNumber;
	
	//instruction parameters
	unsigned int gate, qtgt, qctrl, qimm;
	
	//lenght of the butterfly block
	unsigned int lenght;
	
	frac = parallelism-2;
	
	INV_SQRT_2 = (long long int)round_nearest_even(0.70710678118654752440084436210485*pow(2.0, (double)frac));

	// open the output file 
	ofstream outFile(outputfilename);
	ifstream sincosFile(sinecosinefilename);
	ifstream instrFile(istructionfilename);	
	
	//check if the file are correctly opened
	if(instrFile.is_open() && sincosFile.is_open()){
		if(verbose == true){
			cout << "Files was correctly opened!\n";			
		}
	}else{
		return -1;
	}
	
	//Read and memorize sin and cosine
	
	//Read the first line to know the number of sine and cosin
	getline (sincosFile,line);

	//Convert the first line from string to integer
	sincosNumber = stoi(line);

	//create a vector of the sincos element of the proper lenght
	vector<gon> sincosVector(sincosNumber);
	
	if(verbose==true){
		cout << "There are " << sincosNumber << " sin-cos couples in this simulation\n"; 
	}
	
	unsigned int sincosIndex = 0;

	int val_sin;
	int val_cos;
	char lines[50];
	
	//if there are sincos numbers
	if ( sincosNumber != 0 ) {
		
		//while the file is not finished
		while ( sincosFile.getline(lines, 50)){
	
			cout << lines;

			//read a value
			if (sscanf(lines, "%d %d\n",  &val_sin, &val_cos) == 2){
			
				cout << val_sin << " " << val_cos << "\n";

				//convert the value in floating point and put it inside the vector
				sincosVector[sincosIndex].sin = val_sin;

				//convert the value in floating point and put it inside the vector
				sincosVector[sincosIndex].cos = val_cos;

				//increament the vector index
				sincosIndex ++;
			}

		}

	}
	
	sincosFile.close();
	
	//Read instructions and number of qubits required for the simulation
	
	//Read the first line of the istruction file to know the number of qubits in the simulation
	getline (instrFile,line);
	
	//convert the string to integer
	qubitNumber = stoi(line);
	
	//compute the number of states 2**(qubitNumber)
	stateNumber = 1 << qubitNumber;
	
	if(verbose==true){
		cout << "The number of qubits is equal to " << qubitNumber << "\n";
		cout << "The number of states is equal to " << stateNumber << "\n";
	}
	
	//declere the state vector of the proper dimension
	vector<qstate> stateVector(stateNumber);
	
	//Initalize properly the state vector (|000....00> state)
	stateVector[0].real=1*(long long int)round_nearest_even(pow(2.0, (double) frac));
	stateVector[0].img=0;

	for ( unsigned int i=1; i < stateNumber; i ++ ){
		stateVector[i].real=0;
		stateVector[i].img=0;
	}

	//Print the initial state vector
	if (verbose == true){

		for (unsigned int i=0; i < stateNumber; i ++){

			fprintf(stdout, "%d: %f +j%f\n",i,(float)stateVector[i].real/pow(2.0, (double) frac),(float)stateVector[i].img/pow(2.0, (double) frac));

		}
		fprintf(stdout,"\n");
	}	
	
	//compute and save the interacting couples
	
	//compute the number of couples
	couplesNumber = stateNumber/2;
	
	//declare the matrix of couples of dimensions 2, number of couples and number of quibits
	vector<unsigned int> c(2);
	vector<vector<unsigned int>> gc(couplesNumber, c);
	vector<vector<vector<unsigned int>>> couplesCube(qubitNumber, gc);
	if (verbose == true){
		cout << "Couples vector allocated \n\n";
	}
	
	for( unsigned int target_index = 0; target_index < qubitNumber; target_index ++ ){
		if(verbose == true){
			cout << "For the target index " << target_index << "\n";
		}
		// 2**target index, lenght of the subblock
		lenght = 1 << target_index;
		// range 0 to 2**numberQubit/2**(target_index+1) (the number of sub blocks in the scheme)
		for(unsigned int j = 0; j < (stateNumber >> (target_index+1)); j++){
			// range 0 to lenght of the subblock
			for(unsigned int i = 0; i < lenght; i ++){
				//address equal to j*length +i 
				//val1 i+j*2*lenght 
				couplesCube[target_index][(j << target_index)+i][0] = i+(j<<(target_index+1));
				//val2  i+j*2*lenght+lenght
				couplesCube[target_index][(j << target_index)+i][1] = i+(j<<(target_index+1))+lenght;		
				if(verbose == true){
					cout << "The couple " << (j << target_index)+i << " is: " << i+(j<<(target_index+1)) << " " << i+(j<<(target_index+1))+lenght << "\n";
				}				
			}
		}
		if(verbose == true){
			cout << "\n\n";
		}
	}

	//read the istruction field of each line
    // gate_opcode target_qubit control_qubit immediate
	while ( instrFile.getline(lines, 50)) {
		
		if (sscanf(lines, "%d %d %d %d\n",  &gate, &qtgt, &qctrl, &qimm) == 4){
			
			
			if (verbose){
				cout << "Instruction " << gate << " " << qtgt << " " << qctrl << " " << qimm << "\n";
			}

				  
			//execution of gate
			//presence of control qubit?
			if ( qtgt == qctrl ) {
				
				if (verbose){
					cout << "Apply a gate on qubit " << qtgt << " without control\n";
				}

				//if there is no control, loop on all the possible couples without checking
				for ( unsigned int couples_index = 0; couples_index < couplesNumber; couples_index ++) {

					//based on the gate number, executes the desired gate
					switch (gate){
						
						// x gate
						case 0:
							execute_X( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply x gate \n";
							}
						break;
							
						// y gate
						case 1:
							execute_Y( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply y gate \n";
							}
						break;

						// z gate
						case 2:
							execute_Z( stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply z gate \n";
							}
						break;

						// h gate
						case 3:
							execute_H( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply H gate \n";
							}
						break;
						
						// s gate
						case 4:
							execute_S ( stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply S gate \n";
							}
						break;
						
						// s dagger gate
						case 5:
							execute_SDG ( stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply SDG gate \n";
							}
						break;

						// t gate
						case 6:
							execute_T ( stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply T gate \n";
							}
						break;
						
						// t dagger gate
						case 7:
							execute_TDG ( stateVector[couplesCube[qtgt][couples_index][1]] );
							if (verbose){
								cout << "Apply TDG gate \n";
							}
						break;

						// rx gate
						case 8:
							execute_RX ( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
							if (verbose){
								cout << "Apply rx gate \n";
							}
						break;

						// ry gate
						case 9:
							execute_RY ( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
							if (verbose){
								cout << "Apply ry gate \n";
							}
						break;
		
						// rz gate
						case 10:
							execute_RZ ( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
							if (verbose){
								cout << "Apply rz gate \n";
							}
						break;
						
						// U1 gate
						case 11:
							execute_U1 ( stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
							if (verbose){
								cout << "Apply u1 gate \n";
							}
						break;

						default:
						break;
					}

				}

			//if there is a control, select only the interested couples
			} else {
				
				if (verbose){
					cout << "Apply a gate on qubit " << qtgt << " with control on qubit " << qctrl << "\n";
				}

				for ( unsigned int couples_index = 0; couples_index < couplesNumber; couples_index ++) {

					//if the control acts on one of the possible states, execute the gate
					if ( (couplesCube[qtgt][couples_index][0] >> qctrl ) & 1 ) {

						//based on the gate number, executes the desired gate
						switch (gate){
							
							//execute a cx gate
							case 0:
								execute_X( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply cx gate \n";
								}
							break;

							// execute a cy gate
							case 1:
								execute_Y( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply cy gate \n";
								}
							break;

							// execute a cz gate
							case 2:
								execute_Z( stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply cz gate \n";
								}
							break;

							// execute a ch gate
							case 3:
								execute_H( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply ch gate \n";
								}
							break;
		
							// execute a cs gate
							case 4:
								execute_S ( stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply cs gate \n";
								}
							break;

							// execute a cs dagger gate
							case 5:
								execute_SDG ( stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply csdg gate \n";
								}
							break;
							
							// execute a ct gate
							case 6:
								execute_T ( stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply ct gate \n";
								}
							break;
		
							// execute a ct dagger gate
							case 7:
								execute_TDG ( stateVector[couplesCube[qtgt][couples_index][1]] );
								if (verbose){
									cout << "Apply ctdg gate \n";
								}
							break;

							// execute an crx gate
							case 8:
								execute_RX ( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
								if (verbose){
									cout << "Apply crx gate \n";
								}
							break;

							// execute a cry gate
							case 9:
								execute_RY ( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
								if (verbose){
									cout << "Apply cry gate \n";
								}
							break;

							// exeute a crz gate
							case 10:
								execute_RZ ( stateVector[couplesCube[qtgt][couples_index][0]] , stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
								if (verbose){
									cout << "Apply crz gate \n";
								}
							break;
							
							// execute a cu1 gate
							case 11:
								execute_U1 ( stateVector[couplesCube[qtgt][couples_index][1]] , sincosVector[qimm] );
								if (verbose){
									cout << "Apply cu1 gate \n";
								}
							break;

							default:
								break;
						}
					}

				}


			}
			
			//Print the intermediate state vector
			if (verbose == true){

				for (unsigned int i=0; i < stateNumber; i ++){

					fprintf(stdout, "%d: %f +j%f\n",i,(float)stateVector[i].real/pow(2.0, (double) frac),(float)stateVector[i].img/pow(2.0, (double) frac));

				}
				fprintf(stdout,"\n");
			}
		}
		
	
	}
	
	
	instrFile.close();

	//Print the final state vector
	if (verbose == true){

		for (unsigned int i=0; i < stateNumber; i ++){

			fprintf(stdout, "%d: %f +j%f\n",i,(float)stateVector[i].real/pow(2.0, (double) frac),(float)stateVector[i].img/pow(2.0, (double) frac));

		}
		fprintf(stdout,"\n");
	}
	
	if (verbose == true){
		cout << "I will write in the output file\n";
	}


		
	for (unsigned int i=0; i < stateNumber; i ++){

		outFile << stateVector[i].real << " " << stateVector[i].img << "j\n";
		//re_state[i] = stateVector[i].real;
		//im_state[i] = stateVector[i].img;
	}
	
	if (verbose == true){
		cout << "Output file correctly written \n";
	}

	outFile.close();
	
	//delete[] couplesCube;
	//delete[] stateVector;
	//delete[] sincosVector;

      
    return 0;
	
}
