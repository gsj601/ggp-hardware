

# Library imports
import Queue
import SocketServer
import json
import random
import socket

random.seed()

# Local imports
import ggpServerProcess




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
		





# Send messages to ready hosts 

class Game(object):
	
	def __init__(self, gameKey, numPlayers):
		self.gameKey = gameKey 
		self.numPlayers = numPlayers

class Match(object):
	
	# These should be externalized with a config file
	# or, for the current random game.
	default_startClock = 60
	default_playClock = 30
	
	# This should be externalized with a config file as well. 
	default_playerTypes = [
		"SampleClojureGamerStub", 
		"SampleSearchLightGamer", 
		"RandomGamer", 
		"SampleNoopGamer", 
		"SamplePythonGamerStub", 
		"SampleLegalGamer", 
		"SampleMonteCarloGamer", 
		"KioskGamer", 
		"HumanGamer"
		]
	
	default_games = [
		Game("ticTacToe", 2)
		]
	
	def __init__(self, tourneyName):
		# Initialize fields that are set with arguments
		self.tourneyName = tourneyName
		
		# Initialize fields that are set elsewhere
		self._playerHosts = []
		self._playerTypes = []
		self.numPlayers = None
		self.gameKey = None
		
		self.startClock = Match.default_startClock
		self.playClock = Match.default_playClock
		
		self._availablePlayerTypes= Match.default_playerTypes
		self._availableGames = Match.default_games
		
		
	def generate_random_match(self):
		# Pick a game
		game = random.choice(self._availableGames)
		self.numPlayers = game.numPlayers
		self.gameKey = game.gameKey
		
		# Given a number of players by knowing what game we're playing, 
		# pick player types for the players.  
		for player in self.numPlayers:
			self._playerTypes.append(
				random.choice(self._availablePlayerTypes))
		
	def assign_playerHost(self, playerHost):
		self._playerHosts.append(playerHost)
	
	def _announceGame(self):
		for i in range(0,self.numPlayers):
			configuration = {
				"playerType": self._playerTypes[i], 
				"port": self._playerHosts[i].port
				}
			playerHost = self._playerHosts[i]
			
		to_send = json.dumps(configuration)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(playerHost.get_address_tuple())
		s.send(to_send)
		s.close()
	
	def playMatch(self):
		self._announceGame()
		self._ggpPlayer = ggpServerProcess.GGPServerProcess(
			self.tourneyName, 
			self.gameKey,
			self.startClock,
			self.playClock
			)
		for playerHost in self._playerHosts:
			(hostname, port) = playerHost.get_address_tuple()
			self._ggpPlayer.add_host(hostname, hostname, port)
		
		self._ggpPlayer.run()
			











class DispatchServer(object):
	
	# These should be externalized with a config file instead of used.
	default_ourHostname = 'localhost'
	default_ourDispatchPort = 20000
	
	default_tourneyName = "testing"
	
	
	
	
	def __init__(self, random=False):
		self._run_random = random
		
		self._ourHostname = DispatchServer.default_ourHostname
		self._ourDispatchPort = DispatchServer.default_ourDispatchPort
		
		h_p = (self._ourHostname, self._ourDispatchPort)
		self._readyWorkerServer = SocketServer.ThreadingTCPServer(
			h_p, ReadyWorkerHandler)
		
		self._tourneyName = DispatchServer.default_tourneyName
	
	
	def run(self):
		# Read in an experiment config file if there is one.
		
		# If there isn't (or if reading from config file isn't working yet...)
		if self._run_random:
			while True: 
				self._currentMatch = Match()
				self._currentMatch.generate_random_match()
				for i in range(self._currentMatch.numPlayers):
					playerHost = PlayerHostQueue.get_host()
					self._currentMatch.assign_playerHost(playerHost)
				self._currentMatch.playMatch()
				
				
		










