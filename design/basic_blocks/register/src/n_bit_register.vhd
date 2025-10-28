LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.all;
use ieee.numeric_std.all;

ENTITY n_bit_register IS
	generic (n_bit: INTEGER);
	port (REG_IN_DATA: IN STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0);
		    REG_IN_CLK, REG_IN_CLEAR, REG_IN_ENABLE: IN STD_LOGIC;
		    REG_OUT_DATA: OUT STD_LOGIC_VECTOR(n_bit - 1 DOWNTO 0));
END ENTITY n_bit_register;

ARCHITECTURE beh OF n_bit_register IS

BEGIN

	PROCESS(REG_IN_CLK)
	BEGIN
		
		IF(REG_IN_CLK'EVENT AND REG_IN_CLK = '1') THEN
			
			IF (REG_IN_CLEAR = '1') THEN
			   
			   REG_OUT_DATA <= (others => '0');
			
			elsif REG_IN_ENABLE = '1' THEN
			
			   REG_OUT_DATA <= REG_IN_DATA;
			   
			END IF;
		END IF;
	END PROCESS;

END ARCHITECTURE beh;