
import worker.workerServer

import optparse


parser = optparse.OptionParser()
parser.add_option("-p", "--port",
        dest="port",
        help="What port to run the server with.",
        default=9147
        )
(options, args) = parser.parse_args()


ws = worker.workerServer.WorkerServer(int(options.port))
ws.run()


