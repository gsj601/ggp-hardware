

# Standard imports
import json
import logging




class Config(object):
	"""Config class: to extend; methods converting dict to fields. 
		It's essentially a set of useful methods for taking values from a dict 
		and using them to build a class with names.  The process assumes that 
		there is a set of default field values to be set from the start, and 
		then replaced by values from a dict (or, eventually a file or other 
		sources).  
		To use the Config model, for each class that uses the model, a new 
		class should override the Config class.  The class has two fields that 
		should then be overriden: 
			- for_classname, a string with the name of the class being 
			  configured, so that the class's configuration can be read from a 
			  dict with many 
			- defaults, which a dictionary matching fields with their default 
			  values.  
		Partially inspired by:
		http://www.infoq.com/articles/5-config-mgmt-best-practices
	"""
	
	defaults = []
	for_classname = ""
	
	def __init__(self):
		self._set_defaults()
	
	@classmethod
	def configFrom_dict(cls, d):
		"""Config object built with defaults, but overriden from dict.
			The dict should be structured as follows: 
				{ C1 : {f1:v1, f2:v2, f3:v3}, C2 : {...}, ... }
			where C1 and C2 are classes that can be configured whose names match
			a for_classname field in the subclass of Config, and (f1,v1) are 
			fieldnames and values of the configuration.  
		"""
		c = cls()
		specific_config = {}
		try:
			specific_config = d[c.for_classname]
		except KeyError as e:
			logging.getLogger("Config").warn(
				"Couldn't get config section for class " + c.for_classname
				)
			logging.getLogger("Config").debug(
				"Config dictionary was : " + str(d)
				)
		for key in specific_config:
			c.__dict__[key] = specific_config[key]
		return c
	
	def _set_defaults(self):
		"""Config._set_defaults uses defaults field to set fields.
			The defaults field is not set by the Config class, but has to be 
			set by individual inheriting classes. 
			The defaults field should be a dictionary, so that each key/val 
			pair in the dictionary becomes a set field.
		"""
		if self.defaults:
			for key in self.defaults:
				self.__dict__[key] = self.defaults[key]
	
	
	








