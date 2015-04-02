"""java_runner
A module for helping you run java as an external process.
"""

# Local libraries
import config_help

# Standard Imports
import subprocess

# Setting up logging:
# https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
import logging
LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())



class JavaProcess(object):
    """JavaProcess:
        Represents an external process that happens to be a java program.
        Has built-in tools for building the appropriate classpath, etc.
    """

    def __init__(self, config, class_loc, args=[]):
        """JavaProcess.__init__(self, class_loc, args=[])
            Initializes an external Java process. 
            class_loc: the location, relative to classpath, where the 
                compiled Java class file lives. 
            args: a list of strings, where each is a command-line argument
                to the external Java process. (Default: no args; empty list.) 
        """
        JavaProcess.config = JavaProcessConfig.configFrom_dict(config)
        
        
        self._cp = self._construct_classpath_str()
        self.class_loc = class_loc
        self.args = args
        
        self._process = None
        self._stdout = None
        self._stderr = None

        LOG.debug("JavaProcess constructed for %s", self.class_loc)
        return
    
    def run(self):
        """JavaProcess.run(self):
            Runs the external Java process.  
            Takes no parameters; the object should have its fields set 
            as intended before calling run().
        """
        command_list = ["java"]
        command_list.extend(["-cp", self._cp])
        command_list.append(self.class_loc)
        command_list.extend(self.args)
        
        
        self._process = subprocess.Popen(command_list)
        #self._process = subprocess.Popen(
        #   command_list, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        LOG.debug("Starting to run %s,%s",self.class_loc, self.args)
        (o,e) = self._process.communicate()
        LOG.debug("Finished java process, output: %s", str(o))
        LOG.debug("Finished java process, error: %s", str(e))
        return
    
    def _construct_classpath_str(self):
        """_construct_classpath_str:
             --> string
            The string returned contains a Java classpath.
            Requires the absolute path of the installation of ggp-base. 
        """
        absolute_prepend = JavaProcess.config.ggpBaseInstall_loc
        cp = absolute_prepend + JavaProcess.config.javaBin_loc
    
        lib_str = absolute_prepend + JavaProcess.config.javaLib_loc
    
        for lib in JavaProcess.config.java_libs:
            cp = cp + ":" + lib_str + lib + "/*"
    
        return cp
    


class JavaProcessConfig(config_help.Config):
    
    for_classname = "JavaProcess"
    
    defaults = {
        'java_libs': [
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
            "reflections"
            ], 
        'ggpBaseInstall_loc' : 
            "/Users/gsj601/git/ggp-hardware.git/",
        'javaBin_loc' :
            "build/classes/main/",
        'javaLib_loc' :
            "lib/"
        }


