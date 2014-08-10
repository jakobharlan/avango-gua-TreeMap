#!/usr/bin/python

from folder import folder
import avango
import avango.gua
import mimetypes

class TM_Element():

	def __init__(self, input_entity):
		self.input_entity = input_entity
		self.children = []
		if self.input_entity.__class__ == folder:
			for child in self.input_entity.children:
				self.children.append(TM_Element(child))

		self.material = self.select_material()

		loader = avango.gua.nodes.TriMeshLoader()

		self.geometry = loader.create_geometry_from_file(
			"cube",
			"data/objects/cube.obj",
			self.material,
			avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE,
		)


	def create_scenegraph_structure(self):
		for child in self.children:
			self.geometry.Children.value.append( child.create_scenegraph_structure() )
		return self.geometry

	def select_material(self):
		mimetype = mimetypes.guess_type(self.input_entity.path)[0]

		if self.input_entity.__class__ == folder:
			return "data/materials/Grey.gmd"

		elif not mimetype == None:

			if mimetype.startswith("text"):
				return "data/materials/Blue.gmd"
			elif mimetype.startswith("image"):
				return "data/materials/Red.gmd"

		return "data/materials/Cyan.gmd"
