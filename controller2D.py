#!/usr/bin/python

import avango.script
from avango.script import field_has_changed
import avango.gua

class Controller2D(avango.script.Script):
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()
	Position = avango.gua.SFVec3()
	Speed = avango.SFFloat()
	Keyboard = None
	Picker = None


	def __init__(self):
		self.super(Controller2D).__init__()
		self.always_evaluate(True)
		self.Position.value = avango.gua.Vec3(0, 1, 0)
		self.Speed.value = 0.01
		self.zoom = 3
		self.zoomspeed = 0.1

	def evaluate(self):

		distance = 100
		MovementX = 0
		MovementZ = 0

		if len(self.Picker.Results.value) > 0:
			distance = self.Picker.Results.value[0].Distance.value
		else:
			distance = None

		if self.Keyboard.KeyW.value and self.Position.value.z > -0.5 and self.Position.value.x > -0.5 and self.Position.value.x < 0.5:
			MovementZ = -1 * self.Speed.value

		if self.Keyboard.KeyA.value and self.Position.value.x > -0.5 and self.Position.value.z > -0.5 and self.Position.value.z < 0.5:
			MovementX = -1 * self.Speed.value

		if self.Keyboard.KeyS.value and self.Position.value.z < 0.5 and self.Position.value.x > -0.5 and self.Position.value.x < 0.5:
			MovementZ += 1 * self.Speed.value

		if self.Keyboard.KeyD.value and self.Position.value.x < 0.5 and self.Position.value.z > -0.5 and self.Position.value.z < 0.5:
			MovementX += 1 * self.Speed.value

		if not distance == None:	#if the view is over the map
			if distance < 1:					#if the  view is in a close range to the map
				self.Position.value += avango.gua.Vec3(MovementX * distance, 0, MovementZ * distance)	#slow down the movement speed depending on the distance
			else:											
				self.Position.value += avango.gua.Vec3(MovementX , 0, MovementZ)	#set the position normally

		if self.Keyboard.KeyQ.value:	#zoom out
			if not distance == None and self.Position.value.z > -0.5 and self.Position.value.x > -0.5 and self.Position.value.x < 0.5 and self.Position.value.z < 0.5:									#allow to zoom out while picker finds something only
				if distance < 1:												#if picker is more close to the map then 1
					self.zoom += ( 1 * distance * self.zoomspeed )	#zoom out slower
				else:
					self.zoom += ( 1 * self.zoomspeed )

		if self.Keyboard.KeyE.value and self.Position.value.z > -0.5 and self.Position.value.x > -0.5 and self.Position.value.x < 0.5 and self.Position.value.z < 0.5:	#zoom in
			if distance == None:												#allow zoom if too far away
				self.zoom -= ( 1 * self.zoomspeed )
			elif distance > 0.04:												#stop zoom if to close
				self.zoom -= ( 1 * distance * self.zoomspeed )

		positionx = self.Position.value.x 						
		positionz = self.Position.value.z
		self.Position.value = avango.gua.Vec3(positionx, self.zoom, positionz)		#set the zoom level only

		if (	self.Position.value.x < 0.5 and
					self.Position.value.x > -0.5 and
					self.Position.value.z < 0.5 and
					self.Position.value.z > -0.5):
			self.OutTransform.value = avango.gua.make_trans_mat(self.Position.value) * avango.gua.make_rot_mat(-90, 1, 0, 0)

	def setKeyboard(self, Keyboard):
		self.Keyboard = Keyboard

	def setPicker(self, Picker):
		self.Picker = Picker		