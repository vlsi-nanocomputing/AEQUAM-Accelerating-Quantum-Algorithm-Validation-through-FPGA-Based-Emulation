OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

s q[0];
x q[2];
x q[0];
x q[2];
z q[0];
cx q[2],q[3];
cx q[0],q[1];
t q[2];
y q[2];