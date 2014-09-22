#!/usr/bin/python

import avango.script
from avango.script import field_has_changed
import avango.gua
import math

class ControllerOut(avango.script.Script):
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()
	Position = avango.gua.Vec3()
	Speed = avango.SFFloat()
	Keyboard = None
	angle = avango.SFFloat()
	heightAngle = avango.SFFloat()
	distance = 2


	def __init__(self):
		self.super(ControllerOut).__init__()
		self.always_evaluate(True)
		self.Position = avango.gua.Vec3(0, 2, self.distance)
		self.angle.value = 90
		self.heightAngle.value = -45

	def evaluate(self):
		positiony = self.Position.y
		heightAngle = 0

		if self.Keyboard != None:
			if self.Keyboard.KeyA.value:
				self.angle.value += 1
			if self.Keyboard.KeyD.value:
				self.angle.value -= 1
			if self.Keyboard.KeyQ.value and self.distance > 0.3:
				self.distance -= 0.01
				# heightAngle += 0.15
				positiony -= 0.01
			if self.Keyboard.KeyE.value:
				self.distance += 0.01
				# heightAngle -= 0.15
				positiony += 0.01
			# if self.Keyboard.KeyS.value:
			# 	positiony -= 0.01
				# heightAngle += 0.15
			# if self.Keyboard.KeyW.value:
			# 	positiony += 0.01
				# heightAngle -= 0.15

			# self.heightAngle.value += heightAngle

			positionx = math.cos(( ( 2*math.pi )/360 ) * self.angle.value)
			positionz = math.sin(( ( 2*math.pi )/360 ) * self.angle.value)

			self.Position.x = positionx * self.distance
			self.Position.y = positiony
			self.Position.z = positionz * self.distance

			self.Rotation = avango.gua.make_rot_mat(-(self.angle.value -90), 0.0, 1.0, 0.0) * \
								 avango.gua.make_rot_mat(self.heightAngle.value, 1.0, 0.0, 0.0) #calc view rotation

			# self.Rotation = self.get_rot_mat()

			self.OutTransform.value = avango.gua.make_trans_mat(self.Position) * \
																self.Rotation

	def get_rot_mat(self):
		vec1 = avango.gua.Vec3(0, 0, -1)
		vec2 = avango.gua.Vec3(0 - self.Position.x, 0 - self.Position.y, 0 - self.Position.z)

		vec1.normalize()
		vec2.normalize()

		angle = math.degrees(math.acos(vec1.dot(vec2)))
		axis = vec1.cross(vec2)

		return avango.gua.make_rot_mat(angle, axis) 

	def setKeyboard(self, Keyboard):
		self.Keyboard = Keyboard	