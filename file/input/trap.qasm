// quantum ripple-carry adder from Cuccaro et al, quant-ph/0410184



// Cin = q[0]

// A Input = q[1], q[2], q[3], q[4]

// B Input = q[5], q[6], q[7], q[8]

// Cout = q[9]



OPENQASM 2.0;

include "qelib1.inc";



qreg q[10];

creg ans[5];



// set input states

x q[1];

x q[5];

x q[6];

x q[7];

x q[8];



// add a to b, storing result in b



// majority q[0],q[5],q[1];



cx q[1],q[5];

cx q[1],q[0];

