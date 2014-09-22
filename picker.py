#!/usr/bin/python

import avango.script
from avango.script import field_has_changed

import avango.gua

class Picker(avango.script.Script):

  PickedSceneGraph = avango.gua.SFSceneGraph()
  Ray        = avango.gua.SFRayNode()
  Options    = avango.SFInt()
  Mask       = avango.SFString()
  Results    = avango.gua.MFPickResult()

  def __init__(self):
    self.super(Picker).__init__()
    self.always_evaluate(True)

    self.PickedSceneGraph.value = avango.gua.nodes.SceneGraph()
    self.Ray.value  = avango.gua.nodes.RayNode()
    self.Options.value = avango.gua.PickingOptions.PICK_ONLY_FIRST_OBJECT \
                       | avango.gua.PickingOptions.PICK_ONLY_FIRST_FACE 

    self.Mask.value = ""

  def evaluate(self):
    results = self.PickedSceneGraph.value.ray_test(self.Ray.value,
                                             self.Options.value,
                                             self.Mask.value)
    self.Results.value = results.value


class FocusUpdater(avango.script.Script):
  Results = avango.gua.MFPickResult()
  
  def __init__(self):
    self.super(FocusUpdater).__init__()

  def setTreeMap(self, treemap):
    self.treemap = treemap

  @field_has_changed(Results)
  def update_pickresults(self):
    if len(self.Results.value) > 0:
      pass
      node = self.Results.value[0].Object.value
      self.treemap.focus(node)