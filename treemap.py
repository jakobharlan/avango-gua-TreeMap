#!/usr/bin/python

import tm_element
import avango
import avango.gua
import avango.script



class Treemap(avango.script.Script):
	Focuspath = avango.SFString()
	Focuspath.value = ""

	DEPTH = 1
	LAST_ACCESSD = 2
	LAST_MODIFIED = 3


	def __init__(self):
		self.super(Treemap).__init__()
		avango.gua.load_materials_from("data/materials")
		avango.gua.load_materials_from("data/materials/font")

	def my_constructor(self, root):
		self.root = tm_element.TM_Element(root)
		self.root_node = avango.gua.nodes.TransformNode(
			Name = "TreeMapRoot",
			Transform = avango.gua.make_scale_mat(1, 0.02, 1)
		)
		self.focus_element = self.root
		self.init_dict()
		self.init_third_dim(self.DEPTH)

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

	def init_third_dim(self,third_dim_mode):
		elements = []
		elements.extend(self.root.children)
		self.root.third_dimension_mode = third_dim_mode
		max_value = self.root.get_third_dim_value()
		min_value = self.root.get_third_dim_value()

		# first run through to get the min max values
		while not len(elements) == 0:
			current = elements[0]
			current.third_dimension_mode = third_dim_mode
			max_value = max(max_value, current.get_third_dim_value())
			min_value = min(min_value, current.get_third_dim_value())
			elements.remove(current)
			elements.extend(current.children)

		# second run through to set the height values
		self.root.set_height(min_value, max_value)
		elements.extend(self.root.children)
		while not len(elements) == 0:
			current = elements[0]
			current.set_height(min_value, max_value)
			elements.remove(current)
			elements.extend(current.children)

	def layout(self	):
		elements = []
		elements.append(self.root)
		current_parent = None
		offset = 0.0

		while not len(elements) == 0:
			current = elements[0]
			elements.remove(current)

			if not current.parent == current_parent:
				offset = 0.0
				current_parent = current.parent

			scale = 0.0
			height_offset = 0
			if current_parent == None:
				scale = 1.0
			else:
				height_offset = current.height / 2 + current_parent.height / 2
				if not current.input_entity.parent.size == 0:
					scale = float(current.input_entity.size) / current.input_entity.parent.size
			position = -0.5 + (scale/2) + offset
			offset += scale


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
