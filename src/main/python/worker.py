

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
        
        self._announce_max = 5
        self._announce_sleep = 5
        self._wait_max = 1
        self._wait_sleep = 5
        
    
    def is_running(self):
        return self._state > 0
    
    def start(self):
        self._state = 1
        
        self._announce_count = 0
        self._wait_count = 0
        
    def _set_announcing(self):
        self._state = 1
        self._announce_count = 0
        
    def _set_waiting(self):
        self._state = 2
        self._wait_count = 0
    
    def _set_playing(self):
        self._state = 3
    
    def _set_finished(self):
        self._state = 0
    
    def is_announcing(self):
        return self._state == 1
    
    def is_waiting(self):
        return self._state == 2
    
    def is_playing(self):
        return self._state == 3
    
    def _announce_worked(self):
        self._set_waiting()
    
    def _announce_failed(self):
        if self._announce_count == self._announce_max:
            LOG.info("WorkerServer announced ready " + \
                str(self._announce_max) + " times, giving up.")
            self._set_finished()
        else:
            LOG.debug("WorkerServer could not announce ready, waiting for " + \
                str(self._announce_sleep) + "s.")
            self._announce_count += 1
            time.sleep(self._announce_sleep)
    
    def _wait_worked(self):
        self._set_playing()
    
    def _wait_failed(self):
        if self._wait_count == self._wait_max:
            LOG.info("WorkerServer waited for match details " + \
                str(self._wait_max) + " times, announcing ready again.")
            self._set_announcing()
        else:
            LOG.debug("WorkerServer could not get match details, waiting " + \
                "for " + str(self._wait_sleep) + "s.")
            self._wait_count += 1
            time.sleep(self._wait_sleep)
    
    def _play_worked(self):
        self._set_announcing()
    
    def _play_failed(self):
        self._set_announcing()
    
    def do_announce_ready(self):
        # Tell the dispatcher we're ready to play a game.  
        wars = NET.WorkerAnnounceReadyServer(
            self._dispatcher_hp,
            self._ourHostname, self._ourPlayerPort, self._ourWorkerPort
            )
        wars.run()
        return wars.finished() and wars.successful()
    
    def do_wait(self):
        data = None
        wgmps = NET.WorkerGetMatchParamsServer(
                self._ourHostname, self._ourWorkerPort
                )
        try:
            wgmps.run()
            LOG.debug("WorkerServer got match to play.")
        except NET.WorkerGetMatchParamsServerAllowableError as e:
            LOG.debug(e)
        except Exception as e:
            LOG.warn(e)
        if wgmps.finished() and wgmps.successful():
            data = wgmps.response()
        return data
    
    def do_play(self, data):
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
        self.start()
        while self.is_running():
            # Tell the dispatcher we're ready to play a game.
            if self.is_announcing():
                success = self.do_announce_ready()
                if success:
                    self._announce_worked()
                else:
                    self._announce_failed()
            # Then wait to hear about what playerType to play as.
            elif self.is_waiting():
                data = self.do_wait()
                if data == None:
                    self._wait_failed()
                else:
                    self._wait_worked()
            # Then play that game. 
            elif self.is_playing():
                self.do_play(data)
                self._play_worked()
            # Otherwise, error:
            else:
                raise WorkerServerInvalidStateError()
    
class WorkerServerConfig(util.config_help.Config):
    
    for_classname = "WorkerServer"
    
    defaults = {
        'pPort' : 9147,
        'wPort' : 21000,
        'ourHostname' :'localhost',
        'dispatchServerAddress' : 'localhost',
        'dispatchServerPort' : 20000
        }



class WorkerServerInvalidStateError(RuntimeError):
    
    def __init__(self):
        RuntimeError.__init__(self, "WorkerServer wound up in invalid state.")


