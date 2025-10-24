#### emulator_gen.py #### 
# Created by Lorenzo Lagostina in 10/10/2022
# 
# The program allows to automatically write the vhdl description of the top entity of the emulator architecture
# If the decoder or Quantum Emulator Process do not yet exist for the desired parameters, it creates them


import sys
import os
import math
from QEP_gen import QEP_gen
from dec_gen import dec_gen
from mux_gen import mux_gen

def emulator_gen(qubit_number, windowing_order, cu_sharing_order, qimm_parallelism):

    N = int(qubit_number)
    W = int(windowing_order)
    S = int(cu_sharing_order)
    Q = int(qimm_parallelism)


    #Argument correctness chack
    if W > N-1 or S > N-W-1:

        print('ILLEGAL windowing order\n')
        exit(-1)


    # Creates missing components
    QPEFile = '../QPE/QEP_N_' + qubit_number +'_W_' + windowing_order + '_S_' + cu_sharing_order + '.vhd'

    if not(os.path.exists(QPEFile)):
        QEP_gen(qubit_number=qubit_number,windowing_order=windowing_order,cu_sharing_order=cu_sharing_order)

    decFile = '../basic_blocks/decoders/src/state_decoder_N_' + qubit_number + '.vhd'

    if not(os.path.exists(decFile)):
        dec_gen(qubit_number=qubit_number)

    muxFile = '../basic_blocks/multiplexers/src/multiplexer_' + str(2**Q) + '_1.vhd'

    if not(os.path.exists(muxFile)):

        mux_gen(str(2**Q))


    ##### Header and entity
    #
    entityName = 'EMULATOR_N_' + qubit_number +'_W_' + windowing_order + '_S_' + cu_sharing_order + '_Q_' + qimm_parallelism
    fileOutName = '../emulator/src/' + entityName + '.vhd'
    fileOut = open(fileOutName, 'w')

    newLine = 'LIBRARY IEEE;\nUSE IEEE.STD_LOGIC_1164.ALL;\n\nENTITY ' + entityName + ' IS\nGENERIC( K : INTEGER := 20 );\nPORT (\n'
    fileOut.write(newLine)

    newLine = '\t' + entityName + '_IN_FROM_MCU : IN STD_LOGIC_VECTOR (1 DOWNTO 0);\n'
    fileOut.write(newLine)
    
    newLine = '\t' + entityName + '_IN_CLK : IN STD_LOGIC;\n'
    fileOut.write(newLine)
    
    newLine = '\t' + entityName + '_IN_RSTN : IN STD_LOGIC;\n'
    fileOut.write(newLine)

    newLine = '\t' + entityName + '_OUT_TO_MCU : OUT STD_LOGIC_VECTOR (1 DOWNTO 0);\n'
    fileOut.write(newLine)

    newLine = '\t' + entityName + '_IN_OUT_BUS : INOUT STD_LOGIC_VECTOR (K-1 DOWNTO 0)\n'
    fileOut.write(newLine)

    newLine = ');\nEND ENTITY;\n'
    fileOut.write(newLine)
    #
    #####


    ##### Begin architecture and declare components
    #

    newLine = 'ARCHITECTURE generated OF ' + entityName + ' IS\n'
    fileOut.write(newLine)
    
    # QPE control
    newLine = 'COMPONENT QPE_control IS\n'
    fileOut.write(newLine)
    newLine = 'PORT (\n		QPE_CONTROL_IN_FROM_MCU : IN STD_LOGIC_VECTOR (1 DOWNTO 0);\n		QPE_CONTROL_IN_ACK : IN STD_LOGIC;\n		QPE_CONTROL_IN_COMPLETED : IN STD_LOGIC;\n      QPE_CONTROL_IN_GATE_COMP : IN STD_LOGIC;\n		QPE_CONTROL_IN_CLK : IN STD_LOGIC;\n        QPE_CONTROL_IN_RSTN : IN STD_LOGIC;\n		QPE_CONTROL_OUT_TO_MCU : OUT STD_LOGIC_VECTOR (1 DOWNTO 0);\n		QPE_CONTROL_OUT_CLR_ALL : OUT STD_LOGIC;\n		QPE_CONTROL_OUT_SAVE_QUBIT_NUMB : OUT STD_LOGIC;\n		QPE_CONTROL_OUT_SAMPLE_INSTR : OUT STD_LOGIC;\n		QPE_CONTROL_OUT_SAMPLE_SIN_COS : OUT STD_LOGIC;\n		QPE_CONTROL_OUT_SAVE_SIN_COS : OUT STD_LOGIC;\n		QPE_CONTROL_OUT_EN_RES_CNT : OUT STD_LOGIC;\n       QPE_CONTROL_OUT_EN_OUT_BUF : OUT STD_LOGIC;\n       QPE_CONTROL_OUT_MCU_ACK_TOGGLE : OUT STD_LOGIC;\nQPE_CONTROL_OUT_EN_QEP_DONE : OUT STD_LOGIC\n	);\n'
    fileOut.write(newLine)
    newLine = 'END COMPONENT;\n'
    fileOut.write(newLine)

    # Counter
    newLine = 'COMPONENT counter IS\n'
    fileOut.write(newLine)
    newLine = 'GENERIC (N : NATURAL := 32);\nPORT (\nCOUNTER_IN_EN : IN STD_LOGIC;\nCOUNTER_IN_CLR : IN STD_LOGIC;\nCOUNTER_IN_CLK : IN STD_LOGIC;\nCOUNTER_OUT_DATA : OUT STD_LOGIC_VECTOR(N-1 DOWNTO 0)\n);\n'
    fileOut.write(newLine)
    newLine = 'END COMPONENT;'
    fileOut.write(newLine)

    #register
    newLine = 'COMPONENT n_bit_register IS\n	generic (n_bit: INTEGER);\n	port (REG_IN_DATA: IN STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0);\n		    REG_IN_CLK, REG_IN_CLEAR, REG_IN_ENABLE: IN STD_LOGIC;\n		    REG_OUT_DATA: OUT STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)
    
    #Component mux_2_1
    newLine = 'COMPONENT multiplexer_2_1 IS\n	GENERIC (K : INTEGER := 20);\n	PORT (\n		MUX_2_1_IN_0 : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n		MUX_2_1_IN_1 : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n		MUX_2_1_IN_SEL : IN STD_LOGIC_VECTOR (0 DOWNTO 0);\n		MUX_2_1_OUT_RES : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)

    #Component mux_2**Q_1
    newLine = 'COMPONENT multiplexer_' + str(2**Q) + '_1 IS\n	GENERIC (K : INTEGER := 20);\n	PORT (\n'
    fileOut.write(newLine)

    for input_ind in range(2**Q):
        newLine = '\t\tMUX_' + str(2**Q) + '_1_IN_' + str(input_ind) + ' : IN STD_LOGIC_VECTOR (K-1 DOWNTO 0);\n'
        fileOut.write(newLine)
    newLine = '		MUX_' + str(2**Q) + '_1_IN_SEL : IN STD_LOGIC_VECTOR (' + str(Q-1) + ' DOWNTO 0);\n		MUX_' + str(2**Q) + '_1_OUT_RES : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND COMPONENT;\n'
    fileOut.write(newLine)

    # decoder
    decName = 'STATE_DECODER_N_' + qubit_number
    newLine = 'COMPONENT state_decoder_N_' + qubit_number + ' IS\n PORT (\n ' + decName + '_IN_QTGT : IN STD_LOGIC_VECTOR( ' + str(math.ceil(math.log2(N))-1) + ' DOWNTO 0);\n ' + decName + '_IN_QCTRL : IN STD_LOGIC_VECTOR( ' + str(math.ceil(math.log2(N))-1) + ' DOWNTO 0);\n ' + decName + '_IN_OPCODE : IN STD_LOGIC_VECTOR (3 DOWNTO 0);\n ' + decName + '_IN_SAVE_QBIT_NUMBER : IN STD_LOGIC;\n ' + decName + '_IN_CLEAR : IN STD_LOGIC;\n ' + decName + '_IN_CLK : IN STD_LOGIC;\n ' + decName + '_OUT_MASK_FIRST : OUT STD_LOGIC;  \n' + decName + '_OUT_CTRL_MASK : OUT STD_LOGIC_VECTOR ( ' + str((2**N)-1) + ' DOWNTO 0)\n );\n END COMPONENT;\n'
    fileOut.write(newLine)

    # QEP
    QEPName = 'QEP_N_' + qubit_number +'_W_' + windowing_order + '_S_' + cu_sharing_order

    newLine = 'COMPONENT ' + QEPName + ' IS \n	GENERIC (K : INTEGER := 20);\n	PORT (\n'
    fileOut.write(newLine)
    
    newLine = '\t\t' + QEPName + '_IN_START : IN STD_LOGIC;\n\t\t' + QEPName + '_IN_QTGT : IN STD_LOGIC_VECTOR (' + str(math.ceil(math.log2(N))-1) +' DOWNTO 0); \n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_CTRL_MASK : IN STD_LOGIC_VECTOR(' + str((2**N)-1) +' DOWNTO 0);\n\t\t'+ QEPName + '_IN_OPCODE : IN STD_LOGIC_VECTOR(3 DOWNTO 0);\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_SIN : IN STD_LOGIC_VECTOR(K-1 DOWNTO 0);\n\t\t' + QEPName + '_IN_COS : IN STD_LOGIC_VECTOR(K-1 DOWNTO 0);\n'
    fileOut.write(newLine)

    if W > 0:
        newLine  ='\t\t' + QEPName + '_IN_WIN_SEL : IN STD_LOGIC_VECTOR (' + str(W-1) + ' DOWNTO 0);\n'
        fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_OUT_STATE_SEL : IN STD_LOGIC_VECTOR(' + str(N-1) + ' DOWNTO 0);\n\t\t' + QEPName + '_IN_REAL_IMAG_SEL : IN STD_LOGIC_VECTOR (0 DOWNTO 0);\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_CLK : IN STD_LOGIC;\n\t\t' + QEPName + '_IN_CLEAR : IN STD_LOGIC;\n\t\t' + QEPName + '_IN_MASK_FIRST_COEFF : IN STD_LOGIC;\n\t\t' + QEPName + '_IN_ENABLE_STATE_UPDATE : IN STD_LOGIC;\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_OUT_DONE : OUT STD_LOGIC;\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_OUT_DATA : OUT STD_LOGIC_VECTOR (K-1 DOWNTO 0));\nEND COMPONENT\n;'
    fileOut.write(newLine)

    #
    #####



    ##### Signal declaration
    #

    #QPE control
    newLine = 'SIGNAL FROM_QPE_CTRL_EN_QEP_DONE, GATE_COMPLETE, FETCH_INSTRUCTION, TO_QPE_CTRL_ACK, TO_QPE_CTRL_COMPLETE, FROM_QPE_CTRL_SAMPLE_SIN_COS, FROM_QPE_CTRL_SAVE_SIN_COS, FROM_QPE_CTRL_CLEAR, FROM_QPE_CTRL_SAMPLE_INSTR, FROM_QPE_CTRL_SAVE_QBIT_NUMB, FROM_QPE_CTRL_EN_RES_CNT : STD_LOGIC;\n'
    fileOut.write(newLine)

    #Sin cos addresses
    newLine = 'SIGNAL FROM_TRIG_ADD_SIN_COS_ADD : STD_LOGIC_VECTOR(' + qimm_parallelism + ' DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL FROM_DEC_MASK_FIRST : STD_LOGIC;\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL FROM_DEC_QIMM : STD_LOGIC_VECTOR(' + str(Q-1) + ' DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL FROM_TRIG_UNIT_SIN, FROM_TRIG_UNIT_COS, FROM_FETCH_SIN_COS : STD_LOGIC_VECTOR (K-1 DOWNTO 0);'
    fileOut.write(newLine)

    newLine = 'SIGNAL ROW_SEL_SIN_COS, ENABLE_SIN_DEC, ENABLE_COS_DEC : STD_LOGIC_VECTOR( ' + str((2**Q)-1) + ' DOWNTO 0);\n'
    fileOut.write(newLine)


    #FROM_SIN_REG
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**Q):

        newLine += 'FROM_SIN_REG_' + str(sig_ind)

        if sig_ind != (2**Q)-1:
            newLine += ','
    newLine += ': STD_LOGIC_VECTOR(K-1 DOWNTO 0);\n'
    fileOut.write(newLine)

    #FROM_COS_REG
    newLine = 'SIGNAL '
    
    for sig_ind in range(2**Q):

        newLine += 'FROM_COS_REG_' + str(sig_ind)

        if sig_ind != (2**Q)-1:
            newLine += ','
    newLine += ': STD_LOGIC_VECTOR(K-1 DOWNTO 0);\n'
    fileOut.write(newLine)

   

    newLine = 'SIGNAL ENABLE_SIN_REG, ENABLE_COS_REG : STD_LOGIC;\n'
    fileOut.write(newLine)

    
    newLine = 'SIGNAL FROM_FETCH_INSTR : STD_LOGIC_VECTOR(' + str(Q + 3 + 2*(math.ceil(math.log2(N)))) + ' DOWNTO 0);'
    fileOut.write(newLine)
    newLine = 'SIGNAL CTRL_MASK : STD_LOGIC_VECTOR ( ' + str((2**N)-1) + ' DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL OPCODE : STD_LOGIC_VECTOR (3 DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL QTGT, QCTRL : STD_LOGIC_VECTOR (' + str(math.ceil(math.log2(N)) -1 ) + ' DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL FROM_QEP_DONE, QEP_DONE_ENABLED, TO_QEP_START, TO_QEP_START_PIPE :STD_LOGIC;\n'
    fileOut.write(newLine)

    if W > 0:
        newLine = 'SIGNAL FROM_WIN_CNT_TC : STD_LOGIC;\n'
        fileOut.write(newLine)
        newLine = 'SIGNAL WINDOW_SELECTOR : STD_LOGIC_VECTOR( ' + str(W-1) + ' DOWNTO 0);\n'
        fileOut.write(newLine)
        
    newLine = 'SIGNAL RESULT_SELECTOR : STD_LOGIC_VECTOR(' + str(N) + ' DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL BUFFER_IN, BUFFER_OUT, RESULT : STD_LOGIC_VECTOR(K-1 DOWNTO 0);\n'
    fileOut.write(newLine)
    newLine = 'SIGNAL OUT_BUF_EN, MCU_ACK_TOGGLE : STD_LOGIC;\n'
    fileOut.write(newLine)
    
    
    #
    #####
    
    ##### Begin and connections
    #
    newLine = 'BEGIN\n'
    fileOut.write(newLine)

    # QPE control
    newLine = 'QPE_CTRL: QPE_control PORT MAP(\n		QPE_CONTROL_IN_FROM_MCU => ' + entityName + '_IN_FROM_MCU ,\n		QPE_CONTROL_IN_ACK => TO_QPE_CTRL_ACK ,\n		QPE_CONTROL_IN_COMPLETED => TO_QPE_CTRL_COMPLETE , \n       QPE_CONTROL_IN_GATE_COMP => GATE_COMPLETE,\n		QPE_CONTROL_IN_CLK => ' + entityName + '_IN_CLK ,\n     QPE_CONTROL_IN_RSTN => ' + entityName + '_IN_RSTN,\n		QPE_CONTROL_OUT_TO_MCU => ' + entityName + '_OUT_TO_MCU ,\n		QPE_CONTROL_OUT_CLR_ALL => FROM_QPE_CTRL_CLEAR ,\n		QPE_CONTROL_OUT_SAVE_QUBIT_NUMB => FROM_QPE_CTRL_SAVE_QBIT_NUMB ,\n		QPE_CONTROL_OUT_SAMPLE_INSTR => FROM_QPE_CTRL_SAMPLE_INSTR ,\n		QPE_CONTROL_OUT_SAMPLE_SIN_COS => FROM_QPE_CTRL_SAMPLE_SIN_COS ,\n		QPE_CONTROL_OUT_SAVE_SIN_COS => FROM_QPE_CTRL_SAVE_SIN_COS ,\n		QPE_CONTROL_OUT_EN_RES_CNT => FROM_QPE_CTRL_EN_RES_CNT,\n     QPE_CONTROL_OUT_EN_OUT_BUF => OUT_BUF_EN,\n     QPE_CONTROL_OUT_MCU_ACK_TOGGLE => MCU_ACK_TOGGLE,\nQPE_CONTROL_OUT_EN_QEP_DONE =>	FROM_QPE_CTRL_EN_QEP_DONE);\n'
    fileOut.write(newLine)

    # Trig counter
    newLine = 'CNT_TRIG_ADD : counter GENERIC MAP (' + str(Q+1) + ')\nPORT MAP (\nCOUNTER_IN_EN => FROM_QPE_CTRL_SAVE_SIN_COS ,\nCOUNTER_IN_CLR => FROM_QPE_CTRL_CLEAR,\nCOUNTER_IN_CLK => ' + entityName + '_IN_CLK,\nCOUNTER_OUT_DATA => FROM_TRIG_ADD_SIN_COS_ADD);\n'
    fileOut.write(newLine)
    
    ##### Trigronometric address selector
    #
    newLine = 'ENABLE_SIN_REG <= FROM_QPE_CTRL_SAVE_SIN_COS AND ( NOT FROM_TRIG_ADD_SIN_COS_ADD(0) );\n'
    fileOut.write(newLine)

    newLine = 'ENABLE_COS_REG <= FROM_QPE_CTRL_SAVE_SIN_COS AND FROM_TRIG_ADD_SIN_COS_ADD(0);\n'
    fileOut.write(newLine)
    #newLine = 'MUX_TRIG_ADD_SELECTION : multiplexer_2_1 GENERIC MAP (K => ' + qimm_parallelism + ')\n									PORT MAP (\n\t\t								MUX_2_1_IN_0 => FROM_DEC_QIMM ,\n\t\t								MUX_2_1_IN_1 => FROM_TRIG_ADD_SIN_COS_ADD(' + qimm_parallelism + ' DOWNTO 1) ,\n\t\t\t\t                    			MUX_2_1_IN_SEL => FROM_QPE_CTRL_SAVE_SIN_COS ,\n										MUX_2_1_OUT_RES => SEL_TRIG_ADD\n									);\n'
    #fileOut.write(newLine)
    newLine = 'ROW_SEL_SIN_COS <= \n'
    fileOut.write(newLine)

    for sin_cos_index in range(2**Q):

        newLine = '\"' + '{0:b}'.format(2**sin_cos_index).zfill(2**Q) + '\" WHEN FROM_TRIG_ADD_SIN_COS_ADD( ' + qimm_parallelism + ' DOWNTO 1) = \"' + '{0:b}'.format(sin_cos_index).zfill(Q) + '\" ELSE\n'
        fileOut.write(newLine)
    newLine = '(OTHERS => \'0\');\n'
    fileOut.write(newLine)

    for sin_cos_ind in range(2**Q):

        newLine = 'ENABLE_SIN_DEC(' + str(sin_cos_ind) + ') <= ENABLE_SIN_REG AND ROW_SEL_SIN_COS(' + str(sin_cos_ind) + ');\n'
        fileOut.write(newLine)
        newLine = 'ENABLE_COS_DEC(' + str(sin_cos_ind) + ') <= ENABLE_COS_REG AND ROW_SEL_SIN_COS(' + str(sin_cos_ind) + ');\n'
        fileOut.write(newLine)

    #
    #####
    
    # Sin Cos regs

    for reg_ind in range(2**Q):
        
        newLine = 'SIN_REG_' + str(reg_ind) + ' : n_bit_register\nGENERIC MAP (K)\nPORT MAP(\n												REG_IN_DATA => FROM_FETCH_SIN_COS ,\n												REG_IN_ENABLE => ENABLE_SIN_DEC(' + str(reg_ind) + ') ,\n												REG_IN_CLEAR => FROM_QPE_CTRL_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => FROM_SIN_REG_' + str(reg_ind) + ');\n'
        fileOut.write(newLine)

        newLine = 'COS_REG_' + str(reg_ind) + ' : n_bit_register\nGENERIC MAP (K)\nPORT MAP(\n												REG_IN_DATA => FROM_FETCH_SIN_COS ,\n												REG_IN_ENABLE => ENABLE_COS_DEC(' + str(reg_ind) + ') ,\n												REG_IN_CLEAR => FROM_QPE_CTRL_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => FROM_COS_REG_' + str(reg_ind) + ');\n'
        fileOut.write(newLine)

    
    ##### Sin Cos selection mux
    #
    newLine = 'SIN_SELECTION : multiplexer_' + str(2**Q) + '_1 	GENERIC MAP (K)\n									PORT MAP (\n'
    fileOut.write(newLine)

    for sin_cos_ind in range(2**Q):

        newLine = '\t\t								MUX_' + str(2**Q) + '_1_IN_' + str(sin_cos_ind) + ' => FROM_SIN_REG_' + str(sin_cos_ind) + ' ,\n'
        fileOut.write(newLine)
							
    newLine ='\t\t\t\t                    			MUX_' + str(2**Q) + '_1_IN_SEL => FROM_DEC_QIMM ,\n										MUX_' + str(2**Q) + '_1_OUT_RES => FROM_TRIG_UNIT_SIN\n									);\n'
    fileOut.write(newLine)

    newLine = 'COS_SELECTION : multiplexer_' + str(2**Q) + '_1 	GENERIC MAP (K)\n									PORT MAP (\n'
    fileOut.write(newLine)

    for sin_cos_ind in range(2**Q):

        newLine = '\t\t								MUX_' + str(2**Q) + '_1_IN_' + str(sin_cos_ind) + ' => FROM_COS_REG_' + str(sin_cos_ind) + ' ,\n'
        fileOut.write(newLine)
							
    newLine ='\t\t\t\t                    			MUX_' + str(2**Q) + '_1_IN_SEL => FROM_DEC_QIMM ,\n										MUX_' + str(2**Q) + '_1_OUT_RES => FROM_TRIG_UNIT_COS\n									);\n'
    fileOut.write(newLine)
    #
    #####

    ##### Fetch registers
    #

    newLine = 'BUFFER_IN <= ' + entityName + '_IN_OUT_BUS;\n'
    fileOut.write(newLine)

    newLine = 'REG_FETCH_SIN_COS : n_bit_register\nGENERIC MAP (K)\nPORT MAP(\n												REG_IN_DATA => BUFFER_IN ,\n												REG_IN_ENABLE => FROM_QPE_CTRL_SAMPLE_SIN_COS ,\n												REG_IN_CLEAR => FROM_QPE_CTRL_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => FROM_FETCH_SIN_COS);\n'
    fileOut.write(newLine)

    newLine = 'FETCH_INSTRUCTION <= FROM_QPE_CTRL_SAMPLE_INSTR;\n'
    fileOut.write(newLine)

    newLine = 'TO_QPE_CTRL_ACK <= FROM_QPE_CTRL_SAMPLE_SIN_COS OR FETCH_INSTRUCTION;\n'
    fileOut.write(newLine)
    newLine = 'REG_FETCH_INSTR : n_bit_register\nGENERIC MAP (' + str(Q + 4 + 2*(math.ceil(math.log2(N)))) + ')\nPORT MAP(\n												REG_IN_DATA => BUFFER_IN(' + str(Q + 3 + 2*(math.ceil(math.log2(N)))) + ' DOWNTO 0) ,\n												REG_IN_ENABLE => FETCH_INSTRUCTION ,\n												REG_IN_CLEAR => FROM_QPE_CTRL_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA => FROM_FETCH_INSTR);\n'
    fileOut.write(newLine)


    #
    #####

    ##### Decoding stage
    #

    newLine = 'DEC_STAGE : state_decoder_N_' + qubit_number + ' \n PORT MAP (\n ' + decName + '_IN_QTGT => QTGT,\n ' + decName + '_IN_QCTRL => FROM_FETCH_INSTR( ' + str(Q + math.ceil(math.log2(N))-1) + ' DOWNTO ' + str(Q) + '),\n ' + decName + '_IN_OPCODE => FROM_FETCH_INSTR(' + str(Q + 3 + 2*math.ceil(math.log2(N))) + ' DOWNTO ' + str(Q + 2*math.ceil(math.log2(N))) + '),\n ' + decName + '_IN_SAVE_QBIT_NUMBER => FROM_QPE_CTRL_SAVE_QBIT_NUMB,\n ' + decName + '_IN_CLEAR => FROM_QPE_CTRL_CLEAR,\n ' + decName + '_IN_CLK => ' + entityName + '_IN_CLK,\n ' + decName + '_OUT_MASK_FIRST => FROM_DEC_MASK_FIRST, \n' + decName + '_OUT_CTRL_MASK => CTRL_MASK\n );\n'
    fileOut.write(newLine)


    newLine = 'FROM_DEC_QIMM <= FROM_FETCH_INSTR (' + str(Q-1) + ' DOWNTO 0);\n'
    fileOut.write(newLine)

    newLine = 'OPCODE <= FROM_FETCH_INSTR(' + str(Q + 3 + 2*(math.ceil(math.log2(N)))) + ' DOWNTO ' + str(Q + 2*(math.ceil(math.log2(N)))) + ');\n'
    fileOut.write(newLine)

    newLine = 'QTGT <= FROM_FETCH_INSTR(' + str(Q -1 + 2*(math.ceil(math.log2(N)))) + ' DOWNTO ' + str(Q + (math.ceil(math.log2(N)))) + ');\n'
    fileOut.write(newLine)

    #newLine = 'QTGT <= FROM_FETCH_INSTR(' + str(Q -1 + (math.ceil(math.log2(N)))) + ' DOWNTO ' + str(Q) + ');\n'
    #fileOut.write(newLine)

    #
    #####

    ##### Enable qep done
    #

    
    newLine = 'QEP_DONE_ENABLED <= FROM_QPE_CTRL_EN_QEP_DONE AND FROM_QEP_DONE;\n'
    fileOut.write(newLine)

    #
    #####



    ##### Window selection cnt
    #

    if W > 0:

        newLine = 'CNT_WIN_SEL : counter GENERIC MAP (' + str(W) + ')\nPORT MAP (\nCOUNTER_IN_EN => QEP_DONE_ENABLED ,\nCOUNTER_IN_CLR => FROM_QPE_CTRL_CLEAR,\nCOUNTER_IN_CLK => ' + entityName + '_IN_CLK,\nCOUNTER_OUT_DATA => WINDOW_SELECTOR);\n'
        fileOut.write(newLine)
        newLine = 'FROM_WIN_CNT_TC <= \'1\' WHEN WINDOW_SELECTOR = \"' + '{0:b}'.format((2**W)-1).zfill(W) + '\" ELSE \'0\';\n'
        fileOut.write(newLine)
        newLine = 'GATE_COMPLETE <= FROM_WIN_CNT_TC AND FROM_QEP_DONE AND QEP_DONE_ENABLED;\n'
        fileOut.write(newLine)
    else :
        newLine = 'GATE_COMPLETE <= QEP_DONE_ENABLED;\n'
        fileOut.write(newLine)
    #
    #####

    ##### Results counter
    #

    newLine = 'CNT_RES_SEL : counter GENERIC MAP (' + str(N+1) + ')\nPORT MAP (\nCOUNTER_IN_EN => FROM_QPE_CTRL_EN_RES_CNT ,\nCOUNTER_IN_CLR => FROM_QPE_CTRL_CLEAR,\nCOUNTER_IN_CLK => ' + entityName + '_IN_CLK,\nCOUNTER_OUT_DATA => RESULT_SELECTOR);\n'
    fileOut.write(newLine)
    
    newLine = 'TO_QPE_CTRL_COMPLETE <= \'1\' WHEN RESULT_SELECTOR = \"' + '{0:b}'.format((2**(N+1))-1).zfill(N+1) + '\" ELSE \'0\';\n'
    fileOut.write(newLine)

    #
    #####

    ##### QEP
    #

    newLine = 'TO_QEP_START_PIPE <= FETCH_INSTRUCTION AND NOT FROM_QPE_CTRL_SAVE_QBIT_NUMB;\n'
    fileOut.write(newLine)

    newLine = 'REG_START_PIPE : n_bit_register\nGENERIC MAP (1)\nPORT MAP(\n												REG_IN_DATA(0) => TO_QEP_START_PIPE ,\n												REG_IN_ENABLE => \'1\' ,\n												REG_IN_CLEAR => FROM_QPE_CTRL_CLEAR ,\n												REG_IN_CLK => ' + entityName + '_IN_CLK ,\n												REG_OUT_DATA(0) => TO_QEP_START);\n'
    fileOut.write(newLine)

    newLine = 'QEP_UNIT : ' + QEPName + ' \n	GENERIC MAP (K)\n	PORT MAP (\n'
    fileOut.write(newLine)
    
    newLine = '\t\t' + QEPName + '_IN_START => TO_QEP_START,\n\t\t' + QEPName + '_IN_QTGT => QTGT, \n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_CTRL_MASK => CTRL_MASK,\n\t\t'+ QEPName + '_IN_OPCODE => OPCODE,\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_SIN => FROM_TRIG_UNIT_SIN,\n\t\t' + QEPName + '_IN_COS => FROM_TRIG_UNIT_COS ,\n'
    fileOut.write(newLine)

    if W > 0:
        newLine  ='\t\t' + QEPName + '_IN_WIN_SEL => WINDOW_SELECTOR ,\n'
        fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_OUT_STATE_SEL => RESULT_SELECTOR(' + str(N) + ' DOWNTO 1) ,\n\t\t' + QEPName + '_IN_REAL_IMAG_SEL => RESULT_SELECTOR(0 DOWNTO 0),\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_IN_CLK => ' + entityName + '_IN_CLK,\n\t\t' + QEPName + '_IN_CLEAR  => FROM_QPE_CTRL_CLEAR,\n\t\t' + QEPName + '_IN_MASK_FIRST_COEFF => FROM_DEC_MASK_FIRST,\n\t\t' + QEPName + '_IN_ENABLE_STATE_UPDATE => FROM_QPE_CTRL_EN_QEP_DONE,\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_OUT_DONE => FROM_QEP_DONE,\n'
    fileOut.write(newLine)

    newLine = '\t\t' + QEPName + '_OUT_DATA => RESULT);\n'
    fileOut.write(newLine)

    newLine = 'BUFFER_OUT <= RESULT WHEN OUT_BUF_EN = \'1\' ELSE (OTHERS => \'Z\');\n'
    fileOut.write(newLine)
    #
    #####
    
    newLine = '' + entityName + '_IN_OUT_BUS <= BUFFER_OUT;\n'
    fileOut.write(newLine)
    #
    #####



    newLine = 'END generated;\n'
    fileOut.write(newLine)


    

emulator_gen(sys.argv[1], sys.argv[2],sys.argv[3], sys.argv[4])
