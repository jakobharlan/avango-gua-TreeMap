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


	def __init__(self):
		self.super(Navigator).__init__()
		self.always_evaluate(True)
		self.OutTransform.connect_from(self.controller2D.OutTransform)
		self.KeySTRG = False


	@field_has_changed(Is_overview_modus)
	def update_mode(self):
		if self.Is_overview_modus.value:
			self.OutTransform.disconnect_from(self.controller3D.OutTransform)
			self.OutTransform.connect_from(self.controller2D.OutTransform)
		else:
			self.OutTransform.disconnect_from(self.controller2D.OutTransform)
			self.controller3D.StartLocation.value = avango.gua.make_identity_mat().get_translate()
			self.OutTransform.connect_from(self.controller3D.OutTransform)

	def evaluate(self):
		if self.Keyboard.KeySTRG.value and not self.KeySTRG:
			self.Is_overview_modus.value = not self.Is_overview_modus.value
		self.KeySTRG = self.Keyboard.KeySTRG.value