

# Library imports
import json
import socket
import errno

# Local imports
import server


# Setting up logging:
# https://docs.python.org/2/howto/logging.html#configuring-logging-for-a-library
import logging
LOG = logging.getLogger(__name__)
LOG.addHandler(logging.NullHandler())



class WorkerAnnounceReadyServer(server.Server):
    
    def __init__(self, 
            dispatcher_hp, 
            ourHostname, ourPlayerPort, ourWorkerPort):
        server.Server.__init__(self)
        
        self._dispatcher_hp = dispatcher_hp
        
        self._configuration = {
            "hostname": ourHostname,
            "pPort": ourPlayerPort,
            "wPort": ourWorkerPort
            }
        
    
    
    def run(self):
        """WorkerAnnounceReadyServer.run(): tell dispatcher we're ready to
            play, by sending them a json object of our hostname and ports.
        """
        
        LOG.debug("WorkerServer announcing ready with %s", 
                self._configuration)
        LOG.debug("WorkerServer announcing to %s", self._dispatcher_hp)
        
        try:
            to_send = json.dumps(self._configuration)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            addr = str(self._dispatcher_hp[0])
            port = self._dispatcher_hp[1]
            s.connect((addr,port))
            LOG.debug("WorkerReadyAnnounceServer connected.")
            s.send(to_send)
            LOG.debug("WorkerReadyAnnounceServer sent.")
            s.close()
            self._set_successful()
        except socket.error as e:
            LOG.debug(
                "WorkerServer could not connect to DispatchServer, " + \
                "error was: " + str(e))
            self._set_unsuccessful()
        
        




class WorkerGetMatchParamsServer(server.ReceivingServer):
    
    def __init__(self, ourHostname, ourWorkerPort, timeout=20):
        server.ReceivingServer.__init__(self)
        self._ourHostname = ourHostname
        self._ourWorkerPort = ourWorkerPort
        self._timeout = timeout
        
    
    def run(self):
        """WorkerGetMatchParamsServer.run: wait for notification of match 
            We want the information needed to start up a GGPPlayerProcess:
                - what player type to play as
            (The other piece of info is what port for the player to communicate
            on, but that, we sent to the dispatcher ourselves.)
            The non-server listening code was taken from:
                https://wiki.python.org/moin/TcpCommunication
        """
        LOG.info("WorkerServer waiting for match to play.")
        
        if self._ourHostname != "0.0.0.0":
            LOG.debug("WorkerGetMatchParamsServer will use 0.0.0.0 to " + \
            "listen externally instead of hostname " + str(self._ourHostname))
        
        #our_hp = (self._ourHostname, self._ourWorkerPort)
        our_hp = ("0.0.0.0", self._ourWorkerPort)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.settimeout(self._timeout)
            s.bind(our_hp)
            s.listen(1)
            conn, addr = s.accept()
            LOG.debug("WorkerServer received match connection.")
            data = json.loads(conn.recv(100000).strip())
            conn.close()
            LOG.debug("WorkerServer read match details.")
            connected = True
            self._set_response(data)
        except socket.timeout as e:
            self._set_unsuccessful()
            raise WorkerGetMatchParamsServerTimeoutError()
        except Exception as e:
            error_number = e.errno
            self._set_unsuccessful()
            if error_number == errno.EADDRINUSE:
                raise WorkerGetMatchParamsServerAddressInUseError(our_hp)
            elif error_number == errno.EAGAIN:
                raise WorkerGetMatchParamsServerTryAgainError()
            else:
                raise e
        finally:
            s.close()
    
    



class WorkerGetMatchParamsServerAllowableError(Exception):
    pass


class WorkerGetMatchParamsServerAddressInUseError(
            WorkerGetMatchParamsServerAllowableError):
    
    def __init__(self, address_tuple):
        WorkerGetMatchParamsServerAllowableError.__init__(self, 
                "Worker could not wait for match details at " + \
                str(address_tuple)
                )


class WorkerGetMatchParamsServerTryAgainError(
            WorkerGetMatchParamsServerAllowableError):
    
    def __init__(self):
        WorkerGetMatchParamsServerAllowableError.__init__(self, 
                "Told to try again while waiting for match details."
                )


class WorkerGetMatchParamsServerTimeoutError(
            WorkerGetMatchParamsServerAllowableError):
    
    def __init__(self):
        WorkerGetMatchParamsServerAllowableError.__init__(self,
                "WorkerServer timed out waiting to get match details."
                )


