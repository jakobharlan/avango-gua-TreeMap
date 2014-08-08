#!/usr/bin/python

from tm_element import TM_Element
import avango
import avango.gua

class Treemap():

	def __init__(self, root):
		self.root = TM_Element(root)
		self.root_node = avango.gua.nodes.TransformNode(
      Name = "TreeMapRoot",
    )

	def layout(self):
		self.root.layout()

	def create_scenegraph_structure(self):
		self.root_node.Children.value.append(self.root.create_scenegraph_structure())
