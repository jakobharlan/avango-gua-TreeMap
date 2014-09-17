#!/usr/bin/python

import avango.script
from avango.script import field_has_changed
from controller2D import Controller2D
from controller3D import Controller3D
import device
import time

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
	running_animation = False
	# Position2D = avango.gua.Vec3()
	# Position3D = avango.gua.Vec3()


	def __init__(self):
		self.super(Navigator).__init__()
		self.always_evaluate(True)
		self.OutTransform.connect_from(self.controller2D.OutTransform)
		self.KeySTRG = False

		self.controller2D.setKeyboard(self.Keyboard)
		self.controller3D.setMouse(self.Mouse)
		self.controller3D.setKeyboard(self.Keyboard)

		# self.Position2D.value = avango.gua.Vec3(0, 1, 0)
		# self.Position3D.value = avango.gua.Vec3(0, 1, 0)

	def setPicker(self, Picker):
		self.Picker = Picker
		self.controller2D.setPicker(self.Picker)
		self.controller3D.setPicker(self.Picker)


	@field_has_changed(Is_overview_modus)
	def update_mode(self):
		self.running_animation = True
		# print "Position2D" + str(self.controller2D.Position)
		# print "Position3D" + str(self.controller3D.Position)

		if self.Is_overview_modus.value:
			self.controller2D.Position.x = self.controller3D.Position.x
			self.controller2D.Position.z = self.controller3D.Position.z
			start_position = self.controller3D.Position
			end_position = self.controller2D.Position


			start_rotation = self.controller3D.Rotation.get_rotate()
			end_rotation = avango.gua.make_rot_mat(-90, 1, 0, 0).get_rotate()

			self.OutTransform.disconnect_from(self.controller3D.OutTransform)
			animation = Animation()
			animation.my_constructor(start_position, end_position, start_rotation, end_rotation, self.animation_ended, 3.0)
			self.OutTransform.connect_from(animation.OutTransform)
		else:
			self.controller3D.Position.x = self.controller2D.Position.x
			self.controller3D.Position.z = self.controller2D.Position.z
			start_position = self.controller2D.Position
			end_position = self.controller3D.Position

			start_rotation = avango.gua.make_rot_mat(-90, 1, 0, 0).get_rotate()
			end_rotation = self.controller3D.Rotation.get_rotate()

			self.controller3D.height = self.controller2D.zoom - self.Picker.Results.value[0].Distance.value * 5
			self.OutTransform.disconnect_from(self.controller2D.OutTransform)
			animation = Animation()
			animation.my_constructor(start_position, end_position, start_rotation, end_rotation, self.animation_ended, False, 3.0)
			self.OutTransform.connect_from(animation.OutTransform)

	def evaluate(self):
		if not self.running_animation:
			if self.Keyboard.KeySTRG.value and not self.KeySTRG:
				self.Is_overview_modus.value = not self.Is_overview_modus.value
			self.KeySTRG = self.Keyboard.KeySTRG.value

	def animation_ended(self):
		self.OutTransform.disconnect()
		if self.Is_overview_modus.value:
			self.OutTransform.connect_from(self.controller2D.OutTransform)
		else:
			self.OutTransform.connect_from(self.controller3D.OutTransform)
		self.running_animation = False

class Animation(avango.script.Script):
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()

	def __init__(self):
		self.super(Animation).__init__()
		self.always_evaluate(True)

	def my_constructor(self, start_position, end_position, start_rotation, end_rotation, callback, rotation_first = True, animation_duration = 3):
		self.start_position = start_position
		self.end_position = end_position
		self.start_rotation = start_rotation
		self.end_rotation = end_rotation
		self.rotation_first = rotation_first

		self.animation_duration = animation_duration
		self.start_time = time.time()
		self.callback = callback

	def evaluate(self):

		current_time = time.time()
		progress = (current_time - self.start_time) / self.animation_duration

		progress = self.easing_function(current_time-self.start_time, 0, progress ,	self.animation_duration)

		if progress < 1.0:
			if self.rotation_first:
				if progress > 0.5:
					current_rotation = avango.gua.make_rot_mat(self.end_rotation)
				else:
					current_rotation = avango.gua.make_rot_mat(self.start_rotation.slerp_to(self.end_rotation, progress * 2))
			else:
				if progress < 0.5:
					current_rotation = avango.gua.make_rot_mat(self.start_rotation)
				else:
					current_rotation = avango.gua.make_rot_mat(self.start_rotation.slerp_to(self.end_rotation, (progress - 0.5) * 2))
			current_position = self.start_position.lerp_to(self.end_position, progress)
			self.OutTransform.value = avango.gua.make_trans_mat(current_position) * current_rotation
		else:
			self.always_evaluate(False)
			self.callback()

	def easing_function(self, t, b, c, d):
		t = t / (d/2)
		if t < 1:
			return c/2*t*t*t + b
		t -= 2
		return c/2*(t*t*t + 2) + b


class KeyController(avango.script.Script):
	Keyboard = device.KeyboardDevice()

	def __init__(self):
		self.super(KeyController).__init__()
		self.always_evaluate(True)	

		self.Key1 = False
		self.Key2 = False
		self.Key3 = False

		self.KeyF = False
		self.OnlyFolders = False

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
			self.OnlyFolders = not self.OnlyFolders
			self.TM.clear_scenegraph_structure()
			self.TM.create_scenegraph_structure(OnlyFolders = self.OnlyFolders)
		self.KeyF = self.Keyboard.KeyF.value

		if self.Keyboard.KeyDown.value and not self.KeyDown:
			self.TM.focus_parent()
		self.KeyDown = self.Keyboard.KeyDown.value

		if self.Keyboard.KeyUp.value and not self.KeyUp:
			self.TM.focus_child()
		self.KeyUp = self.Keyboard.KeyUp.value