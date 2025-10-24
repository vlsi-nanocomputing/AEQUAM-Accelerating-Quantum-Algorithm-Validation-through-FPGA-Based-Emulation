OPENQASM 2.0;
include "qelib1.inc";

qreg q[4];
creg c[4];

t q[1];
y q[3];
s q[1];
h q[3];
tdg q[1];
z q[3];
cx q[0],q[1];
h q[3];
y q[0];
ry(pi/2) q[1];
cx q[2],q[3];
x q[0];
ry(pi/2) q[1];
x q[3];
h q[0];
ry(pi/2) q[1];
x q[0];
rx(4) q[0];