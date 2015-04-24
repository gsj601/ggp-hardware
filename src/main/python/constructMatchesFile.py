

import optparse
import json
import sys


GAMES = \
    [
        [], # 0 Players
        [   # 1 Players
        ],
        [   # 2 Players
            "2pffa",
            #"2pffa_zerosum",
            "2pttc",
            #"biddingTicTacToe",
            #"biddingTicTacToe_10coins",
            "blocker",
            "breakthrough",
            #"breakthroughSmall",
            #"breakthroughWalls",
            #"cephalopodMicro",
            "checkers",
            #"checkersSmall",
            #"checkersTiny",
            "chineseCheckers2",
            "chinook",
            #"cittaceot",
            #"connect5",
            "connectFour",
            #"connectFourLarge",
            #"connectFourLarger",
            #"connectFourSimultaneous",
            #"connectFourSuicide",
            "dotsAndBoxes",
            #"dotsAndBoxesSuicide",
            #"englishDraughts",
            #"escortLatch",
            #"gt_attrition",
            #"gt_centipede",
            #"gt_chicken",
            "gt_dollar",
            "gt_prisoner",
            #"gt_staghunt",
            #"gt_ultimatum",
            #"knightThrough",
            #"nineBoardTicTacToe",
            "pentago",
            #"pentagoSuicide",
            "quarto",
            #"quartoSuicide",
            #"qyshinshu",
            "reversi",
            #"sheepAndWolf",
            "speedChess",
            "ticTacToe",
            #"ticTacToeLarge",
            #"ticTacToeLargeSuicide",
            #"ttcc4_2player"
        ]
    ]


PLAYERS = [
    #"SampleClojureGamerStub", 
    #"SampleSearchLightGamer", 
    "RandomGamer", 
    "SampleNoopGamer", 
    #"SamplePythonGamerStub", 
    "SampleLegalGamer", 
    "SampleMonteCarloGamer", 
    ]




def run(file_name, options, againstSelf, R):
    
    n = options.numPlayers
    
    matches = []
    
    
    for i in range(len(PLAYERS)):
        for j in range(len(PLAYERS)):
            for k in range(len(GAMES[n])):
                if againstSelf or (not againstSelf and i != j): 
                    match = construct_match(options)
                    match["playerTypes"] = [PLAYERS[i], PLAYERS[j]]
                    match["gameKey"] = GAMES[n][k]
                    for r in range(R):
                        matches.append(match)
    
    if options.verbose:
        output = "Num players: " + str(len(PLAYERS)) + "\n"
        output += "Num games: " + str(len(GAMES[n])) + "\n"
        output += "Reps: " + str(R) + "\n"
        output += "Total matches generated: " + str(len(matches))
        print >> sys.stderr, output
        
    
    if file_name == None:
        s = json.dumps(matches, 
            sort_keys=True, indent=4, separators=(',', ': '))
        print s
    else:
        f = open(file_name, "w")
        json.dump(matches, f, 
            sort_keys=True, indent=4, separators=(',', ': '))
    
    
    
    


def construct_match(options):
    """construct_match: 
        Very much a helper, just extract options to dictionary
    """
    result = {}
    result["tourneyName"] = options.tourneyName
    result["startClock"] = options.startClock
    result["playClock"] = options.playClock
    result["numPlayers"] = options.numPlayers
    return result





if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-f", "--file",
        dest="data_file",
        help="The output match file to write to; none, and writes to stdout",
        metavar="FILE",
        action="store",
        type="string")
    parser.add_option("-r", "--numRepetitions",
        dest="R",
        help="How many repetitions of each match to include",
        action="store",
        type="int",
        default=1)
    parser.add_option("-t", "--tourneyName",
        dest="tourneyName",
        help="Name of the tournament to run matches under",
        action="store",
        type="str",
        default=None)
    parser.add_option("-s", "--startClock",
        dest="startClock",
        help="Amount of time before the match starts",
        action="store",
        type="int",
        default=60)
    parser.add_option("-p", "--playClock",
        dest="playClock",
        help="Amount of time for each move in the game",
        action="store",
        type="int",
        default=30)
    parser.add_option("-n", "--numPlayers",
        dest="numPlayers",
        help="Amount of time before the match starts",
        action="store",
        type="int",
        default=2)
    parser.add_option("--self",
        dest="againstSelf",
        help="Should players face off against themselves?",
        action="store_true")
    parser.add_option("-v", "--verbose", 
        dest="verbose",
        help="Prints the clusterer when it's done.",
        action="store_true")
    (options, args) = parser.parse_args()
    
    if options.tourneyName == None:
        print "Please enter a tourney name with -t."
        sys.exit(1)
    
    try:
        run(options.data_file, options, options.againstSelf, options.R)
    except IOError as e:
        pass





