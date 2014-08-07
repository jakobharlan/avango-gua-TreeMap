#!/usr/bin/python

from entity import entity

class folder(entity):

	def __init__(self, path):
		entity.__init__(self, path)
		self.children = []

	def print_structure(self, depth = 0):
		for i in range(depth):
			print "  ",
		print self.path
		for child in self.children:
			child.print_structure(depth+1)