## Generated SDC file "fpga-user.out.sdc"

## Copyright (C) 2021  Intel Corporation. All rights reserved.
## Your use of Intel Corporation's design tools, logic functions 
## and other software and tools, and any partner logic 
## functions, and any output files from any of the foregoing 
## (including device programming or simulation files), and any 
## associated documentation or information are expressly subject 
## to the terms and conditions of the Intel Program License 
## Subscription Agreement, the Intel Quartus Prime License Agreement,
## the Intel FPGA IP License Agreement, or other applicable license
## agreement, including, without limitation, that your use is for
## the sole purpose of programming logic devices manufactured by
## Intel and sold by Intel or its authorized distributors.  Please
## refer to the applicable agreement for further details, at
## https://fpgasoftware.intel.com/eula.


## VENDOR  "Altera"
## PROGRAM "Quartus Prime"
## VERSION "Version 21.1.0 Build 842 10/21/2021 SJ Lite Edition"

## DATE    "Tue Nov 15 16:57:44 2022"

##
## DEVICE  "10CL025YE144C8G"
##


#**************************************************************
# Time Information
#**************************************************************

set_time_format -unit ns -decimal_places 3



#**************************************************************
# Create Clock
#**************************************************************

create_clock -name {mainClk} -period 100.000 -waveform { 0.000 0.500 } [get_ports { mainClk }]


#**************************************************************
# Create Generated Clock
#**************************************************************

create_generated_clock -name {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]} -source [get_pins {myAltPll_inst|altpll_component|auto_generated|pll1|inclk[0]}] -duty_cycle 50/1 -multiply_by 1 -master_clock {mainClk} [get_pins {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}] 


#**************************************************************
# Set Clock Latency
#**************************************************************



#**************************************************************
# Set Clock Uncertainty
#**************************************************************

set_clock_uncertainty -rise_from [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}] -rise_to [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  0.020  
set_clock_uncertainty -rise_from [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}] -fall_to [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  0.020  
set_clock_uncertainty -fall_from [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}] -rise_to [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  0.020  
set_clock_uncertainty -fall_from [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}] -fall_to [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  0.020  


#**************************************************************
# Set Input Delay
#**************************************************************



#**************************************************************
# Set Output Delay
#**************************************************************

set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[0]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[1]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[2]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[3]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[4]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[5]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[6]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[7]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[8]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[9]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[10]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[11]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[12]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[13]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[14]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[15]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[16]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[17]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[18]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[19]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[20]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[21]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[22]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[23]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[24]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[25]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[26]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[27]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[28]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[29]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[30]}]
set_output_delay -add_delay  -clock [get_clocks {myAltPll_inst|altpll_component|auto_generated|pll1|clk[0]}]  5.000 [get_ports {lsasBus[31]}]


#**************************************************************
# Set Clock Groups
#**************************************************************



#**************************************************************
# Set False Path
#**************************************************************



#**************************************************************
# Set Multicycle Path
#**************************************************************



#**************************************************************
# Set Maximum Delay
#**************************************************************



#**************************************************************
# Set Minimum Delay
#**************************************************************



#**************************************************************
# Set Input Transition
#**************************************************************

