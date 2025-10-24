### mux_gen.py ###
# Created by Lorenzo Lagostina in 03/10/2022
# The program allows to create a behavioral description of an N-way multiplexer in VHDL


import sys
import math

def mux_gen(mux_numb):

    fileOutName = '../basic_blocks/multiplexers/src/multiplexer_' + mux_numb + '_1.vhd'

    fileOut = open(fileOutName, 'w')

    newLine = ('library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\nENTITY multiplexer_' + mux_numb +'_1 IS \n	GENERIC (K : INTEGER := 20);\n	PORT (\n')
    fileOut.write(newLine)

    for mux_ind in range(int(mux_numb)):

        newLine = ('\t\tMUX_' + mux_numb + '_1_IN_' + str(mux_ind) + ' : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n')

        fileOut.write(newLine)

    newLine = '\t\tMUX_' + mux_numb + '_1_IN_SEL : IN STD_LOGIC_VECTOR (' + str(math.ceil(math.log2(int(mux_numb)))-1) + ' DOWNTO 0);\n		MUX_' + mux_numb + '_1_OUT_RES : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND ENTITY;\n\nARCHITECTURE behavioral OF multiplexer_' + mux_numb + '_1 IS\n\nBEGIN\n\n	MUX_' + mux_numb + '_1_OUT_RES <= \n'
    fileOut.write(newLine)

    for mux_ind in range(int(mux_numb)):

        newLine = '\t\t\t\tMUX_' + mux_numb + '_1_IN_' + str(mux_ind) + ' WHEN MUX_' + mux_numb + '_1_IN_SEL = \"' + '{0:b}'.format(mux_ind).zfill(math.ceil(math.log2(int(mux_numb)))) + '\" ELSE\n'
        fileOut.write(newLine)

    newLine = '\t\t\t\t(OTHERS => \'0\');\n\n\nEND behavioral;'
    fileOut.write(newLine)

    fileOut.close()

mux_gen(sys.argv[1])