#!/usr/bin/python

from entity import entity

class file(entity):

	def __init__(self, path):
		entity.__init__(self, path)