

# Standard imports
import os
import socket
import json
import time
import errno


# Local imports
import processes.ggpPlayerProcess
import util.config_help
import networking.working




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
    
    def do_announce_ready(self):
        if self.running:
            # Tell the dispatcher we're ready to play a game.  
            rs = network.working.WorkerAnnounceReadyServer(
                LOG, 
                self._dispatcher_hp,
                self._ourHostname, self._ourPlayerPort, self._ourWorkerPort
                )
            rs.run()
            self.running = rs.successful
    
    def do_wait_and_play(self):
        if self.running:
            # The wait half:
            wap = networking.working.WorkerWaitAndPlayServer(
                LOG,
                )
            wap.run()
            self.running = wap.finished and wap.successful
        
            # The play half:
            LOG.debug("WorkerServer is setting up player.")
            port, playerType = (self._ourPlayerPort, data["playerType"])
            player = processes.ggpPlayerProcess.GGPPlayerProcess(
                self.config, port, playerType)
            LOG.info("WorkerServer starting player %s, %i", 
                    playerType, port)
            player.run()
            LOG.info("Player has run.")
        
    def run(self):
        """WorkerServer.run(): just loops: announcing ready, wait to play.
            Loops as long as self.running is True, in case of error. 
        """
        self.running = True
        while self.running:
            # Tell the dispatcher we're ready to play a game.
            self.do_announce_ready()
            # Then wait to hear about what playerType to play as, and 
            # play that game. 
            self.do_wait_and_play()
        
class WorkerServerConfig(util.config_help.Config):
    
    for_classname = "WorkerServer"
    
    defaults = {
        'pPort' : 9147,
        'wPort' : 21000,
        'ourHostname' :'localhost',
        'dispatchServerAddress' : 'localhost',
        'dispatchServerPort' : 20000
        }




