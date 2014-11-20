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





"""construct_classpath_str:
	 --> string
	The string returned contains a Java classpath.
"""
def construct_classpath_str():
	global java_libs
	
	cp = ".:bin/"
	
	lib_str = "lib/"
	
	for lib in java_libs:
		cp = cp + ":" + lib_str + lib + "/*"
	
	return cp




