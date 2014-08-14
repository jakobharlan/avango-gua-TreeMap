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
		self.min_max = self.init_third_dim()

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

	def init_third_dim(self):
		elements = []
		elements.extend(self.root.children)
		max_value = self.root.input_entity.access_time
		min_value = self.root.input_entity.access_time

		while not len(elements) == 0:
			current = elements[0]
			max_value = max(max_value, current.input_entity.access_time)
			min_value = min(min_value, current.input_entity.access_time)
			elements.remove(current)
			elements.extend(current.children)

		return min_value, max_value

	def layout(self	):
		elements = []
		elements.append(self.root)
		current_parent = None
		offset = 0.0

		while not len(elements) == 0:
			current = elements[0]
			elements.remove(current)

			current.set_height(self.min_max)

			if not current.parent == current_parent:
				offset = 0.0
				current_parent = current.parent

			scale = 0.0
			if current_parent == None:
				scale = 1.0
			elif not current.input_entity.parent.size == 0:
				scale = float(current.input_entity.size) / current.input_entity.parent.size
			position = -0.5 + (scale/2) + offset
			offset += scale

			height_offset = current.height / 2

			if current.input_entity.depth % 2 == 0:
				current.transform.Transform.value = avango.gua.make_trans_mat(position, height_offset  , 0) * avango.gua.make_scale_mat(scale * 0.97, 1.0, 0.97)
			else:
				current.transform.Transform.value = avango.gua.make_trans_mat(0, height_offset , position) * avango.gua.make_scale_mat(0.97, 1.0, scale * 0.97)
			current.geometry.Transform.value =  avango.gua.make_scale_mat(1, current.height, 1)

			elements.extend(current.children)

	def focus(self, selector):
		self.focus_element.highlight(False)
		self.focus_element = self.elementdict[selector.Name.value]
		self.focus_element.highlight(True)
		self.Focuspath.value = self.focus_element.input_entity.path



	def create_scenegraph_structure(self):
		self.root_node.Children.value.append(self.root.create_scenegraph_structure())
