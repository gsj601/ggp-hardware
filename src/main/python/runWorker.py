
# Local imports
import worker.workerServer
import util.logging_help
import util.config_help

# Library imports
import optparse
import json

# Set up logging
import logging
import logging.config
logging.config.fileConfig("logging.w.conf",disable_existing_loggers=False)


class RunWorkerConfig(util.config_help.Config):
	
	for_classname = "RunWorker"
	
	defaults = {
		'pPort' : 9147,
		'wPort' : 21000
		}
	


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
default_config_file = "system.conf"
parser.add_option("-j", "--json-config-file",
		dest="json_config_file",
		help="What JSON-formatted config file to read.",
		default=default_config_file
		)
(options, args) = parser.parse_args()

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
workerServerConfig = worker.workerServer.WorkerServerConfig.configFrom_dict(
	config
	)

# Change the file location for this worker, now that we know the port.
util.logging_help.set_fileHandler_file(
		logging.getLogger(),
		"testing/worker." + str(workerServerConfig.wPort) + ".log")

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



ws = worker.workerServer.WorkerServer(config)
ws.run()

