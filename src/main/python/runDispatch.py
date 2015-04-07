
# Local imports
import util.logging_help
import dispatcher

# Library imports
import optparse
import json
import sys

# Setup logging
import logging
import logging.config





# Parse the command-line options. 
parser = optparse.OptionParser()
parser.add_option("-r", "--random",
        dest="random",
        help="Turn on playing random games when config file is exhausted.",
        action="store_true"
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
default_config_file = "config/system.conf"
parser.add_option("-j", "--json-config-file",
        dest="json_config_file",
        help="What JSON-formatted config file to read.",
        default=default_config_file
        )
default_log_config_file = "config/logging.d.conf"
parser.add_option("-l", "--log-config-file",
        dest="log_config_file",
        help="What Python logging config file should be used.",
        default=default_log_config_file
        )
(options, args) = parser.parse_args()

# Initialize the logger. 

try:
    logging.config.fileConfig(
           options.log_config_file,disable_existing_loggers=False)
except IOError as e:
    print >> sys.stderr, "Could not open the logging file specified in " + \
        options.log_config_file
    print >> sys.stderr, "Error message was:\n " + str(e)
    sys.exit(1)



# Set the logging level based on options. 
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



# Check the config file. 
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


# Start the server. 
ds = dispatcher.DispatchServer(config, options.random)
ds.run()


