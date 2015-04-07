

# Library imports
import Queue
import SocketServer
import json
import random
import socket
import time
import threading

random.seed()

# Local imports
import processes.ggpServerProcess
import util.config_help
import networking.dispatching as NET

# Setting up logging:
# https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
import logging
LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())




# Manage the set of player hosts that are ready to play a game.


class PlayerHost(object):
    """PlayerHost:
        A (hostname, port) that has contacted the server to say that it's 
        ready to play a match.
    """
    
    def __init__(self, hostname, pPort, wPort):
        """PlayerHost.__init__(self, hostname, pPort, wPort):
            str, int, int --> new PlayerHost with fields set
        """
        self.hostname = hostname
        self.playerPort = pPort
        self.workerPort = wPort
    
    def get_player_tuple(self):
        """PlayerHost.get_player_tuple: PlayerHost -> (str, int)
            Returns a tuple of the PlayerHost to talk to ggp-Player 
            Fields are public; so this is a convenience method for some socket 
            functions that take an address as (address, port)
        """
        return (self.hostname, self.playerPort)
    
    def get_worker_tuple(self):
        """PlayerHost.get_address_tuple: PlayerHost -> (str, int)
            Returns a tuple of the PlayerHost to talk to worker. 
            Fields are public; so this is a convenience method for some socket 
            functions that take an address as (address, port)
        """
        return (self.hostname, self.workerPort)


    


class PlayerHostQueue(object):
    """PlayerHostQueue:
        A Queue.Queue of PlayerHosts.  
        Maintains a single static queue, with static class methods, so that it 
        can be statically accessed.  The queue is added to by a TCPServer using
        the ReadyWorkerHandler, which can only be overriden so much, in Python.
        The TCPServer takes a class reference, not an object, so we have no 
        control of the fields of the ReadyWorkerHandler being used. Therefore, 
        any accesses the handler makes outside of its handle() function, have 
        to be static ones. 
    """
    
    _queue = Queue.Queue()
    """PlayerHostQueue._queue
        The PlayerHostQueue's actual Queue.Queue. 
        Underscored so that only static methods should access it.
    """
    
    
    @classmethod
    def put_host(PlayerHostQueue, hostname, pPort, wPort):
        """PlayerHostQueue.put_host: hostname, port, port --> 
                adds host to queue. 
            Constructs a PlayerHost and uses the static queue's put() method.
        """
        pHost = PlayerHost(hostname, pPort, wPort)
        PlayerHostQueue._queue.put(pHost)
        LOG.debug(
                "PlayerHost added to queue, %s, %i, %i", 
                hostname, pPort, wPort)
    
    @classmethod
    def get_host(PlayerHostQueue):
        """PlayerHostQueue.get_host:   --> a PlayerHost
            Sleeps for 1s increments until the queue is not empty; 
            then returns the PlayerHost at the front of the queue. 
            Note that this behaviour should be achievable by the Queue.Queue's
            built-in get() method, if the first parameter ("blocking") is set 
            to True.  In testing, it seemed like this blocked all threads 
            (stupid global interpreter lock...).  But it's possible that 
            other code wasn't properly starting the other threads.  
        """
        p = None
        while p == None:
            if PlayerHostQueue._queue.empty():
                time.sleep(1)
            else:
                p = PlayerHostQueue._queue.get(False)
        LOG.debug(
                "PlayerHost popped from queue, %s, %i, %i", 
                p.hostname, p.playerPort, p.workerPort)
        return p
        
    




# Listen for incoming connections from ready Workers


class ReadyWorkerHandler(SocketServer.StreamRequestHandler):
    """
    Based partially on this:
        http://thomasfischer.biz/python-simple-json-tcp-server-and-client/
    Partially on Python docs:
        https://docs.python.org/2/library/socketserver.html
    """
    
    def handle(self):
        """ReadyWorkerHandler.handle
            Reads from the rfile; load it from json; send an okay back; 
            get out the hostname and port that was sent to us from the worker
            that reported ready; and then add that player to our queue of 
            available workers.  
        """
        LOG.debug("Handling ready worker connection.")
        # Read in from the stream:
        # Parse the data as json:
        data = json.load(self.rfile)
        # Return an okay on the socket.  
        self.request.sendall(json.dumps({'return':'ok'}))
        
        # Get out the fields we want:
        hostname, pPort = (data["hostname"], data["pPort"])
        wPort = data["wPort"]
        LOG.info("Handled worker was %s, %s, %s", hostname, pPort, wPort)
        # Add the ready worker to the queue.  
        PlayerHostQueue.put_host(hostname, pPort, wPort)
        





# Send messages to ready hosts 

class Game(object):
    """Game: noun, a competitive activity; not a single instance of one.
        Represented by the gameKey used to identify a game from ggp servers.
    """
    
    def __init__(self, gameKey, numPlayers):
        """Game.__init__: just store parameters as fields."""
        self.gameKey = gameKey 
        self.numPlayers = numPlayers

class Match(object):
    """Match: a single instance of a competitive activity. 
        Keeps track of all elements of this specific instance of a Game:
            - start clock, play clock 
            - what gameKey this match is playing
            - what tourneyKey this match is being played with
            - what PlayerHost each player is
            - what player type each player is
            - how to announce to the PlayerHost what playerType they should 
                play as
    """
    
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
        ]
    
    default_games = [
        Game("ticTacToe", 2)
        ]
    
    _availablePlayerTypes = default_playerTypes
    _availableGames = default_games
    
    def __init__(self, config, tourneyName):
        self.config = config
        # Initialize fields that are set with arguments
        self.tourneyName = tourneyName
        
        # Initialize fields that are set elsewhere
        self._playerHosts = []
        self.playerTypes = []
        self.numPlayers = None
        self.gameKey = None
        
        self.startClock = Match.default_startClock
        self.playClock = Match.default_playClock
        
        LOG.debug("Constructed a Match, %s, %i, %i", 
                self.tourneyName, self.startClock, self.playClock)
    
    def from_dict(self, fields):
        """Match.from_dict: Sets our fields to those in the parameter dict.
            This is for building a Match object from json, eg:
            a_dict = json.loads(a string from a file)
            a_match.from_dict(a_dict)
        """
        for field in fields:
            self.__dict__[field] = fields[field]
    
    def to_dict(self):
        """Match.to_dict: Returns a dict of the fields of this Match.
            This is for outputting a Match to a file, eg:
            a_dict = a_match.to_dict()
            print json.dumps(a_dict)
            Note: Excludes fields whose names start with underscores.
        """
        result = {}
        for field in self.__dict__:
            # Only copy "non-private" fields, without underscores
            if not field[0] == "_":
                result[field] = self.__dict__[field]
        return result
        
        
    def generate_random_match(self):
        """Match.generate_random_match: randomly picks the elements of the Match
            that can be randomly picked.
        """
        # Pick a game
        game = random.choice(Match._availableGames)
        self.numPlayers = game.numPlayers
        self.gameKey = game.gameKey
        
        LOG.debug("Randomly generating a game, %s, %i", 
                self.gameKey, self.numPlayers)

        # Given a number of players by knowing what game we're playing, 
        # pick player types for the players.  
        for player in range(0,self.numPlayers):
            self.playerTypes.append(
                random.choice(Match._availablePlayerTypes))
        LOG.debug("Random players will be %s", self.playerTypes)

        
    def assign_playerHost(self, playerHost):
        """Match.assign_playerHost: adds a PlayerHost to list of players."""
        self._playerHosts.append(playerHost)
        LOG.debug("Match of %s will be played with %s, %i", 
                self.gameKey, playerHost.hostname, playerHost.playerPort)
    
    def _announceGame(self):
        """Match._announceGame: all fields set; tell PlayerHosts to start 
            playing, and what playerType they should play as.
        """
        for i in range(0,self.numPlayers):
            configuration = {
                    "playerType": self.playerTypes[i], 
                    "pPort": self._playerHosts[i].playerPort
                    }
            LOG.debug("Match of %s is announcing to %s",
                    self.gameKey, configuration)
            playerHost = self._playerHosts[i]
            
            successful = False
            while not successful:
                dams = NET.DispatchAnnounceMatchServer(
                        LOG, configuration, playerHost.get_worker_tuple())
                dams.run()
                if not (dams.finished() and dams.successful()):
                    LOG.debug("Couldn't connect to announce game to %s", 
                            workerTuple)
                    time.sleep(1)
                else:
                    LOG.debug("Announced game to %s.", 
                            workerTuple)
                    successful = True
    
    def playMatch(self):
        """Match.playMatch: public method that handles running an individual
            match: announces to players that they should start up; starts up 
            a ggp-base game server.
        """
        LOG.debug("Match of %s is starting", self.gameKey)
        self._announceGame()
        self._ggpPlayer = processes.ggpServerProcess.GGPServerProcess(
            self.config,
            self.tourneyName, 
            self.gameKey,
            self.startClock,
            self.playClock
            )
        for playerHost in self._playerHosts:
            (hostname, port) = playerHost.get_player_tuple()
            self._ggpPlayer.add_host(hostname, hostname, port)
        
        LOG.info("Match of %s will be run in 10s...", self.gameKey)
        time.sleep(10)
        self._ggpPlayer.run()
        LOG.info("Match finished")
        LOG.debug("Match finished was %s", self.to_dict())
            







# The actual server to run. 



class DispatchServer(object):
    """DispatchServer: runs; listens for workers; picks games to play."""
    
    def __init__(self, config, random):
        """DispatchServer.__init__: prepares the server:
            - builds the TCPServer that will listen for ready workers
            - preps other info like our tourney name, our hostname, etc.
        """
        self.config = config
        DispatchServer.config = DispatchServerConfig.configFrom_dict(config)
        
        self._run_random = random
        
        self._ourHostname = DispatchServer.config.ourHostname
        self._ourDispatchPort = DispatchServer.config.ourDispatchPort
        
        h_p = (self._ourHostname, self._ourDispatchPort)
        self._readyWorkerServer = SocketServer.ThreadingTCPServer(
            h_p, ReadyWorkerHandler)
        
        self._tourneyName = DispatchServer.config.tourneyName
        LOG.debug("Dispatch Server constructed.")
        
        experimentFile_loc = DispatchServer.config.experimentFileLoc
        self.experimentFile = None
        try:
            self.experimentFile = open(experimentFile_loc)
            LOG.info("Match file read, %s", 
                experimentFile_loc)
        except IOError as e:
            LOG.debug("Couldn't find experiment file %s, %s", 
                experimentFile_loc, e.message)
    
    def _playMatch(self, matchArgs):
        self._currentMatch = Match(self.config, self._tourneyName)
        self._currentMatch.generate_random_match()
        LOG.debug("Setting match to %s", matchArgs)
        self._currentMatch.from_dict(matchArgs)
        LOG.debug("Dispatch server has match ready.")
        for i in range(self._currentMatch.numPlayers):
            playerHost = PlayerHostQueue.get_host()
            self._currentMatch.assign_playerHost(playerHost)
        LOG.info("Match starting.")
        self._currentMatch.playMatch()
    
    def run(self):
        """DispatchServer.run: starts listening for workers; starts looping 
            over the games to play. 
        """
        
        # Start listening for ready workers. 
        LOG.info("Starting listening for ready workers.")
        t = threading.Thread(
            target=self._readyWorkerServer.serve_forever)
        t.daemon = True
        t.start()
        LOG.debug("Listening for ready workers started.")
        
        # Read in an experiment config file if there is one.
        matches = []
        if not self.experimentFile == None:
            try:
                matches = json.load(self.experimentFile)
                LOG.info("Matches read from file.")
            except Exception as e:
                LOG.warn("Couldn't read experiment file, error was: %s", 
                    e.message)
            finally:
                self.experimentFile.close()
        for match_description in matches:
            self._playMatch( match_description )
        
        # If there isn't (or if reading from config file isn't working yet...)
        if self._run_random:
            LOG.info("Dispatch server will run random games.")
            while True: 
                an_empty_dict = {}
                self._playMatch( an_empty_dict )
        
        LOG.info("Dispatcher is finished work.")
                
                
        
class DispatchServerConfig(util.config_help.Config):
    
    for_classname = "DispatchServer"

    defaults = {
        'ourHostname' : 'localhost',
        'ourDispatchPort' : 20000,
        'tourneyName' : 'testing',
        'experimentFileLoc' : 'matches.expr'
        }









