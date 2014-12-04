
import worker.workerServer

import optparse


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
(options, args) = parser.parse_args()

pPort = int(options.pPort)
wPort = int(options.wPort)
ws = worker.workerServer.WorkerServer(pPort, wPort)
ws.run()


