
# Local imports
import util.logging_help
import dispatcher.dispatchServer

# Library imports
import optparse

# Setup logging
import logging
import logging.config
logging.config.fileConfig("logging.d.conf",disable_existing_loggers=False)

parser = optparse.OptionParser()
parser.add_option("-d", "--debug",
		dest="debug",
		help="Turn logging level to DEBUG.",
		action="store_true"
		)
parser.add_option("-v", "--verbose",
		dest="verbose",
		help="Turn logging level to VERBOSE.",
		action="store_true"
		)
(options, args) = parser.parse_args()


if options.debug:
	util.logging_help.set_streamHandler_levels(
			logging.getLogger(),
			logging.DEBUG)
	logging.getLogger("dispatcher").debug("Set log level to debug.")
elif options.verbose:
	util.logging_help.set_streamHandler_levels(
			logging.getLogger(),
			logging.INFO)
else:
	util.logging_help.set_streamHandler_levels(
			logging.getLogger(),
			logging.WARN)


ds = dispatcher.dispatchServer.DispatchServer(random=True)
ds.run()


