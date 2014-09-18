#!/usr/bin/python

import avango.script
import math
from avango.script import field_has_changed

class Controller3D(avango.script.Script):
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()
	Mouse = None
	Keyboard = None
	Position = avango.gua.Vec3()
	Rotation = avango.gua.make_rot_mat(0, 0.0, 1.0, 0.0)
	rel_rot_x = 0
	rel_rot_y = 0
	Picker = None
	Down_Picker = None
	Move_Picker = None
	height = 0
	size = 0.02
	position_y = 0
	horizontal_speed = 0.3
	vertical_speed = 0.3
	walkspeed = avango.SFFloat()
	viewing_direction = avango.gua.Vec3()
	is_falling = False
	fall_speed = 0.0007
	ascend_speed = 0.0007
	run_speed = 4

	def __init__(self):
		self.super(Controller3D).__init__()
		self.always_evaluate(True)
		self.walkspeed.value = 0.001

	def evaluate(self):
		MovementX = 0
		MovementZ = 0

		self.config_Down_Picker()	#sets the down picker

		self.rel_rot_x += self.Mouse.RelX.value
		self.rel_rot_y += self.Mouse.RelY.value

		self.Rotation = avango.gua.make_rot_mat(-self.rel_rot_x * self.horizontal_speed, 0.0, 1.0, 0.0) * \
							 avango.gua.make_rot_mat(-self.rel_rot_y * self.vertical_speed, 1.0, 0.0, 0.0) #calc view rotation

		self.viewing_direction = self.get_ray_direction(self.Picker.Ray.value, avango.gua.Vec3(0.00001, 0.00001, 5))


		if self.Keyboard.KeyW.value:
			MovementX += 1 * self.walkspeed.value * self.viewing_direction.x
			MovementZ += 1 * self.walkspeed.value * self.viewing_direction.z

		if self.Keyboard.KeyA.value:
			MovementX += 0.3 * self.walkspeed.value * self.viewing_direction.z
			MovementZ += -0.3 * self.walkspeed.value * self.viewing_direction.x

		if self.Keyboard.KeyS.value:
			MovementX += -1 * self.walkspeed.value * self.viewing_direction.x
			MovementZ += -1 * self.walkspeed.value * self.viewing_direction.z

		if self.Keyboard.KeyD.value:
			MovementX += -0.3 * self.walkspeed.value * self.viewing_direction.z
			MovementZ += 0.3 * self.walkspeed.value * self.viewing_direction.x

		if self.Keyboard.KeySHIFT.value and not self.is_falling:
			MovementX *= self.run_speed
			MovementZ *= self.run_speed

		if self.is_falling:
			MovementX *= 0.4
			MovementZ *= 0.4

		self.config_Move_Picker(MovementX, MovementZ)
		if len(self.Move_Picker.Results.value) > 0:
			movement_speed = math.sqrt(math.pow(MovementX, 2) + math.pow(MovementZ, 2))
			if self.Move_Picker.Results.value[0].Distance.value < movement_speed:
				MovementX = 0
				MovementZ = 0

		if not self.Keyboard.KeySPACE.value:
			if len(self.Down_Picker.Results.value) > 0:
				self.setPosition()
		else:
			self.height += self.ascend_speed
			self.position_y = self.height + self.size


		self.Position += avango.gua.Vec3(MovementX, 0, MovementZ)

		position_x = self.Position.x 						
		position_z = self.Position.z

		self.Position = avango.gua.Vec3(position_x, self.position_y, position_z)

		self.OutTransform.value = avango.gua.make_trans_mat(self.Position) * \
															self.Rotation


	def setPosition(self):
		if 5 - self.Down_Picker.Results.value[0].Distance.value*10 < self.height:
			self.is_falling = True
			self.height -= self.fall_speed
		elif 5 - self.Down_Picker.Results.value[0].Distance.value*10 - self.height > 0.001:
			self.height = 5 - self.Down_Picker.Results.value[0].Distance.value*10
		else:
			self.is_falling = False
			self.height = 5 - self.Down_Picker.Results.value[0].Distance.value*10
		self.position_y = self.height + self.size

	def get_ray_direction(self, ray, ray_scale):
		ray_start = ray.WorldTransform.value.get_translate()

		matrix = ray.WorldTransform.value * avango.gua.make_scale_mat(1.0/ray_scale.x , 1.0/ray_scale.y , 1.0/ray_scale.z)
		ray_direction = avango.gua.make_rot_mat(matrix.get_rotate()) * avango.gua.Vec3(0,0,-1)
		ray_direction = avango.gua.Vec3(ray_direction.x, ray_direction.y, ray_direction.z)

		return ray_direction

	def setKeyboard(self, Keyboard):
		self.Keyboard = Keyboard

	def setMouse(self, Mouse):
		self.Mouse = Mouse

	def setPicker(self, Picker):
		self.Picker = Picker

	def setDown_Picker(self, Picker):
		self.Down_Picker = Picker

	def setMove_Picker(self, Picker):
		self.Move_Picker = Picker

	def config_Down_Picker(self):
		self.Down_Picker.Ray.value.Transform.value = avango.gua.make_trans_mat(self.Position.x, 5, self.Position.z) * \
																									avango.gua.make_rot_mat(-90, 1.0, 0.0, 0.0) * \
																									avango.gua.make_scale_mat(0.00001, 0.00001, 10)

	def config_Move_Picker(self, MovementX, MovementZ):
		if not MovementX == 0 or not MovementZ == 0:
			moving_direction = avango.gua.Vec2(MovementX, MovementZ)
			standard_direction = avango.gua.Vec2(0, -1)	

			angle = (360)/(2 * math.pi) * math.acos( (moving_direction.dot(standard_direction))/( moving_direction.normalize() * standard_direction.normalize() ) )
			if moving_direction.x > 0:
				angle = 360 - angle

			self.Move_Picker.Ray.value.Transform.value = avango.gua.make_trans_mat(self.Position.x, self.Position.y - self.size+0.0001, self.Position.z) * \
																								avango.gua.make_rot_mat(int(angle), 0.0, 1.0, 0.0) * \
																								avango.gua.make_scale_mat(0.00001, 0.00001, 5)	

	def get_angle(self):
		pass
