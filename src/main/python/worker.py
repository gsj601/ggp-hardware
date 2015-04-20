

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
        state = WorkerServerState()
        
        while state.is_running():
            # Tell the dispatcher we're ready to play a game.
            if state.is_announcing():
                success = self.do_announce_ready()
                if success:
                    state.announce_worked()
                else:
                    state.announce_failed()
            # Then wait to hear about what playerType to play as.
            elif state.is_waiting():
                data = self.do_wait()
                if data == None:
                    state.wait_failed()
                else:
                    state.wait_worked()
            # Then play that game. 
            elif state.is_playing():
                self.do_play(data)
                state.play_worked()
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
        'dispatchServerPort' : 20000,
        'announce_max' : 5,
        'announce_sleep' : 5,
        'wait_max' : 1,
        'wait_sleep' : 5
        }



class WorkerServerInvalidStateError(RuntimeError):
    
    def __init__(self):
        RuntimeError.__init__(self, "WorkerServer wound up in invalid state.")




class WorkerServerState(object):
    
    
    def __init__(self):
        self._announce_max = WorkerServer.config.announce_max
        self._announce_sleep = WorkerServer.config.announce_sleep
        self._wait_max = WorkerServer.config.wait_max
        self._wait_sleep = WorkerServer.config.wait_sleep
        
        self._set_initial_state()
    
    state_finished = 0
    state_announce = 1
    state_wait = 2
    state_play = 3
    
    def _set_initial_state(self):
        self._set_announcing()
    
    def is_running(self):
        return not self._state == WorkerServerState.state_finished
    
    def start(self):
        self._state = WorkerServerState.state_announce
        
        self._announce_count = 0
        self._wait_count = 0
        
    def _set_announcing(self):
        self._state = WorkerServerState.state_announce
        self._announce_count = 0
        
    def _set_waiting(self):
        self._state = WorkerServerState.state_wait
        self._wait_count = 0
    
    def _set_playing(self):
        self._state = WorkerServerState.state_play
    
    def _set_finished(self):
        self._state = WorkerServerState.state_finished
    
    def is_announcing(self):
        return self._state == 1
    
    def is_waiting(self):
        return self._state == 2
    
    def is_playing(self):
        return self._state == 3
    
    def announce_worked(self):
        self._set_waiting()
    
    def announce_failed(self):
        if self._announce_count == self._announce_max:
            LOG.info("WorkerServer announced ready " + \
                str(self._announce_max) + " times, giving up.")
            self._set_finished()
        else:
            LOG.debug("WorkerServer could not announce ready, waiting for " + \
                str(self._announce_sleep) + "s.")
            self._announce_count += 1
            time.sleep(self._announce_sleep)
    
    def wait_worked(self):
        self._set_playing()
    
    def wait_failed(self):
        if self._wait_count == self._wait_max:
            LOG.info("WorkerServer waited for match details " + \
                str(self._wait_max) + " times, announcing ready again.")
            self._set_announcing()
        else:
            LOG.debug("WorkerServer could not get match details, waiting " + \
                "for " + str(self._wait_sleep) + "s.")
            self._wait_count += 1
            time.sleep(self._wait_sleep)
    
    def play_worked(self):
        self._set_announcing()
    
    def play_failed(self):
        self._set_announcing()
    
    

