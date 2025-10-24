// quantum Fourier transform
OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
x q[0];
x q[1];
ccx q[0],q[1],q[2];
cx q[0],q[1];
rx(0) q[0];
