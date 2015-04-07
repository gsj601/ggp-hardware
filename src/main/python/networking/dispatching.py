


# Library imports
import socket
import json



# Local imports
import server




class DispatchAnnounceMatchServer(Server):
    
    def __init__(self, logger, configuration, playerHostWorkerTuple):
        self._logger = logger
        self._configuration = configuration
        self._playerHostWorkerTuple = playerHostWorkerTuple
    
    def run(self):
        to_send = json.dumps(self._configuration)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        workerTuple = self._playerHostWorkerTuple
        try:
            s.connect(workerTuple)
            connected = True
            s.send(to_send)
            self._set_successful()
        except socket.error as e:
            self._logger.debug("Socket error connecting to announce game to %s", 
                    workerTuple)
            self._set_unsuccessful()
        finally:
            s.close()
        




