#!/usr/bin/python
import filesystemloader
from treemap import Treemap
import treemap_tutorial
from controller import Navigator, KeyController
from picker import Picker, FocusUpdater
from Text import TextField

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
		Transform = avango.gua.make_trans_mat(0.0, 0.0, -2.5)
	)

	eye = avango.gua.nodes.TransformNode(
		Name = "eye",
		Transform = avango.gua.make_trans_mat(0.0, 0.0, 7.5)
	)

	eye.Children.value = [screen]

	graph.Root.value.Children.value.append(eye)

	camera = avango.gua.nodes.Camera(
		LeftEye = "/eye",
		RightEye = "/eye",
		LeftScreen = "/eye/screen",
		RightScreen = "/eye/screen",
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
		SsaoIntensity = 0.5,
		LeftResolution = size,
		EnableRayDisplay = True,
		EnableFPSDisplay = True,
		EnableBackfaceCulling = False,
		NearClip = 0.001
	)
	# pipe.BackgroundTexture.value = "data/textures/skymap.jpg"
	# pipe.BackgroundMode.value = avango.gua.BackgroundMode.SKYMAP_TEXTURE

	# ## Transform Test
	# TMtest = avango.gua.nodes.TransformNode(Name = "Test")
	# TMtest.Transform.value = avango.gua.make_scale_mat(0.1)
	# graph.Root.value.Children.value.append(TMtest)

	## Setup visualization-------------------
	print treemap_tutorial.create_tutorial()
	root = filesystemloader.load(sys.argv[1])
	TM = Treemap()
	TM.my_constructor(root)
	TM.create_scenegraph_structure()
	graph.Root.value.Children.value.append(TM.root_node)
	graph.update_cache()
	TM.layout()

	## Setup Text
	text = TextField()
	text_transform = avango.gua.nodes.TransformNode( Name = "text_transform",
												 # Transform = avango.gua.make_trans_mat(0.1 * (-0.8 / 2.5), 0.1 *(-0.4 / 2.5), -0.1) * avango.gua.make_scale_mat(0.03 * 0.1/2.5))
												 Transform = avango.gua.make_trans_mat(0.01 * (-0.8 / 2.5),  0.01 *(-0.42 / 2.5), -0.0101) * avango.gua.make_scale_mat(0.002 * 0.1/2.5) )
	eye.Children.value.append(text_transform)
	text.my_constructor(text_transform)
	text.sf_text.connect_from(TM.Focuspath)

	## Setup Controllers
	keyController = KeyController()
	keyController.setTreeMap(TM)

	navigator = Navigator()
	eye.Transform.connect_from(navigator.OutTransform)

	TM_Picker = Picker()
	TM_Picker.PickedSceneGraph.value = graph
	pick_ray = avango.gua.nodes.RayNode(Name = "pick_ray")
	pick_ray.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0) * \
														 avango.gua.make_scale_mat(0.0001, 0.0001, 5)
	eye.Children.value.append(pick_ray)
	TM_Picker.Ray.value = pick_ray

	navigator.setPicker(TM_Picker)

	## Fucus Updater
	focuser = FocusUpdater()
	focuser.setTreeMap(TM)
	focuser.Results.connect_from(TM_Picker.Results)

	Down_Picker = Picker()
	Down_Picker.PickedSceneGraph.value = graph
	pick_ray = avango.gua.nodes.RayNode(Name = "down_pick_ray")
	pick_ray.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0) * \
														 avango.gua.make_rot_mat(-10, 1.0, 0.0, 0.0) * \
														 avango.gua.make_scale_mat(0.0005, 0.0005, 5)
	graph.Root.value.Children.value.append(pick_ray)
	Down_Picker.Ray.value = pick_ray

	navigator.controller3D.setDown_Picker(Down_Picker)

	Move_Picker = Picker()
	Move_Picker.PickedSceneGraph.value = graph
	pick_ray = avango.gua.nodes.RayNode(Name = "move_pick_ray")
	pick_ray.Transform.value = avango.gua.make_trans_mat(0.0, 0.0, 0.0) * \
														 avango.gua.make_rot_mat(0, 0.0, 1.0, 0.0) * \
														 avango.gua.make_scale_mat(0.0005, 0.0005, 5)
	graph.Root.value.Children.value.append(pick_ray)
	Move_Picker.Ray.value = pick_ray

	navigator.controller3D.setMove_Picker(Move_Picker)

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
	# sun = avango.gua.nodes.SunLightNode(
	# 	Name = "sun",
	# 	Color = avango.gua.Color(1, 1, 1),
	# 	Transform = avango.gua.make_rot_mat(-45, 1, 0, 0),
	# 	EnableShadows = True
	# )

	# graph.Root.value.Children.value.append(sun)

	light = avango.gua.nodes.PointLightNode(
		Name = "light",
		Color = avango.gua.Color(1,1,1),
		Transform = avango.gua.make_trans_mat(0, 3, 0) * avango.gua.make_scale_mat(5),
		# EnableSpecularShading = False,
		# EnableShadows = True
	)
	graph.Root.value.Children.value.append(light)

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
	print nodetupel[0].Name.value
	#print nodetupel[0]
	# print nodetupel[0].Transform.value
	# print nodetupel[0].WorldTransform.value


if __name__ == '__main__':
	start()

