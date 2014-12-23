

import json




class Config(object):
	"""Partially inspired by:
		http://www.infoq.com/articles/5-config-mgmt-best-practices
	"""
	
	def __init__(self):
		self._set_defaults()
	
	@classmethod
	def configFrom_dict(cls, d):
		"""Config object constructed with defaults, but overriden from dict"""
		c = cls()
		for key in d:
			c.__dict__[key] = d[key]
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
	
	
	








