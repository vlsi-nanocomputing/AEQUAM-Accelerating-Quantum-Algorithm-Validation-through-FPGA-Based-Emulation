### dec_gen.py ###
# Created by Lorenzo Lagostina in 07/10/2022 and revised by Deborah Volpe
# The program allows to create a behavioral description of the ctrl_mask generation block in VHDL


import sys
import math


def dec_gen(qubit_number):

    N = int(qubit_number)

    entityName = 'STATE_DECODER_N_' + qubit_number

    fileOuTName = '../basic_blocks/decoders/src/state_decoder_N_' + qubit_number + '.vhd'

    fileOut = open (fileOuTName, 'w')

    ##### Write entity
    #
    newLine = 'LIBRARY IEEE;\n USE IEEE.STD_LOGIC_1164.ALL;\n ENTITY state_decoder_N_' + qubit_number + ' IS\n PORT (\n ' + entityName + '_IN_QTGT : IN STD_LOGIC_VECTOR( ' + str(math.ceil(math.log2(N))-1) + ' DOWNTO 0);\n ' + entityName + '_IN_QCTRL : IN STD_LOGIC_VECTOR( ' + str(math.ceil(math.log2(N))-1) + ' DOWNTO 0);\n ' + entityName + '_IN_OPCODE : IN STD_LOGIC_VECTOR (3 DOWNTO 0);\n ' + entityName + '_IN_SAVE_QBIT_NUMBER : IN STD_LOGIC;\n ' + entityName + '_IN_CLEAR : IN STD_LOGIC;\n ' + entityName + '_IN_CLK : IN STD_LOGIC;\n ' + entityName + '_OUT_MASK_FIRST : OUT STD_LOGIC;  \n' + entityName + '_OUT_CTRL_MASK : OUT STD_LOGIC_VECTOR ( ' + str((2**N)-1) + ' DOWNTO 0)\n );\n END ENTITY;\n'
    fileOut.write(newLine)
    #
    #####


    ##### Begin architecture and declare components and signals
    #

    newLine = 'ARCHITECTURE generated OF state_decoder_N_' + str(N) + ' IS\n '
    fileOut.write(newLine)

    #register
    newLine = 'COMPONENT n_bit_register IS\n	generic (n_bit: INTEGER);\n	port (REG_IN_DATA: IN STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0);\n		    REG_IN_CLK, REG_IN_CLEAR, REG_IN_ENABLE: IN STD_LOGIC;\n		    REG_OUT_DATA: OUT STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)

    newLine = 'SIGNAL TO_SAVE_BUF, FROM_SAVE_BUF : STD_LOGIC_VECTOR(0 DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL DEC_QCTRL, DEC_USED, QUBIT_USED, QUBIT_MASK, QCTRL_ENABLED_STATES : STD_LOGIC_VECTOR(' + str(N-1) + ' DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL CLR_SAVE_QUBIT, ctrl_tgt_diff  : STD_LOGIC;\n'
    fileOut.write(newLine)
    newLine = 'BEGIN\n'
    fileOut.write(newLine)

    #
    #####

    ##### Generate mask_first
    #

    newLine = '' + entityName + '_OUT_MASK_FIRST <= \'0\' WHEN ' + entityName + '_IN_OPCODE = \"0010\" OR ' + entityName + '_IN_OPCODE = \"0100\" OR ' + entityName + '_IN_OPCODE = \"0101\" OR ' + entityName + '_IN_OPCODE = \"0110\" OR ' + entityName + '_IN_OPCODE = \"0111\" OR ' + entityName + '_IN_OPCODE = \"1011\" ELSE \'1\';\n'
    fileOut.write(newLine)

    #
    #####

    ##### Generate qctrl decoder and qubit mask
    #

    newLine = 'DEC_QCTRL <= \n'
    fileOut.write(newLine)

    for qubit_index in range(N):

        newLine = '\"' + '{0:b}'.format(2**qubit_index).zfill(N) + '\" WHEN ' + entityName + '_IN_QCTRL = \"' + '{0:b}'.format(qubit_index).zfill(math.ceil(math.log2(N))) + '\" ELSE\n'
        fileOut.write(newLine)
    newLine = '(OTHERS => \'0\');\n'
    fileOut.write(newLine)
    newLine = 'ctrl_tgt_diff <= \'1\' WHEN STATE_DECODER_N_' + str(N) + '_IN_QCTRL = STATE_DECODER_N_' + str(N) + '_IN_QTGT ELSE \'0\';\n' 
    fileOut.write(newLine)
    newLine = 'QCTRL_ENABLED_STATES <= (OTHERS => \'1\') WHEN ctrl_tgt_diff = \'1\' ELSE DEC_QCTRL;\n'
    fileOut.write(newLine)

    newLine = 'DEC_USED <= \n'
    fileOut.write(newLine)

    for qubit_index in range(N):

        newLine = '\"' + '{0:b}'.format((2**(qubit_index+1))-1).zfill(N) + '\" WHEN ' + entityName + '_IN_QCTRL = \"' + '{0:b}'.format(qubit_index).zfill(math.ceil(math.log2(N))) + '\" ELSE\n'
        fileOut.write(newLine)
    newLine = '(OTHERS => \'0\');\n'
    fileOut.write(newLine)

    
    for qubit_index in range(N):

        newLine = 'QUBIT_MASK(' + str(qubit_index) + ') <= QCTRL_ENABLED_STATES(' + str(qubit_index) + ') ;\n'
        fileOut.write(newLine)
    

    #
    #####

    ##### Generate registers
    #
    newLine = 'TO_SAVE_BUF(0) <= ' + entityName + '_IN_SAVE_QBIT_NUMBER;\n'
    fileOut.write(newLine)
    
    newLine = 'CLR_SAVE_QUBIT <= ' + entityName + '_IN_CLEAR OR FROM_SAVE_BUF(0);\n'
    fileOut.write(newLine)
    
    newLine = 'REG_SAVE_FLAG : n_bit_register\nGENERIC MAP (1)\nPORT MAP(\n												REG_IN_DATA => TO_SAVE_BUF ,\n												REG_IN_ENABLE => ' + entityName + '_IN_SAVE_QBIT_NUMBER ,\n												REG_IN_CLEAR => CLR_SAVE_QUBIT ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => FROM_SAVE_BUF);\n'
    fileOut.write(newLine)

    newLine = 'REG_SAVE_QUBIT_NUMBER : n_bit_register\nGENERIC MAP (' + str(N) + ')\nPORT MAP(\n												REG_IN_DATA => DEC_USED ,\n												REG_IN_ENABLE => FROM_SAVE_BUF(0) ,\n												REG_IN_CLEAR => ' + entityName + '_IN_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => QUBIT_USED);\n'
    fileOut.write(newLine)
    #
    #####

    ##### Generate mask decoder
    #

    for out_index in range (2**N):

        if out_index == 0:

            newLine = entityName + '_OUT_CTRL_MASK(' + str(out_index) + ') <= ctrl_tgt_diff;\n'
            fileOut.write(newLine)

        else :

            signalList = []

            for qubit_index in range(N):

                if not( (out_index & (2**qubit_index)) == 0 ):
                    newLine = 'QUBIT_MASK(' + str(qubit_index) + ')'
                    signalList.append(newLine)

            newLine = entityName + '_OUT_CTRL_MASK(' + str(out_index) + ') <= ' + ' OR '.join(signalList) + ';\n'
            fileOut.write(newLine)
    #
    #####

    newLine = ''
    fileOut.write(newLine)
    newLine = 'END generated;'
    fileOut.write(newLine)

dec_gen(sys.argv[1])
