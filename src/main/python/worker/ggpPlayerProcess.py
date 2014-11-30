


# Local library imports
import util.java_runner




class GGPPlayerProcess(util.java_runner.JavaProcess):
	"""GGPPlayerProcess
		A class to represent the external Java process that is a game server. 
		Based on the util.java_runner.JavaProcess class; only specification here
		is how to run the Player.  
	"""

	# This should be externalized with a config file
	default_ggpPlayerClass_loc = "org/ggp/base/apps/player/PlayerRunner"

	def __init__(self, port, playerClass):
		"""GGPPlayerProcess.__init__(self, port, playerClass)
			Initialize the GGPPlayerProcess.  
			The class to run is not a parameter, but instead is externalized. 
			port: which port to listen on for play moves
			playerClass: which player to play as
		"""
		# Call superconstructor
		self._ggpPlayerClass_loc = self._construct_ggpPlayerClass_loc()
		super(GGPPlayerProcess, self).__init__(self._ggpPlayerClass_loc)
		
		# Set fields:
		self._port = port
		self._playerClass = playerClass
		
		# Initialize args list:
		# DEPENDENCY: static processing of arguments in 
		# 	org/ggp/base/apps/player/PlayerRunner
		self.args = []
		# args[0]: port: which port to communicate with game server over
		self.args.append(str(self._port))
		# args[1]: name: the class name of the player to play as
		self.args.append(self._playerClass)
		
	
	
	def _construct_ggpPlayerClass_loc(self):
		"""_construct_ggpPlayerClass_loc():
			 --> string
			The string returned contains the file location of the class to run--
			in this case, should be PlayerRunner from ggp-base. 
		"""
		return GGPPlayerProcess.default_ggpPlayerClass_loc




