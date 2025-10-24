// Probability distribution of eigenstates is
//  0.0348    0.1194    0.0348    0.0797    0.0334    0.4014    0.0335    0.2630

OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
creg c[3];
rx(pi) q[0];
ry(-pi/2) q[1];
cz q[2],q[1];
cz q[0],q[1];
rx(pi/2) q[0];
ry(-pi/4) q[0];
rx(-pi/2) q[0];
rx(-pi/4) q[1];
rx(-3*pi/4) q[2];
ry(-pi/2) q[2];
cz q[2],q[1];
rx(pi/4) q[1];
ry(pi/2) q[2];
rx(pi) q[2];
cz q[0],q[2];
cz q[0],q[1];
rx(-pi/4) q[1];
rx(-pi/4) q[2];
cz q[0],q[2];
ry(pi/2) q[2];
rx(pi) q[2];
cz q[2],q[1];
rx(pi/4) q[1];
ry(pi/2) q[2];
rx(pi) q[2];
cz q[2],q[1];
ry(pi/2) q[1];
rx(pi) q[1];