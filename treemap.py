#!/usr/bin/python

from tm_element import TM_Element
import avango
import avango.gua
import avango.script

class Treemap(avango.script.Script):
	Focuspath = avango.SFString()
	Focuspath.value = ""

	def __init__(self):
		self.super(Treemap).__init__()
		avango.gua.load_materials_from("data/materials")
		avango.gua.load_materials_from("data/materials/font")

	def my_constructor(self, root):
		self.root = TM_Element(root)
		self.root_node = avango.gua.nodes.TransformNode(
			Name = "TreeMapRoot",
			Transform = avango.gua.make_scale_mat(1, 0.02, 1)
		)
		self.focus_element = self.root
		self.init_dict()

	def init_dict(self):
		elements = []
		self.elementdict = {}
		elements.append(self.root)

		# search for the selector
		while (not len(elements) == 0):
			current = elements.pop()
			self.elementdict[current.geometry.Name.value] = current
			for child in current.children:
				elements.append(child)



	def layout(self):
		entities = []
		entities.extend(self.root.children)
		current_parent = None
		offset = 0.0

		while not len(entities) == 0:
			current = entities[0]
			entities.remove(current)

			if not current.input_entity.parent == current_parent:
				offset = 0.0
				current_parent = current.input_entity.parent

			scale = 0.0
			if not current.input_entity.parent.size == 0:
				scale = float(current.input_entity.size) / current.input_entity.parent.size
			position = -0.5 + (scale/2) + offset
			offset += scale

			if current.input_entity.depth % 2 == 0:
				current.geometry.Transform.value = avango.gua.make_trans_mat(position, 1.0, 0) * avango.gua.make_scale_mat(scale * 0.97, 0.97, 0.97)
			else:
				current.geometry.Transform.value = avango.gua.make_trans_mat(0, 1.0, position) * avango.gua.make_scale_mat(0.97, 0.97, scale * 0.97)

			entities.extend(current.children)

	def focus(self, selector):
		self.focus_element.highlight(False)
		self.focus_element = self.elementdict[selector.Name.value]
		self.focus_element.highlight(True)
		self.Focuspath.value = self.focus_element.input_entity.path



	def create_scenegraph_structure(self):
		self.root_node.Children.value.append(self.root.create_scenegraph_structure())
