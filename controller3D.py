#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

class Controller3D(avango.script.Script):
	OutTransform = avango.gua.SFMatrix4()
	OutTransform.value = avango.gua.make_identity_mat()
	
	def __init__(self):
		self.super(Controller3D).__init__()

	def evaluate(self):
		pass