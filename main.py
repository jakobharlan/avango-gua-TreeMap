#!/usr/bin/python
import filesystemloader

import avango
import avango.gua

from examples_common.GuaVE import GuaVE

## Parameters:
size = avango.gua.Vec2ui(2560, 2560*9/16)


def viewing_setup_scene(graph):

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
		SsaoIntensity = 2.0,
		EnableBloom = True,
		BloomThreshold = 0.8,
		BloomRadius = 10.0,
		BloomIntensity = 0.8,
		EnableHDR = True,
		HDRKey = 5,
		LeftResolution = size,
		EnableFPSDisplay = True
	)

	return pipe


def start():


	##initializing scene -------------------
	graph = avango.gua.nodes.SceneGraph(
		Name = "scenegraph"
	)

	## Setup visualization-------------------
	filesystemloader.load("/opt/sublime_text")

	pipe = viewing_setup_scene(graph)


	# setup Reference
	loader = avango.gua.nodes.TriMeshLoader()
	reference_cubes = []
	for i in range(4):
		reference_cubes.append( loader.create_geometry_from_file(
			"reference_cube",
			"data/objects/cube.obj",
			"data/materials/Red.gmd",
			avango.gua.LoaderFlags.DEFAULTS,
		))

	reference_cubes[0].Transform.value = avango.gua.make_trans_mat(-0.5,-0.5 ,0) * avango.gua.make_scale_mat(0.1)
	reference_cubes[1].Transform.value = avango.gua.make_trans_mat( 0.5,-0.5 ,0) * avango.gua.make_scale_mat(0.1)
	reference_cubes[2].Transform.value = avango.gua.make_trans_mat(-0.5, 0.5 ,0) * avango.gua.make_scale_mat(0.1)
	reference_cubes[3].Transform.value = avango.gua.make_trans_mat( 0.5, 0.5 ,0) * avango.gua.make_scale_mat(0.1)
	graph.Root.value.Children.value.append(reference_cubes[0])
	graph.Root.value.Children.value.append(reference_cubes[1])
	graph.Root.value.Children.value.append(reference_cubes[2])
	graph.Root.value.Children.value.append(reference_cubes[3])

	# Light for the Treemap
	sun = avango.gua.nodes.SunLightNode(
		Name = "sun",
		Color = avango.gua.Color(1, 1, 1),
		Transform = avango.gua.make_rot_mat(-80, 1, 0, 0)
	)

	graph.Root.value.Children.value.append(sun)

	guaVE = GuaVE()
	guaVE.start(locals(), globals())

	viewer = avango.gua.nodes.Viewer()

	viewer.Pipelines.value = [pipe]
	viewer.SceneGraphs.value = [graph]

	viewer.run()

if __name__ == '__main__':
	start()

