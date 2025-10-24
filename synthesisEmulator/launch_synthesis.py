from synthesis_utils import synthesisEmulator
import sys

N = [6]
S = 0
Q = [4]


for n in N:
    W = [1,2]#range(3, n-1)
    for w in W:
        for q in Q:
            path = "SynthesisRes_N_" + format(n) + "_W_" + format(w) + "_S_" + format(S) + "_Q_" + format(q) + "/"
            try:
                synthesisEmulator(n, w,  S, q, path)
            except:
                print("Not available combinations")

            print("\n\n\n\n\nDone with N = ", n, " W = ", w, " S = ", S, " Q = ", q, "\n\n\n\n\n\n")