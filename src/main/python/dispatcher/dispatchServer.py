


import Queue






# Manage the set of player hosts that are ready to play a game.


class PlayerHost(object):
	
	def __init__(self, hostname, port):
		self._hostname = hostname
		self._port = port
	
	def get_address_tuple(self):
		return (self._hostname, self._port)
	


class PlayerHostQueue(object):
	
	_queue = Queue.Queue()
	
	
	@classmethod
	def put_host(hostname, port):
		pHost = PlayerHost(hostname, port)
		_queue.put(pHost)
	
	@classmethod
	def get_host(self):
		return _queue.get(True)
	
	


