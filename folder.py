#!/usr/bin/python

from os.path import join, getsize, isdir
from entity import entity

class folder(entity):

	def __init__(self, path):
		entity.__init__(self, path)
		self.children = []

	def print_structure(self, depth = 0):
		for i in range(depth):
			print "  ",
		print self.path + "   Size: " + str(self.size) 
		for child in self.children:
			child.print_structure(depth+1)
