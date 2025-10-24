
OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
creg c[2];

// Initialization
rx(pi) q[1];

// First CX
rx(pi) q[0];
ry(-pi/2) q[0];
cz q[1],q[0];
rx(pi) q[0];
ry(-pi/2) q[0];

// Second CX
rx(pi) q[1];
ry(-pi/2) q[1];
cz q[1],q[0];
rx(pi) q[1];
ry(-pi/2) q[1];

// Third CX
rx(pi) q[0];
ry(-pi/2) q[0];
cz q[1],q[0];
rx(pi) q[0];
ry(-pi/2) q[0];