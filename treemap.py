#!/usr/bin/python

from tm_element import TM_Element
import avango
import avango.gua

class Treemap():

	def __init__(self, root):
		self.root = TM_Element(root)
		self.root_node = avango.gua.nodes.TransformNode(
      Name = "TreeMapRoot",
      Transform = avango.gua.make_scale_mat(1, 0.02, 1)
    )

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

			scale = float(current.input_entity.size) / current.input_entity.parent.size
			position = -0.5 + (scale/2) + offset
			offset += scale

			if current.input_entity.depth % 2 == 0:
				current.geometry.Transform.value = avango.gua.make_trans_mat(position, 0.3, 0) * avango.gua.make_scale_mat(scale * 0.95, 0.95, 0.95)
			else:
				current.geometry.Transform.value = avango.gua.make_trans_mat(0, 0.3, position) * avango.gua.make_scale_mat(0.95, 0.95, scale * 0.95)

			entities.extend(current.children)



	def create_scenegraph_structure(self):
		self.root_node.Children.value.append(self.root.create_scenegraph_structure())
