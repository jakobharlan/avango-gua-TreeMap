#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

import avango.gua

import device

class Navigator(avango.script.Script):

  OutTransform = avango.gua.SFMatrix4()
  OutTransform.value = avango.gua.make_identity_mat()

  Mouse = device.MouseDevice()
  # Keyboard = device.KeyboardDevice()

  def __init__(self):
    self.super(Navigator).__init__()
    self.always_evaluate(True)

  def evaluate(self):
  	print self.Mouse.RelY.value
  	print self.Mouse.RelX.value
