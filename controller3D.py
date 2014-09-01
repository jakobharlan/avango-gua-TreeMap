#!/usr/bin/python

import avango.script
from avango.script import field_has_changed
import device

class Controller3D(avango.script.Script):
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()
	Mouse = None
	Keyboard = None
	Position = avango.gua.SFVec3()
	rel_rot_x = 0
	rel_rot_y = 0
	Picker = None
	
	def __init__(self):
		self.super(Controller3D).__init__()
		self.always_evaluate(True)

	def evaluate(self):
		# print self.Picker.Results.value[0].distance.value

		rel_rot_x = self.Mouse.RelX.value
		rel_rot_y = self.Mouse.RelY.value

 		self.rel_rot_x += rel_rot_x
		self.rel_rot_y += rel_rot_y

		rotation = avango.gua.make_rot_mat(-self.rel_rot_x * 0.5, 0.0, 1.0, 0.0)
               # avango.gua.make_rot_mat(self.rel_rot_y * 1.0, 0.0, 0.0, 1.0)

		# print self.rel_rot_x.value
		# print self.rel_rot_y.value

		# print self.Position.value
		positionx = self.Position.value.x 						
		positionz = self.Position.value.z

		self.Position.value = avango.gua.Vec3(positionx, 2, positionz)		#set the zoom level only

		self.OutTransform.value = avango.gua.make_trans_mat(self.Position.value) * avango.gua.make_rot_mat(-90, 1, 0, 0) * rotation

	def setKeyboard(self, Keyboard):
		self.Keyboard = Keyboard

	def setMouse(self, Mouse):
		self.Mouse = Mouse

	def setPicker(self, Picker):
		self.Picker = Picker