"""java_runner
A module for helping you run java as an external process.
"""



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
	
	def __init__(self):
		self._java_libs = self._construct_libs()
		self._cp = self._construct_classpath_str()
	
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
	



