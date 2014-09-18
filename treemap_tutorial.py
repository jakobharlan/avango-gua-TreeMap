def create_tutorial():
	tut = ""
	tut += "\n\n-----------------------------------------------------------------\n"
	tut += "--Welcome to the 3D Treemap visualization Tool for your filesystem--\n"
	tut += "------------------------------------------------------------------\n\n"

	tut += "WASD ..... moving\n\n"
	tut += "STRG ..... switch between Overview and Immersive modes\n\n"

	tut += "OVERVIEW:\n"
	tut += "Q and E ..... zoom\n\n"

	tut += "IMMERSIVE:\n"
	tut += "SHIFT ..... move faster \n"
	tut += "SPACE ..... hover upwards \n\n"

	tut += "INTERACTION:\n"
	tut += "UP and Down ..... move focus up and down in the hirachy\n"
	tut += "R ..... flip files shown under focus\n"
	tut += "F ..... flip files shown at all - sometime necessary for performance\n"
	tut += "V ..... create new Treemap with focus folder as root, for drill down\n"
	tut += "C ..... remove focus element from treemap\n"
	tut += "X ..... create treemap for parent of root, if within the initial filesystem\n"
	tut += "Y ..... reload filesystem from initial root\n\n"

	tut += "THIRD DIMENSION:\n"
	tut += "1 ..... depth \n"
	tut += "2 ..... last access \n"
	tut += "3 ..... last modified \n\n"

	tut += "---------\n"
	tut += "--enjoy--\n"
	tut += "---------\n\n\n"
	return tut