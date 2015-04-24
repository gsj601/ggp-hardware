

import optparse
import json
import sys




def run(options):
    
    num_digits = len(str(options.n))
    formatter = "%0" + str(num_digits) + "d"
    for i in range(options.s, options.s + options.n):
        d = {}
        d["JavaProcess"] = {}
        d["JavaProcess"]["ggpBaseInstall_loc"] = "/project/selab/ggp-hardware/"
        d["WorkerServer"] = {}
        d["WorkerServer"]["pPort"] = options.p + i 
        d["WorkerServer"]["wPort"] = options.w + i
        d["WorkerServer"]["ourHostname"] = "minion" + str(i) 
        d["WorkerServer"]["dispatchServerAddress"] = "skorpio"  
        d["WorkerServer"]["dispatchServerPort"] = 35000
        
        curr_digit = formatter % i 
        f_name = options.file_name_start + curr_digit + ".conf"
        f = open(f_name, "w")
        json.dump(d, f, 
            sort_keys=True, indent=4, separators=(',', ': '))

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file",
        dest="file_name_start",
        help="The beginning of the name of the output config files",
        metavar="FILE",
        action="store",
        type="string")
    parser.add_option("-w", "--startingWorkerPort",
        dest="w",
        help="The first port to run workers from",
        action="store",
        type="int",
        default=30000)
    parser.add_option("-p", "--startingPlayerPort",
        dest="p",
        help="The first port to run players from",
        action="store",
        type="int",
        default=32000)
    parser.add_option("-s", "--startNumber",
        dest="s",
        help="The first sequential number to make a config file for",
        action="store",
        type="int",
        default=1)
    parser.add_option("-n", "--number",
        dest="n",
        help="The number of sequential config files to make",
        action="store",
        type="int",
        default=30)
    (options, args) = parser.parse_args()
    
    try:
        run(options)
    except IOError as e:
        pass





