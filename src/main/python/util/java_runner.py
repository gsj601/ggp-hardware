"""java_runner
A module for helping you run java as an external process.
"""


# This list should be externalized with a config file later.
java_libs = [
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



"""JavaProcess:
	Represents an external process that happens to be a java program.
	Has built-in tools for building the appropriate classpath, etc.
"""
class JavaProcess:

	def __init__(self):
		self.cp = self._construct_classpath_str()
	
	"""_construct_classpath_str:
		 --> string
		The string returned contains a Java classpath.
	"""
	def _construct_classpath_str(self):
		global java_libs
	
		cp = ".:bin/"
	
		lib_str = "lib/"
	
		for lib in java_libs:
			cp = cp + ":" + lib_str + lib + "/*"
	
		self.cp = cp
	



