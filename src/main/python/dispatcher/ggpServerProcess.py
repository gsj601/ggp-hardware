


# Local library imports
import util.java_runner


# Setting up logging:
# https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
import logging
LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())




class GGPServerProcess(util.java_runner.JavaProcess):
    """GGPServerProcess
        A class to represent the external Java process that is a game server. 
        Based on the util.java_runner.JavaProcess class; only specification here
        is how to run the GameServer.  
    """

    # This should be externalized with a config file
    default_ggpServerClass_loc = "org/ggp/base/apps/utilities/GameServerRunner"

    def __init__(self, config, tourneyName, gameKey, startClock, playClock):
        """GGPServerProcess.__init__(self, 
                tourneyName, gameKey, startClock, playClock)
            self, str, str, int, int -> new GGPServerProcess
            Initialize the GGPServerProcess.  
            The class to run is not a parameter, but instead is externalized. 
            - tourneyName identifies where to store data from gameplay
            - gameKey identifies which game to paly
            - startClock is the amount of time players have before turns start
            - playClock is the amount of time players have to make a move. 
        """
        # Call super constructor:
        self._ggpServerClass_loc = self._construct_ggpServerClass_loc()
        super(GGPServerProcess, self).__init__(
            config, self._ggpServerClass_loc)
        
        # Set fields from arguments:
        self._tourneyName = tourneyName
        self._gameKey = gameKey
        self._startClock = startClock
        self._playClock = playClock
        
        # Initialize other fields:
        self._hosts = []
        
        # Initialize the arguments list:
        #DEPENDENCY: static processing of arguments in 
        #   org/ggp/base/apps/utilities/GameServerRunner
        self.args = []
        # args[0]: tourneyName: where to save data?
        self.args.append(self._tourneyName)
        # args[1]: gameKey: what game are we playing?
        self.args.append(self._gameKey)
        # args[2]: startClock: how much time before turns?
        self.args.append(str(self._startClock))
        # args[3]: playClock: how much time per turn?
        self.args.append(str(self._playClock))

        # The remaining arguments should be constructed after adding hosts!
        
        LOG.debug(
                "GGPServer constructed, %s,%s", 
                self._tourneyName, self._gameKey)
        
    
    def add_host(self, hostName, playerName, portNumber):
        """GGPServerProcess.add_host(self, hostName, playerName, portNumber)
            self, str, str, int -> adds player-host to self._hosts
        """
        # Construct the new host
        newHost = ConnectedHost(hostName, playerName, portNumber)
        newArgs = newHost.to_args()
        
        # Add the host to our fields
        self._hosts.append(newHost)
        self.args.extend(newArgs)

        LOG.debug(
                "GGPServer added host to play, %s,%s,%i", 
                hostName, playerName, portNumber)


    def _construct_ggpServerClass_loc(self):
        """_construct_ggpServerClass_loc():
             --> string
            The string returned contains the file location of the class to run--
            in this case, should be GameServerRunner from ggp-base. 
        """
        return GGPServerProcess.default_ggpServerClass_loc




class ConnectedHost(object):
    """ConnectedHost
        A class to join together 
            - the host address
            - player name
            - and port number
        of a player that is connecting to the ggp-base server. 
    """

    def __init__(self, hostName, playerName, portNumber):
        """ConnectedHost.__init__(self, hostName, playerName, portNumber)
            Initializes a ConnectedHost. 
            hostName: string; IP address or DNS name
            playerName: string; an arbitrary, unique identifier
            portNumber: int; the port that hostName is talking on
        """
        self._hostName = hostName
        self._playerName = playerName
        self._portNumber = portNumber
    
    def to_args(self):
        """ConnectedHost.to_args(self):
            Given the fields of this object, construct a list of args for 
            Java command-line. 
        """
        args = [self._hostName, str(self._portNumber), self._playerName]
        return args


