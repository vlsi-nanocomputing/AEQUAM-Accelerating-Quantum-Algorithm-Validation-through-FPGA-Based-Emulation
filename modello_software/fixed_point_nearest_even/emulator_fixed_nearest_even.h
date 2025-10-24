//emulator.h
//create in 22/05/2023
//code developed by Lorenzo Lagostina and Deborah Volpe
//this files containts data structure and functions declarations
#ifndef EMULATOR
#define EMULATOR
using namespace std;

#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <vector>

//data structure for imaginary numbers: real +i img
typedef struct {
    long long int real;
    long long int img;
} qstate;

//data structure for the couple sin-cosine
typedef struct {
    long long int sin;
    long long int cos;
} gon;

//function for nearest even approximation
long long int round_nearest_even(float val);

//considering state x = a+ib and y = c+di

//function for the x gate exectution
//x matrix is equal to ((0, 1)
//                    , (1, 0))
// it correspond to exchange the probability amplitude of 
// the state 0 and the state 1
//x = c+di, y = a+bi
void execute_X (qstate &x, qstate &y);

//function for the y gate exectution
//y matrix is equal to ((0 -i)
//                    , (i, 0))
////x = -ci+d, y = ai-b
void execute_Y (qstate &x, qstate &y);

//function for the z gate exectution
//z matrix is equal to ((1, 0)
//                    , (0, -1))
//change the sign of y
////x = a+bi, y = -c-di
void execute_Z (qstate &y);

//function for the H gate exectution
//H matrix is equal to 1/sqrt(2) ((1, 1)
//                    , (1, -1))
//create superposition
////x = 1/sqrt(2)*(a+bi+c+di), y = 1/sqrt(2)*(a+bi-c-di)
void execute_H (qstate &x, qstate &y);

//function for the sdagger gate exectution
//s matrix is equal to ((1, 0)
//                    , (0, i))
//rotation of pi/2
////x = a+bi, y = ci-d
void execute_S (qstate &y);

//function for the s gate exectution
//s dagger matrix is equal to ((1, 0)
//                           , (0, -i))
//rotation of -pi/2
////x = a+bi, y = -ci+d
void execute_SDG (qstate &y);

//function for the t gate exectution
//t matrix is equal to ((1, 0)
//                    , (0, e^(ipi/4)))
//rotation of pi/4
////x = a+bi, y = 1/sqrt(2)*((c-d) +i(c+d))
void execute_T (qstate &y);

//function for the t dagger gate exectution
//t dagger matrix is equal to ((1, 0)
//                    		 , (0, e^(-ipi/4)))
//rotation of -pi/
////x = a+bi, y = 1/sqrt(2)*((c+d) +i(d-c))
void execute_TDG (qstate &y);

//function for the rx gate exectution
//rx matrix is equal to ((cos(t/2), -isin(t/2))
//                     , (-isin(t/2), cos(t/2))
//rotation of t along the x axis
////x = (acos(t/2)+ dsin(t/2))+i(bcos(t/2)-csin(t/2)), 
////y = (bsin(t/2)+ ccos(t/2))+i(dcos(t/2)-asin(t/2))
void execute_RX (qstate &x, qstate &y, gon &imm);

//function for the ry gate exectution
//ry matrix is equal to ((cos(t/2), -sin(t/2))
//                    , (sin(t/2), cos(t/2))
//rotation of t along the y axis
////x = (acos(t/2) - csin(t/2))+i(bcos(t/2)+dsin(t/2)), 
////y = (asin(t/2)+ccos(t/2))+i(dcos(t/2)+bsin(t/2))
void execute_RY (qstate &x, qstate &y, gon &imm);

//function for the rz gate exectution
//rz matrix is equal to ((e^(-it/2), 0)
//                    , (0, e^it/2)
//rotation of t along the y axis
////x = (acos(t/2) + bsin(t/2))+i(-asin(t/2) + cos(t/2)), 
////y = (ccos(t/2) - dsin(t/2))+i(csin(t/2)+dcos(t/2))
void execute_RZ (qstate &x, qstate &y, gon &imm);

//function for the U1 gate exectution
//U2 matrix is equal to ((1, 0)
//                     , (0, e^il)
//rotation of t along the y axis
////x = a+bi, 
////y = (ccos(l) - dsin(l))+i(csin(l)+dcos(l))
void execute_U1 (qstate &y, gon &imm);


//function for the complete emulation
//it accepts as input the instruction filename, the sinecosine filename and return an array of qstate
int emulatorVLSI_fixed_nearest_even(string istructionfilename, string sinecosinefilename, string outputfilename, int parallelism, bool verbose);

#endif