# CS121: Polling places
#
# Utilities

import json
import random
import time
import sys

def gen_voter_parameters(arrival_rate, voting_duration_rate):
    '''
    Draw gap and voting duration from exponetial distribution

    Inputs:
        arrival_rate: (float) lambda for gap
        voting_duration_rate: (float) lambda for voting duration

    Returns:
        (gap, voting duration) as a pair of floats 
    '''
    return (random.expovariate(arrival_rate),
            random.expovariate(voting_duration_rate))


def setup_config(config_filename, num_booths):
    '''
    Load a configuration file and initialize the seed for the random
    number generator, if appropriate.

    Inputs: 
        config_filename: (string) name of the configuration file
        num_booths: (integer) number of booths to use for the
          simulation

    Returns:
        configuration dictionary
    '''

    try:
        config = json.load(open(config_filename))
    except OSError as e:
        print("{}".format(e), file=sys.stderr)
        return None

    config["number_of_booths"] = num_booths

    if "seed" in config:
        seed = config["seed"]
    else:
        seed = int(time.time())
        config["seed"] = seed

    random.seed(seed)

    return config


def print_voters(voters, filename=None):
    '''
    Print the voters generated by the simulation.

    Inputs:
      voters: a list of voter objects
      filename: (string) specifies the name of a file to use,
         if included.
    '''
    if filename is None:
        file = sys.stdout
    else:
        try:
            file = open(filename, "w")
        except OSError as e:
            print(e, file=sys.stderr)
            sys.exit(1)

    print("Arrival Time   Voting Duration   Start Time    Departure Time", 
          file=file)
    for v in voters:
        s = "{:10.2f}"
        none_str = "      None"
        at = s.format(v.arrival_time) if v.arrival_time else none_str
        vd = s.format(v.voting_duration) if v.voting_duration else none_str
        st = s.format(v.start_time) if v.start_time else none_str
        if v.arrival_time is None or \
           v.voting_duration is None or \
           v.start_time is None:
            dt = none_str
        else:
            dt = s.format(v.start_time + v.voting_duration)
        combined = "{}   {}       {}        {}\n"
        print(combined.format(at, vd, st, dt), file=file)