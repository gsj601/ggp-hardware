


# Local library imports
import util.java_runner




"""GGPServerProcess
	A class to represent the external Java process that is a game server. 
	Based on the util.java_runner.JavaProcess class; only specification here
	is how to run the GameServer.  
"""
class GGPServerProcess(util.java_runner.JavaProcess):

	# This should be externalized with a config file
	default_ggpServerClass_loc = "org/ggp/base/apps/utilities/GameServerRunner"

	"""GGPServerProcess.__init__(self, args)
		Initialize the GGPServerProcess.  
		The class to run is not a parameter, but instead is externalized. 
		The arguments are currently temporary; should be constructed based on 
		fields, such as player hosts/ports.  
	"""
	def __init__(self, args=[]):
		self._ggpServerClass_loc = self._construct_ggpServerClass_loc()
		super(GGPServerProcess, self).__init__(self._ggpServerClass_loc, args)
	
	"""_construct_ggpServerClass_loc():
		 --> string
		The string returned contains the file location of the class to run--
		in this case, should be GameServerRunner from ggp-base. 
	"""
	def _construct_ggpServerClass_loc(self):
		return GGPServerProcess.default_ggpServerClass_loc




