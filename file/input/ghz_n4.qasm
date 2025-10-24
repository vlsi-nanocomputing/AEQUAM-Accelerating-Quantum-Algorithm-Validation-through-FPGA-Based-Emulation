// Probability distribution of eigenstates is
// 0.4898    0.0043    0.0006    0.0022    0.0004    0.0003    0.0002    0.0023    0.0044    0.0005    0.0004    0.0002    0.0033    0.0006    0.0044    0.4861

OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
creg c[4];
ry(pi/2) q[0];
rx(pi) q[0];
ry(pi/2) q[1];
rx(pi) q[1];
cz q[0],q[1];
ry(pi/2) q[1];
rx(pi) q[1];
ry(pi/2) q[2];
rx(pi) q[2];
cz q[1],q[2];
ry(pi/2) q[2];
rx(pi) q[2];
ry(pi/2) q[3];
rx(pi) q[3];
cz q[2],q[3];
ry(pi/2) q[3];
rx(pi) q[3];