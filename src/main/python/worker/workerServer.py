


import socket
import json
import errno



import ggpPlayerProcess
import util.config_help




# Setting up logging:
# https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
import logging
LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())




class WorkerServer(object):
	"""WorkerServer: handles telling dispatch we're ready; listening for match
		information; running a ggp-base player. 
	"""
	
	def __init__(self, config):
		"""WorkerServer.__init__: sets address of us and of dispatcher."""
		self.config = config
		WorkerServer.config = WorkerServerConfig.configFrom_dict(config)
		
		self._ourPlayerPort = WorkerServer.config.pPort
		self._ourWorkerPort = WorkerServer.config.wPort
		
		self._ourHostname = WorkerServer.config.ourHostname
				
		self._dispatcher_hp = (
			WorkerServer.config.dispatchServerAddress, 
			WorkerServer.config.dispatchServerPort
			)

		LOG.debug("WorkerServer constructed, %s, %i, %i", 
				self._ourHostname, self._ourWorkerPort, self._ourPlayerPort)
	
	def announce_ready(self):
		"""WorkerServer.announce_ready(): tell dispatcher we're ready to play, 
			by sending them a json object of our hostname and port.
		"""
		configuration = {
			"hostname": self._ourHostname,
			"pPort": self._ourPlayerPort,
			"wPort": self._ourWorkerPort
			}
		LOG.debug("WorkerServer announcing ready with %s", 
				configuration)
		
		try:
			to_send = json.dumps(configuration)
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(self._dispatcher_hp)
			LOG.debug("WorkerServer ready announce connected.")
			s.send(to_send)
			LOG.debug("WorkerServer ready announce sent.")
			s.close()
		except socket.error as e:
			LOG.info(
				"Shutting down WorkerServer because no DispatchServer found.")
			self.running = False
	
	def wait_and_play(self):
		"""WorkerServer.wait_and_play: wait for notification of match 
			We want the information needed to start up a GGPPlayerProcess:
				- what player type to play as
				- what port to run on, that game will run on.
		This non-server listening code taken from:
			https://wiki.python.org/moin/TcpCommunication
		"""
		LOG.info("WorkerServer waiting for match to play.")
		
		connected = False
		while (not connected) and self.running:
			try:
				# The wait half:
				our_hp = (self._ourHostname, self._ourWorkerPort)
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.settimeout(20)
				s.bind(our_hp)
				s.listen(1)
				conn, addr = s.accept()
				LOG.debug("WorkerServer received match connection.")
				data = json.loads(conn.recv(100000).strip())
				conn.close()
				LOG.debug("WorkerServer read match details.")
				connected = True
			except socket.timeout as e:
				LOG.info("Shutting down WorkerServer after not hearing about a game.")
				self.running = False
				return 
			except Exception as e:
				n = e.errno
				allowable = [errno.EAGAIN, errno.EADDRINUSE]
				if n in allowable:
					LOG.warn(
						"WorkerServer couldn't start server " + 
						"to listen for match.  Trying again."
						)
				else:
					LOG.warn("Other problem with waiting for match to play.")
					LOG.warn(e)
					self.running = False
					return
		
		# The play half:
		LOG.debug("WorkerServer is setting up player.")
		port, playerType = (self._ourPlayerPort, data["playerType"])
		player = ggpPlayerProcess.GGPPlayerProcess(
			self.config, port, playerType)
		LOG.info("WorkerServer starting player %s, %i", 
				playerType, port)
		player.run()
		LOG.info("Player has run.")
		
		
		
	
	def run(self):
		"""WorkerServer.run(): just loops: announcing ready, wait to play."""
		self.running = True
		while self.running:
			# Tell the dispatcher we're ready to play a game.  
			self.announce_ready()
			# Then wait to hear about what playerType to play as, and 
			# play that game. 
			self.wait_and_play()
		
class WorkerServerConfig(util.config_help.Config):
	
	for_classname = "WorkerServer"
	
	defaults = {
		'pPort' : 9147,
		'wPort' : 21000,
		'ourHostname' :'localhost',
		'dispatchServerAddress' : 'localhost',
		'dispatchServerPort' : 20000
		}




