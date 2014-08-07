#!/usr/bin/python

from entity import entity

class folder(entity):

	def __init__(self, path):
		entity.__init__(self, path)
		self.children = []
