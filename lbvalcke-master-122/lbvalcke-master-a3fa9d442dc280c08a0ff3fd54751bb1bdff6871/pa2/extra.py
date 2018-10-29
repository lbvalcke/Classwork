#  CS121: Schelling Model of Housing Segregation
#
#  Author: Luis Buenaventura and Leo Allen (partners)
#
#   Program for simulating of a variant of Schelling's model of
#   housing segregation.  This program takes four parameters:
#
#    filename -- name of a file containing a sample grid
#
#    R - The radius of the neighborhood: home (i, j) is in the
#        neighborhood of home (k,l) if |k-i| + |l-j| <= R.
#
#    threshold - minimum acceptable threshold for ratio of neighbor
#    value to the total number of homes in his neighborhood.
#
#    max_steps - the maximum number of passes to make over the
#    neighborhood during a simulation.
#
#  Sample use: python3 schelling.py tests/sample-grid.txt 1 0.51 3
#
 
import os
import sys
import utility

 
def getkey(item):
    '''
    Calls element to be sorted and returns the value in the first index for sorting
 
    Inputs:
        item(sublist or tuple): item to be sorted  
        
    Outputs:
        item[0]: picks positional element for list to be used for sorting.
    '''
    # Picks the first item in a sublist or tuple to sort by
    return item[0]


def get_neighborhood(grid, R, location):
    '''
    Gets the neighborhood around a given location based on the 'radius'
    of the neighborhood.
 
    Inputs:
        grid: list of lists of strings representing the grid grid
        R: integer radius around house that denotes the size of neighborhood
        location: tuple indicating the location of the house of interest on
            the grid
 
    Outputs:
        neighbor_location: a list of tuples that represent addresses of
        houses in neighborhood of interest.
    '''
    
    # Initializes an empty list to be populated with neighbor_locations
    neighbor_location = []
    
    # Defines max neighborhood boundaries in cardinal directions 
    for str_step in range(-R, R + 1):
        for add_step in range(-R, R + 1):
            # Defines possible neighborhood boundaries for all directions
            if abs(str_step) + abs(add_step) <= R:
                
                # Checks to see if neighbor locations are within grid
                if 0 <= location[0] + str_step <= len(grid) - 1:
                    if 0 <= location[1] + add_step <= len(grid) - 1:
                        nl = (location[0] + str_step, location[1] + add_step)
                        neighbor_location.append(nl)
 
    return neighbor_location

 
def neighbor_type(grid, R, location):
    '''
    Finds the home type of each house in a given neighborhood
 
    Inputs:
        grid (list of lists): list of lists of strings representing the grid grid
        R (int): integer radius around house that denotes the size of neighborhood
        location (int, int): tuple indicating the location of the house of interest on
            the grid
 
    Outputs: 
        neighbortype (strings): a list of neighbor types 
    '''
    
    # Initializes an empty list of neigbhor types
    neighbortype = []
    
    # Calls get_neighborhood to find the locations of all neighborhood houses
    neighborsloc = get_neighborhood(grid, R, location)
    # Finds the home type at each location in the neighborhood 
    # and stores in list
    for neighbors in neighborsloc:
        nbr_type = grid[neighbors[0]][neighbors[1]]
        neighbortype.append(nbr_type)
 
    return neighbortype  

 
def get_open_list(grid):
    '''
    Creates a list of tuple that store the location of each open home in a grid
 
    Inputs:
        grid (list of lists): list of lists of strings representing the grid grid
 
    Outputs:
        open_homes (list of tuples): a list of tuple locations of homes that are 
        not occupied by either type
 
    '''
    
    # Initializes an empty list to store open home locations
    open_homes = []
    
    # Combs through each possible location in the grid and picks out 
    # open home locations
    for index_i, street in enumerate(grid):
        for index_j, address in enumerate(street):
            home = (index_j, index_i)
            if grid[index_j][index_i] == "O":
                open_homes.append(home)
    # Sorts homes based on their row location
    open_homes = sorted(open_homes, key = getkey)

    return open_homes
 
 
def is_satisfied(grid, R, threshold, location):
    '''
    Checks if the homeowner at the specified location is satisfied.
 
    Inputs:
        grid (list of lists of strings): city grid
        R (int): radius for the neighborhood
        threshold (float): satisfaction threshold
        location (int, int): a grid location
 
    Returns:
        satisfied (boolean): variable indicating if the location's neighbor score 
        is at or above the threshold
    '''
    
    # Defines home type of a grid location of
    home_type = grid[location[0]][location[1]]
    # Calls get_neighborhood type function to get list of neighbors
    neighbor_type_list = neighbor_type(grid, R, location)
    # Sets baseline number of homes similar to the one of interest to 0
    similar_homes = 0
    # Sets baseline number of open homes in neighborhood to 0
    empty_homes = 0
    
    # Checks to see if the location of interest is empty
    if home_type == 'O':
        satisfied = True
    # Finds the number of empty homes and similar homes 
    # in a home's neighborhood
    else:
        for neighbor in neighbor_type_list:
            if neighbor == home_type:
                similar_homes = similar_homes + 1
            elif neighbor == "O":
                empty_homes = empty_homes + 1
        # Calculates satisfaction index for the home of interest
        satisfaction = similar_homes + (0.5 * empty_homes)
        # Normalizes satisfaction index based on size of neighborhood
        size_neighborhood = len(neighbor_type_list)
        prop_satisfaction = satisfaction / size_neighborhood
        # Sets satisfied to either true or false depending on whether the
        # satisfaction threshold is met for the home of interest
        if prop_satisfaction  >= threshold:
            satisfied = True
        elif prop_satisfaction < threshold:
            satisfied = False    
 
    return satisfied
 

def get_unsatisfied_list(grid, R, threshold):
    '''
    Checks all the locations on the grid to identify the unsatsified homes
 
    Inputs:
        grid: (list of lists of strings) the grid
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
 
    Returns:
        unsatisfied_list (list of tuples): A list of locations for 
            homes with neighbors score below the threshold
    '''

    # Initializes an empty list for unsatisfied home locations
    unsatisfied_list = []
    
    # Combs each location on the grid for unsatified homes, stores their tuple
    # location in a list called unsatisfied_list
    for index_i, street in enumerate(grid):
        for index_j, address in enumerate(street):
            satisfied = is_satisfied(grid, R, threshold, (index_j, index_i))
            if satisfied == False:
                loc = (index_j, index_i)
                unsatisfied_list.append(loc)
    
    # Sorts list based on row position
    unsatisfied_list = sorted(unsatisfied_list, key = getkey)

    return unsatisfied_list
 
 
def do_simulation(grid, R, threshold, max_steps):
    '''
    Do a full simulation.
 
    Inputs:
        grid: (list of lists of strings) the grid
        R: (int) radius for the neighborhood
        threshold: (float) satisfaction threshold
        max_steps: (int) maximum number of steps to do
 
    Returns:
        steps (int): the function number of steps executed.
    '''

    # Populates list of unsatisfied homes for step by 
    # calling get_unsatisfied_list func
    unsatisfied_list = get_unsatisfied_list(grid, R, threshold)
    # Creates duplicate list of unsatisfied homes
    # to use to check if a step changed the unsatisfied homes present
    unsatisfied_list_dup = []
    # Creates list with all currently open homes
    possible_locations = get_open_list(grid)
    
    # Initializes a step count value of 0
    steps = 0
    
    #Initiatlizes the simulation step
    while steps < max_steps:
        # Stops loop if there are no unsatisfied homes
        if unsatisfied_list == []: 
            steps += 1
            break
        # Checks to see if the list of unsatisfied homes after loop
        # is the same as before loop to stop simulation step
        elif unsatisfied_list_dup == unsatisfied_list:
            break
        # Combs unsatisfied home through open homes to check if they
        # will be satisfied with that location
        else:
            for unsatisfied_home in unsatisfied_list:
                # Checks if previously unsatisfied home is satisfied after
                # other homes have moved before attempting move 
                if is_satisfied(grid, R, threshold, unsatisfied_home) == True:
                    pass
                else:
                    for pos_location in possible_locations:
                        # Saves type of home at unsatisfied home location in
                        # case open location does not satisfy unsatisfied home  
                        unsat_home = grid[unsatisfied_home[0]][unsatisfied_home[1]]
                        # Switches the two home types
                        grid[unsatisfied_home[0]][unsatisfied_home[1]] = "O"
                        grid[pos_location[0]][pos_location[1]] = unsat_home
                        # Checks to see if unsatisfied home is now satisfied
                        satisfied = is_satisfied(grid, R, threshold, pos_location)
                        # If it is satisfied
                        if satisfied == True:
                            # Defines the location of the sold home as tuple
                            sold_home = (unsatisfied_home[0], unsatisfied_home[1])
                            # Adds sold home to the front of 
                            # the list of open homes
                            possible_locations.insert(0, sold_home)
                            # Removes the filled location from the 
                            # list of possible locs
                            possible_locations.remove(pos_location)
                            break
                        # If it is not satisfied
                        else:
                            # Returns the homes to their original types
                            grid[pos_location[0]][pos_location[1]] = "O"
                            grid[unsatisfied_home[0]][unsatisfied_home[1]] = unsat_home
            # At the end of loop duplicates original list of unsatisfied homes
            # to check to see if they changed after trying to relocate them 
            unsatisfied_list_dup = unsatisfied_list 
            # Calls get_unsatisfied_list() func to collect new list of 
            # unsatisfied homes
            unsatisfied_list = get_unsatisfied_list(grid, R, threshold)
            # Adds a step
            steps += 1

    return steps
 
 
def go(args):
    '''
    Put it all together: parse the arguments, do the simulation and
    process the results.
 
    Inputs:
        args: (list of strings) the command-line arguments
    '''
 
    usage = "usage: python schelling.py <grid file name> <R > 0> <0 < threshold <= 1.0> <max steps >= 0>\n"
    grid = None
    threshold = 0.0
    R = 0
    max_steps = 0
    MAX_SMALL_GRID = 20
 
    if (len(args) != 5):
        print(usage)
        sys.exit(0)
 
    # parse and check the arguments
    try:
        grid = utility.read_grid(args[1])
 
        R = int(args[2])
        if R <= 0:
            print("R must be greater than zero")
            sys.exit(0)
 
        threshold = float(args[3])
        if (threshold <= 0.0 or threshold > 1.0):
            print("threshold must satisfy: 0 < threshold <= 1.0")
            sys.exit(0)
 
        max_steps = int(args[4])
        if max_steps <= 0:
            print("max_steps must be greater than or equal to zero")
            sys.exit(0)
 
    except:
        print(usage)
        sys.exit(0)
 
    num_steps = do_simulation(grid, R, threshold, max_steps)
    if len(grid) < MAX_SMALL_GRID:
        for row in grid:
            print(row)
    else:
        print("Result grid too large to print")
 
    print("Number of steps simulated: " + str(num_steps))
 
 
if __name__ == "__main__":
    go(sys.argv)