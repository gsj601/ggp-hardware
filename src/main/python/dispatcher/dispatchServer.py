


import Queue
import SocketServer
import json






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
	
	




# Listen for incoming connections from ready Workers


class ReadyWorkerHandler(SocketServer.StreamRequestHandler):
	"""
	Based partially on this:
		http://thomasfischer.biz/python-simple-json-tcp-server-and-client/
	Partially on Python docs:
		https://docs.python.org/2/library/socketserver.html
	"""
	
	
	def handle(self):
		# Read in from the stream:
		read_data = self.rfile.readline().strip()
		# Return an okay on the socket.  
		self.request.sendall(json.dumps({'return':'ok'}))
		
		# Parse the data as json:
		data = json.load(read_data)
		# Get out the fields we want:
		hostname, port = (data.hostname, data.port)
		# Add the ready worker to the queue.  
		PlayerHostQueue.put_host(hostname, port)
		


