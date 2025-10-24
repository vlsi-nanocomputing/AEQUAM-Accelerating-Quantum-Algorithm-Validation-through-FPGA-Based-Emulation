OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

x q[0];
x q[1];
h q[0];
h q[1];
cx q[0],q[1];
rx(pi/4) q[0];
z q[1];
t q[0];
ry(pi/2) q[1];
z q[1];
ry(pi/3) q[0];
s q[0];
ry(pi/2) q[0];
rx(pi/8) q[0];
t q[0];
rx(pi/2) q[0];
ry(pi/2) q[0];
rx(pi/5) q[0];
s q[0];
z q[0];
ry(pi/6) q[0];