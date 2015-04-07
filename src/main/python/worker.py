

# Standard imports
import os
import socket
import json
import time


# Local imports
import processes.ggpPlayerProcess
import util.config_help
import networking.working as NET




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
        
        self.running = None
    
    def do_announce_ready(self):
        if self.running:
            # Tell the dispatcher we're ready to play a game.  
            wars = NET.WorkerAnnounceReadyServer(
                self._dispatcher_hp,
                self._ourHostname, self._ourPlayerPort, self._ourWorkerPort
                )
            wars.run()
            self.running = wars.finished() and wars.successful()
    
    def do_wait(self):
        data = None
        max_times = 1
        times = 1
        while self.running and data == None:
            # The wait half:
            wgmps = NET.WorkerGetMatchParamsServer(
                self._ourHostname, self._ourWorkerPort
                )
            try:
                wgmps.run()
                LOG.debug("WorkerServer got match to play.")
            except NET.WorkerGetMatchParamsServerAllowableError as e:
                LOG.debug(e)
                time.sleep(5)
            except Exception as e:
                LOG.warn(e)
                self.running = False
            if wgmps.finished() and wgmps.successful():
                data = wgmps.response()
            if times == max_times:
                LOG.info("WorkerServer tried to get match " + \
                    str(max_times) + " times; shutting down.")
                self.running = False
            else:
                times = times + 1
        return data
    
    def do_play(self, data):
        if self.running:
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
            # Then wait to hear about what playerType to play as.
            data = self.do_wait()
            # Then play that game. 
            self.do_play(data)
    
class WorkerServerConfig(util.config_help.Config):
    
    for_classname = "WorkerServer"
    
    defaults = {
        'pPort' : 9147,
        'wPort' : 21000,
        'ourHostname' :'localhost',
        'dispatchServerAddress' : 'localhost',
        'dispatchServerPort' : 20000
        }




