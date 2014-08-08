#!/usr/bin/python

from folder import folder
import avango
import avango.gua

class TM_Element():

	def __init__(self, input_entity):
		self.input_entity = input_entity
		self.children = []

		if self.input_entity.__class__ == folder:
			for child in self.input_entity.children:
				self.children.append(TM_Element(child))

		loader = avango.gua.nodes.TriMeshLoader()
		self.geometry = loader.create_geometry_from_file(
			"cube",
			"data/objects/cube.obj",
			"data/materials/Grey.gmd",
			avango.gua.LoaderFlags.DEFAULTS
		)

	def layout(self):
		pass

	def create_scenegraph_structure(self):
		for child in self.children:
			self.geometry.Children.value.append( child.create_scenegraph_structure() )
		return self.geometry