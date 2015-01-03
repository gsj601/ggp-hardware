
# Local imports
import util.logging_help
import dispatcher.dispatchServer

# Library imports
import optparse
import json

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
default_config_file = "system.conf"
parser.add_option("-j", "--json-config-file",
		dest="json_config_file",
		help="What JSON-formatted config file to read.",
		default=default_config_file
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

config = {}
try:
	f = open(options.json_config_file)
	config = json.load(f)
except IOError as e:
	if options.json_config_file != default_config_file:
		logging.getLogger("dispatcher").error(
			"Couldn't find non-default config file."
			)
		logging.getLogger("dispatcher").error(e.message)
	else:
		logging.getLogger("dispatcher").debug(
			"Couldn't find default config file, ignoring."
			)


ds = dispatcher.dispatchServer.DispatchServer(config, random=True)
ds.run()


