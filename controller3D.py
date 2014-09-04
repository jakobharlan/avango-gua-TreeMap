#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

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
	position_y = 0
	horizontal_speed = 0.3
	vertical_speed = 0.3
	walkspeed = avango.SFFloat()
	viewing_direction = avango.gua.Vec3()
	is_falling = False
	fall_speed = 0.0007

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


		self.viewing_direction = self.get_ray_direction(self.Picker.Ray.value, avango.gua.Vec3(0.0005, 0.0005, 5))


		if self.Keyboard.KeyW.value:
			MovementX += 1 * self.walkspeed.value * self.viewing_direction.x
			MovementZ += 1 * self.walkspeed.value * self.viewing_direction.z

		if self.Keyboard.KeyA.value:
			MovementX += 1 * self.walkspeed.value * self.viewing_direction.z
			MovementZ += -1 * self.walkspeed.value * self.viewing_direction.x

		if self.Keyboard.KeyS.value:
			MovementX += -1 * self.walkspeed.value * self.viewing_direction.x
			MovementZ += -1 * self.walkspeed.value * self.viewing_direction.z

		if self.Keyboard.KeyD.value:
			MovementX += -1 * self.walkspeed.value * self.viewing_direction.z
			MovementZ += 1 * self.walkspeed.value * self.viewing_direction.x

		self.Position.value += avango.gua.Vec3(MovementX, 0, MovementZ)
		
		self.position_y = self.height + self.size
		
		if not self.Keyboard.KeySPACE.value:
			if len(self.Down_Picker.Results.value) > 0:
				if self.Down_Picker.Results.value[0].Distance.value * 5 > self.size:
					if self.is_falling == False:
						self.is_falling = True
					self.height -= self.fall_speed
				else:
					self.is_falling = False
		else:
			self.height += 0.001

		position_x = self.Position.value.x 						
		position_z = self.Position.value.z

		self.Position.value = avango.gua.Vec3(position_x, self.position_y, position_z)

		self.OutTransform.value = avango.gua.make_trans_mat(self.Position.value) * \
															rotation

		self.Down_Picker.Ray.value.Transform.value = avango.gua.make_inverse_mat(self.OutTransform.value)
		self.Down_Picker.Ray.value.Transform.value *= avango.gua.make_trans_mat(self.Position.value) * \
																									avango.gua.make_rot_mat(-90, 1.0, 0.0, 0.0) * \
																									avango.gua.make_scale_mat(0.0005, 0.0005, 5)

	def setPosition(self):
		# self.height -= (self.Down_Picker.Results.value[0].Distance.value * 5 - self.size)
		# self.position_y = self.height + self.size
		pass

	def get_ray_direction(self, ray, ray_scale):
		ray_start = ray.WorldTransform.value.get_translate()

		matrix = ray.WorldTransform.value * avango.gua.make_scale_mat(1.0/ray_scale.x , 1.0/ray_scale.y , 1.0/ray_scale.z)
		ray_direction = avango.gua.make_rot_mat(matrix.get_rotate()) * avango.gua.Vec3(0,0,-1)
		ray_direction = avango.gua.Vec3(ray_direction.x, ray_direction.y, ray_direction.z)

		# ray_direction.normalize()
		return ray_direction

	def setKeyboard(self, Keyboard):
		self.Keyboard = Keyboard

	def setMouse(self, Mouse):
		self.Mouse = Mouse

	def setPicker(self, Picker):
		self.Picker = Picker

	def setDown_Picker(self, Picker):
		self.Down_Picker = Picker
