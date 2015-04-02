





class Server(object):
    
    def __init__(self):
        self._finished = False
        self._success = None
    
    def _set_finished(self):
        self._finished = True
    
    def _set_successful(self):
        self._success = True
    
    def _set_unsuccessful(self):
        self._success = False
    
    def finished(self):
        return self._finished
    
    def successful(self):
        if self._success == None:
            raise ServerNotFinishedError()
        else:
            return self._success


class ServerNotFinishedError(Exception):
    
    def __init__(self):
        self.msg = "Tried to check server success before it was finished."
    
    
