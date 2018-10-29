# CS121: Polling places
#
# YOUR NAME(s) HERE
#
# Main file for polling place simulation

import sys
import util

from queue import PriorityQueue


### YOUR voter, voter_sample, and precinct classes GO HERE.

def simulate_election_day(config):
    # YOUR CODE HERE.
    # REPLACE [] with a list of voter objects
    return []


if __name__ == "__main__":
    # process arguments
    num_booths = 1

    if len(sys.argv) == 2:
        config_filename = sys.argv[1]
    elif len(sys.argv) == 3:
        config_filename = sys.argv[1]
        num_booths = int(sys.argv[2])
    else:
        s = "usage: python3 {0} <configuration filename>"
        s = s + " [number of voting booths]"
        s = s.format(sys.argv[0])
        print(s)
        sys.exit(0)

    config = util.setup_config(config_filename, num_booths)
    voters = simulate_election_day(config)
    util.print_voters(voters)
