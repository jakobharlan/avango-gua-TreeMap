#!/usr/bin/python

import os
from os.path import join, getsize, isdir
from folder import folder
from file import file

def walk(path):
  current_folder = folder(path)
  # current_folder.size = get_folder_size(current_folder.path)
  for child in os.listdir(path):
    full_path = join(path, child)
    if isdir(full_path):
      current_folder.children.append(walk(full_path))
    else:
      current_folder.children.append(file(full_path))
  return current_folder

def load(path):
  print "loading filesystem from " + path
  root = walk(path)
  calc_folder_size(root)
  root.print_structure()
  return root

def calc_folder_size(folder):
  folder_size = 0
  for child in folder.children:
    if isdir(child.path):
      folder_size += calc_folder_size(child)
    else:
      folder_size += getsize(child.path)
  folder.size = folder_size
  return folder_size