// Probability distribution of eigenstates is
//  0.4940    0.0039    0.0003    0.0019    0.0028    0.0003    0.0043    0.4926

OPENQASM 2.0;
include "qelib1.inc";

qreg q[3];
creg c[3];

h q[0];
cx q[0], q[1];
cx q[1], q[2];