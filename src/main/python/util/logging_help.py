

import logging


def set_streamHandler_levels(logger, level):
	"""set_streamHandler_levels: gets logger's stream handlers, changes level.
		This is so that we can choose to watch with debug/info/warning levels, 
		while still leaving all of the logs be debug, always. (Files can be 
		grepped, the command probably shouldn't be.)  The reason for having a 
		function to do this is that if you set the logger's level, it affects
		all handlers' output.  To change some handlers' levels, you need the 
		handlers themselves, which we don't construct if we config from a file.
	"""
	isStreamHandler = lambda x: type(x) == logging.StreamHandler
	stream_handlers = filter(isStreamHandler, logger.__dict__["handlers"])
	
	setToLevel = lambda x: x.setLevel(level)
	map(setToLevel, stream_handlers)


def _set_file_and_filename(handler, log_loc):
	handler.stream = open( log_loc, "a" )
	handler.baseFilename = log_loc

def set_fileHandler_file(logger, log_loc):
	"""set_fileHandler_file: gets a logger's file handlers, change their loc.
		This will terminate successfully, but it only might let all of the
		file handlers write to the same file.
	"""
	# Get all of the handlers that are FileHandlers
	isFileHandler = lambda x: type(x) == logging.FileHandler
	file_handlers = filter(isFileHandler, logger.__dict__["handlers"])
	
	# Set all of the handlers' files, and baseFilename field. 
	setToLoc = lambda x: _set_file_and_filename(x, log_loc) 
	map(setToLoc, file_handlers)



