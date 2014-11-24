


# Local library imports
import util.java_runner




"""GGPPlayerProcess
	A class to represent the external Java process that is a game server. 
	Based on the util.java_runner.JavaProcess class; only specification here
	is how to run the Player.  
"""
class GGPPlayerProcess(util.java_runner.JavaProcess):

	# This should be externalized with a config file
	default_ggpPlayerClass_loc = "org/ggp/base/apps/player/PlayerRunner"

	"""GGPPlayerProcess.__init__(self, args)
		Initialize the GGPPlayerProcess.  
		The class to run is not a parameter, but instead is externalized. 
		The arguments are currently temporary; should be constructed based on 
		fields, such as player hosts/ports.  
	"""
	def __init__(self, args=[]):
		self._ggpPlayerClass_loc = self._construct_ggpPlayerClass_loc()
		super(GGPPlayerProcess, self).__init__(self._ggpPlayerClass_loc, args)
	
	"""_construct_ggpPlayerClass_loc():
		 --> string
		The string returned contains the file location of the class to run--
		in this case, should be PlayerRunner from ggp-base. 
	"""
	def _construct_ggpPlayerClass_loc(self):
		return GGPPlayerProcess.default_ggpPlayerClass_loc




