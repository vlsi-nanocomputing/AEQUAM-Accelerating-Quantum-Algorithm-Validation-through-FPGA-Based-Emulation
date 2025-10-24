OPENQASM 2.0;
include "qelib1.inc";

qreg q[16];
creg c[16];

ry(2) q[0];
ry(2) q[1];
cx q[0],q[1];
ry(2) q[0];
ry(2) q[1];

ry(2) q[2];
ry(2) q[3];
cx q[2],q[3];

cx q[4],q[5];
ry(2) q[4];
ry(2) q[5];

cx q[6],q[7];

rx(2) q[9];
cx q[8],q[9];

cx q[10],q[11];
rz(2) q[10];
cx q[10],q[11];

cx q[12],q[13];
ry(-2) q[12];
cx q[12],q[13];