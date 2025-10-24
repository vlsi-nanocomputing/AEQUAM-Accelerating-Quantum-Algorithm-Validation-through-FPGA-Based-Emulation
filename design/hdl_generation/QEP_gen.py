### QEP_gen.py ###
# Created by Lorenzo Lagostina in 04/10/2022
# The program generate a VHDL description of the Quantum Emulator Processor
# User can specify qubit number (N), windowing order (W), degree of shared datapath per CU (S) , and, eventually, the employed architecture of the sub-blocks


from hashlib import new
from re import T
from mux_gen import mux_gen
import sys
import os.path
import math


def QEP_gen(qubit_number, windowing_order, cu_sharing_order):

    N = int(qubit_number)
    W = int(windowing_order)
    S = int(cu_sharing_order)

    if W > N-1 or S > N-W-1:

        print('ILLEGAL windowing order\n')
        exit(-1)

    ##### Check if the necessary multiplexers have been generated, if not, generates them #####
    #
    muxFile = '../basic_blocks/multiplexers/src/multiplexer_' + qubit_number + '_1.vhd'

    if not(os.path.exists(muxFile)):

        mux_gen(qubit_number)

    muxFile = '../basic_blocks/multiplexers/src/multiplexer_' + str(2**N) + '_1.vhd'

    if not(os.path.exists(muxFile)):

        mux_gen(str(2**N))

    muxFile = '../basic_blocks/multiplexers/src/multiplexer_' + str(2**W) + '_1.vhd'

    if not(os.path.exists(muxFile)):

        mux_gen(str(2**W))

    #
    #####



    ##### Write file header and entity #####
    #
    entityName = 'QEP_N_' + qubit_number +'_W_' + windowing_order + '_S_' + cu_sharing_order
   
    fileOutName = '../QEP/src/' + entityName + '.vhd'
    fileOut = open(fileOutName, 'w')

    

    newLine = 'library IEEE;\nuse IEEE.STD_LOGIC_1164.ALL;\nENTITY ' + entityName + ' IS \n	GENERIC (K : INTEGER := 20);\n	PORT (\n'
    fileOut.write(newLine)
    
    newLine = '\t\t' + entityName + '_IN_START : IN STD_LOGIC;\n\t\t' + entityName + '_IN_QTGT : IN STD_LOGIC_VECTOR (' + str(math.ceil(math.log2(N))-1) +' DOWNTO 0);  \n'
    fileOut.write(newLine)

    newLine = '\t\t' + entityName + '_IN_CTRL_MASK : IN STD_LOGIC_VECTOR(' + str((2**N)-1) +' DOWNTO 0);\n\t\t'+ entityName + '_IN_OPCODE : IN STD_LOGIC_VECTOR(3 DOWNTO 0);\n'
    fileOut.write(newLine)

    newLine = '\t\t' + entityName + '_IN_SIN : IN STD_LOGIC_VECTOR(K-1 DOWNTO 0);\n\t\t' + entityName + '_IN_COS : IN STD_LOGIC_VECTOR(K-1 DOWNTO 0);\n'
    fileOut.write(newLine)

    if W > 0:
        newLine  ='\t\t' + entityName + '_IN_WIN_SEL : IN STD_LOGIC_VECTOR (' + str(W-1) + ' DOWNTO 0);\n'
        fileOut.write(newLine)

    newLine = '\t\t' + entityName + '_IN_OUT_STATE_SEL : IN STD_LOGIC_VECTOR(' + str(N-1) + ' DOWNTO 0);\n\t\t' + entityName + '_IN_REAL_IMAG_SEL : IN STD_LOGIC_VECTOR (0 DOWNTO 0);\n'
    fileOut.write(newLine)

    newLine = '\t\t' + entityName + '_IN_CLK : IN STD_LOGIC;\n\t\t' + entityName + '_IN_CLEAR : IN STD_LOGIC;\n\t\t' + entityName + '_IN_MASK_FIRST_COEFF : IN STD_LOGIC;\n\t\t' + entityName + '_IN_ENABLE_STATE_UPDATE : IN STD_LOGIC;\n'
    fileOut.write(newLine)

    newLine = '\t\t' + entityName + '_OUT_DONE : OUT STD_LOGIC;\n'
    fileOut.write(newLine)

    newLine = '\t\t' + entityName + '_OUT_DATA : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND ENTITY;'
    fileOut.write(newLine)
    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Write architecture begin and components #####
    #

    newLine = 'ARCHITECTURE generated OF ' + entityName + ' IS\n'
    fileOut.write(newLine)

    #Component mux_2_1
    newLine = 'COMPONENT multiplexer_2_1 IS\n	GENERIC (K : INTEGER := 20);\n	PORT (\n		MUX_2_1_IN_0 : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n		MUX_2_1_IN_1 : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n		MUX_2_1_IN_SEL : IN STD_LOGIC_VECTOR (0 DOWNTO 0);\n		MUX_2_1_OUT_RES : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)

    if N != 2 :
        #Component mux_N_1
        newLine = 'COMPONENT multiplexer_' + str(N) + '_1 IS\n	GENERIC (K : INTEGER := 20);\n	PORT (\n'
        fileOut.write(newLine)

        for input_ind in range(N):
            newLine = '\t\tMUX_' + str(N) + '_1_IN_' + str(input_ind) + ' : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n'
            fileOut.write(newLine)
        newLine = '		MUX_' + str(N) + '_1_IN_SEL : IN STD_LOGIC_VECTOR (' + str(math.ceil(math.log2(int(N)))-1) + ' DOWNTO 0);\n		MUX_' + str(N) + '_1_OUT_RES : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND COMPONENT;\n'
        fileOut.write(newLine)

    #Component mux_2**N_1
    newLine = 'COMPONENT multiplexer_' + str(2**N) + '_1 IS\n	GENERIC (K : INTEGER := 20);\n	PORT (\n'
    fileOut.write(newLine)

    for input_ind in range(2**N):
        newLine = '\t\tMUX_' + str(2**N) + '_1_IN_' + str(input_ind) + ' : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n'
        fileOut.write(newLine)
    newLine = '		MUX_' + str(2**N) + '_1_IN_SEL : IN STD_LOGIC_VECTOR (' + str(N-1) + ' DOWNTO 0);\n		MUX_' + str(2**N) + '_1_OUT_RES : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)

    if (2**W) != N and (2**W) != 2 and W>0:
        #Component mux_2**W_1
        newLine = 'COMPONENT multiplexer_' + str(2**W) + '_1 IS\n	GENERIC (K : INTEGER := 20);\n	PORT (\n'
        fileOut.write(newLine)

        for input_ind in range(2**W):
            newLine = '\t\tMUX_' + str(2**W) + '_1_IN_' + str(input_ind) + ' : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n'
            fileOut.write(newLine)
        newLine = '		MUX_' + str(2**W) + '_1_IN_SEL : IN STD_LOGIC_VECTOR (' + str(W-1) + ' DOWNTO 0);\n		MUX_' + str(2**W) + '_1_OUT_RES : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND COMPONENT;\n'
        fileOut.write(newLine)

    #register
    newLine = 'COMPONENT n_bit_register IS\n	generic (n_bit: INTEGER);\n	port (REG_IN_DATA: IN STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0);\n		    REG_IN_CLK, REG_IN_CLEAR, REG_IN_ENABLE: IN STD_LOGIC;\n		    REG_OUT_DATA: OUT STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)

    #register initialized to 1
    newLine = 'COMPONENT n_bit_register_clear_1 IS\n	generic (n_bit: INTEGER);\n	port (REG_IN_DATA: IN STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0);\n		    REG_IN_CLK, REG_IN_CLEAR, REG_IN_ENABLE: IN STD_LOGIC;\n		    REG_OUT_DATA: OUT STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)


    #Datapath
    newLine = 'COMPONENT datapath is\n    GENERIC (K : INTEGER := 20);	--K represents the chosen parallelism\n	PORT(\n		--Data signals\n		DATAPATH_IN_A : IN STD_LOGIC_VECTOR (2*K-1 DOWNTO 0);\n		DATAPATH_IN_B : IN STD_LOGIC_VECTOR (2*K-1 DOWNTO 0);\n		DATAPATH_IN_SINE : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n		DATAPATH_IN_COSINE : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n		DATAPATH_IN_PIPE : IN STD_LOGIC_VECTOR (2 DOWNTO 0);\n		DATAPATH_IN_LD : IN STD_LOGIC_VECTOR (2 DOWNTO 0);\n		DATAPATH_IN_MUX_CTRL : IN STD_LOGIC_VECTOR (24 DOWNTO 0);\n		DATAPATH_IN_SUB : IN STD_LOGIC_VECTOR (1 DOWNTO 0);\n		DATAPATH_IN_SAVED : IN STD_LOGIC_VECTOR (2 DOWNTO 0);\n		DATAPATH_IN_CLEAR : IN STD_LOGIC;\n		DATAPATH_IN_CLK : IN STD_LOGIC;\n		DATAPATH_OUT_A : OUT STD_LOGIC_VECTOR (2*K-1 DOWNTO 0);\n		DATAPATH_OUT_B : OUT STD_LOGIC_VECTOR (2*K-1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)

    #Control Unit
    newLine = 'COMPONENT control_unit IS\n 	PORT (\n		--Input signals\n		CONTROL_UNIT_IN_START : IN STD_LOGIC;\n		CONTROL_UNIT_IN_OPCODE : IN STD_LOGIC_VECTOR(3 DOWNTO 0);\n		CONTROL_UNIT_IN_CLK : IN STD_LOGIC;\n		CONTROL_UNIT_IN_CLEAR : IN STD_LOGIC;\n		CONTROL_UNIT_OUT_PIPE: OUT STD_LOGIC_VECTOR (2 DOWNTO 0);\n		CONTROL_UNIT_OUT_LD : OUT STD_LOGIC_VECTOR (2 DOWNTO 0);\n		CONTROL_UNIT_OUT_MUX_CTRL : OUT STD_LOGIC_VECTOR (24 DOWNTO 0);\n		CONTROL_UNIT_OUT_SUB : OUT STD_LOGIC_VECTOR (1 DOWNTO 0);\n		CONTROL_UNIT_OUT_SAVED : OUT STD_LOGIC_VECTOR (2 DOWNTO 0);\n		CONTROL_UNIT_OUT_DONE : OUT STD_LOGIC);\nEND COMPONENT;\n'
    fileOut.write(newLine)

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Signal declaration
    #

    #TO_STATE_REG
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**N):

        newLine += 'TO_STATE_REG_' + str(sig_ind)

        if sig_ind != (2**N)-1:
            newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)
    
    #FROM_STATE_REG
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**N):

        newLine += 'FROM_STATE_REG_' + str(sig_ind)

        if sig_ind != (2**N)-1:
            newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)
    
    
    #FROM_SELECTION_UNIT
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**N):

        newLine += 'FROM_SELECTION_UNIT_' + str(sig_ind)

        if sig_ind != (2**N)-1:
            newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)
    

    #FROM_WINDOW
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**(N-W)):

        newLine += 'FROM_WINDOW_' + str(sig_ind)

        if sig_ind != (2**(N-W))-1:
            newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)
    
    #MASKED_INPUT
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**(N-W)):

        if sig_ind % 2 == 0:
            newLine += 'MASKED_INPUT_' + str(sig_ind)

            if sig_ind != (2**(N-W))-2:
                newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)
    
    

    #FROM_DATAPATHS
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**(N-W)):

        newLine += 'FROM_DATAPATHS_' + str(sig_ind)

        if sig_ind != (2**(N-W))-1:
            newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)
    
    #FROM_CONTROL_UNITS
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**(N-W-S)):

        newLine += 'FROM_CONTROL_UNITS_' + str(sig_ind)

        if sig_ind != (2**(N-W-S))-1:
            newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)

    #UNWINDOWED
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**(N)):

        newLine += 'UNWINDOWED_' + str(sig_ind)

        if sig_ind != (2**(N))-1:
            newLine += ','
        
    newLine += ': STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)

    # Update signals

    newLine = 'SIGNAL FROM_WINDOW_DEC_MASK : STD_LOGIC_VECTOR(' + str((2**W)-1) + ' DOWNTO 0);\n'
    fileOut.write(newLine)

    newLine = 'SIGNAL UNWINDOWED_MASK, REORDERED_MASK, STATE_UPDATE_MASK : STD_LOGIC_VECTOR(' + str((2**N)-1) + ' DOWNTO 0);\n'
    fileOut.write(newLine)

    #SELECTED_OUTPUT
    newLine = 'SIGNAL SELECTED_OUTPUT: STD_LOGIC_VECTOR((2*K)-1 DOWNTO 0);\n'
    fileOut.write(newLine)

    # Done signal
    newLine = 'SIGNAL FROM_FIRST_CU_DONE : STD_LOGIC;\n'
    fileOut.write(newLine)
    

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)
    

    ##### Component architecture selection and begin
    #

    newLine = 'BEGIN\n'
    fileOut.write(newLine)
    

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)
    
    ##### Write state register
    #

    newLine = 'STATE_REG_0 : n_bit_register_clear_1\nGENERIC MAP (2*K)\nPORT MAP(\n												REG_IN_DATA => TO_STATE_REG_0 ,\n												REG_IN_ENABLE => STATE_UPDATE_MASK(0) ,\n												REG_IN_CLEAR => ' + entityName + '_IN_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => FROM_STATE_REG_0);\n'
    fileOut.write(newLine)

    for reg_ind in range(2**N):

        if reg_ind != 0:
        
            newLine = 'STATE_REG_' + str(reg_ind) + ' : n_bit_register\nGENERIC MAP (2*K)\nPORT MAP(\n												REG_IN_DATA => TO_STATE_REG_' + str(reg_ind) + ' ,\n												REG_IN_ENABLE => STATE_UPDATE_MASK(' + str(reg_ind) + ') ,\n												REG_IN_CLEAR => ' + entityName + '_IN_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => FROM_STATE_REG_' + str(reg_ind) + ');\n'
            fileOut.write(newLine)

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Compute inputs of multiplexers for selection and reordening
    #

    reorderList = []
    for i in range(N):
        sigList = []
        for t in range(2**N):
            sigList.append(0)
        reorderList.append(sigList)

    inputList = []

    for target_index in range(N):

        sigList = []
        reordInd = 0
        for branch_index in range(2**(N-target_index-1)):

            for block_index in range(2**(target_index)):

                firstVal = (branch_index * (2**(target_index+1))) + block_index
                sigList.append(firstVal)

                reorderList[target_index][firstVal] = reordInd

                reordInd += 1

                secondVal = firstVal + (2**target_index)
                sigList.append(secondVal)

                reorderList[target_index][secondVal] = reordInd
                reordInd += 1


        inputList.append(sigList)
    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Write multiplexers for the selection unit
    #

    for mux_ind in range(2**N):

        newLine = 'MUX_SEL_UNIT_' + str(mux_ind) + ' : multiplexer_' + str(N) + '_1 	GENERIC MAP (2*K)\n									PORT MAP (\n'
        fileOut.write(newLine)

        for target_index in range(N):

            newLine = '\t\t								MUX_' + str(N) + '_1_IN_' + str(target_index) + ' => FROM_STATE_REG_' + str(inputList[target_index][mux_ind]) + ' ,\n'
            fileOut.write(newLine)
							
        newLine ='\t\t\t\t                    			MUX_' + str(N) + '_1_IN_SEL => ' + entityName + '_IN_QTGT ,\n										MUX_' + str(N) + '_1_OUT_RES => FROM_SELECTION_UNIT_' + str(mux_ind) + '\n									);\n'
        fileOut.write(newLine)

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Write multiplexers for windowing structure
    #

    if W > 0:

        for mux_ind in range(2**(N-W)):

            newLine = 'MUX_WINDOWING_UNIT_' + str(mux_ind) + ' : multiplexer_' + str(2**W) + '_1 	GENERIC MAP (2*K)\n									PORT MAP (\n'
            fileOut.write(newLine)

            for windowing_index in range(2**W):

                newLine = '\t\t								MUX_' + str(2**W) + '_1_IN_' + str(windowing_index) + ' => FROM_SELECTION_UNIT_' + str(mux_ind + (windowing_index * (2**(N-W)))) + ' ,\n'
                fileOut.write(newLine)
            
            newLine ='\t\t\t\t                    			MUX_' + str(2**W) + '_1_IN_SEL => ' + entityName + '_IN_WIN_SEL ,\n										MUX_' + str(2**W) + '_1_OUT_RES => FROM_WINDOW_' + str(mux_ind) + '\n									);\n'
            fileOut.write(newLine)

    #
    #####

    ##### Mask of the first coefficient of the couple 
    #

    for mask_ind in range(2**(N-W)):

        if mask_ind % 2 == 0:

            if W > 0 :

                newLine = 'MASKED_INPUT_' + str(mask_ind) + ' <= FROM_WINDOW_' + str(mask_ind) + ' WHEN ' + entityName + '_IN_MASK_FIRST_COEFF = \'1\' ELSE (OTHERS => \'0\');\n'
                fileOut.write(newLine)

            else :
                newLine = 'MASKED_INPUT_' + str(mask_ind) + ' <= FROM_SELECTION_UNIT_' + str(mask_ind) + ' WHEN ' + entityName + '_IN_MASK_FIRST_COEFF = \'1\' ELSE (OTHERS => \'0\');\n'
                fileOut.write(newLine)
                

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Decode window selection in binary format
    #


    if W > 0:
        
        newLine = 'FROM_WINDOW_DEC_MASK <= \n'
        fileOut.write(newLine)

        for wind_ind in range(2**W):

            newLine = '\"' + '{0:b}'.format(2**wind_ind).zfill(2**W) + '\" WHEN ' + entityName + '_IN_WIN_SEL = \"' + '{0:b}'.format(wind_ind).zfill(math.ceil(W)) + '\" ELSE\n'
            fileOut.write(newLine)
        newLine = '(OTHERS => \'0\');\n'
        fileOut.write(newLine)


    else :
        newLine = 'FROM_WINDOW_DEC_MASK <= "1";\n'
        fileOut.write(newLine)
        
    
    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Un-window update signals
    #
    """
    for unwin_ind in range(2**N):

        if unwin_ind % 2 == 0:
            newLine = 'UNWINDOWED_MASK(' + str(unwin_ind) + ') <= ' + entityName + '_IN_MASK_FIRST_COEFF AND FROM_WINDOW_DEC_MASK(' + str(unwin_ind % (2**(N-W))) + ');\n'
            fileOut.write(newLine)
        else :
            newLine = 'UNWINDOWED_MASK(' + str(unwin_ind) + ') <= FROM_WINDOW_DEC_MASK(' + str(wind_ind) + ');\n'
            fileOut.write(newLine)
    """
    for wind_ind in range(2**W):

        for sig_ind in range(2**(N-W)):
            
            if sig_ind % 2 == 0:
                newLine = 'UNWINDOWED_MASK(' + str(sig_ind + (wind_ind * (2**(N-W)))) + ') <= ' + entityName + '_IN_MASK_FIRST_COEFF AND FROM_WINDOW_DEC_MASK(' + str(wind_ind) + ');\n'
                fileOut.write(newLine)
            else :
                newLine = 'UNWINDOWED_MASK(' + str(sig_ind + (wind_ind* (2**(N-W)))) + ') <= FROM_WINDOW_DEC_MASK(' + str(wind_ind) + ');\n'
                fileOut.write(newLine)
    

    #
    #####newLine = '\n'
    fileOut.write(newLine)

    ##### Write multiplexers for update reordening
    #

    for mux_ind in range(2**N):

        newLine = 'MUX_REORD_UPDATE_' + str(mux_ind) + ' : multiplexer_' + str(N) + '_1 	GENERIC MAP (1)\n									PORT MAP (\n'
        fileOut.write(newLine)

        for target_index in range(N):

            newLine = '\t\t								MUX_' + str(N) + '_1_IN_' + str(target_index) + ' => UNWINDOWED_MASK(' + str(reorderList[target_index][mux_ind]) + ' DOWNTO ' + str(reorderList[target_index][mux_ind]) + ') ,\n'
            fileOut.write(newLine)
							
        newLine ='\t\t\t\t                    			MUX_' + str(N) + '_1_IN_SEL => ' + entityName + '_IN_QTGT ,\n										MUX_' + str(N) + '_1_OUT_RES => REORDERED_MASK(' + str(mux_ind) + ' DOWNTO ' + str(mux_ind) + ')\n									);\n'
        fileOut.write(newLine)

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Generate update mask
    #

    for sig_ind in range(2**N):

        newLine = 'STATE_UPDATE_MASK(' + str(sig_ind) + ') <= ' + entityName + '_IN_ENABLE_STATE_UPDATE AND FROM_FIRST_CU_DONE AND REORDERED_MASK(' + str(sig_ind) + ') AND ' + entityName + '_IN_CTRL_MASK(' + str(sig_ind) + ');\n'
        fileOut.write(newLine)

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)


    ##### Write control units
    #
    newLine = entityName + '_OUT_DONE <= FROM_FIRST_CU_DONE;\n'
    fileOut.write(newLine)

    for cu_index in range(2**(N-W-S-1)):

        #Connect the done signal of only the first CU to the uputput one of the QEP
        if cu_index == 0:
            newLine = 'CONTROL_UNIT_' + str(cu_index) + ' : control_unit PORT MAP(\n		CONTROL_UNIT_IN_START =>  ' + entityName + '_IN_START,\n		CONTROL_UNIT_IN_OPCODE => '+ entityName + '_IN_OPCODE ,\n		CONTROL_UNIT_IN_CLK => '+ entityName + '_IN_CLK ,\n		CONTROL_UNIT_IN_CLEAR => '+ entityName + '_IN_CLEAR ,\n		CONTROL_UNIT_OUT_PIPE => FROM_CONTROL_UNITS_' + str(cu_index) + '(35 DOWNTO 33) ,\n		CONTROL_UNIT_OUT_LD => FROM_CONTROL_UNITS_' + str(cu_index) + '(32 DOWNTO 30) ,\n		CONTROL_UNIT_OUT_MUX_CTRL => FROM_CONTROL_UNITS_' + str(cu_index) + '(29 DOWNTO 5) ,\n		CONTROL_UNIT_OUT_SUB => FROM_CONTROL_UNITS_' + str(cu_index) + '(4 DOWNTO 3) ,\n		CONTROL_UNIT_OUT_SAVED => FROM_CONTROL_UNITS_' + str(cu_index) + '(2 DOWNTO 0) ,\n		CONTROL_UNIT_OUT_DONE => FROM_FIRST_CU_DONE );\n'
            fileOut.write(newLine)

        else :
            newLine = 'CONTROL_UNIT_' + str(cu_index) + ' : control_unit PORT MAP(\n		CONTROL_UNIT_IN_START =>  ' + entityName + '_IN_START,\n		CONTROL_UNIT_IN_OPCODE => '+ entityName + '_IN_OPCODE ,\n		CONTROL_UNIT_IN_CLK => '+ entityName + '_IN_CLK ,\n		CONTROL_UNIT_IN_CLEAR => '+ entityName + '_IN_CLEAR ,\n		CONTROL_UNIT_OUT_PIPE => FROM_CONTROL_UNITS_' + str(cu_index) + '(35 DOWNTO 33) ,\n		CONTROL_UNIT_OUT_LD => FROM_CONTROL_UNITS_' + str(cu_index) + '(32 DOWNTO 30) ,\n		CONTROL_UNIT_OUT_MUX_CTRL => FROM_CONTROL_UNITS_' + str(cu_index) + '(29 DOWNTO 5) ,\n		CONTROL_UNIT_OUT_SUB => FROM_CONTROL_UNITS_' + str(cu_index) + '(4 DOWNTO 3) ,\n		CONTROL_UNIT_OUT_SAVED => FROM_CONTROL_UNITS_' + str(cu_index) + '(2 DOWNTO 0));\n'
            fileOut.write(newLine)

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Write datapaths
    #

    if W > 0:
        for dp_index in range(2**(N-W-1)):

            #if dp_index % 2 == 0:    
            newLine = 'DATAPATH_' + str(dp_index) + ': datapath GENERIC MAP (K => K)\n        PORT MAP(\n            DATAPATH_IN_A => MASKED_INPUT_' + str( 2*dp_index ) + ' ,\n            DATAPATH_IN_B => FROM_WINDOW_' + str( 2*dp_index + 1 ) + ' ,\n            DATAPATH_IN_SINE => ' + entityName + '_IN_SIN ,\n            DATAPATH_IN_COSINE => ' + entityName + '_IN_COS ,\n            DATAPATH_IN_PIPE => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(35 DOWNTO 33) ,\n            DATAPATH_IN_LD => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(32 DOWNTO 30) ,\n            DATAPATH_IN_MUX_CTRL => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(29 DOWNTO 5) ,\n            DATAPATH_IN_SUB => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(4 DOWNTO 3) ,\n            DATAPATH_IN_SAVED => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(2 DOWNTO 0) ,\n            DATAPATH_IN_CLEAR => ' + entityName + '_IN_CLEAR ,\n            DATAPATH_IN_CLK => ' + entityName + '_IN_CLK ,\n             DATAPATH_OUT_A => FROM_DATAPATHS_' + str( 2*dp_index ) + ' ,\n            DATAPATH_OUT_B => FROM_DATAPATHS_' + str( 2*dp_index + 1 ) + ');\n'
            fileOut.write(newLine)
            #else :
                #newLine = 'DATAPATH_' + str(dp_index) + ': datapath GENERIC MAP (K => K)\n        PORT MAP(\n            DATAPATH_IN_A => FROM_WINDOW_' + str( 2*dp_index ) + ' ,\n            DATAPATH_IN_B => FROM_WINDOW_' + str( 2*dp_index + 1 ) + ' ,\n            DATAPATH_IN_SINE => ' + entityName + '_IN_SIN ,\n            DATAPATH_IN_COSINE => ' + entityName + '_IN_COS ,\n            DATAPATH_IN_PIPE => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(35 DOWNTO 33) ,\n            DATAPATH_IN_LD => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(32 DOWNTO 30) ,\n            DATAPATH_IN_MUX_CTRL => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(29 DOWNTO 5) ,\n            DATAPATH_IN_SUB => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(4 DOWNTO 3) ,\n            DATAPATH_IN_SAVED => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(2 DOWNTO 0) ,\n            DATAPATH_IN_CLEAR => ' + entityName + '_IN_CLEAR ,\n            DATAPATH_IN_CLK => ' + entityName + '_IN_CLK ,\n             DATAPATH_OUT_A => FROM_DATAPATHS_' + str( 2*dp_index ) + ' ,\n            DATAPATH_OUT_B => FROM_DATAPATHS_' + str( 2*dp_index + 1 ) + ');\n'
                #fileOut.write(newLine)
    else :
        for dp_index in range(2**(N-W-1)):

            #if dp_index % 2 == 0:
            newLine = 'DATAPATH_' + str(dp_index) + ': datapath GENERIC MAP (K => K)\n        PORT MAP(\n            DATAPATH_IN_A => MASKED_INPUT_' + str( 2*dp_index ) + ' ,\n            DATAPATH_IN_B => FROM_SELECTION_UNIT_' + str( 2*dp_index + 1 ) + ' ,\n            DATAPATH_IN_SINE => ' + entityName + '_IN_SIN ,\n            DATAPATH_IN_COSINE => ' + entityName + '_IN_COS ,\n            DATAPATH_IN_PIPE => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(35 DOWNTO 33) ,\n            DATAPATH_IN_LD => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(32 DOWNTO 30) ,\n            DATAPATH_IN_MUX_CTRL => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(29 DOWNTO 5) ,\n            DATAPATH_IN_SUB => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(4 DOWNTO 3) ,\n            DATAPATH_IN_SAVED => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(2 DOWNTO 0) ,\n            DATAPATH_IN_CLEAR => ' + entityName + '_IN_CLEAR ,\n            DATAPATH_IN_CLK => ' + entityName + '_IN_CLK ,\n             DATAPATH_OUT_A => FROM_DATAPATHS_' + str( 2*dp_index ) + ' ,\n            DATAPATH_OUT_B => FROM_DATAPATHS_' + str( 2*dp_index + 1 ) + ');\n'
            fileOut.write(newLine)
            #else :
                #newLine = 'DATAPATH_' + str(dp_index) + ': datapath GENERIC MAP (K => K)\n        PORT MAP(\n            DATAPATH_IN_A => FROM_SELECTION_UNIT_' + str( 2*dp_index ) + ' ,\n            DATAPATH_IN_B => FROM_SELECTION_UNIT_' + str( 2*dp_index + 1 ) + ' ,\n            DATAPATH_IN_SINE => ' + entityName + '_IN_SIN ,\n            DATAPATH_IN_COSINE => ' + entityName + '_IN_COS ,\n            DATAPATH_IN_PIPE => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(35 DOWNTO 33) ,\n            DATAPATH_IN_LD => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(32 DOWNTO 30) ,\n            DATAPATH_IN_MUX_CTRL => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(29 DOWNTO 5) ,\n            DATAPATH_IN_SUB => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(4 DOWNTO 3) ,\n            DATAPATH_IN_SAVED => FROM_CONTROL_UNITS_' + str(dp_index//(2**S)) + '(2 DOWNTO 0) ,\n            DATAPATH_IN_CLEAR => ' + entityName + '_IN_CLEAR ,\n            DATAPATH_IN_CLK => ' + entityName + '_IN_CLK ,\n             DATAPATH_OUT_A => FROM_DATAPATHS_' + str( 2*dp_index ) + ' ,\n            DATAPATH_OUT_B => FROM_DATAPATHS_' + str( 2*dp_index + 1 ) + ');\n'
                #fileOut.write(newLine)

    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Un-windowing
    #

    for unwin_ind in range(2**N):

        newLine = 'UNWINDOWED_' + str(unwin_ind) + ' <= FROM_DATAPATHS_' + str(unwin_ind % (2**(N-W))) + ';\n'
        fileOut.write(newLine)
    #
    #####

    newLine = '\n'
    fileOut.write(newLine)


    ##### Write reordening unit
    #

    for mux_ind in range(2**N):

        newLine = 'MUX_REORD_UNIT_' + str(mux_ind) + ' : multiplexer_' + str(N) + '_1 	GENERIC MAP (2*K)\n									PORT MAP (\n'
        fileOut.write(newLine)

        for target_index in range(N):

            newLine = '\t\t								MUX_' + str(N) + '_1_IN_' + str(target_index) + ' => UNWINDOWED_' + str(reorderList[target_index][mux_ind]) + ' ,\n'
            fileOut.write(newLine)
							
        newLine ='\t\t\t\t                    			MUX_' + str(N) + '_1_IN_SEL => ' + entityName + '_IN_QTGT ,\n										MUX_' + str(N) + '_1_OUT_RES => TO_STATE_REG_' + str(mux_ind) + '\n									);\n'
        fileOut.write(newLine)


    #
    #####

    newLine = '\n'
    fileOut.write(newLine)

    ##### Output selection multiplexer
    #

    newLine = 'MUX_OUTPUT_SELECTION : multiplexer_' + str(2**N) + '_1 	GENERIC MAP (2*K)\n									PORT MAP (\n'
    fileOut.write(newLine)

    for state_ind in range(2**N):

        newLine = '\t\t								MUX_' + str(2**N) + '_1_IN_' + str(state_ind) + ' => FROM_STATE_REG_' + str(state_ind) + ' ,\n'
        fileOut.write(newLine)
							
    newLine ='\t\t\t\t                    			MUX_' + str(2**N) + '_1_IN_SEL => ' + entityName + '_IN_OUT_STATE_SEL ,\n										MUX_' + str(2**N) + '_1_OUT_RES => SELECTED_OUTPUT\n									);\n'
    fileOut.write(newLine)


    newLine = 'MUX_REAL_IMAG_SELECTION : multiplexer_2_1 GENERIC MAP (K => K)\n									PORT MAP (\n\t\t								MUX_2_1_IN_0 => SELECTED_OUTPUT((2*K-1) DOWNTO K),\n\t\t								MUX_2_1_IN_1 => SELECTED_OUTPUT((K-1) DOWNTO 0),\n\t\t\t\t                    			MUX_2_1_IN_SEL => ' + entityName + '_IN_REAL_IMAG_SEL ,\n										MUX_2_1_OUT_RES => ' + entityName + '_OUT_DATA\n									);\n'
    fileOut.write(newLine)

    #
    #####


    newLine = '\n'
    fileOut.write(newLine)
    newLine = 'END generated;'
    fileOut.write(newLine)
    
    
QEP_gen(sys.argv[1], sys.argv[2], sys.argv[3])