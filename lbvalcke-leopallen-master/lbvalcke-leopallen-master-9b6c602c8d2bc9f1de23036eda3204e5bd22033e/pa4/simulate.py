

# CS121: Polling places
#
# Leo Allen, Luis Buenaventura-Valcke
#
# Main file for polling place simulation

import sys
import util

from queue import PriorityQueue


class precinct(object):
    '''
    This is where we are going to put our priority queue - voters are 
    ordered by their departure time. Voter instances are passed to the priority 
    queue by the voter_sample class
    '''
    def __init__(self, data, number):
        self.sample_config = util.setup_config(data, number)
        self._booths = None
        self.number = number
        self.set_arrival_rate()
        self.set_time_open()
        self.set_num_voters()
        self.set_number_of_booths()
        self.set_voting_duration_rate()

    #The following 5 functions extract parameters from a given config file
    def set_arrival_rate(self):    
        self._arrival_rate = self.sample_config["arrival_rate"]

    def set_time_open(self):
        hours_open = self.sample_config["hours_open"]
        self._time_open = hours_open * 60

    def set_num_voters(self):
        self._num_voters = self.sample_config["num_voters"]

    def set_number_of_booths(self):
        self._number_of_booths = self.sample_config["number_of_booths"]
        
    def set_voting_duration_rate(self):
        self._voting_duration_rate = self.sample_config["voting_duration_rate"]

    #checks to see if there is room in the priority queue
    def has_room(self):
        return self._booths.full() != True
    

    def set_booths(self): 
        self._booths = PriorityQueue(self.number)

class voter_sample(object):
    '''
    Generates new voter instances who are put in a queue to vote. If there is
    room in the voting booths, voters are passed to the priority queue. 
    '''
    
    def __init__(self, data, number):
        self._voter_queue = []
        self.precinct = precinct(data, number) 
        self._parameters = None
        self._voting_gap = None
        self._voting_duration = None 
        self._VoterID = 0

    #pulls a voter from the end of the queue to put in a voting booth  
    def extract_last(self):
        return self._voter_queue.pop()
    
    #puts a generated voter at the beginning of the 'line' for the
    #voting booths
    def add_first(self, voter):
        return self._voter_queue.insert(0, voter)

    #checks if there is another valid voter to generate
    def has_next(self):
        num_voters = self.precinct._num_voters
        if self._voter_queue[0].VoterID <= num_voters:
            return True
        else:
            return False

    #finds the arrival time of the last generated voter
    def peek_queue_start(self):
        if self._voter_queue == []:
            peek = 0
            return peek 
        else:
            first_voter = self._voter_queue[0]
            peek = first_voter._arrival_time
            return peek

    #sets the voting gap and voting duration used for 
    #defining new voter instances
    def set_parameters(self):
        self._parameters = util.gen_voter_parameters(self.precinct._arrival_rate, self.precinct._voting_duration_rate)
        self._voting_gap = self._parameters[0]
        self._voting_duration = self._parameters[1]

    #finds the departure time of the next voter to depart the
    #voting booths
    def peek_priority(self):
        if self.precinct._booths.full() == False:
            return 0
        else:
            peek_val = self.precinct._booths.get()
            self.precinct._booths.put(peek_val)
            return peek_val

    #generates new voter instances
    def gen_next_voter(self, data, number): 
        self._VoterID += 1
        self.set_parameters()
        peek = self.peek_queue_start()
        voter_obj = voter(data, number, self._voting_gap, self._voting_duration, peek, self._VoterID)
        voter_obj.set_arrival_time()
        voter_obj.set_start_time()

        #If there is room in the voting booth, this branch
        #puts in the last voter from the queue in a  voting booth
        #with start time  = arrival time
        if self._voter_queue != []: 
            if self.precinct.has_room() == True:
                last_voter = self.extract_last()
                taken = last_voter._departure_time
                self.precinct._booths.put(taken)
                if self.precinct.has_room() == False:
                    if self.peek_priority() > voter_obj._start_time:
                        voter_obj._start_time = self.peek_priority()
                    self.precinct._booths.get()
            
            #If there is no room in a voting booth, this branch
            #assigns the start time of the generated voter to be
            #the highest priority departure time. 
            elif self.precinct.has_room() == False:
                self.precinct._booths.get()
                last_voter = self.extract_last()
                taken = last_voter._departure_time
                self.precinct._booths.put(taken)
                if self.peek_priority() > voter_obj._start_time:
                    voter_obj._start_time = self.peek_priority()

        #if there is no one in the voter queue (not voting booths)
        #this branch defines the start time of a voter as the 
        #highest priority departure time in the voting booths          
        else: 
            if self.precinct.has_room() == False:
                if self.peek_priority() > voter_obj._start_time:
                    voter_obj._start_time = self.peek_priority()
                self.precinct._booths.get()
        
        voter_obj._departure_time = voter_obj._start_time + voter_obj.voting_duration
        
        self.add_first(voter_obj)
    
        return voter_obj



class voter(object):
    '''
    Defines / stores the attributes associated with each voter object passed to 
    the voting booths. 
    '''
    def __init__(self, data, number, voting_gap, voting_dur, peek, VoterID):
        self.VoterID = VoterID
        self.voting_gap = voting_gap
        self.voting_duration = voting_dur
        self._peek = peek
        self._start_time = None
        self._arrival_time = None
        self._departure_time = None

    #sets, gets the arrival time property of a voter instance
    def set_arrival_time(self):
        self._arrival_time = self.voting_gap + self._peek

    def get_arrival_time(self):
        return self._arrival_time

    arrival_time = property(get_arrival_time, set_arrival_time)

    #sets, gets the start time property of a voter instance 
    def set_start_time(self):
        self._start_time = self._arrival_time

    def get_start_time(self):
        return self._start_time

    start_time = property(get_start_time, set_start_time)


def simulate_election_day(config, number):
    '''
    Simulates an election day at a precinct as defined by a config
    file. The heavy lifting in this function is carried out by methods
    defined in the three above classes

    Inputs: config - a configuration file that contains information about the 
            precinct that will be simulated
            number - the number of booths the precinct being simulated

    Outputs: voter_list - a list of voter instances sorted in increasing order
            by arrival time
    '''
    voter_list = []
    pre = precinct(config, number)
    v_sample = voter_sample(config, number)
    v_sample.precinct.set_booths()
    voter_obj = v_sample.gen_next_voter(config, number)
    t = voter_obj.arrival_time
    
    #loops over times less than the amount of time the precinct is open
    while t < v_sample.precinct._time_open:
        
        voter_list.append(voter_obj)
        voter_obj = v_sample.gen_next_voter(config, number)
        t += voter_obj.voting_gap
        
        #breaks the loop if we have exceeded the number of eligible voters
        if voter_obj.VoterID > pre._num_voters:
            break
    
    return util.print_voters(voter_list)


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

