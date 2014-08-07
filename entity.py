#!/usr/bin/python

class entity:
	id_counter = 0

	def __init__(self, path):
		self.parent = None
		self.id = entity.id_counter
		entity.id_counter += 1
		self.path = path
		self.size = 0
