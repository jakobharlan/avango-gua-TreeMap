#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

import avango.gua

import device

class Navigator(avango.script.Script):

  OutTransform = avango.gua.SFMatrix4()
  OutTransform.value = avango.gua.make_identity_mat()
  Position = avango.gua.SFVec3()
  Speed = avango.SFFloat()
  Mouse = device.MouseDevice()
  # Keyboard = device.KeyboardDevice()

  def __init__(self):
	self.super(Navigator).__init__()
	self.always_evaluate(True)
	self.Position.value = avango.gua.Vec3(0, 1, 0)
	self.Speed.value = 0.001
	self.MovementX = 0
	self.MovementY = 0

  def evaluate(self):

	self.MovementX = self.Mouse.RelX.value * self.Speed.value
	self.MovementY = self.Mouse.RelY.value * self.Speed.value
	self.Position.value += avango.gua.Vec3(self.MovementX, 0, self.MovementY)
	self.OutTransform.value = avango.gua.make_trans_mat(self.Position.value) * avango.gua.make_rot_mat(-90, 1, 0, 0)

