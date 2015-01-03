
# Local imports
import worker.workerServer
import util.logging_help

# Library imports
import optparse
import json

# Set up logging
import logging
import logging.config
logging.config.fileConfig("logging.w.conf",disable_existing_loggers=False)


parser = optparse.OptionParser()
parser.add_option("-p", "--pPort",
        dest="pPort",
        help="What port to run the player with.",
        default=9147
        )
parser.add_option("-w", "--wPort",
		dest="wPort",
		help="What port to run the worker with.",
		default=21000
		)
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
default_config_file = "system.conf"
parser.add_option("-j", "--json-config-file",
		dest="json_config_file",
		help="What JSON-formatted config file to read.",
		default=default_config_file
		)
(options, args) = parser.parse_args()

# Change the file location for this worker, now that we know the port.
util.logging_help.set_fileHandler_file(
		logging.getLogger(),
		"testing/worker." + str(options.wPort) + ".log")

if options.debug:
	util.logging_help.set_streamHandler_levels(
			logging.getLogger(),
			logging.DEBUG)
	logging.getLogger("worker").debug("Set log level to debug.")
elif options.verbose:
	util.logging_help.set_streamHandler_levels(
			logging.getLogger(),
			logging.INFO)
else:
	util.logging_help.set_streamHandler_levels(
			logging.getLogger(),
			logging.WARN)

config = {}
try:
	f = open(options.json_config_file)
	config = json.load(f)
except IOError as e:
	if options.json_config_file != default_config_file:
		logging.getLogger("worker").error(
			"Couldn't find non-default config file."
			)
		logging.getLogger("worker").error(e.message)
	else:
		logging.getLogger("worker").debug(
			"Couldn't find default config file, ignoring."
			)


pPort = int(options.pPort)
wPort = int(options.wPort)
ws = worker.workerServer.WorkerServer(config, pPort, wPort)
ws.run()

