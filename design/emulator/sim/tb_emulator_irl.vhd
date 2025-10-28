LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
USE STD.TEXTIO.ALL;
USE IEEE.STD_LOGIC_TEXTIO.ALL;

ENTITY tb_emulator IS

END ENTITY;

ARCHITECTURE beh OF tb_emulator IS

	COMPONENT EMULATOR_N_3_W_0_S_0_Q_2 IS
		GENERIC( K : INTEGER := 20 );
		PORT (
			EMULATOR_N_3_W_0_S_0_Q_2_IN_FROM_MCU : IN STD_LOGIC_VECTOR (1 DOWNTO 0);
			EMULATOR_N_3_W_0_S_0_Q_2_IN_CLK : IN STD_LOGIC;
	EMULATOR_N_3_W_0_S_0_Q_2_IN_RSTN : IN STD_LOGIC;
			EMULATOR_N_3_W_0_S_0_Q_2_OUT_TO_MCU : OUT STD_LOGIC_VECTOR (1 DOWNTO 0);
			EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS : INOUT STD_LOGIC_VECTOR (K-1 DOWNTO 0)
		);
	END COMPONENT;

	SIGNAL RST : STD_LOGIC;
	SIGNAL SEND_DATA_DEL : STD_LOGIC := '0';
	SIGNAL CLK_FPGA,START, SEND_DATA, CLK_MCU : STD_LOGIC;
	SIGNAL TO_MCU, FROM_MCU: STD_LOGIC_VECTOR(1 DOWNTO 0);
	SIGNAL TO_INTERFACE : STD_LOGIC_VECTOR(19 DOWNTO 0) := (OTHERS => 'Z');
	SIGNAL INTERFACE, INTERFACE_BUF : STD_LOGIC_VECTOR(19 DOWNTO 0):=(OTHERS => 'Z');

	FILE TEST_FILE, RES_FILE : TEXT;

BEGIN

	DUT : EMULATOR_N_3_W_0_S_0_Q_2  GENERIC MAP (20)
									PORT MAP (
										EMULATOR_N_3_W_0_S_0_Q_2_IN_FROM_MCU => FROM_MCU ,
										EMULATOR_N_3_W_0_S_0_Q_2_IN_CLK => CLK_FPGA ,
										EMULATOR_N_3_W_0_S_0_Q_2_IN_RSTN => RST,
										EMULATOR_N_3_W_0_S_0_Q_2_OUT_TO_MCU => TO_MCU ,
										EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS => INTERFACE
									);

	CLK_GEN_MCU : PROCESS 
	BEGIN
	
		CLK_MCU <= '1';
		WAIT FOR 100 NS;
		CLK_MCU <= '0';
		WAIT FOR 100 NS;
	
	END PROCESS CLK_GEN_MCU;

	CLK_GEN_FPGA : PROCESS 
	BEGIN
	
		CLK_FPGA <= '1';
		WAIT FOR 10 NS;
		CLK_FPGA <= '0';
		WAIT FOR 10 NS;
	
	END PROCESS CLK_GEN_FPGA;

	RST <= '0', '1' AFTER 30 NS;

	START <= '0', '1' AFTER 50 NS;

	FILE_OPEN(TEST_FILE,"test_file.txt",read_mode);
	FILE_OPEN(RES_FILE,"res_file.txt",write_mode);

	
	DEL_DATA : PROCESS
	BEGIN
	
		SEND_DATA_DEL <= '0';
		WAIT FOR 2 NS;
		SEND_DATA_DEL <= SEND_DATA;
		WAIT FOR 8 NS;
	END PROCESS DEL_DATA;

	--INTERFACE_BUF <= TO_INTERFACE WHEN SEND_DATA_DEL = '1' ELSE (OTHERS => 'Z');
	--INTERFACE <= INTERFACE_BUF;
	INTERFACE <= TO_INTERFACE;
	

		
		SEND_DATA <= '0';
	TO_INTERFACE <=	 x"00008" after 400 ns,
					 x"00000" after 800 ns,
					 x"40000" after 1200 ns,
					 x"000c0" after 1600 ns,
					 x"001c0" after 2000 ns,
					 x"00180" after 2400 ns,
					 x"00140" after 2800 ns,
					 x"00100" after 3200 ns,
					 x"00200" after 3600 ns,
					(others => 'Z') after 4000 ns;
					
	FROM_MCU(1) <= '0', '1' after 60 ns, '0' after 1400 ns, '1' after 4200 ns;
	
	FROM_MCU(0) <= '0', '1' after 100 ns, '0' after 140 ns, '1' after 440 ns, '0' after 520 ns,
															'1' after 840 ns, '0' after 920 ns,
															'1' after 1240 ns, '0' after 1320 ns,
															'1' after 1640 ns, '0' after 1720 ns,
															'1' after 2040 ns, '0' after 2120 ns,
															'1' after 2440 ns, '0' after 2520 ns,
															'1' after 2840 ns, '0' after 2920 ns,
															'1' after 3240 ns, '0' after 3320 ns,
															'1' after 3640 ns, '0' after 3720 ns,
															'1' after 4840 ns, '0' after 4920 ns,
															'1' after 5240 ns, '0' after 5320 ns,
															--'1' after 5640 ns, '0' after 5720 ns,
															--'1' after 6040 ns, '0' after 6120 ns,
															--'1' after 6440 ns, '0' after 6520 ns,
															'1' after 6840 ns, '0' after 6920 ns,
															'1' after 7240 ns, '0' after 7320 ns,
															'1' after 7640 ns, '0' after 7720 ns,
															'1' after 8040 ns, '0' after 8120 ns,
															'1' after 8440 ns, '0' after 8520 ns,
															'1' after 8840 ns, '0' after 8920 ns,
															'1' after 9240 ns, '0' after 9320 ns,
															'1' after 9640 ns, '0' after 9720 ns,
															'1' after 10040 ns, '0' after 10120 ns,
															'1' after 10440 ns, '0' after 10520 ns,
															'1' after 10840 ns, '0' after 10920 ns
															;

END beh;