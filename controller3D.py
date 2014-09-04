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
	Down_Picker = None
	height = 0
	size = 0.02
	horizontal_speed = 0.3
	vertical_speed = 0.3
	walkspeed = avango.SFFloat()
	viewing_direction = avango.gua.SFVec3()

	def __init__(self):
		self.super(Controller3D).__init__()
		self.always_evaluate(True)
		self.walkspeed.value = 0.001

	def evaluate(self):
		self.rel_rot_x += self.Mouse.RelX.value
		self.rel_rot_y += self.Mouse.RelY.value

		rotation = avango.gua.make_rot_mat(-self.rel_rot_x * self.horizontal_speed, 0.0, 1.0, 0.0) * \
							 avango.gua.make_rot_mat(-self.rel_rot_y * self.vertical_speed, 1.0, 0.0, 0.0)

		MovementX = 0
		MovementZ = 0

		# print self.viewing_direction.value
		# print self.viewing_direction.value

		if self.Keyboard.KeyW.value:
			MovementX = 1 * self.walkspeed.value

		if self.Keyboard.KeyA.value:
			MovementZ = 1 * self.walkspeed.value

		if self.Keyboard.KeyS.value:
			MovementZ += -1 * self.walkspeed.value

		if self.Keyboard.KeyD.value:
			MovementX += -1 * self.walkspeed.value

		self.Position.value += avango.gua.Vec3(MovementX, 0, MovementZ)
		
		position_y = self.height + self.size
		if not self.Keyboard.KeySPACE.value:
			if len(self.Down_Picker.Results.value) > 0:
				# print self.Down_Picker.Results.value[0].Distance.value * 5
				if self.Down_Picker.Results.value[0].Distance.value * 5 > self.size:
					self.height -= self.Down_Picker.Results.value[0].Distance.value * 5
					position_y = self.height + self.size
		else:
			print "space"

		positionx = self.Position.value.x 						
		positionz = self.Position.value.z


		self.Position.value = avango.gua.Vec3(positionx, position_y, positionz)

		self.OutTransform.value = avango.gua.make_trans_mat(self.Position.value) * \
															rotation

		self.Down_Picker.Ray.value.Transform.value = avango.gua.make_inverse_mat(self.OutTransform.value)
		self.Down_Picker.Ray.value.Transform.value *= avango.gua.make_trans_mat(self.Position.value) * \
																								 	avango.gua.make_rot_mat(-90, 1.0, 0.0, 0.0) * \
														 										 	avango.gua.make_scale_mat(0.0005, 0.0005, 5)

	def setKeyboard(self, Keyboard):
		self.Keyboard = Keyboard

	def setMouse(self, Mouse):
		self.Mouse = Mouse

	def setPicker(self, Picker):
		self.Picker = Picker

	def setDown_Picker(self, Picker):
		self.Down_Picker = Picker