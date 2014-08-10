#!/usr/bin/python

import avango.script
from avango.script import field_has_changed
import avango.gua
import device

class Controller2D(avango.script.Script):
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()
	Position = avango.gua.SFVec3()
	Speed = avango.SFFloat()
	Mouse = device.MouseDevice()
	Keyboard = device.KeyboardDevice()
	Picker = None


	def __init__(self):
		self.super(Controller2D).__init__()
		self.always_evaluate(True)
		self.Position.value = avango.gua.Vec3(0, 1, 0)
		self.Speed.value = 0.01
		self.zoom = 1
		self.zoomspeed = 0.1

	def evaluate(self):
		distance = 100
		MovementX = 0
		MovementZ = 0

		print self.zoom

		if len(self.Picker.Results.value) > 0:
			print self.Picker.Results.value[0].Distance.value
			distance = self.Picker.Results.value[0].Distance.value
			
		if self.Keyboard.KeyW.value:
			MovementZ = -1 * self.Speed.value
		if self.Keyboard.KeyA.value:
			MovementX = -1 * self.Speed.value
		if self.Keyboard.KeyS.value:
			MovementZ += 1 * self.Speed.value
		if self.Keyboard.KeyD.value:
			MovementX += 1 * self.Speed.value

		self.Position.value += avango.gua.Vec3(MovementX, 0, MovementZ)

		if self.Keyboard.KeyQ.value:
			self.zoom += ( 1 * self.zoomspeed )
		if self.Keyboard.KeyE.value:
			if distance > 0.1:
				self.zoom -= ( 1 * self.zoomspeed )

		positionx = self.Position.value.x
		positionz = self.Position.value.z
		self.Position.value = avango.gua.Vec3(positionx, self.zoom, positionz)


		self.OutTransform.value = avango.gua.make_trans_mat(self.Position.value) * avango.gua.make_rot_mat(-90, 1, 0, 0)