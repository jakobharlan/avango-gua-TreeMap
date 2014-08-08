#!/usr/bin/python

from os import stat
from stat import *

class entity:
	id_counter = 0

	def __init__(self, path):
		self.parent = None
		self.id = entity.id_counter
		entity.id_counter += 1
		self.path = path
		self.size = 0
		st = stat(path)
		self.access_time = st[ST_ATIME]
		self.modified_time = st[ST_MTIME]
		self.depth = 0

	def __str__(self):
		return "member of"
