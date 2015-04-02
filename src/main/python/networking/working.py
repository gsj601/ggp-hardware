

# Library imports
import json
import socket

# Local imports
import server





class WorkerAnnounceReadyServer(server.Server):
    
    def __init__(self, 
            logger, 
            dispatcher_hp, 
            ourHostname, ourPlayerPort, ourWorkerPort):
        self._logger = logger
        
        self._dispatcher_hp = dispatcher_hp
        
        self._configuration = {
            "hostname": self._ourHostname,
            "pPort": self._ourPlayerPort,
            "wPort": self._ourWorkerPort
            }
        
    
    
    def run(self):
        """WorkerAnnounceReadyServer.run(): tell dispatcher we're ready to
            play, by sending them a json object of our hostname and ports.
        """
        
        self._logger.debug("WorkerServer announcing ready with %s", 
                configuration)
        
        try:
            to_send = json.dumps(self._configuration)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(self._dispatcher_hp)
            self._logger.debug("WorkerReadyAnnounceServer connected.")
            s.send(to_send)
            self._logger.debug("WorkerReadyAnnounceServer sent.")
            s.close()
            self._set_successful()
        except socket.error as e:
            self._logger.info(
                "Shutting down WorkerServer because no DispatchServer found.")
            self._set_unsuccessful()
        finally:
            self._set_finished()
        
        





