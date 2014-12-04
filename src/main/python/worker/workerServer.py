


import socket
import json



import ggpPlayerProcess











class WorkerServer(object):
	"""WorkerServer: handles telling dispatch we're ready; listening for match
		information; running a ggp-base player. 
	"""
	
	default_dispatchServerAddress = "localhost"
	default_dispatchServerPort = 20000
	
	default_ourHostname = 'localhost'
	
	default_ourPlayerPort = 9147
	default_ourWorkerPort = 21000
	
	def __init__(self, pPort=None, wPort=None):
		"""WorkerServer.__init__: sets address of us and of dispatcher."""
		if not pPort == None:
			self._ourPlayerPort = pPort
		else:
			self._ourPlayerPort = WorkerServer.default_ourPlayerPort
		
		if not wPort == None:
			self._ourWorkerPort = wPort
		else:
			self._ourWorkerPort = WorkerServer.default_ourWorkerPort
		
		self._ourHostname = WorkerServer.default_ourHostname
				
		self._dispatcher_hp = (
			WorkerServer.default_dispatchServerAddress, 
			WorkerServer.default_dispatchServerPort
			)
	
	def announce_ready(self):
		"""WorkerServer.announce_ready(): tell dispatcher we're ready to play, 
			by sending them a json object of our hostname and port.
		"""
		configuration = {
			"hostname": self._ourHostname,
			"pPort": self._ourPlayerPort,
			"wPort": self._ourWorkerPort
			}
		
		to_send = json.dumps(configuration)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(self._dispatcher_hp)
		s.send(to_send)
		s.close()
	
	def wait_and_play(self):
		"""WorkerServer.wait_and_play: wait for notification of match 
			We want the information needed to start up a GGPPlayerProcess:
				- what player type to play as
				- what port to run on, that game will run on.
		This non-server listening code taken from:
			https://wiki.python.org/moin/TcpCommunication
		"""
		# The wait half:
		our_hp = (self._ourHostname, self._ourWorkerPort)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(our_hp)
		s.listen(1)
		conn, addr = s.accept()
		data = json.loads(conn.recv(100000).strip())
		conn.close()
		
		# The play half:
		port, playerType = (self._ourPlayerPort, data["playerType"])
		player = ggpPlayerProcess.GGPPlayerProcess(port, playerType)
		player.run()
		
	
	def run(self):
		"""WorkerServer.run(): just loops: announcing ready, wait to play."""
		while True:
			# Tell the dispatcher we're ready to play a game.  
			self.announce_ready()
			# Then wait to hear about what playerType to play as, and 
			# play that game. 
			self.wait_and_play()
		
	
