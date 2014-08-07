#!/usr/bin/python
import os
from os.path import join, getsize

def start():
  for thing in os.walk("/home/yuqo8702/Desktop/ProjektInfoVis/ConeTree2"):
    print thing
    print getsize(thing[0])

if __name__ == '__main__':
  start()

