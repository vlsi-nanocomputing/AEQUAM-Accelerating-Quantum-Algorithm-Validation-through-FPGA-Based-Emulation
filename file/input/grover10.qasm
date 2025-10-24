// Probability distribution of eigenstates is
//  0.0858    0.0128    0.8159    0.0856

OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];

// Initialization
rx(pi) q[0];
rx(pi) q[1];

// Equal superposition
rx(pi) q[0];
ry(-pi/2) q[0];
rx(pi) q[1];
ry(-pi/2) q[1];

// Oracle
rx(pi) q[0];
cz q[1],q[0];
rx(pi) q[0];

// Diffusion
rx(pi) q[0];
ry(-pi/2) q[0];
rx(pi) q[1];
ry(-pi/2) q[1];
cz q[1],q[0];
rx(pi) q[0];
ry(-pi/2) q[0];
rx(pi) q[1];
ry(-pi/2) q[1];
