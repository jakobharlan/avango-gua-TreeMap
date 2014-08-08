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
		print self

	def __str__(self):
		string = self.path
		for x in range(0, 100-len(self.path)):
		 	string += "."
		return string + "Size: " + str(self.size) + "   access-time: " + str(self.access_time) + "   modified-time: " + str(self.modified_time)