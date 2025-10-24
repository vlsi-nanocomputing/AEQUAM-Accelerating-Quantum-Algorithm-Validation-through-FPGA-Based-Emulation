# Copyright (C) 2017  Intel Corporation. All rights reserved.
# Your use of Intel Corporation's design tools, logic functions 
# and other software and tools, and its AMPP partner logic 
# functions, and any output files from any of the foregoing 
# (including device programming or simulation files), and any 
# associated documentation or information are expressly subject 
# to the terms and conditions of the Intel Program License 
# Subscription Agreement, the Intel Quartus Prime License Agreement,
# the Intel MegaCore Function License Agreement, or other 
# applicable license agreement, including, without limitation, 
# that your use is for the sole purpose of programming logic 
# devices manufactured by Intel and sold by Intel or its 
# authorized distributors.  Please refer to the applicable 
# agreement for further details.

# Quartus Prime: Generate Tcl File for Project
# File: fpga-user.tcl
# Generated on: Thu Aug 22 10:03:38 2024

# Load Quartus Prime Tcl Project package
package require ::quartus::project

set need_to_close_project 0
set make_assignments 1

# Check that the right project is open
if {[is_project_open]} {
	if {[string compare $quartus(project) "fpga-user"]} {
		puts "Project fpga-user is not open"
		set make_assignments 0
	}
} else {
	# Only open if not already open
	if {[project_exists fpga-user]} {
		project_open -revision fpga-user fpga-user
	} else {
		project_new -revision fpga-user fpga-user
	}
	set need_to_close_project 1
}

# Make assignments
if {$make_assignments} {
	set_global_assignment -name FAMILY "Cyclone 10 LP"
	set_global_assignment -name DEVICE 10CL025YE144C8G
	set_global_assignment -name TOP_LEVEL_ENTITY user
	set_global_assignment -name ORIGINAL_QUARTUS_VERSION 20.1.0
	set_global_assignment -name PROJECT_CREATION_TIME_DATE "23:10:36  OCTOBER 30, 2020"
	set_global_assignment -name LAST_QUARTUS_VERSION "17.0.0 Lite Edition"
	set_global_assignment -name MIN_CORE_JUNCTION_TEMP 0
	set_global_assignment -name MAX_CORE_JUNCTION_TEMP 85
	set_global_assignment -name POWER_PRESET_COOLING_SOLUTION "23 MM HEAT SINK WITH 200 LFPM AIRFLOW"
	set_global_assignment -name POWER_BOARD_THERMAL_MODEL "NONE (CONSERVATIVE)"
	set_global_assignment -name DEVICE_FILTER_PACKAGE TQFP
	set_global_assignment -name DEVICE_FILTER_PIN_COUNT 144
	set_global_assignment -name ENABLE_OCT_DONE OFF
	set_global_assignment -name ENABLE_CONFIGURATION_PINS OFF
	set_global_assignment -name ENABLE_BOOT_SEL_PIN OFF
	set_global_assignment -name CYCLONEIII_CONFIGURATION_SCHEME "PASSIVE SERIAL"
	set_global_assignment -name USE_CONFIGURATION_DEVICE OFF
	set_global_assignment -name GENERATE_RBF_FILE ON
	set_global_assignment -name CRC_ERROR_OPEN_DRAIN ON
	set_global_assignment -name STRATIX_DEVICE_IO_STANDARD "3.3-V LVCMOS"
	set_global_assignment -name RESERVE_DATA1_AFTER_CONFIGURATION "USE AS REGULAR IO"
	set_global_assignment -name RESERVE_FLASH_NCE_AFTER_CONFIGURATION "USE AS REGULAR IO"
	set_global_assignment -name OUTPUT_IO_TIMING_NEAR_END_VMEAS "HALF VCCIO" -rise
	set_global_assignment -name OUTPUT_IO_TIMING_NEAR_END_VMEAS "HALF VCCIO" -fall
	set_global_assignment -name OUTPUT_IO_TIMING_FAR_END_VMEAS "HALF SIGNAL SWING" -rise
	set_global_assignment -name OUTPUT_IO_TIMING_FAR_END_VMEAS "HALF SIGNAL SWING" -fall
	set_global_assignment -name DEVICE_MIGRATION_LIST "10CL025YE144C8G,10CL006YE144C8G,10CL010YE144C8G,10CL016YE144C8G"
	set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id Top
	set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id Top
	set_global_assignment -name PARTITION_COLOR 16764057 -section_id Top
	set_global_assignment -name FORCE_CONFIGURATION_VCCIO ON
	set_global_assignment -name CONFIGURATION_VCCIO_LEVEL 3.3V
	set_global_assignment -name CYCLONEII_RESERVE_NCEO_AFTER_CONFIGURATION "USE AS REGULAR IO"
	set_global_assignment -name VHDL_FILE ../basic_blocks/multiplexers/src/multiplexer_4_1.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/multiplexers/src/multiplexer_5_1.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/register/src/n_bit_register_clear_1.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/register/src/n_bit_register.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/multiplier/src/multiplier.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/multiplier/src/arch_multiplier_behavioral.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/decoders/src/state_decoder_N_3.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/multiplexers/src/multiplexer_8_1.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/multiplexers/src/multiplexer_3_1.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/multiplexers/src/multiplexer_2_1.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/counters/src/counter.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/adder_subtractor/src/comb_adder.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/adder_subtractor/src/arch_comb_adder_behavioral.vhd
	set_global_assignment -name VHDL_FILE ../basic_blocks/adder_subtractor/src/adder_subtractor.vhd
	set_global_assignment -name VHDL_FILE ../control_unit/src/rot_rom.vhd
	set_global_assignment -name VHDL_FILE ../control_unit/src/non_rot_rom.vhd
	set_global_assignment -name VHDL_FILE ../control_unit/src/control_unit.vhd
	set_global_assignment -name VHDL_FILE ../control_unit/src/arch_control_unit_rom_based.vhd
	set_global_assignment -name VHDL_FILE ../datapath/src/datapath.vhd
	set_global_assignment -name VHDL_FILE ../datapath/src/arch_datapath_trigonometric_prec_mult_pipe_0_nearest.vhd
	set_global_assignment -name VHDL_FILE ../QPE_control/src/QPE_control.vhd
	set_global_assignment -name VHDL_FILE ../QEP/src/QEP_N_3_W_0_S_0.vhd
	set_global_assignment -name VHDL_FILE ../emulator/src/EMULATOR_N_3_W_0_S_0_Q_2.vhd
	set_global_assignment -name VHDL_FILE "fpga-user.vhd"
	set_location_assignment PIN_68 -to leds[3]
	set_location_assignment PIN_69 -to leds[2]
	set_location_assignment PIN_71 -to leds[1]
	set_location_assignment PIN_72 -to leds[0]
	set_location_assignment PIN_144 -to lsasBus[31]
	set_location_assignment PIN_143 -to lsasBus[30]
	set_location_assignment PIN_142 -to lsasBus[29]
	set_location_assignment PIN_141 -to lsasBus[28]
	set_location_assignment PIN_137 -to lsasBus[27]
	set_location_assignment PIN_136 -to lsasBus[26]
	set_location_assignment PIN_135 -to lsasBus[25]
	set_location_assignment PIN_133 -to lsasBus[24]
	set_location_assignment PIN_132 -to lsasBus[23]
	set_location_assignment PIN_125 -to lsasBus[22]
	set_location_assignment PIN_121 -to lsasBus[21]
	set_location_assignment PIN_120 -to lsasBus[20]
	set_location_assignment PIN_119 -to lsasBus[19]
	set_location_assignment PIN_115 -to lsasBus[18]
	set_location_assignment PIN_114 -to lsasBus[17]
	set_location_assignment PIN_113 -to lsasBus[16]
	set_location_assignment PIN_112 -to lsasBus[15]
	set_location_assignment PIN_111 -to lsasBus[14]
	set_location_assignment PIN_106 -to lsasBus[13]
	set_location_assignment PIN_105 -to lsasBus[12]
	set_location_assignment PIN_103 -to lsasBus[11]
	set_location_assignment PIN_101 -to lsasBus[10]
	set_location_assignment PIN_100 -to lsasBus[9]
	set_location_assignment PIN_99 -to lsasBus[8]
	set_location_assignment PIN_98 -to lsasBus[7]
	set_location_assignment PIN_87 -to lsasBus[6]
	set_location_assignment PIN_86 -to lsasBus[5]
	set_location_assignment PIN_85 -to lsasBus[4]
	set_location_assignment PIN_83 -to lsasBus[3]
	set_location_assignment PIN_80 -to lsasBus[2]
	set_location_assignment PIN_77 -to lsasBus[1]
	set_location_assignment PIN_76 -to lsasBus[0]
	set_location_assignment PIN_66 -to switches[7]
	set_location_assignment PIN_65 -to switches[6]
	set_location_assignment PIN_60 -to switches[5]
	set_location_assignment PIN_59 -to switches[4]
	set_location_assignment PIN_51 -to switches[3]
	set_location_assignment PIN_50 -to switches[2]
	set_location_assignment PIN_49 -to switches[1]
	set_location_assignment PIN_46 -to switches[0]
	set_location_assignment PIN_23 -to slowClk
	set_location_assignment PIN_24 -to reset
	set_location_assignment PIN_10 -to mcuUartTx
	set_location_assignment PIN_8 -to mcuUartRx
	set_location_assignment PIN_7 -to mcuI2cSda
	set_location_assignment PIN_6 -to mcuI2cScl
	set_location_assignment PIN_22 -to mainClk
	set_instance_assignment -name PARTITION_HIERARCHY root_partition -to | -section_id Top

	# Commit assignments
	export_assignments

	# Close project
	if {$need_to_close_project} {
		project_close
	}
}
