OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c[3];

h q;
ccx q[0],q[1],q[2];
