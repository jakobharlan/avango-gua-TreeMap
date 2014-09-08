#!/usr/bin/python

import avango.script
from avango.script import field_has_changed
from controller2D import Controller2D
from controller3D import Controller3D
import device

import avango.gua


class Navigator(avango.script.Script):
	Is_overview_modus = avango.SFBool()
	Is_overview_modus.value = True
	controller2D = Controller2D()
	controller3D = Controller3D()
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()
	Keyboard = device.KeyboardDevice()
	Mouse = device.MouseDevice()
	Picker = None


	def __init__(self):
		self.super(Navigator).__init__()
		self.always_evaluate(True)
		self.OutTransform.connect_from(self.controller2D.OutTransform)
		self.KeySTRG = False

		self.controller2D.setKeyboard(self.Keyboard)
		self.controller3D.setMouse(self.Mouse)
		self.controller3D.setKeyboard(self.Keyboard)

	def setPicker(self, Picker):
		self.Picker = Picker
		self.controller2D.setPicker(self.Picker)
		self.controller3D.setPicker(self.Picker)


	@field_has_changed(Is_overview_modus)
	def update_mode(self):
		if self.Is_overview_modus.value:
			self.controller2D.Position.value = self.controller3D.Position.value
			self.OutTransform.disconnect_from(self.controller3D.OutTransform)
			self.OutTransform.connect_from(self.controller2D.OutTransform)
		else:
			self.controller3D.height = self.controller2D.zoom - self.Picker.Results.value[0].Distance.value * 5
			# self.controller3D.setPosition()
			self.controller3D.rel_rot_x = 0
			self.controller3D.rel_rot_y = 0
			self.controller3D.Position.value = self.controller2D.Position.value
			self.OutTransform.disconnect_from(self.controller2D.OutTransform)
			self.OutTransform.connect_from(self.controller3D.OutTransform)

	def evaluate(self):
		if self.Keyboard.KeySTRG.value and not self.KeySTRG:
			self.Is_overview_modus.value = not self.Is_overview_modus.value
		self.KeySTRG = self.Keyboard.KeySTRG.value

class KeyController(avango.script.Script):
	Keyboard = device.KeyboardDevice()

	def __init__(self):
		self.super(KeyController).__init__()
		self.always_evaluate(True)

		self.Key1 = False
		self.Key2 = False
		self.Key3 = False

		self.KeyR = False
		self.KeyE = False
		self.KeyV = False
		self.KeyC = False
		self.ShowFiles = False

		self.KeyUp = False
		self.KeyDown = False

	def setTreeMap(self, TreeMap):
		self.TM = TreeMap

	def evaluate(self):
		if self.Keyboard.Key1.value and not self.Key1:
			self.TM.init_third_dim(self.TM.DEPTH)
			self.TM.layout()
		self.Key1 = self.Keyboard.Key1.value

		if self.Keyboard.Key2.value and not self.Key2:
			self.TM.init_third_dim(self.TM.LAST_ACCESSD)
			self.TM.layout()
		self.Key2 = self.Keyboard.Key2.value

		if self.Keyboard.Key3.value and not self.Key3:
			self.TM.init_third_dim(self.TM.LAST_MODIFIED)
			self.TM.layout()
		self.Key3 = self.Keyboard.Key3.value

		if self.Keyboard.KeyF.value and not self.KeyF:
			self.ShowFiles = not self.ShowFiles
			self.TM.clear_scenegraph_structure()
			self.TM.create_scenegraph_structure(ShowFiles = self.ShowFiles)
		self.KeyF = self.Keyboard.KeyF.value

		if self.Keyboard.KeyR.value and not self.KeyR:
			if self.ShowFiles:
				self.TM.show_files_under_focus()
				self.TM.clear_scenegraph_structure()
				self.TM.create_scenegraph_structure(ShowFiles = self.ShowFiles)
		self.KeyR = self.Keyboard.KeyR.value

		if self.Keyboard.KeyV.value and not self.KeyV:
			self.TM.drill_down_at_focus()
		self.KeyV = self.Keyboard.KeyV.value

		if self.Keyboard.KeyC.value and not self.KeyC:
			self.TM.remove_focus_element()
		self.KeyC = self.Keyboard.KeyC.value

		if self.Keyboard.KeyDown.value and not self.KeyDown:
			self.TM.focus_parent()
		self.KeyDown = self.Keyboard.KeyDown.value

		if self.Keyboard.KeyUp.value and not self.KeyUp:
			self.TM.focus_child()
		self.KeyUp = self.Keyboard.KeyUp.value
