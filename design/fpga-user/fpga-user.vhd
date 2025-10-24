library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library lpm;
use lpm.lpm_components.all;
library altera_mf;
use altera_mf.altera_mf_components.all;

entity user is
	port
	(
		-- Main clock inputs
		mainClk	: in std_logic;
		slowClk	: in std_logic;
		-- Main reset input
		reset		: in std_logic;
		-- MCU interface (UART, I2C)
		mcuUartTx	: in std_logic;
		mcuUartRx	: out std_logic;
		mcuI2cScl	: in std_logic;
		mcuI2cSda	: inout std_logic;
		-- Logic state analyzer/stimulator
		lsasBus	: inout std_logic_vector( 31 downto 0 );
		-- Dip switches
		switches	: in std_logic_vector( 7 downto 0 );
		-- LEDs
		leds		: out std_logic_vector( 3 downto 0 )
	);
end user;

architecture behavioural of user is

	signal clk: std_logic;
	signal pllLock: std_logic;

	--signal lsasBusIn: std_logic_vector( 31 downto 0 );
	--signal lsasBusOut: std_logic_vector( 31 downto 0 );
	--signal lsasBusEn: std_logic_vector( 31 downto 0 ) := ( others => '0' );

	signal mcuI2cDIn: std_logic;
	signal mcuI2CDOut: std_logic;
	signal mcuI2cEn: std_logic := '0';	


	component myAltPll
		PORT
		(
			areset		: IN STD_LOGIC  := '0';
			inclk0		: IN STD_LOGIC  := '0';
			c0		: OUT STD_LOGIC ;
			locked		: OUT STD_LOGIC 
		);
	end component;
	
	component EMULATOR_N_3_W_0_S_0_Q_2 is
	GENERIC( K : INTEGER := 20 );
PORT (
	EMULATOR_N_3_W_0_S_0_Q_2_IN_FROM_MCU : IN STD_LOGIC_VECTOR (1 DOWNTO 0);
	EMULATOR_N_3_W_0_S_0_Q_2_IN_CLK : IN STD_LOGIC;
	EMULATOR_N_3_W_0_S_0_Q_2_IN_RSTN : IN STD_LOGIC;
	EMULATOR_N_3_W_0_S_0_Q_2_OUT_TO_MCU : OUT STD_LOGIC_VECTOR (1 DOWNTO 0);
	EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS : INOUT STD_LOGIC_VECTOR (K-1 DOWNTO 0)
	--RETURN_BACK : OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
);
	end component;
	
	--signal bus_buffer: std_logic_vector(19 downto 0);
	
begin

--**********************************************************************************
--* Main clock PLL
--**********************************************************************************

	EMULATOR: EMULATOR_N_3_W_0_S_0_Q_2	GENERIC MAP(20)
													PORT MAP(
														EMULATOR_N_3_W_0_S_0_Q_2_IN_FROM_MCU => lsasBus(31 DOWNTO 30),
														EMULATOR_N_3_W_0_S_0_Q_2_IN_CLK => clk,
														EMULATOR_N_3_W_0_S_0_Q_2_IN_RSTN => switches(0),
														EMULATOR_N_3_W_0_S_0_Q_2_OUT_TO_MCU => lsasBus(29 DOWNTO 28),
														--EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS => bus_buffer--lsasBus(19 DOWNTO 0)
														--RETURN_BACK => lsasBus(27 downto 20)
														EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS(19 downto 9) =>lsasBus(19 downto 9),
														EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS(8) => lsasBus(20),
														EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS(7 downto 0) => lsasBus(7 downto 0)
													);

	myAltPll_inst : myAltPll PORT MAP (
		areset	 => switches(1),
		inclk0	 => mainClk,
		c0	 => clk,
		locked	 => pllLock
	);
	--lsasBus(27) <= clk;
	--lsasBus(26)<=mainClk;

--**********************************************************************************
--* LEDs
--**********************************************************************************

	leds <= lsasBus(31 DOWNTO 28);
	--leds(3) <= '1';
	--bus_buffer <= lsasBus(19 downto 9) & lsasBus(20) & lsasBus(7 downto 0);
	--leds(3 downto 2) <= lsasBus(31 DOWNTO 30);
	--lsasBus(29 DOWNTO 28) <= switches(7 downto 6);
	
--**********************************************************************************
--* Logic state analyzer/stimulator dummy process definition
--* Just a simple up counter
--* 		lsasBus	: inout std_logic_vector( 31 downto 0 )
--**********************************************************************************

	--lsasBusIn <= lsasBus;

	--lsasBus_tristate:
	--process( lsasBusEn, lsasBusOut ) is
	--begin
	--	for index in 0 to 31 loop
	--		if lsasBusEn( index ) = '1'  then
	--			lsasBus( index ) <= lsasBusOut ( index );
	--		else
	--			lsasBus( index ) <= 'Z';
	--		end if;
	--	end loop;
	--end process;
	
end behavioural;
