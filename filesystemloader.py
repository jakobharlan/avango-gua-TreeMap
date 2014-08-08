#!/usr/bin/python

import os
from os.path import join, getsize, isdir
from folder import folder
from file import file

def walk(path):
  current_folder = folder(path)
  current_folder.size = get_folder_size(current_folder.path)
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
  
  root.print_structure()

def get_folder_size(path):
  folder_size = 0
  for child in os.listdir(path):
    full_path = join(path, child)
    if isdir(full_path):
      folder_size += get_folder_size(full_path)
    else:
      folder_size += getsize(full_path)
  return folder_size

  # for folder in os.walk(path):
  #   print folder
  #   print getsize(folder[0])

