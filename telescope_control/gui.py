#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.6.8 on Thu Aug 22 11:17:06 2013
#

#Again, this is just nonsense, you don't need to worry about it
#(although if I was you, I would want a better gui to work with.)

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
	def __init__(self, *args, **kwds):
		# begin wxGlade: MyFrame.__init__
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		self.statusReadoutPanel                   = wx.Panel(self, wx.ID_ANY)
		self.graphDisplayPanel                    = wx.Panel(self, wx.ID_ANY)
		self.graphPanelStaticbox                  = wx.StaticBox(self.graphDisplayPanel, wx.ID_ANY, "Graph")
		self.controlButtonPanel                   = wx.Panel(self, wx.ID_ANY)

		self.controlNotebook                      = wx.Notebook(self, wx.ID_ANY, style=0)



		self.__do_layout()
		self.__set_properties()

		self.Bind(wx.EVT_BUTTON, self.stop, self.button_stop_all)
		self.Bind(wx.EVT_BUTTON, self.stop, self.button_stop_az)
		self.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_motor_state, self.buttton_az_motor)
		self.Bind(wx.EVT_BUTTON, self.stop, self.button_stop_el)
		self.Bind(wx.EVT_TOGGLEBUTTON, self.toggle_motor_state, self.button_el_motor)
		self.Bind(wx.EVT_TEXT_ENTER, self.set_step_size, self.step_size_input)
		self.Bind(wx.EVT_BUTTON, self.move_rel, self.button_up)
		self.Bind(wx.EVT_BUTTON, self.move_rel, self.button_left)
		self.Bind(wx.EVT_BUTTON, self.move_rel, self.button_right)
		self.Bind(wx.EVT_BUTTON, self.move_rel, self.button_down)
		self.Bind(wx.EVT_BUTTON, self.move_abs, self.button_start_move)
		self.Bind(wx.EVT_BUTTON, self.goto, self.buttonGotoPosition)
		self.Bind(wx.EVT_BUTTON, self.calibrate, self.buttonDoRaDecCalibrate)
		self.Bind(wx.EVT_BUTTON, self.track_radec, self.buttonTrackPosition)
		self.Bind(wx.EVT_BUTTON, self.scan, self.buttonScanStart)
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: MyFrame.__set_properties
		self.SetTitle("Telescope Control Code")
		self.comboBoxScanOptions.SetSelection(0)
		# end wxGlade

	def __create_status_sizer(self):


		self.az_status     = wx.StaticText(self.statusReadoutPanel, wx.ID_ANY, "Az: 0.00 Degrees")
		self.el_status     = wx.StaticText(self.statusReadoutPanel, wx.ID_ANY, "El: 0.00 Degrees")
		self.ra_status     = wx.StaticText(self.statusReadoutPanel, wx.ID_ANY, "Ra: 0.00 Degrees")
		self.dec_status    = wx.StaticText(self.statusReadoutPanel, wx.ID_ANY, "Dec: 0.00 Degrees")
		self.utc_status    = wx.StaticText(self.statusReadoutPanel, wx.ID_ANY, "Utc: 0.00")
		self.lst_status    = wx.StaticText(self.statusReadoutPanel, wx.ID_ANY, "Lst: 0.00")
		self.local_status  = wx.StaticText(self.statusReadoutPanel, wx.ID_ANY, "Local: 0.00")

		textItems = [self.az_status, self.el_status, self.ra_status, self.dec_status, self.utc_status, self.lst_status, self.local_status]

		for item in textItems:
			item.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "MS Shell Dlg 2"))

		self.statusSizerStaticbox = wx.StaticBox(self.statusReadoutPanel, wx.ID_ANY, "Status")
		self.statusSizerStaticbox.Lower()
		sizer = wx.StaticBoxSizer(self.statusSizerStaticbox, wx.VERTICAL)
		sizer.AddMany(textItems)

		return sizer

	def __create_controls_sizer(self):
		self.button_stop_all          = wx.Button(self.controlButtonPanel, wx.ID_ANY, "Stop All")
		self.button_stop_az           = wx.Button(self.controlButtonPanel, wx.ID_ANY, "Stop AZ")
		self.buttton_az_motor         = wx.ToggleButton(self.controlButtonPanel, wx.ID_ANY, "AZ Motor On")
		self.button_goto_balloon      = wx.Button(self.controlButtonPanel, wx.ID_ANY, "Goto Balloon")
		self.button_stop_el           = wx.Button(self.controlButtonPanel, wx.ID_ANY, "Stop EL")
		self.button_el_motor          = wx.ToggleButton(self.controlButtonPanel, wx.ID_ANY, "EL Motor On")

		gridSizer = wx.GridSizer(rows=3, cols=2)

		items = [self.button_stop_all, self.button_stop_az, self.buttton_az_motor, self.button_goto_balloon, self.button_stop_el, self.button_el_motor]
		for item in items:
			gridSizer.Add(item, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND)
		
		
		self.controlButtonsStaticBox        = wx.StaticBox(self.controlButtonPanel, wx.ID_ANY, "Universal Controls")
		self.controlButtonsStaticBox.Lower()
		sizer = wx.StaticBoxSizer(self.controlButtonsStaticBox, wx.HORIZONTAL)
		sizer.Add(gridSizer, 1, 0, 0)

		return sizer

	def __create_ra_dec_pane(self):	# TODO: CLEANUP, name sizers sanely
		self.notebookRaDecPane                    = wx.Panel(self.controlNotebook, wx.ID_ANY)
		self.label_1                              = wx.StaticText(self.notebookRaDecPane, wx.ID_ANY, "Ra: ")
		self.textCtrlGotoRightAscension           = wx.TextCtrl(self.notebookRaDecPane, wx.ID_ANY, "")
		self.label_2                              = wx.StaticText(self.notebookRaDecPane, wx.ID_ANY, "Dec:")
		self.textCtrlGotoDeclination              = wx.TextCtrl(self.notebookRaDecPane, wx.ID_ANY, "")
		self.buttonGotoPosition                   = wx.Button(self.notebookRaDecPane, wx.ID_ANY, "Goto Position")
		self.sizer_6_staticbox                    = wx.StaticBox(self.notebookRaDecPane, wx.ID_ANY, "Goto Ra/Dec")
		self.label_1_copy                         = wx.StaticText(self.notebookRaDecPane, wx.ID_ANY, "Ra: ")
		self.textCtrlRightAscensionCalInput       = wx.TextCtrl(self.notebookRaDecPane, wx.ID_ANY, "")
		self.label_2_copy                         = wx.StaticText(self.notebookRaDecPane, wx.ID_ANY, "Dec:")
		self.textCtrlDeclinationCalInput          = wx.TextCtrl(self.notebookRaDecPane, wx.ID_ANY, "")
		self.buttonDoRaDecCalibrate               = wx.Button(self.notebookRaDecPane, wx.ID_ANY, "Calibrate")
		self.sizer_16_staticbox                   = wx.StaticBox(self.notebookRaDecPane, wx.ID_ANY, "Calibrate Ra/Dec")
		self.label_1_copy_1                       = wx.StaticText(self.notebookRaDecPane, wx.ID_ANY, "Ra: ")
		self.textCtrlTrackingRightAscension       = wx.TextCtrl(self.notebookRaDecPane, wx.ID_ANY, "")
		self.label_2_copy_1                       = wx.StaticText(self.notebookRaDecPane, wx.ID_ANY, "Dec:")
		self.textCtrlTrackingDeclination          = wx.TextCtrl(self.notebookRaDecPane, wx.ID_ANY, "")
		self.buttonTrackPosition                  = wx.Button(self.notebookRaDecPane, wx.ID_ANY, "Track Position")
		self.buttonTrackingToggle                 = wx.ToggleButton(self.notebookRaDecPane, wx.ID_ANY, "Tracking On")
		self.sizer_17_staticbox                   = wx.StaticBox(self.notebookRaDecPane, wx.ID_ANY, "Ra/Dec Tracking")

		self.sizer_17_staticbox.Lower()
		self.sizer_16_staticbox.Lower()
		self.sizer_6_staticbox.Lower()

		sizer_13 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13.Add(self.label_1, 0, 0, 0)
		sizer_13.Add(self.textCtrlGotoRightAscension, 0, 0, 0)

		sizer_14 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_14.Add(self.label_2, 0, 0, 0)
		sizer_14.Add(self.textCtrlGotoDeclination, 0, 0, 0)
		
		sizer_7 = wx.BoxSizer(wx.VERTICAL)
		sizer_7.Add(sizer_13, 1, wx.EXPAND, 0)
		sizer_7.Add(sizer_14, 1, wx.EXPAND, 0)
		sizer_7.Add(self.buttonGotoPosition, 0, 0, 0)

		sizer_6 = wx.StaticBoxSizer(self.sizer_6_staticbox, wx.HORIZONTAL)
		sizer_6.Add(sizer_7, 1, wx.EXPAND, 0)

		sizer_13_copy = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13_copy.Add(self.label_1_copy, 0, 0, 0)
		sizer_13_copy.Add(self.textCtrlRightAscensionCalInput, 0, 0, 0)

		sizer_14_copy = wx.BoxSizer(wx.HORIZONTAL)
		sizer_14_copy.Add(self.label_2_copy, 0, 0, 0)
		sizer_14_copy.Add(self.textCtrlDeclinationCalInput, 0, 0, 0)
		
		sizer_7_copy = wx.BoxSizer(wx.VERTICAL)
		sizer_7_copy.Add(sizer_13_copy, 1, wx.EXPAND, 0)
		sizer_7_copy.Add(sizer_14_copy, 1, wx.EXPAND, 0)
		sizer_7_copy.Add(self.buttonDoRaDecCalibrate, 0, 0, 0)
		
		sizer_16 = wx.StaticBoxSizer(self.sizer_16_staticbox, wx.HORIZONTAL)
		sizer_16.Add(sizer_7_copy, 1, wx.EXPAND, 0)
		
		sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_5.Add(sizer_6, 1, wx.EXPAND, 0)
		sizer_5.Add(sizer_16, 1, wx.EXPAND, 0)

		sizer_13_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13_copy_1.Add(self.label_1_copy_1, 0, 0, 0)
		sizer_13_copy_1.Add(self.textCtrlTrackingRightAscension, 0, wx.LEFT, 0)

		sizer_14_copy_1 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_14_copy_1.Add(self.label_2_copy_1, 0, 0, 0)
		sizer_14_copy_1.Add(self.textCtrlTrackingDeclination, 0, 0, 0)
		
		sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_22.Add(self.buttonTrackPosition, 0, 0, 0)
		sizer_22.Add((90, 20), 0, 0, 0)
		sizer_22.Add(self.buttonTrackingToggle, 0, 0, 0)
		
		sizer_7_copy_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_7_copy_1.Add(sizer_13_copy_1, 1, wx.EXPAND, 0)
		sizer_7_copy_1.Add(sizer_14_copy_1, 1, wx.EXPAND, 0)
		sizer_7_copy_1.Add(sizer_22, 1, wx.EXPAND, 0)

		sizer_18 = wx.BoxSizer(wx.VERTICAL)
		sizer_18.Add(sizer_7_copy_1, 1, wx.EXPAND, 0)
		
		sizer_17 = wx.StaticBoxSizer(self.sizer_17_staticbox, wx.HORIZONTAL)
		sizer_17.Add(sizer_18, 1, wx.EXPAND, 0)
		
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
		sizer_1.Add(sizer_17, 1, wx.EXPAND, 0)


		self.notebookRaDecPane.SetSizer(sizer_1)
		return self.notebookRaDecPane

	def __create_joystick_pane(self):	# TODO: CLEANUP, name sizers sanely
		self.notebookJoystickPane                 = wx.Panel(self.controlNotebook, wx.ID_ANY)
		self.step_size_input                      = wx.TextCtrl(self.notebookJoystickPane, wx.ID_ANY, "", style=wx.TE_PROCESS_ENTER)
		self.label_6                              = wx.StaticText(self.notebookJoystickPane, wx.ID_ANY, "Degrees")
		self.button_up                            = wx.Button(self.notebookJoystickPane, wx.ID_ANY, "^")
		self.button_left                          = wx.Button(self.notebookJoystickPane, wx.ID_ANY, "<")
		self.button_right                         = wx.Button(self.notebookJoystickPane, wx.ID_ANY, ">")
		self.button_down                          = wx.Button(self.notebookJoystickPane, wx.ID_ANY, "v")
		self.sizer_21_staticbox                   = wx.StaticBox(self.notebookJoystickPane, wx.ID_ANY, "Relative Move")
		self.label_7                              = wx.StaticText(self.notebookJoystickPane, wx.ID_ANY, "AZ")
		self.ctrl_az                              = wx.TextCtrl(self.notebookJoystickPane, wx.ID_ANY, "")
		self.label_8                              = wx.StaticText(self.notebookJoystickPane, wx.ID_ANY, "EL")
		self.ctrl_el                              = wx.TextCtrl(self.notebookJoystickPane, wx.ID_ANY, "")
		self.button_start_move                    = wx.Button(self.notebookJoystickPane, wx.ID_ANY, "Start Move")
		self.sizer_32_staticbox                   = wx.StaticBox(self.notebookJoystickPane, wx.ID_ANY, "Absolute Move")
		self.label_9                              = wx.StaticText(self.notebookJoystickPane, wx.ID_ANY, "AZ")
		self.calibrate_az_input                   = wx.TextCtrl(self.notebookJoystickPane, wx.ID_ANY, "")
		self.label_10                             = wx.StaticText(self.notebookJoystickPane, wx.ID_ANY, "EL")
		self.calibrate_el_input                   = wx.TextCtrl(self.notebookJoystickPane, wx.ID_ANY, "")
		self.button_calibrate                     = wx.Button(self.notebookJoystickPane, wx.ID_ANY, "Calibrate")
		self.sizer_36_staticbox                   = wx.StaticBox(self.notebookJoystickPane, wx.ID_ANY, "Calibrate")
		self.button_index_az                      = wx.Button(self.notebookJoystickPane, wx.ID_ANY, "AZ")
		self.button_index_el                      = wx.Button(self.notebookJoystickPane, wx.ID_ANY, "EL")
		self.sizer_37_staticbox                   = wx.StaticBox(self.notebookJoystickPane, wx.ID_ANY, "Index")

		sizer_24 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_24.Add(self.step_size_input, 0, 0, 0)
		sizer_24.Add(self.label_6, 0, 0, 0)

		sizer_30 = wx.BoxSizer(wx.VERTICAL)
		sizer_30.Add(self.button_up, 0, 0, 0)

		sizer_26 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_26.Add(sizer_30, 1, wx.EXPAND, 0)
		
		sizer_25 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_25.Add(sizer_26, 1, wx.EXPAND, 0)
				
		sizer_28 = wx.BoxSizer(wx.VERTICAL)
		sizer_28.Add(self.button_right, 0, wx.ALIGN_RIGHT, 0)
		
		sizer_29 = wx.BoxSizer(wx.VERTICAL)
		sizer_29.Add(self.button_left, 0, 0, 0)

		sizer_27 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_27.Add(sizer_29, 1, wx.EXPAND, 0)
		sizer_27.Add(sizer_28, 1, wx.EXPAND, 0)
		
		sizer_31 = wx.BoxSizer(wx.VERTICAL)
		sizer_31.Add(self.button_down, 0, 0, 0)
		
		sizer_30_copy = wx.BoxSizer(wx.VERTICAL)
		sizer_30_copy.Add(sizer_31, 1, wx.EXPAND, 0)
		
		sizer_26_copy = wx.BoxSizer(wx.HORIZONTAL)
		sizer_26_copy.Add(sizer_30_copy, 1, wx.EXPAND, 0)
		
		sizer_23 = wx.BoxSizer(wx.VERTICAL)
		sizer_23.Add(sizer_24, 1, wx.EXPAND, 0)
		sizer_23.Add(sizer_25, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
		sizer_23.Add(sizer_27, 1, wx.EXPAND, 0)
		sizer_23.Add(sizer_26_copy, 1, wx.ALIGN_CENTER_HORIZONTAL, 0)
		
		sizer_21 = wx.StaticBoxSizer(self.sizer_21_staticbox, wx.HORIZONTAL)
		sizer_21.Add(sizer_23, 1, wx.EXPAND, 0)
		
		sizer_34 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_34.Add(self.label_7, 0, 0, 0)
		sizer_34.Add(self.ctrl_az, 0, 0, 0)
		sizer_34.Add(self.label_8, 0, 0, 0)
		sizer_34.Add(self.ctrl_el, 0, 0, 0)

		sizer_33 = wx.BoxSizer(wx.VERTICAL)
		sizer_33.Add(sizer_34, 1, wx.EXPAND, 0)
		sizer_33.Add(self.button_start_move, 0, 0, 0)
		
		sizer_32 = wx.StaticBoxSizer(self.sizer_32_staticbox, wx.HORIZONTAL)
		sizer_32.Add(sizer_33, 1, wx.EXPAND, 0)
		
		sizer_20 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_20.Add(sizer_21, 1, wx.EXPAND, 0)
		sizer_20.Add(sizer_32, 1, wx.EXPAND, 0)
		
		sizer_39 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_39.Add(self.label_9, 0, 0, 0)
		sizer_39.Add(self.calibrate_az_input, 0, 0, 0)
		sizer_39.Add(self.label_10, 0, 0, 0)
		sizer_39.Add(self.calibrate_el_input, 0, 0, 0)
		
		sizer_38 = wx.BoxSizer(wx.VERTICAL)
		sizer_38.Add(sizer_39, 1, wx.EXPAND, 0)
		sizer_38.Add(self.button_calibrate, 0, 0, 0)
		
		sizer_36 = wx.StaticBoxSizer(self.sizer_36_staticbox, wx.HORIZONTAL)
		sizer_36.Add(sizer_38, 1, wx.EXPAND, 0)
		
		sizer_40 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_40.Add(self.button_index_az, 0, 0, 0)
		sizer_40.Add(self.button_index_el, 0, 0, 0)
		
		sizer_37 = wx.StaticBoxSizer(self.sizer_37_staticbox, wx.HORIZONTAL)
		sizer_37.Add(sizer_40, 1, wx.EXPAND, 0)
		
		sizer_35 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_35.Add(sizer_36, 1, wx.EXPAND, 0)
		sizer_35.Add(sizer_37, 1, wx.EXPAND, 0)
		
		sizer_19 = wx.BoxSizer(wx.VERTICAL)
		sizer_19.Add(sizer_20, 1, wx.EXPAND, 0)
		sizer_19.Add(sizer_35, 1, wx.EXPAND, 0)
		
		self.notebookJoystickPane.SetSizer(sizer_19)

		self.sizer_37_staticbox.Lower()
		self.sizer_36_staticbox.Lower()
		self.sizer_32_staticbox.Lower()
		self.sizer_21_staticbox.Lower()


		return self.notebookJoystickPane

	def __create_scanning_pane(self):	# TODO: CLEANUP, name sizers sanely
		self.notebookScanningPane                 = wx.Panel(self.controlNotebook, wx.ID_ANY)
		self.label_1_copy_2                       = wx.StaticText(self.notebookScanningPane, wx.ID_ANY, "Min: ")
		self.textCtrlScanMinAz                    = wx.TextCtrl(self.notebookScanningPane, wx.ID_ANY, "")
		self.label_2_copy_2                       = wx.StaticText(self.notebookScanningPane, wx.ID_ANY, "Max:")
		self.textCtrlScanMaxAz                    = wx.TextCtrl(self.notebookScanningPane, wx.ID_ANY, "")
		self.sizer_44_staticbox                   = wx.StaticBox(self.notebookScanningPane, wx.ID_ANY, "Az")
		self.label_1_copy_3                       = wx.StaticText(self.notebookScanningPane, wx.ID_ANY, "Min: ")
		self.textCtrlScanMinEl                    = wx.TextCtrl(self.notebookScanningPane, wx.ID_ANY, "")
		self.label_2_copy_3                       = wx.StaticText(self.notebookScanningPane, wx.ID_ANY, "Max:")
		self.textCtrlScanMaxEl                    = wx.TextCtrl(self.notebookScanningPane, wx.ID_ANY, "")
		self.sizer_45_staticbox                   = wx.StaticBox(self.notebookScanningPane, wx.ID_ANY, "El")
		self.label_scan_period                    = wx.StaticText(self.notebookScanningPane, wx.ID_ANY, "Period:")
		self.scan_period_input                    = wx.TextCtrl(self.notebookScanningPane, wx.ID_ANY, "")
		self.label_scan_cycles                    = wx.StaticText(self.notebookScanningPane, wx.ID_ANY, "Cycles:")
		self.scan_cycles_input                    = wx.TextCtrl(self.notebookScanningPane, wx.ID_ANY, "")
		self.scan_continuous_input                = wx.CheckBox(self.notebookScanningPane, wx.ID_ANY, "Continuous")
		self.checkbox_radec                       = wx.CheckBox(self.notebookScanningPane, wx.ID_ANY, "Ra/Dec")
		self.buttonScanStart                      = wx.Button(self.notebookScanningPane, wx.ID_ANY, "Scan")
		self.comboBoxScanOptions                  = wx.ComboBox(self.notebookScanningPane, wx.ID_ANY, choices=["Azimuth", "Elevation", "Square", "Serpentine", "Spin"], style=wx.CB_DROPDOWN | wx.CB_READONLY)
		self.sizer_49_staticbox                   = wx.StaticBox(self.notebookScanningPane, wx.ID_ANY, "Scan Options")


		self.sizer_49_staticbox.Lower()
		self.sizer_45_staticbox.Lower()
		self.sizer_44_staticbox.Lower()


		sizer_13_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13_copy_2.Add(self.label_1_copy_2, 0, 0, 0)
		sizer_13_copy_2.Add(self.textCtrlScanMinAz, 0, 0, 0)

		sizer_14_copy_2 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_14_copy_2.Add(self.label_2_copy_2, 0, 0, 0)
		sizer_14_copy_2.Add(self.textCtrlScanMaxAz, 0, 0, 0)
		
		sizer_7_copy_2 = wx.BoxSizer(wx.VERTICAL)
		sizer_7_copy_2.Add(sizer_13_copy_2, 1, wx.EXPAND, 0)
		sizer_7_copy_2.Add(sizer_14_copy_2, 1, wx.EXPAND, 0)
		
		sizer_44 = wx.StaticBoxSizer(self.sizer_44_staticbox, wx.HORIZONTAL)
		sizer_44.Add(sizer_7_copy_2, 1, wx.EXPAND, 0)
		
		sizer_13_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13_copy_3.Add(self.label_1_copy_3, 0, 0, 0)
		sizer_13_copy_3.Add(self.textCtrlScanMinEl, 0, 0, 0)
				
		sizer_14_copy_3 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_14_copy_3.Add(self.label_2_copy_3, 0, 0, 0)
		sizer_14_copy_3.Add(self.textCtrlScanMaxEl, 0, 0, 0)
		
		sizer_7_copy_3 = wx.BoxSizer(wx.VERTICAL)
		sizer_7_copy_3.Add(sizer_13_copy_3, 1, wx.EXPAND, 0)
		sizer_7_copy_3.Add(sizer_14_copy_3, 1, wx.EXPAND, 0)
		
		sizer_45 = wx.StaticBoxSizer(self.sizer_45_staticbox, wx.HORIZONTAL)
		sizer_45.Add(sizer_7_copy_3, 1, wx.EXPAND, 0)
		
		sizer_43 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_43.Add(sizer_44, 1, wx.EXPAND, 0)
		sizer_43.Add(sizer_45, 1, wx.EXPAND, 0)
		
		sizer_13_copy_4 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13_copy_4.Add(self.label_scan_period, 0, 0, 0)
		sizer_13_copy_4.Add(self.scan_period_input, 0, 0, 0)
		
		sizer_14_copy_4 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_14_copy_4.Add(self.label_scan_cycles, 0, 0, 0)
		sizer_14_copy_4.Add(self.scan_cycles_input, 0, 0, 0)
		
		sizer_7_copy_4 = wx.BoxSizer(wx.VERTICAL)
		sizer_7_copy_4.Add(sizer_13_copy_4, 1, wx.EXPAND, 0)
		sizer_7_copy_4.Add(sizer_14_copy_4, 1, wx.EXPAND, 0)
		sizer_7_copy_4.Add(self.scan_continuous_input, 0, 0, 0)
		sizer_7_copy_4.Add(self.checkbox_radec, 0, 0, 0)
		
		sizer_51 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_51.Add(self.buttonScanStart, 0, 0, 0)
		sizer_51.Add(self.comboBoxScanOptions, 0, 0, 0)
		
		sizer_50 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_50.Add(sizer_7_copy_4, 1, wx.EXPAND, 0)
		sizer_50.Add(sizer_51, 1, wx.EXPAND, 0)
		
		sizer_49 = wx.StaticBoxSizer(self.sizer_49_staticbox, wx.HORIZONTAL)
		sizer_49.Add(sizer_50, 1, wx.EXPAND, 0)

		sizer_42 = wx.BoxSizer(wx.VERTICAL)
		sizer_42.Add(sizer_43, 1, wx.EXPAND, 0)
		sizer_42.Add(sizer_49, 1, wx.EXPAND, 0)
		
		self.notebookScanningPane.SetSizer(sizer_42)


		
		return self.notebookScanningPane

	def __create_options_pane(self):	# TODO: CLEANUP, name sizers sanely

		self.notebookOptionsPane                  = wx.Panel(self.controlNotebook, wx.ID_ANY)
		self.label_1_copy_5                       = wx.StaticText(self.notebookOptionsPane, wx.ID_ANY, "Velocity:       ")  # TODO: Fix this padding issue by using proper sizer structures
		self.ctrl_velocity                        = wx.TextCtrl(self.notebookOptionsPane, wx.ID_ANY, "")
		self.label_2_copy_5                       = wx.StaticText(self.notebookOptionsPane, wx.ID_ANY, "Acceleration:")
		self.ctrl_acceleration                    = wx.TextCtrl(self.notebookOptionsPane, wx.ID_ANY, "")
		self.button_set_accel_vel                 = wx.Button(self.notebookOptionsPane, wx.ID_ANY, "Set Accel/Vel")
		self.radio_btn_az                         = wx.RadioButton(self.notebookOptionsPane, wx.ID_ANY, "AZ")
		self.radio_btn_el                         = wx.RadioButton(self.notebookOptionsPane, wx.ID_ANY, "EL")
		self.button_open_config                   = wx.Button(self.notebookOptionsPane, wx.ID_ANY, "Open Config File")
		self.panel_5                              = wx.Panel(self.notebookOptionsPane, wx.ID_ANY)
		self.sizer_52_staticbox                   = wx.StaticBox(self.notebookOptionsPane, wx.ID_ANY, "Move Options")

		self.sizer_52_staticbox.Lower()

		sizer_13_copy_5 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_13_copy_5.Add(self.label_1_copy_5, 0, 0, 0)
		sizer_13_copy_5.Add(self.ctrl_velocity, 0, 0, 0)

		sizer_14_copy_5 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_14_copy_5.Add(self.label_2_copy_5, 0, 0, 0)
		sizer_14_copy_5.Add(self.ctrl_acceleration, 0, 0, 0)
		
		sizer_7_copy_5 = wx.BoxSizer(wx.VERTICAL)
		sizer_7_copy_5.Add(sizer_13_copy_5, 1, wx.EXPAND, 0)
		sizer_7_copy_5.Add(sizer_14_copy_5, 1, wx.EXPAND, 0)
		sizer_7_copy_5.Add(self.button_set_accel_vel, 0, 0, 0)
		
		sizer_54_copy = wx.BoxSizer(wx.VERTICAL)
		sizer_54_copy.Add(self.radio_btn_az, 0, 0, 0)
		sizer_54_copy.Add(self.radio_btn_el, 0, 0, 0)

		sizer_53 = wx.BoxSizer(wx.HORIZONTAL)
		sizer_53.Add(sizer_7_copy_5, 1, wx.EXPAND, 0)
		sizer_53.Add(sizer_54_copy, 1, wx.EXPAND, 0)
		
		sizer_54 = wx.BoxSizer(wx.VERTICAL)
		sizer_54.Add(sizer_53, 1, wx.EXPAND, 0)
		sizer_54.Add(self.button_open_config, 0, 0, 0)
		sizer_54.Add(self.panel_5, 1, wx.EXPAND, 0)
		
		sizer_52 = wx.StaticBoxSizer(self.sizer_52_staticbox, wx.HORIZONTAL)
		sizer_52.Add(sizer_54, 1, wx.EXPAND, 0)
		
		self.notebookOptionsPane.SetSizer(sizer_52)

		return self.notebookOptionsPane

	def __do_layout(self):
		# begin wxGlade: MyFrame.__do_layout
		
		self.graphPanelStaticbox.Lower()
		sizer_12 = wx.StaticBoxSizer(self.graphPanelStaticbox, wx.HORIZONTAL)


		self.statusReadoutPanel.SetSizer(self.__create_status_sizer())
		self.graphDisplayPanel.SetSizer(sizer_12)
		self.controlButtonPanel.SetSizer(self.__create_controls_sizer())

		headerSizer = wx.BoxSizer(wx.HORIZONTAL)

		headerSizer.Add(self.statusReadoutPanel, proportion=1, flag=wx.EXPAND)


		headerSizer.Add(self.graphDisplayPanel, proportion=1, flag=wx.EXPAND)


		headerSizer.Add(self.controlButtonPanel, proportion=1, flag=wx.EXPAND)
		
		



		self.controlNotebook.AddPage(self.__create_joystick_pane(), "Joy Stick")
		self.controlNotebook.AddPage(self.__create_ra_dec_pane(), "RA/DEC")
		self.controlNotebook.AddPage(self.__create_scanning_pane(), "Scanning ")
		self.controlNotebook.AddPage(self.__create_options_pane(), "Options")
		

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		mainSizer.Add(headerSizer, proportion=1, flag=wx.EXPAND)
		mainSizer.Add(self.controlNotebook, proportion=1, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		
		self.Layout()
		# end wxGlade

	def stop(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'stop' not implemented!"
		event.Skip()

	def toggle_motor_state(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'toggle_motor_state' not implemented!"
		event.Skip()

	def set_step_size(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'set_step_size' not implemented!"
		event.Skip()

	def move_rel(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'move_rel' not implemented!"
		event.Skip()

	def move_abs(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'move_abs' not implemented!"
		event.Skip()

	def goto(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'goto' not implemented!"
		event.Skip()

	def calibrate(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'calibrate' not implemented!"
		event.Skip()

	def track_radec(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'track_radec' not implemented!"
		event.Skip()

	def scan(self, event):  # wxGlade: MyFrame.<event_handler>
		print "Event handler 'scan' not implemented!"
		event.Skip()

# end of class MyFrame
if __name__ == "__main__":
	app = wx.PySimpleApp(0)
	wx.InitAllImageHandlers()
	MyFrame = MyFrame(None, wx.ID_ANY, "")
	app.SetTopWindow(MyFrame)
	MyFrame.Show()
	app.MainLoop()