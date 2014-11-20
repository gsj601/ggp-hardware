"""java_runner
A module for helping you run java as an external process.
"""


# Standard Imports
import subprocess



"""JavaProcess:
	Represents an external process that happens to be a java program.
	Has built-in tools for building the appropriate classpath, etc.
"""
class JavaProcess:
	
	# This list should be externalized with a config file later.
	default_java_libs = [
			"Batik",
			"Clojure",
			"FlyingSaucer",
			"Guava",
			"Htmlparser",
			"JFreeChart",
			"JGoodiesForms",
			"JUnit",
			"Jython",
			"javassist",
			"reflection"
			]
	
	def __init__(self, class_loc, args=[]):
		self._java_libs = self._construct_libs()
		self._cp = self._construct_classpath_str()
		self.class_loc = class_loc
		self.args = args
		
		self._process = None
		self._stdout = None
		self._stderr = None
		return
	
	def run(self):
		command_list = ["java"]
		command_list.append(self.class_loc)
		command_list.extend(["-cp", self._cp])
		command_list.extend(self.args)
		
		self._process = subprocess.Popen(command_list)
		self._process.communicate()
		return
	
	
	"""_construct_libs:
		 --> [string]
		Each string returned is the name of a folder in lib/ to use.
	"""
	def _construct_libs(self):
		# For now, just return the default one! 
		return JavaProcess.default_java_libs

	"""_construct_classpath_str:
		 --> string
		The string returned contains a Java classpath.
	"""
	def _construct_classpath_str(self):
		cp = ".:bin/"
	
		lib_str = "lib/"
	
		for lib in self._java_libs:
			cp = cp + ":" + lib_str + lib + "/*"
	
		return cp
	



