


import socket
import json



import ggpPlayerProcess











class WorkerServer(object):
	
	default_dispatchServerAddress = "localhost"
	default_dispatchServerPort = 20000
	
	default_ourHostname = 'localhost'
	
	default_ourPlayerPort = 9147
	
	def __init__(self, port=None):
		if not port == None:
			self._ourPlayerPort = port
		else:
			self._ourPlayerPort = WorkerServer.default_ourPlayerPort
		
		self._ourHostname = WorkerServer.default_ourHostname
				
		self._dispatcher_hp = (
			WorkerServer.default_dispatchServerAddress, 
			WorkerServer.default_dispatchServerPort
			)
	
	def announce_ready(self):
		configuration = {
			"hostname": self._ourHostname,
			"port": self._ourPlayerPort
			}
		
		to_send = json.dumps(configuration)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(self._dispatcher_hp)
		s.send(to_send)
		s.close()
	
	def wait_and_play(self):
		""" 
		This non-server listening code taken from:
			https://wiki.python.org/moin/TcpCommunication
		"""
		# The wait half:
		our_hp = (self._ourHostname, self._ourPlayerPort)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(our_hp)
		s.listen(1)
		conn, addr = s.accept()
		data = json.loads(conn.recv(100000).strip())
		conn.close()
		
		# The play half:
		port, playerType = (data["port"], data["playerType"])
		player = ggpPlayerProcess.GGPPlayerProcess(port, playerType)
		player.run()
		
		
		
		
	
	def run(self):
		
		while True:
			# Tell the dispatcher we're ready to play a game.  
			self.announce_ready()
			# Then wait to hear about what playerType to play as, and 
			# play that game. 
			self.wait_and_play()
			
			
	
	
	










