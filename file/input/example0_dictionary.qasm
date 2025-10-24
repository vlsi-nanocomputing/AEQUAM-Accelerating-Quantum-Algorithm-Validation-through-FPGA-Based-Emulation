OPENQASM 2.0;
include "qelib1.inc";

qreg q[2];
creg c[2];

rx(pi) q[0];
rx(-pi) q[1];

ry(pi) q[0];
ry(-pi) q[1];

rz(pi) q[0];
rz(-pi) q[1];

rz(pi/2) q[0];
rz(-pi/2) q[1];

rz(pi/4) q[0];
rz(-pi/4) q[1];

rx(3.145556) q[0];
rx(-3.143795) q[1];

ry(3.148569) q[0];
ry(-3.1495995) q[1];

rz(3.14859574) q[0];
rz(-3.14121212) q[1];

rz(1.578669) q[0];
rz(-1.57463959) q[1];

rz(0.78548484) q[0];
rz(-0.785373737) q[1];
