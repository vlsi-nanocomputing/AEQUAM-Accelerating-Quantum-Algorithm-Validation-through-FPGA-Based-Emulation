// Probability distribution of eigenstates is
//  0.0842    0.0724    0.0018    0.0017    0.7873    0.0379    0.0127    0.0019

OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c[3];

h q[0];
x q[2];
cx q[0],q[1];
h q[0];
h q[1];
h q[2];
cx q[2],q[1];
h q[1];
h q[2];
u3(-0.58,0,0) q[2];
h q[1];
h q[2];
cx q[2],q[1];
h q[1];
h q[2];
h q[0];
u3(0.58,0,0) q[2];
cx q[0],q[1];
h q[0];