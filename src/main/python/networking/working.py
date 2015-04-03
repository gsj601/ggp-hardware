

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
        
        




class WorkerWaitAndPlayServer(server.ReceivingServer):
    
    def __init__(self, logger):
        self._logger= logger
        
    
    def run(self):
        """WorkerWaitAndPlayServer.run: wait for notification of match 
            We want the information needed to start up a GGPPlayerProcess:
                - what player type to play as
            (The other piece of info is what port for the player to communicate
            on, but that, we sent to the dispatcher ourselves.)
            The non-server listening code was taken from:
                https://wiki.python.org/moin/TcpCommunication
        """
        self._logger.info("WorkerServer waiting for match to play.")
        
        connected = False
        while (not connected) and not self.finished():
            try:
                our_hp = (self._ourHostname, self._ourWorkerPort)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(20)
                s.bind(our_hp)
                s.listen(1)
                conn, addr = s.accept()
                self._logger.debug("WorkerServer received match connection.")
                data = json.loads(conn.recv(100000).strip())
                conn.close()
                self._logger.debug("WorkerServer read match details.")
                connected = True
                self._set_response(data)
            except socket.timeout as e:
                self._logger.info("Shutting down WorkerServer after not hearing about a game.")
                self._set_unsuccessful()
            except Exception as e:
                n = e.errno
                allowable = [errno.EAGAIN, errno.EADDRINUSE]
                if n in allowable:
                    self._logger.warn(
                        "WorkerServer couldn't start server " + 
                        "to listen for match.  Trying again."
                        )
                    self._logger.debug(
                        "WorkerServer error message was " + 
                        os.strerror(n)
                        )
                    s = 10
                    self._logger.debug(
                        "WorkerServer will wait " + str(s) + "s before " + 
                        "trying to listen for match again."
                        )
                    time.sleep(s)
                else:
                    self._logger.warn("Other problem with waiting for match to play.")
                    self._logger.warn(e)
                    self._set_unsuccessful()
        
        



