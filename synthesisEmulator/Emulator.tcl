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
# File: SpineMachine3.tcl
# Generated on: Sun Sep 03 18:13:43 2023

# Load Quartus Prime Tcl Project package
package require ::quartus::project

set need_to_close_project 0
set make_assignments 1

# Check that the right project is open
if {[is_project_open]} {
	if {[string compare $quartus(project) "EMULATOR_N_3_W_0_S_0_Q_2"]} {
		puts "Project EMULATOR_N_3_W_0_S_0_Q_2 is not open"
		set make_assignments 0
	}
} else {
	# Only open if not already open
	if {[project_exists EMULATOR_N_3_W_0_S_0_Q_2]} {
		project_open -revision EMULATOR_N_3_W_0_S_0_Q_2 EMULATOR_N_3_W_0_S_0_Q_2
	} else {
		project_new -revision EMULATOR_N_3_W_0_S_0_Q_2 EMULATOR_N_3_W_0_S_0_Q_2
	}
	set need_to_close_project 1
}
# Make assignments
if {$make_assignments} {
	set_global_assignment -name FAMILY "Cyclone 10 LP"
	set_global_assignment -name DEVICE 10CL025YE144C8G
	set_global_assignment -name ORIGINAL_QUARTUS_VERSION 17.0.0
	set_global_assignment -name PROJECT_CREATION_TIME_DATE "14:45:09  AUGUST 19, 2024"
	set_global_assignment -name LAST_QUARTUS_VERSION "17.0.0 Lite Edition"
	set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
	set_global_assignment -name MIN_CORE_JUNCTION_TEMP 0
	set_global_assignment -name MAX_CORE_JUNCTION_TEMP 85
	set_global_assignment -name ERROR_CHECK_FREQUENCY_DIVISOR 1
	set_global_assignment -name NOMINAL_CORE_SUPPLY_VOLTAGE 1.2V
	set_global_assignment -name PARTITION_NETLIST_TYPE SOURCE -section_id Top
	set_global_assignment -name PARTITION_FITTER_PRESERVATION_LEVEL PLACEMENT_AND_ROUTING -section_id Top
	set_global_assignment -name PARTITION_COLOR 16764057 -section_id Top
	set_global_assignment -name POWER_PRESET_COOLING_SOLUTION "23 MM HEAT SINK WITH 200 LFPM AIRFLOW"
	set_global_assignment -name POWER_BOARD_THERMAL_MODEL "NONE (CONSERVATIVE)"
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/register/src/n_bit_register_clear_1.vhd
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/register/src/n_bit_register.vhd
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/counters/src/counter.vhd
	multiplexer________________________________________________________________________________
	decoder____________________________________________________________
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplier/src/multiplier.vhd
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/multiplier/src/arch_multiplier_behavioral.vhd
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/adder_subtractor/src/comb_adder.vhd
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/adder_subtractor/src/arch_comb_adder_behavioral.vhd
	set_global_assignment -name VHDL_FILE ../../design/basic_blocks/adder_subtractor/src/adder_subtractor.vhd
	set_global_assignment -name VHDL_FILE ../../design/control_unit/src/rot_rom.vhd
	set_global_assignment -name VHDL_FILE ../../design/control_unit/src/non_rot_rom.vhd
	set_global_assignment -name VHDL_FILE ../../design/control_unit/src/control_unit.vhd
	set_global_assignment -name VHDL_FILE ../../design/control_unit/src/arch_control_unit_rom_based.vhd
	set_global_assignment -name VHDL_FILE ../../design/datapath/src/datapath.vhd
	set_global_assignment -name VHDL_FILE ../../design/datapath/src/arch_datapath_trigonometric_prec_mult_pipe_0_nearest.vhd
	set_global_assignment -name VHDL_FILE ../../design/QEP/src/QEP_N_3_W_0_S_0.vhd
	set_global_assignment -name VHDL_FILE ../../design/QPE_control/src/QPE_control.vhd
	set_global_assignment -name VHDL_FILE ../../design/emulator/src/EMULATOR_N_3_W_0_S_0_Q_2.vhd
	set_global_assignment -name POWER_PRESET_COOLING_SOLUTION "23 MM HEAT SINK WITH 200 LFPM AIRFLOW"
	set_global_assignment -name POWER_BOARD_THERMAL_MODEL "NONE (CONSERVATIVE)"
	set_global_assignment -name TIMEQUEST_MULTICORNER_ANALYSIS ON
	set_global_assignment -name SMART_RECOMPILE ON
	set_global_assignment -name FLOW_ENABLE_IO_ASSIGNMENT_ANALYSIS ON
	set_global_assignment -name AUTO_EXPORT_VER_COMPATIBLE_DB ON
	set_global_assignment -name OPTIMIZATION_MODE "AGGRESSIVE AREA"
	set_global_assignment -name OPTIMIZATION_TECHNIQUE AREA
	set_global_assignment -name OPTIMIZE_POWER_DURING_SYNTHESIS OFF
	set_global_assignment -name SYNTHESIS_EFFORT AUTO
	set_global_assignment -name FLOW_ENABLE_POWER_ANALYZER ON
	set_global_assignment -name POWER_DEFAULT_INPUT_IO_TOGGLE_RATE "12.5 %"	
	set_location_assignment PIN_22 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_CLK
	set_location_assignment PIN_24 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_RSTN
	set_location_assignment PIN_76 -to EMULATOR_N_3_W_0_S_0_Q_2_OUT_TO_MCU[0]
	set_location_assignment PIN_77 -to EMULATOR_N_3_W_0_S_0_Q_2_OUT_TO_MCU[1]
	set_location_assignment PIN_80 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_FROM_MCU[0]
	set_location_assignment PIN_83 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_FROM_MCU[1]
	set_location_assignment PIN_85 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[0]
	set_location_assignment PIN_86 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[1]
	set_location_assignment PIN_87 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[2]
	set_location_assignment PIN_98 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[3]
	set_location_assignment PIN_99 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[4]
	set_location_assignment PIN_100 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[5]
	set_location_assignment PIN_136 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[6]
	set_location_assignment PIN_135 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[7]
	set_location_assignment PIN_105 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[8]
	set_location_assignment PIN_106 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[9]
	set_location_assignment PIN_111 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[10]
	set_location_assignment PIN_112 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[11]
	set_location_assignment PIN_113 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[12]
	set_location_assignment PIN_114 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[13]
	set_location_assignment PIN_115 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[14]
	set_location_assignment PIN_119 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[15]
	set_location_assignment PIN_120 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[16]
	set_location_assignment PIN_121 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[17]
	set_location_assignment PIN_125 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[18]
	set_location_assignment PIN_132 -to EMULATOR_N_3_W_0_S_0_Q_2_IN_OUT_BUS[19]
	set_instance_assignment -name PARTITION_HIERARCHY root_partition -to | -section_id Top

	# Commit assignments
	export_assignments

	# Close project
	if {$need_to_close_project} {
		project_close
	}
}