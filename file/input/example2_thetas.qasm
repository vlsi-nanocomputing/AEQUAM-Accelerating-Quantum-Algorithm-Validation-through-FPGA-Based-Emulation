OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

h q[0];
h q[1];
barrier q;
rz(pi) q[0];
rz(pi/2) q[0];
rz(pi/4) q[0];
rx(pi) q[0];
ry(pi) q[0];
rz(3.14) q[1];
rz(1.57) q[1];
rz(0.785) q[1];
rx(3.14) q[1];
ry(3.14) q[1];
barrier q;
rx(3*pi/2) q[0];
rx(-3*pi/2) q[0];
rx(1.445*pi) q[1];
rx(0.34*pi) q[1];
barrier q;
rx(2*pi) q[0];
rx(-3*pi) q[0];
rx(0.77) q[1];
rx(-0.77) q[1];
barrier q;
rx(3*pi/2) q[0];
rx(-4.713) q[0];
rx(4.713) q[1];
rx(-3*pi/2) q[1];


