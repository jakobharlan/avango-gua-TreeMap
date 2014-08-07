#!/usr/bin/python

from entity import entity
from os.path import getsize

class file(entity):

	def __init__(self, path):
		entity.__init__(self, path)
		self.size = getsize(path)

	def print_structure(self, depth = 0):
		for i in range(depth):
			print "  ",
		print self.path + "   Size: " + str(self.size) 