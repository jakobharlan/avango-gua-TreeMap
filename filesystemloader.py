#!/usr/bin/python

import os
from os.path import join, getsize, isdir
from folder import folder
from file import file

def walk(current):
  print current
  for child in os.listdir(current.path):
    full_path = join(current.path, child)
    if isdir(full_path):
      new_folder = folder(full_path)
      new_folder.children.append(walk(full_path))
    else:
      new_file = file(full_path)


def load(path):
  print "loading filesystem from " + path
  root = folder(path)
  walk(root)

  # for folder in os.walk(path):
  #   print folder
  #   print getsize(folder[0])

