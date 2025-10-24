OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

h q[0];
h q[1];
cx q[0],q[1];
barrier q[0],q[1];
z q[0];
s q[0];
t q[0];
y q[0];
z q[0];
x q[0];
cx q[1],q[0];
z q[0];
cx q[0],q[1];
z q[0];
cx q[0],q[1];
cx q[1],q[0];
x q[0];
z q[0];
y q[0];
tdg q[0];
sdg q[0];
x q[0];
