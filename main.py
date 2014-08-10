#!/usr/bin/python
import filesystemloader
from treemap import Treemap
from controller import Navigator
from picker import Picker

import avango
import avango.gua
import sys
from examples_common.GuaVE import GuaVE

## Parameters:
size = avango.gua.Vec2ui(1920, 1920*9/16)

def start():
	##initializing scene -------------------
	graph = avango.gua.nodes.SceneGraph(
		Name = "scenegraph"
	)

	## Viewing Setup
	screen = avango.gua.nodes.ScreenNode(
		Name = "screen",
		Width = 1.6,
		Height = 0.9,
		Transform = avango.gua.make_trans_mat(0.0, 0.0, 5)
	)

	eye = avango.gua.nodes.TransformNode(
		Name = "eye",
		Transform = avango.gua.make_trans_mat(0.0, 0.0, 2.5)
	)

	screen.Children.value = [eye]

	graph.Root.value.Children.value.append(screen)

	camera = avango.gua.nodes.Camera(
		LeftEye = "/screen/eye",
		RightEye = "/screen/eye",
		LeftScreen = "/screen",
		RightScreen = "/screen",
		SceneGraph = "scenegraph"
	)

	window = avango.gua.nodes.Window(
		Size = size,
		LeftResolution = size
	)

	pipe = avango.gua.nodes.Pipeline(
		Camera = camera,
		Window = window,
		EnableSsao = True,
		SsaoIntensity = 1.0,
		LeftResolution = size,
		EnableRayDisplay = True,
		EnableFPSDisplay = True
	)

	## Setup visualization-------------------
	root = filesystemloader.load(sys.argv[1])
	TM = Treemap(root)
	TM.create_scenegraph_structure()
	graph.Root.value.Children.value.append(TM.root_node)
	TM.layout()

	## Setup Controllers
	navigator = Navigator()
	screen.Transform.connect_from(navigator.OutTransform)

	TM_Picker = Picker()
	TM_Picker.myConstructor(TM)
	TM_Picker.PickedSceneGraph.value = graph
	pick_ray = avango.gua.nodes.RayNode(Name = "pick_ray")
	pick_ray.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0) * \
														 avango.gua.make_scale_mat(0.01, 0.01, 5)
	eye.Children.value.append(pick_ray)
	TM_Picker.Ray.value = pick_ray

	navigator.controller2D.Picker = TM_Picker

	# # setup Reference
	# loader = avango.gua.nodes.TriMeshLoader()
	# reference_cubes = []
	# for i in range(4):
	# 	reference_cubes.append( loader.create_geometry_from_file(
	# 		"reference_cube",
	# 		"data/objects/cube.obj",
	# 		"data/materials/Red.gmd",
	# 		avango.gua.LoaderFlags.DEFAULTS,
	# 	))

	# reference_cubes[0].Transform.value = avango.gua.make_trans_mat(-0.5, 0 , -0.5) * avango.gua.make_scale_mat(0.11)
	# reference_cubes[1].Transform.value = avango.gua.make_trans_mat( 0.5, 0 , -0.5) * avango.gua.make_scale_mat(0.11)
	# reference_cubes[2].Transform.value = avango.gua.make_trans_mat(-0.5, 0 ,  0.5) * avango.gua.make_scale_mat(0.11)
	# reference_cubes[3].Transform.value = avango.gua.make_trans_mat( 0.5, 0 ,  0.5) * avango.gua.make_scale_mat(0.11)
	# graph.Root.value.Children.value.append(reference_cubes[0])
	# graph.Root.value.Children.value.append(reference_cubes[1])
	# graph.Root.value.Children.value.append(reference_cubes[2])
	# graph.Root.value.Children.value.append(reference_cubes[3])

	# Light for the Treemap
	sun = avango.gua.nodes.SunLightNode(
		Name = "sun",
		Color = avango.gua.Color(1, 1, 1),
		Transform = avango.gua.make_rot_mat(-45, 1, 0, 0)
	)

	graph.Root.value.Children.value.append(sun)

	guaVE = GuaVE()
	guaVE.start(locals(), globals())

	viewer = avango.gua.nodes.Viewer()

	viewer.Pipelines.value = [pipe]
	viewer.SceneGraphs.value = [graph]

	viewer.run()


def printscenegraph(scenegraph):
	for node in scenegraph.Root.value.Children.value:
		printhelper(node)

def printhelper(node):
	stack = []
	stack.append((node,0))

	while stack:
		tmp = stack.pop()
		printelement(tmp)
		for child in tmp[0].Children.value:
			stack.append((child,tmp[1]+1))

def printelement(nodetupel):
	for i in range(0, nodetupel[1]):
		print(" "),
	print nodetupel[0].Name.value + "   "
	#print nodetupel[0]
	#print nodetupel[0].Transform.value


if __name__ == '__main__':
	start()

