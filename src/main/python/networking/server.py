





class Server(object):
    
    def __init__(self):
        self._finished = False
        self._success = None
    
    def _set_finished(self):
        self._finished = True
    
    def _set_successful(self):
        self._success = True
        self._set_finished()
    
    def _set_unsuccessful(self):
        self._success = False
        self._set_finished()
    
    def finished(self):
        return self._finished
    
    def successful(self):
        if self._success == None:
            raise ServerNotSuccessfulYetError()
        else:
            return self._success
    
    


class ServerNotFinishedError(Exception):
    
    def __init__(self):
        self.msg = "Tried to check server results before it was finished."
    
    


class ServerNotSuccessfulYetError(ServerNotFinishedError):
    
    def __init__(self):
        self.msg = "Tried to check server success before it was finished."
    
    


class ServerHasNotReceivedYetError(ServerNotFinishedError):
    
    def __init__(self):
        self.msg = "Tried to check server response before it was finished."
    
    


class ServerWasUnsuccessfulError(Exception):
    
    def __init__(self):
        self.mst = "Tried to check server response when it was unsuccessful."


class ReceivingServer(Server):
    
    def __init__(self):
        super(ReceivingServer, self).__init__(self)
        self._response = None
    
    def _set_response(self, response):
        self._response = response
        self._set_successful()
    
    def response(self):
        if not self.finished():
            raise ServerHasNotReceivedYetError()
        elif not self.successful():
            raise ServerWasUnsuccessfulError()
        else:
            return self._response



