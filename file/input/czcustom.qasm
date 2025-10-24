OPENQASM 2.0;
include "qelib1.inc";

qreg q[10];
creg c[10];

ry(3.1415926536) q[1];
cz q[0],q[1];
cz q[3],q[2];
x q[3];
ry(pi/2) q[4];
t q[4];
cz q[4],q[5];
ry(2) q[4];
h q[6];
cz q[7],q[6];
h q[6];
ry(pi/2) q[8];
x q[8];
s q[9];
rx(pi/2) q[9];
s q[9];
cz q[9],q[8];
s q[9];
rx(pi/2) q[9];
s q[9];
y q[9];