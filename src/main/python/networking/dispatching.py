


# Library imports
import socket
import json
import SocketServer


# Local imports
import server




class DispatchAnnounceMatchServer(server.Server):
    
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
        



# Listen for incoming connections from ready Workers


class DispatchReadyWorkerServer(SocketServer.ThreadingTCPServer):
    
    def __init__(self, address_tuple, playerHost_queue):
        SocketServer.ThreadingTCPServer(address_tuple, ReadyWorkerHandler)
        
        self._queue = playerHost_queue




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
        self.server._queue.put_host(hostname, pPort, wPort)
        






