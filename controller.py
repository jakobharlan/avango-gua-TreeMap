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
			# print "picker "+str(self.controller2D.Picker.Results.value[0].WorldPosition.value)
			# print "Distance "+str(self.controller2D.Picker.Results.value[0].Distance.value)
			self.controller2D.Position.value = self.controller3D.Position.value;
			self.OutTransform.disconnect_from(self.controller3D.OutTransform)
			self.OutTransform.connect_from(self.controller2D.OutTransform)
		else:
			# print "picker "+str(self.controller2D.Picker.Results.value[0].WorldPosition.value)
			print "Distance "+str(self.controller2D.Picker.Results.value[0].Distance.value)
			self.controller3D.height = self.controller2D.zoom - self.Picker.Results.value[0].Distance.value * 5
			self.controller3D.rel_rot_x = 0;
			self.controller3D.rel_rot_y = 0;
			self.controller3D.Position.value = self.controller2D.Position.value;
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

		self.KeyI = False
		self.KeyO = False
		self.KeyP = False

	def setTreeMap(self, TreeMap):
		self.TM = TreeMap

	def evaluate(self):
		if self.Keyboard.KeyI.value and not self.KeyI:
			self.TM.init_third_dim(self.TM.DEPTH)
			self.TM.layout()
		self.KeyI = self.Keyboard.KeyI.value

		if self.Keyboard.KeyO.value and not self.KeyO:
			self.TM.init_third_dim(self.TM.LAST_ACCESSD)
			self.TM.layout()
		self.KeyO = self.Keyboard.KeyO.value

		if self.Keyboard.KeyP.value and not self.KeyP:
			self.TM.init_third_dim(self.TM.LAST_MODIFIED)
			self.TM.layout()
		self.KeyP = self.Keyboard.KeyP.value