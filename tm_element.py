#!/usr/bin/python

from folder import folder
import avango
import avango.gua
import mimetypes

class TM_Element():

	def __init__(self, input_entity, parent = None):
		self.input_entity = input_entity
		self.parent = parent
		self.children = []
		if self.input_entity.__class__ == folder:
			for child in self.input_entity.children:
				self.children.append(TM_Element(child,self))

		self.material = self.select_material()

		loader = avango.gua.nodes.TriMeshLoader()
		self.transform = avango.gua.nodes.TransformNode(Name = "transform" + str(self.input_entity.id))
		self.geometry = loader.create_geometry_from_file(
			"cube" + str(self.input_entity.id),
			"data/objects/cube.obj",
			self.material,
			avango.gua.LoaderFlags.DEFAULTS | avango.gua.LoaderFlags.MAKE_PICKABLE,
		)

		self.height = 1.0

	def create_scenegraph_structure(self):
		for child in self.children:
			self.transform.Children.value.append( child.create_scenegraph_structure() )
		self.transform.Children.value.append(self.geometry)
		return self.transform

	def highlight(self, highlight):
		if highlight:
			self.geometry.Material.value = "data/materials/White.gmd"
		else:
			self.geometry.Material.value = self.material

	def select_material(self):
		mimetype = mimetypes.guess_type(self.input_entity.path)[0]
		if self.input_entity.__class__ == folder:
			return "data/materials/Orange.gmd"

		elif not mimetype == None:

			if mimetype.startswith("text"):
				return "data/materials/Blue.gmd"
			elif mimetype.startswith("image"):
				return "data/materials/Red.gmd"
			elif mimetype.startswith("application"):
				return "data/materials/Yellow.gmd"

		return "data/materials/Grey.gmd"
