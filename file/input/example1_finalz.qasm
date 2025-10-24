OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c[3];

h q;
barrier q;
x q[0];
z q[1];
z q[2];
x q[1];
x q[2];
s q[1];
t q[2];
s q[2];
z q[2];
tdg q[2];
sdg q[2];
rz(pi/2) q[2];
barrier q;