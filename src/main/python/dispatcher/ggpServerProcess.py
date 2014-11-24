

import util.java_runner





class GGPServerProcess(util.java_runner.JavaProcess):

	# This should be externalized with a config file
	default_ggpServerClass_loc = "org/ggp/base/apps/utilities/GameServerRunner"

	def __init__(self, args=[]):
		self._ggpServerClass_loc = self._construct_ggpServerClass_loc()
		util.java_runner.JavaProcess.__init__(self, self._ggpServerClass_loc, args)
	
	"""_construct_ggpServerClass_loc():
		 --> string
		The string returned contains the file location of the class to run--
		in this case, should be GameServerRunner from ggp-base. 
	"""
	def _construct_ggpServerClass_loc(self):
		return GGPServerProcess.default_ggpServerClass_loc




