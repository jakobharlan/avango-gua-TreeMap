#!/usr/bin/python

from entity import entity

class file(entity):

	def __init__(self, path):
		entity.__init__(self, path)

	def print_structure(self, depth = 0):
		for i in range(depth):
			print "  ",
		print self.path